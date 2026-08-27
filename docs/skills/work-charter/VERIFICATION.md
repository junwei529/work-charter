# Work Charter Verification

## Accepted migration baseline

- Source commit: `80910a8b2375a11be897e9660c4b00a06d00dd13`
- Package path: `skills/work-charter/`
- Package files: 5
- Provenance manifest: [`../../../provenance/source-map.json`](../../../provenance/source-map.json)

## Repository check

```powershell
python -B scripts/check_repository.py --json
```

This verifies exact Git-blob identity for package/case/fixture/license inputs,
the adapted/native-file hashes and source mappings, expected package and evaluation
shape, UTF-8/BOM and Markdown-link boundaries, and publication safety.
The default standalone route preserves a checker-pinned source-identity map;
it does not assume the former source repository is present.

When the exact source Git object store is available during migration audit, run:

```powershell
python -B scripts/check_repository.py --json --source-repository <source-git-repository>
```

That explicit route resolves the recorded commit/tree and proves every mapped
source path, Git blob, and raw or normalized SHA-256 directly from Git objects;
it never reads source working-tree bytes.

## Adversarial checker matrix

```powershell
python -B scripts/check_repository.py --adversarial
```

This builds every disposable repository strictly from staged Git-index blobs;
working-tree, ignored, untracked, cache, and link-target bytes are not copied.
The admitted publication-classifier input domain is the UTF-8 text of mapped
repository files plus every string value consumed from the v2 provenance
manifest. Manifest paths remain strict POSIX repository-relative paths. Within
that domain, the locator grammar is limited to direct absolute Windows drive
profiles, direct/device UNC locators, and `file:` URIs that resolve to those
forms after exactly one percent-decoding pass. One separator/prefix
canonicalization handles equivalent slash forms and repeated leading
separators in direct and `file:` representations; explicit non-`file:` URIs,
repository-relative paths, POSIX
`file:` paths, and non-profile Windows roots remain portable. Locator-like
`file:` or UNC forms that cannot be classified unambiguously after that pass
fail closed, including `file:` candidates whose raw query or fragment
delimiter or raw-space token boundary would make the local path representation
ambiguous, and candidates whose percent escapes are not valid UTF-8. Direct UNC
forms with a server but no share also fail closed; the
portable `//` syntax-text partition requires no server token. This policy
protects the existing no-private-locator publication
contract; it does not promise another URI or filesystem grammar.
The finite fail-closed matrix covers drive-rooted private Windows profiles with
backslash, forward-slash, and mixed separators; ASCII-space and Unicode profile
names; end-of-string and deeper paths; and recognized device-drive prefixes.
It also covers ordinary, device, and extended UNC locators after one canonical
separator/prefix normalization. A shared structured UNC parser requires
nonempty server and share components, accepts Unicode and internal spaces, and
rejects controls and Windows-invalid component characters. Portable explicit
non-file URI, relative, embedded-drive, empty-profile, singular-root,
syntax-text, POSIX, and non-profile-root partitions remain accepted. A
URI-aware standard-library layer parses `file:` candidates,
decodes percent escapes once, and routes local-drive, `localhost`, UNC-authority,
drive-authority (including a once-decoded drive-rooted authority remainder),
and encoded device-drive representations through the same path predicates;
HTTP/HTTPS, other schemes, non-profile Windows roots, POSIX paths, bare schemes,
and empty-profile forms remain portable. Git-index snapshots remove inherited
`GIT_*` selectors case-insensitively, reintroduce only disabled optional locks,
and use an explicit repository route; a disposable hostile-selector matrix
proves both `ls-files` and `cat-file` stay bound to the intended repository.
The matrix also covers invalid UTF-8 and unpaired-Unicode-surrogate structured failure, manifest
identity and rewrite-source schema, exact-blob source SHA-256 verification,
top-level source-commit/source-tree identity, and a checker-pinned canonical
digest of every destination-to-source identity mapping. Exact tree membership
is established only by the explicit source-object audit above;
manifest duplicate-key rejection, top-level `manifest_provenance` source-record
schema/path validation, decoded-key/value publication safety, unsafe
destinations, source paths free of Unicode General_Category `Cc` controls
(covering C0, DEL, and C1 while preserving other admitted Unicode categories),
missing mapped content, the legacy
reparse fallback, and rejection of link-like source-repository ancestors. An external-link
sentinel proves that a link entry is rejected before its target blob is read or
copied; the result identifies whether the current host also created a real
disposable symlink or used the deterministic index-link-mode branch.

## Focused check

Run the deterministic SOURCE contract check:

```powershell
python -B scripts/check_source_contract.py --json
```

It verifies the exact 5-file package shape and the instruction clauses needed
for direct and indirect selection/activation, authority non-expansion,
coordination/recovery, and Standard O/P/E. It is static source evidence, not a
model run or loaded-copy proof.

Run the install lifecycle self-test:

```powershell
python -B scripts/manage_install.py self-test --source .
```

The self-test uses disposable temporary directories to exercise install,
status, update, rollback, unreceipted/mismatched/wrong-tree/modified/aliased/
drifted-destination refusal, uninstall, and recovery behavior. It does not
install or remove a persistent Skill copy. Receipt checks establish integrity
and routing consistency, not cryptographic ownership against a same-privilege
local actor capable of forging the complete receipt.

The local-release receipt binds accepted candidate C
`732e7efa6211d9aedeb133282ef28ce03f9bdfef`, candidate tree
`cc09ec16f85b05ed2287afd68ac6051dd800d287`, and unchanged package tree
`0ac3cbb0f1fa8fa51d8f832c8127eabc9863ec9e`. The SOURCE checker verifies that
binding and the `LOCAL_RELEASE_READY=VERIFIED` transition. Accepted Q06 provides
fresh projectless, read-only, no-tool, exact-SOURCE forward-behavior evidence
with `gpt-5.6-sol/high`; it does not prove installed-copy behavior,
publication, stable installation, cross-Harness behavior, or broad efficacy.

## Evidence limits

The retained cases are deterministic contract fixtures; they do not create
fresh model, efficacy, release, or installed-copy evidence. SOURCE qualification
proves clause coverage only. A local clean candidate commit and native review
establish the accepted `LOCAL_RELEASE_READY=VERIFIED` receipt; they do not
authorize or prove publication, persistent installation,
a remote, tag, GitHub Release, stable installed-copy behavior, or broad product
efficacy.

## Future-version lifecycle boundary

The lifecycle command accepts `--trusted-target-package-tree` and `--trusted-current-package-tree` for versions outside its built-in trust map. These values are explicit external trust inputs, not candidate-derived metadata. B1 verifies the local mechanism; immutable publication and the human-reviewed release-note carrier remain B2 evidence and are `UNKNOWN` here. If recovery-archive cleanup fails after a successful uninstall, the command reports `ABSENT`, retains and identifies the archive, and returns a warning instead of misreporting the completed uninstall as failed.
