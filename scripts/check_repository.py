from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = 'work-charter'
BASELINE = '80910a8b2375a11be897e9660c4b00a06d00dd13'
EXPECTED_SOURCE_TREE = '2ec2574116a9b2c4e8ec9a1bb4cb2636cb6279af'
EXPECTED_PACKAGE_COUNT = 5
EXPECTED_CASES = set(['cold-resume.md', 'small-task-stays-flat.md', 'work-charter-entry.md', 'work-charter-midstream.md', 'work-charter-planner-executor.md', 'work-charter-recovery-integrity.md', 'work-charter-selection.md', 'work-charter-standard.md'])
EXPECTED_FIXTURES = set(['cold-resume', 'small-task-stays-flat', 'work-charter-entry', 'work-charter-loop', 'work-charter-recovery-integrity', 'work-charter-standard'])
EXCLUDED_PARTS = {
    ".git",
    ".eval-runs",
    "__pycache__",
    ".pytest_cache",
    ".codegraph",
    ".code-review-graph",
}
LINK_PATTERN = re.compile(r"!?\[[^\]]*]\(([^)\n]+)\)")
SHA1_PATTERN = re.compile(r"[0-9a-f]{40}")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
PRIVATE_PATTERNS = {
    "private source or destination path": re.compile(r"(?i)(?:D:[\\/]GitLib[\\/]|\.codex[\\/]worktrees[\\/])"),
    "private Codex data path": re.compile(r"(?i)\.codex[\\/](?:memories|rollouts|sessions)"),
    "UUID-like task identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "secret-like token": re.compile(r"(?i)\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-(?:proj-)?[A-Za-z0-9_-]{16,})"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def normalized_sha256(data: bytes) -> str:
    text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return sha256(text.encode("utf-8"))


def is_windows_reparse_point(path: Path) -> bool:
    if os.name != "nt":
        return False
    is_junction = getattr(path, "is_junction", None)
    if is_junction is not None:
        try:
            if is_junction():
                return True
        except OSError:
            return True
    try:
        metadata = os.lstat(path)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    attributes = getattr(metadata, "st_file_attributes", None)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", None)
    if not isinstance(attributes, int) or not isinstance(reparse_flag, int):
        return True
    return bool(attributes & reparse_flag)


def is_link_like(path: Path) -> bool:
    return path.is_symlink() or is_windows_reparse_point(path)


def has_link_like_component(path: Path) -> bool:
    current = path
    while True:
        if is_link_like(current):
            return True
        if current == ROOT:
            return False
        parent = current.parent
        if parent == current:
            return True
        current = parent


def is_safe_repo_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        return False
    candidate = PurePosixPath(value)
    return not candidate.is_absolute() and ".." not in candidate.parts and candidate.as_posix() == value


def is_hash(value: object, pattern: re.Pattern[str]) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def validate_rewrite_source(
    source: object,
    relative: object,
    index: int,
    failures: list[str],
) -> None:
    label = f"{relative}: rewrite source {index}"
    if not isinstance(source, dict):
        failures.append(f"{label} must be an object")
        return
    if not is_safe_repo_path(source.get("source_path")):
        failures.append(f"{label} has unsafe or missing source_path")
    if not is_hash(source.get("source_blob"), SHA1_PATTERN):
        failures.append(f"{label} has invalid or missing source_blob")
    if not is_hash(source.get("source_normalized_sha256"), SHA256_PATTERN):
        failures.append(f"{label} has invalid or missing source_normalized_sha256")


def files_on_disk(failures: list[str]) -> set[str]:
    result = set()
    pending = [ROOT]
    while pending:
        directory = pending.pop()
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError as error:
            relative = directory.relative_to(ROOT).as_posix() or "."
            failures.append(f"{relative}: directory is unreadable: {error}")
            continue
        for entry in entries:
            path = Path(entry.path)
            relative = path.relative_to(ROOT)
            if any(part in EXCLUDED_PARTS for part in relative.parts):
                continue
            if has_link_like_component(path):
                failures.append(f"{relative.as_posix()}: symlink or junction path is not allowed")
                result.add(relative.as_posix())
                continue
            try:
                if entry.is_dir(follow_symlinks=False):
                    pending.append(path)
                elif entry.is_file(follow_symlinks=False):
                    result.add(relative.as_posix())
            except OSError as error:
                failures.append(f"{relative.as_posix()}: path is unreadable: {error}")
    return result


def check_links(relative: str, text: str, failures: list[str]) -> None:
    if not relative.endswith(".md"):
        return
    path = ROOT / relative
    for match in LINK_PATTERN.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        if not target or target.startswith("#") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
            continue
        target_path = unquote(target.split("#", 1)[0])
        resolved = (path.parent / target_path).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            failures.append(f"{relative}: local link leaves repository: {target_path}")
            continue
        if not resolved.exists():
            failures.append(f"{relative}: missing local link target: {target_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    failures: list[str] = []

    manifest_path = ROOT / "provenance" / "source-map.json"
    if has_link_like_component(manifest_path):
        result = {
            "product": PRODUCT,
            "source_commit": BASELINE,
            "mapped_files": 0,
            "failures": ["provenance/source-map.json: symlink or junction path is not allowed"],
            "result": "FAIL",
        }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True) if args.json else f"{PRODUCT}: FAIL")
        return 1
    try:
        manifest_raw = manifest_path.read_bytes()
        manifest_text = manifest_raw.decode("utf-8")
        manifest = json.loads(manifest_text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        result = {
            "product": PRODUCT,
            "source_commit": BASELINE,
            "mapped_files": 0,
            "failures": [f"provenance/source-map.json: unreadable or invalid JSON: {error}"],
            "result": "FAIL",
        }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True) if args.json else f"{PRODUCT}: FAIL")
        return 1
    if not isinstance(manifest, dict):
        failures.append("provenance manifest root must be an object")
        manifest = {}
    if manifest.get("schema") != "standalone-skill-provenance/v1":
        failures.append("provenance manifest schema mismatch")
    if manifest.get("product") != PRODUCT or manifest.get("source_commit") != BASELINE:
        failures.append("provenance product or source commit mismatch")
    if manifest.get("source_tree") != EXPECTED_SOURCE_TREE:
        failures.append("provenance source tree mismatch")

    entries_value = manifest.get("entries", [])
    if not isinstance(entries_value, list):
        failures.append("provenance entries must be a list")
        entries = []
    else:
        entries = []
        for index, entry in enumerate(entries_value):
            if isinstance(entry, dict):
                entries.append(entry)
            else:
                failures.append(f"provenance entry {index} must be an object")
    destinations = [entry.get("destination") for entry in entries]
    for entry in entries:
        relative = entry.get("destination")
        if not is_safe_repo_path(relative):
            failures.append(f"unsafe provenance destination: {relative!r}")
        if not is_hash(entry.get("target_sha256"), SHA256_PATTERN):
            failures.append(f"{relative}: invalid or missing target_sha256")
        kind = entry.get("kind")
        if kind == "exact-git-blob":
            if not is_safe_repo_path(entry.get("source_path")):
                failures.append(f"{relative}: unsafe or missing source_path")
            if not is_hash(entry.get("source_blob"), SHA1_PATTERN):
                failures.append(f"{relative}: invalid or missing source_blob")
            if not is_hash(entry.get("source_sha256"), SHA256_PATTERN):
                failures.append(f"{relative}: invalid or missing source_sha256")
        elif kind == "standalone-normalized-text-rewrite":
            if not is_hash(entry.get("target_normalized_sha256"), SHA256_PATTERN):
                failures.append(f"{relative}: invalid or missing target_normalized_sha256")
            sources = entry.get("sources")
            if not isinstance(sources, list) or not sources:
                failures.append(f"{relative}: adapted file has no valid source mapping list")
            else:
                for index, source in enumerate(sources):
                    validate_rewrite_source(source, relative, index, failures)
        else:
            failures.append(f"{relative}: unknown provenance kind")
    valid_destinations = [value for value in destinations if isinstance(value, str)]
    if len(valid_destinations) != len(set(valid_destinations)):
        failures.append("duplicate provenance destination")
    expected_files = {value for value in valid_destinations if is_safe_repo_path(value)} | {"provenance/source-map.json"}
    actual_files = files_on_disk(failures)
    missing = sorted(expected_files - actual_files)
    extra = sorted(actual_files - expected_files)
    if missing:
        failures.append(f"missing mapped files: {missing}")
    if extra:
        failures.append(f"unmapped files: {extra}")

    for entry in entries:
        relative = entry.get("destination")
        if not is_safe_repo_path(relative):
            continue
        path = ROOT / relative
        if has_link_like_component(path):
            failures.append(f"{relative}: symlink or junction path is not allowed")
            continue
        if not path.is_file():
            continue
        raw = path.read_bytes()
        if sha256(raw) != entry.get("target_sha256"):
            failures.append(f"{relative}: target SHA-256 mismatch")
        if entry.get("kind") == "exact-git-blob":
            if blob_sha1(raw) != entry.get("source_blob"):
                failures.append(f"{relative}: source Git blob mismatch")
        elif entry.get("kind") == "standalone-normalized-text-rewrite":
            if normalized_sha256(raw) != entry.get("target_normalized_sha256"):
                failures.append(f"{relative}: normalized-text SHA-256 mismatch")

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            failures.append(f"{relative}: not valid UTF-8")
            continue
        if raw.startswith(b"\xef\xbb\xbf"):
            failures.append(f"{relative}: UTF-8 BOM is not allowed")
        for number, line in enumerate(text.splitlines(), start=1):
            if line.endswith((" ", "\t")):
                failures.append(f"{relative}:{number}: trailing whitespace")
        check_links(relative, text, failures)
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{relative}: {label}")

    if manifest_raw.startswith(b"\xef\xbb\xbf"):
        failures.append("provenance/source-map.json: UTF-8 BOM is not allowed")
    for number, line in enumerate(manifest_text.splitlines(), start=1):
        if line.endswith((" ", "\t")):
            failures.append(f"provenance/source-map.json:{number}: trailing whitespace")
    for label, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(manifest_text):
            failures.append(f"provenance/source-map.json: {label}")

    package_root = ROOT / "skills" / PRODUCT
    package_files = {
        path.relative_to(package_root).as_posix()
        for path in package_root.rglob("*") if path.is_file()
    }
    mapped_package_files = {
        entry["destination"].split(f"skills/{PRODUCT}/", 1)[1]
        for entry in entries
        if isinstance(entry.get("destination"), str)
        and entry["destination"].startswith(f"skills/{PRODUCT}/")
    }
    if package_files != mapped_package_files or len(package_files) != EXPECTED_PACKAGE_COUNT:
        failures.append("package path set or file count mismatch")
    skills_root = ROOT / "skills"
    skills = {path.name for path in skills_root.iterdir() if path.is_dir()} if skills_root.is_dir() else set()
    if skills != {PRODUCT}:
        failures.append(f"unexpected Skill roots: {sorted(skills)}")

    cases_root = ROOT / "evals" / "cases"
    fixtures_root = ROOT / "evals" / "fixtures"
    cases = {path.name for path in cases_root.glob("*.md")} if cases_root.is_dir() else set()
    fixtures = {path.name for path in fixtures_root.iterdir() if path.is_dir()} if fixtures_root.is_dir() else set()
    if cases != EXPECTED_CASES:
        failures.append(f"case set mismatch: {sorted(cases)}")
    if fixtures != EXPECTED_FIXTURES:
        failures.append(f"fixture set mismatch: {sorted(fixtures)}")

    skill_path = package_root / "SKILL.md"
    skill_text = ""
    if skill_path.is_file() and not has_link_like_component(skill_path):
        try:
            skill_text = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            failures.append(f"skills/{PRODUCT}/SKILL.md: unreadable UTF-8 text: {error}")
    else:
        failures.append(f"skills/{PRODUCT}/SKILL.md: missing regular file")
    if skill_text and not re.match(r"\A---\n.*?\n---\n", skill_text, re.S):
        failures.append("SKILL.md frontmatter missing or malformed")
    references = package_root / "references"
    if references.exists():
        for reference in references.iterdir():
            if reference.is_file() and f"](references/{reference.name})" not in skill_text:
                failures.append(f"SKILL.md does not directly link references/{reference.name}")

    result = {
        "product": PRODUCT,
        "source_commit": BASELINE,
        "mapped_files": len(entries),
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"{PRODUCT}: {result['result']} ({len(entries)} mapped files)")
        for failure in failures:
            print(f"- {failure}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
