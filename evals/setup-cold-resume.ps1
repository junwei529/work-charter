[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Destination
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$runRoot = Join-Path $repoRoot '.eval-runs'
$sourceRoot = Join-Path $PSScriptRoot 'fixtures\cold-resume'
$runRootFull = [System.IO.Path]::GetFullPath($runRoot)
$sourceFull = [System.IO.Path]::GetFullPath($sourceRoot)
$destinationFull = [System.IO.Path]::GetFullPath($Destination)
$pathComparison = if ($IsWindows) {
    [System.StringComparison]::OrdinalIgnoreCase
}
else {
    [System.StringComparison]::Ordinal
}

function Assert-NoReparsePoint {
    param(
        [Parameter(Mandatory)]
        [string]$Path
    )

    $relativePath = [System.IO.Path]::GetRelativePath($runRootFull, $Path)
    $currentPath = $runRootFull
    $pathsToCheck = [System.Collections.Generic.List[string]]::new()
    $pathsToCheck.Add($currentPath)

    if ($relativePath -ne '.') {
        foreach ($part in ($relativePath -split '[\\/]')) {
            $currentPath = Join-Path $currentPath $part
            $pathsToCheck.Add($currentPath)
        }
    }

    foreach ($candidatePath in $pathsToCheck) {
        if (-not (Test-Path -LiteralPath $candidatePath)) {
            break
        }

        $item = Get-Item -LiteralPath $candidatePath -Force
        if (
            ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0
        ) {
            throw (
                'Destination path must not contain an existing reparse point ' +
                'inside the repository .eval-runs directory.'
            )
        }
    }
}

if (
    -not $destinationFull.StartsWith(
        $runRootFull + [System.IO.Path]::DirectorySeparatorChar,
        $pathComparison
    )
) {
    throw 'Destination must be a child of the repository .eval-runs directory.'
}

Assert-NoReparsePoint -Path $destinationFull

if (Test-Path -LiteralPath $destinationFull) {
    throw "Destination already exists: $destinationFull"
}

[void](New-Item -ItemType Directory -Path $runRootFull -Force)
[void](New-Item -ItemType Directory -Path $destinationFull -Force)

Get-ChildItem -LiteralPath $sourceFull -Recurse -File -Force |
Where-Object {
    $relativePath = [System.IO.Path]::GetRelativePath($sourceFull, $_.FullName)
    $parts = $relativePath -split '[\\/]'
    -not ($parts -contains '.git') -and
    -not ($parts -contains '__pycache__') -and
    $_.Extension -notin @('.pyc', '.pyo')
} |
ForEach-Object {
    $relativePath = [System.IO.Path]::GetRelativePath($sourceFull, $_.FullName)
    $targetPath = Join-Path $destinationFull $relativePath
    [void](New-Item -ItemType Directory -Path (Split-Path -Parent $targetPath) -Force)
    Copy-Item -LiteralPath $_.FullName -Destination $targetPath
}

& git -C $destinationFull init --initial-branch=phase/retry-delay | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw 'Unable to initialize the cold-resume Git fixture.'
}

& git -c core.autocrlf=false -C $destinationFull add --all
if ($LASTEXITCODE -ne 0) {
    throw 'Unable to stage the cold-resume baseline.'
}

& git `
    -C $destinationFull `
    -c 'user.name=Fixture Check' `
    -c 'user.email=fixture@example.invalid' `
    -c 'commit.gpgSign=false' `
    commit -m 'fixture baseline' | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw 'Unable to commit the cold-resume baseline.'
}

$baselineCommit = (& git -C $destinationFull rev-parse HEAD | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or -not $baselineCommit) {
    throw 'Unable to resolve the cold-resume baseline commit.'
}

$retryPath = Join-Path $destinationFull 'src\retry_policy.py'
$ownedImplementation = @'
def retry_delay(attempt: int) -> int:
    if attempt < 1:
        raise ValueError("attempt must be at least 1")
    return min(2 ** (attempt - 1), 8)
'@ -replace "`r`n", "`n"

[System.IO.File]::WriteAllText(
    $retryPath,
    $ownedImplementation + "`n",
    [System.Text.UTF8Encoding]::new($false)
)

[pscustomobject]@{
    Fixture = 'cold-resume'
    Branch = 'phase/retry-delay'
    BaselineCommit = $baselineCommit
    OwnedDirtyFile = 'src/retry_policy.py'
} | ConvertTo-Json -Depth 3
