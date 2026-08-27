from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = 'work-charter'
BASELINE = '80910a8b2375a11be897e9660c4b00a06d00dd13'
EXPECTED_SOURCE_TREE = '2ec2574116a9b2c4e8ec9a1bb4cb2636cb6279af'
EXPECTED_SOURCE_MAPPING_SHA256 = '8ff0e7629b13d17f1f03695ab0363a7a18eb75fcb5573659ce71b2d917770551'
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
CANONICAL_DEVICE_UNC_PREFIX_PATTERN = re.compile(r"(?i)//[?.]/UNC/")
CANONICAL_DEVICE_DRIVE_PREFIX_PATTERN = re.compile(r"(?i)//[?.]/(?=[A-Z]:/)")
WINDOWS_PROFILE_ROOT_PATTERN = re.compile(r"(?i)(?<![A-Za-z0-9:/])[A-Z]:/+Users/+")
URI_SCHEME_PATTERN = re.compile(
    r"(?i)(?<![A-Za-z0-9+.-])(?P<scheme>[A-Za-z][A-Za-z0-9+.-]*):"
)
URI_HARD_TERMINATORS = frozenset("<>\"'`(){}")
FILE_LOCATOR_START_PATTERN = re.compile(r"(?i)(?:[/\\%]|[A-Z]:)")
WINDOWS_ABSOLUTE_DRIVE_PATTERN = re.compile(r"(?i)^[A-Z]:/")
WINDOWS_DRIVE_AUTHORITY_PATTERN = re.compile(r"(?i)^[A-Z]:(?=$|/)")
UNC_INTRODUCER_PATTERN = re.compile(r"(?<![:/])/{2,}(?!/)(?=[^\s\[\](){}'\"`])")
WINDOWS_INVALID_UNC_COMPONENT_PATTERN = re.compile(r"[\x00-\x1f<>:\"|?*]")
REGULAR_INDEX_MODES = {"100644", "100755"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def normalized_sha256(data: bytes):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return sha256(text.encode("utf-8"))


def legacy_windows_reparse_point(path: Path, lstat_function, reparse_flag):
    try:
        metadata = lstat_function(path)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    attributes = getattr(metadata, "st_file_attributes", None)
    if not isinstance(attributes, int) or not isinstance(reparse_flag, int):
        return True
    return bool(attributes & reparse_flag)


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
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", None)
    return legacy_windows_reparse_point(path, os.lstat, reparse_flag)


def is_link_like(path: Path) -> bool:
    return path.is_symlink() or is_windows_reparse_point(path)


def has_link_like_component(path: Path, link_like_function=is_link_like) -> bool:
    current = path
    while True:
        if link_like_function(current):
            return True
        if current == ROOT:
            return False
        parent = current.parent
        if parent == current:
            return True
        current = parent


def has_link_like_ancestor(path: Path, link_like_function=is_link_like) -> bool:
    current = path.absolute()
    while True:
        if link_like_function(current):
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def is_safe_repo_path(value: object) -> bool:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or ":" in value
        or any(unicodedata.category(character) == "Cc" for character in value)
    ):
        return False
    candidate = PurePosixPath(value)
    return not candidate.is_absolute() and ".." not in candidate.parts and candidate.as_posix() == value


def is_hash(value: object, pattern: re.Pattern[str]) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def canonicalize_windows_locator_text(text: str) -> str:
    normalized = text.replace("\\", "/")
    normalized = CANONICAL_DEVICE_UNC_PREFIX_PATTERN.sub("//", normalized)
    return CANONICAL_DEVICE_DRIVE_PREFIX_PATTERN.sub("", normalized)


def has_private_windows_profile_locator(normalized_text: str) -> bool:
    for match in WINDOWS_PROFILE_ROOT_PATTERN.finditer(normalized_text):
        remainder = normalized_text[match.end():]
        profile_component = re.split(r"[\r\n]", remainder.split("/", 1)[0], maxsplit=1)[0]
        if profile_component.strip():
            return True
    return False


def is_valid_unc_component(component: str) -> bool:
    return bool(component.strip()) and WINDOWS_INVALID_UNC_COMPONENT_PATTERN.search(component) is None


def iter_uri_candidates(text: str):
    for match in URI_SCHEME_PATTERN.finditer(text):
        scheme = match.group("scheme").casefold()
        payload_start = match.end()
        if scheme != "file":
            end = payload_start
            while end < len(text) and not text[end].isspace() and text[end] not in URI_HARD_TERMINATORS:
                end += 1
            yield text[match.start():end], match.start(), end, False, False
            continue

        cursor = payload_start
        while cursor < len(text) and text[cursor] in " \t":
            cursor += 1
        if cursor > payload_start and (
            cursor == len(text)
            or text[cursor] in "\r\n"
            or text[cursor] in URI_HARD_TERMINATORS
            or FILE_LOCATOR_START_PATTERN.match(text, cursor) is None
        ):
            yield text[match.start():payload_start], match.start(), payload_start, False, False
            continue

        end = cursor
        leading_whitespace = cursor > payload_start
        raw_whitespace = leading_whitespace
        while end < len(text) and text[end] not in "\r\n" and text[end] not in URI_HARD_TERMINATORS:
            raw_whitespace = raw_whitespace or text[end].isspace()
            end += 1
        yield text[match.start():end], match.start(), end, leading_whitespace, raw_whitespace


def unc_locator_state(normalized_text: str) -> str:
    explicit_uri_spans = [(start, end) for _, start, end, _, _ in iter_uri_candidates(normalized_text)]
    ambiguous = False
    for match in UNC_INTRODUCER_PATTERN.finditer(normalized_text):
        if any(start <= match.start() < end for start, end in explicit_uri_spans):
            continue
        line_remainder = re.split(r"[\r\n]", normalized_text[match.end():], maxsplit=1)[0]
        server, server_separator, share_remainder = line_remainder.partition("/")
        if not server_separator:
            if is_valid_unc_component(server):
                ambiguous = True
            continue
        share = share_remainder.partition("/")[0]
        if is_valid_unc_component(server) and is_valid_unc_component(share):
            return "private"
        if server or share:
            ambiguous = True
    return "ambiguous" if ambiguous else "portable"


def normalized_private_labels(normalized: str) -> list[str]:
    labels = [label for label, pattern in PRIVATE_PATTERNS.items() if pattern.search(normalized)]
    if has_private_windows_profile_locator(normalized):
        labels.append("private Windows user-profile locator")
    unc_state = unc_locator_state(normalized)
    if unc_state == "private":
        labels.append("private UNC locator")
    elif unc_state == "ambiguous":
        labels.append("ambiguous Windows locator")
    return labels


def path_private_labels(text: str) -> list[str]:
    return normalized_private_labels(canonicalize_windows_locator_text(text))


def canonicalize_file_uri_local_path(decoded_path: str) -> str:
    normalized = canonicalize_windows_locator_text(decoded_path)
    without_leading_separators = normalized.lstrip("/")
    if WINDOWS_ABSOLUTE_DRIVE_PATTERN.match(without_leading_separators):
        return without_leading_separators
    if normalized.startswith("//"):
        return "//" + without_leading_separators
    return normalized


def file_uri_local_representations(text: str):
    for candidate, _, _, leading_whitespace, raw_whitespace in iter_uri_candidates(text):
        if candidate[:5].casefold() != "file:":
            continue
        if leading_whitespace:
            yield None, True
            continue
        try:
            parsed = urlsplit(candidate)
        except ValueError:
            if candidate[:5].casefold() == "file:":
                yield None, True
            continue
        if parsed.scheme.casefold() != "file":
            continue
        if any(delimiter in candidate[5:] for delimiter in "?#"):
            yield None, True
            continue
        try:
            authority = canonicalize_windows_locator_text(unquote(parsed.netloc, errors="strict"))
            path = canonicalize_windows_locator_text(unquote(parsed.path, errors="strict"))
        except UnicodeDecodeError:
            yield None, True
            continue
        if "%" in authority or "%" in path:
            yield None, True
            continue
        drive_authority = WINDOWS_DRIVE_AUTHORITY_PATTERN.match(authority)
        if drive_authority:
            authority_remainder = authority[drive_authority.end():]
            local_remainder = authority_remainder.rstrip("/")
            if local_remainder and path:
                local_remainder += "/" + path.lstrip("/")
            elif path:
                local_remainder = path
            representation = authority[:2] + "/" + local_remainder.lstrip("/")
            structurally_ambiguous = not WINDOWS_ABSOLUTE_DRIVE_PATTERN.match(representation)
            yield representation, structurally_ambiguous or (raw_whitespace and not path_private_labels(representation))
            continue
        if authority and authority.casefold() != "localhost":
            representation = "//" + authority.strip("/") + "/" + path.lstrip("/")
            yield representation, raw_whitespace and not path_private_labels(representation)
            continue
        representation = canonicalize_file_uri_local_path(path)
        if not representation:
            yield representation, False
        elif WINDOWS_ABSOLUTE_DRIVE_PATTERN.match(representation) or representation.startswith("/"):
            yield representation, raw_whitespace and not path_private_labels(representation)
        else:
            yield representation, True


def private_labels(text: str) -> list[str]:
    labels = path_private_labels(text)
    for representation, ambiguous in file_uri_local_representations(text):
        if ambiguous:
            if "ambiguous file URI locator" not in labels:
                labels.append("ambiguous file URI locator")
            continue
        for label in path_private_labels(representation):
            if label not in labels:
                labels.append(label)
    return labels


class DuplicateJsonKeyError(ValueError):
    pass


def reject_duplicate_json_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def iter_text_values(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, nested in value.items():
            if isinstance(key, str):
                yield key
            yield from iter_text_values(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_text_values(nested)


def contains_unpaired_unicode_surrogate(value) -> bool:
    return any(
        0xD800 <= ord(character) <= 0xDFFF
        for text in iter_text_values(value)
        for character in text
    )


def inventory_differences(expected: set[str], actual: set[str]) -> tuple[list[str], list[str]]:
    return sorted(expected - actual), sorted(actual - expected)


class SnapshotError(RuntimeError):
    pass


def isolated_git_environment(inherited_environment=None) -> dict[str, str]:
    source = os.environ if inherited_environment is None else inherited_environment
    environment = {
        key: value
        for key, value in source.items()
        if not key.casefold().startswith("git_")
    }
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    return environment


def git_index_output(repository: Path, arguments: list[str], inherited_environment=None) -> bytes:
    exact_repository = repository.absolute()
    if not exact_repository.is_dir():
        raise SnapshotError("Git index snapshot repository is not a directory")
    try:
        completed = subprocess.run(
            ["git", "-c", f"safe.directory={exact_repository}", "-C", str(exact_repository), *arguments],
            env=isolated_git_environment(inherited_environment),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except (OSError, ValueError) as error:
        raise SnapshotError("Git index snapshot command could not start") from error
    if completed.returncode != 0:
        raise SnapshotError("Git index snapshot command failed")
    return completed.stdout


def staged_index_entries(repository: Path, inherited_environment=None):
    raw = git_index_output(
        repository,
        ["ls-files", "--cached", "--stage", "-z"],
        inherited_environment,
    )
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            metadata, path_bytes = record.split(b"\t", 1)
            mode, object_id, stage = metadata.decode("ascii").split()
            relative = path_bytes.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as error:
            raise SnapshotError("Git index contains an invalid entry") from error
        if stage != "0":
            raise SnapshotError("Git index contains an unresolved entry")
        entries.append((mode, object_id, relative))
    return entries


def read_index_blob(repository: Path, object_id: str, inherited_environment=None) -> bytes:
    return git_index_output(
        repository,
        ["cat-file", "blob", object_id],
        inherited_environment,
    )


def materialize_index_snapshot(
    repository: Path,
    destination: Path,
    entries_function=staged_index_entries,
    blob_function=read_index_blob,
) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    seen = set()
    for mode, object_id, relative in entries_function(repository):
        if not is_safe_repo_path(relative):
            raise SnapshotError("Git index contains an unsafe path")
        if relative in seen:
            raise SnapshotError("Git index contains a duplicate path")
        seen.add(relative)
        if mode not in REGULAR_INDEX_MODES:
            raise SnapshotError(f"Git index path is not a regular file: {relative}")
        if not is_hash(object_id, SHA1_PATTERN):
            raise SnapshotError("Git index contains an invalid object identity")
        raw = blob_function(repository, object_id)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        if mode == "100755":
            target.chmod(target.stat().st_mode | stat.S_IXUSR)


def external_link_snapshot_sentinel_proof():
    failures = []
    proof = "deterministic-index-link-mode"
    with tempfile.TemporaryDirectory(prefix=f"{PRODUCT}-snapshot-sentinel-") as temporary:
        root = Path(temporary)
        live_root = root / "live"
        destination = root / "snapshot"
        sentinel = root / "outside-sentinel.txt"
        link = live_root / "external-link"
        live_root.mkdir()
        sentinel_bytes = b"external-target-sentinel"
        sentinel.write_bytes(sentinel_bytes)
        try:
            os.symlink(sentinel, link)
            proof = "real-external-symlink"
        except (NotImplementedError, OSError):
            pass

        blob_reads = []

        def link_entry(_):
            return [("120000", "0" * 40, "external-link")]

        def forbidden_blob_read(source, object_id):
            blob_reads.append((source, object_id))
            return link.read_bytes() if link.is_symlink() else sentinel.read_bytes()

        try:
            materialize_index_snapshot(
                live_root,
                destination,
                entries_function=link_entry,
                blob_function=forbidden_blob_read,
            )
        except SnapshotError:
            pass
        else:
            failures.append("external link index entry was not rejected")
        if blob_reads:
            failures.append("external link target blob was read")
        if (destination / "external-link").exists():
            failures.append("external link target was copied")
        if sentinel.read_bytes() != sentinel_bytes:
            failures.append("external link sentinel changed")
    return failures, proof


def hostile_git_selector_isolation_proof():
    failures = []
    with tempfile.TemporaryDirectory(prefix=f"{PRODUCT}-git-selector-") as temporary:
        root = Path(temporary)
        intended = root / "intended"
        decoy = root / "decoy"
        intended_bytes = b"intended-index-evidence\n"
        decoy_bytes = b"decoy-index-evidence\n"

        def initialize(repository, relative, raw):
            repository.mkdir()
            git_index_output(repository, ["init", "--quiet"])
            (repository / relative).write_bytes(raw)
            git_index_output(repository, ["add", "--", relative])

        try:
            initialize(intended, "intended.txt", intended_bytes)
            initialize(decoy, "decoy.txt", decoy_bytes)
        except SnapshotError as error:
            return [f"disposable Git repository setup failed: {error}"]

        hostile_environment = os.environ.copy()
        hostile_environment.update(
            {
                "GIT_DIR": str(decoy / ".git"),
                "GIT_COMMON_DIR": str(decoy / ".git"),
                "GIT_WORK_TREE": str(decoy),
                "GIT_INDEX_FILE": str(decoy / ".git" / "index"),
                "GIT_OBJECT_DIRECTORY": str(decoy / ".git" / "objects"),
                "GIT_ALTERNATE_OBJECT_DIRECTORIES": str(decoy / ".git" / "objects"),
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "core.worktree",
                "GIT_CONFIG_VALUE_0": str(decoy),
                "GIT_CONFIG_GLOBAL": str(decoy / "global.config"),
                "GIT_CONFIG_SYSTEM": str(decoy / "system.config"),
                "GIT_CONFIG_NOSYSTEM": "0",
                "GIT_CEILING_DIRECTORIES": str(decoy),
                "GIT_DISCOVERY_ACROSS_FILESYSTEM": "1",
                "GIT_OPTIONAL_LOCKS": "1",
            }
        )
        isolated = {
            key.casefold(): value
            for key, value in isolated_git_environment(hostile_environment).items()
            if key.casefold().startswith("git_")
        }
        if isolated != {"git_optional_locks": "0"}:
            failures.append("inherited Git selector variables were not removed case-insensitively")

        try:
            entries = staged_index_entries(intended, hostile_environment)
        except SnapshotError as error:
            failures.append(f"hostile-environment ls-files failed: {error}")
            return failures
        if len(entries) != 1 or entries[0][2] != "intended.txt":
            failures.append("hostile Git selectors redirected ls-files")
            return failures
        try:
            raw = read_index_blob(intended, entries[0][1], hostile_environment)
        except SnapshotError as error:
            failures.append(f"hostile-environment cat-file failed: {error}")
            return failures
        if raw != intended_bytes or raw == decoy_bytes:
            failures.append("hostile Git selectors redirected cat-file")
    return failures


def source_mapping_sha256(manifest: dict) -> str:
    entries = manifest.get("entries")
    if isinstance(entries, list):
        projected_entries = []
        for entry in entries:
            if not isinstance(entry, dict):
                projected_entries.append(entry)
                continue
            projected = {
                "destination": entry.get("destination"),
                "kind": entry.get("kind"),
            }
            if entry.get("kind") == "exact-git-blob":
                projected.update(
                    {
                        "source_path": entry.get("source_path"),
                        "source_blob": entry.get("source_blob"),
                        "source_sha256": entry.get("source_sha256"),
                    }
                )
            elif entry.get("kind") == "standalone-normalized-text-rewrite":
                projected["sources"] = entry.get("sources")
            elif entry.get("kind") == "repository-native":
                projected.update(
                    {
                        "note": entry.get("note"),
                        "target_sha256": entry.get("target_sha256"),
                    }
                )
            projected_entries.append(projected)
    else:
        projected_entries = entries
    projection = {
        "manifest_provenance": manifest.get("manifest_provenance"),
        "entries": projected_entries,
    }
    encoded = json.dumps(
        projection,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded)


def validate_manifest_identity(manifest: dict, failures: list[str]) -> None:
    if manifest.get("schema") != "standalone-skill-provenance/v2":
        failures.append("provenance manifest schema mismatch")
    if manifest.get("product") != PRODUCT or manifest.get("source_commit") != BASELINE:
        failures.append("provenance product or source commit mismatch")
    if manifest.get("source_tree") != EXPECTED_SOURCE_TREE:
        failures.append("provenance source tree mismatch")
    if source_mapping_sha256(manifest) != EXPECTED_SOURCE_MAPPING_SHA256:
        failures.append("provenance source mapping mismatch")


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


def validate_manifest_provenance(manifest: dict, failures: list[str]) -> None:
    sources = manifest.get("manifest_provenance")
    if not isinstance(sources, list) or not sources:
        failures.append("manifest_provenance must be a nonempty source mapping list")
        return
    for index, source in enumerate(sources):
        validate_rewrite_source(source, "manifest_provenance", index, failures)


def iter_manifest_source_records(manifest: dict):
    manifest_sources = manifest.get("manifest_provenance")
    if isinstance(manifest_sources, list):
        yield from manifest_sources
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("kind") == "exact-git-blob":
            yield entry
        elif entry.get("kind") == "standalone-normalized-text-rewrite":
            sources = entry.get("sources")
            if isinstance(sources, list):
                yield from sources


def verify_source_object_membership(
    source_repository: Path,
    manifest: dict,
    failures: list[str],
) -> None:
    exact_repository = source_repository.absolute()
    if not exact_repository.is_dir() or has_link_like_ancestor(exact_repository):
        failures.append("source object repository is missing or link-like")
        return
    try:
        commit = git_index_output(
            exact_repository,
            ["rev-parse", "--verify", f"{BASELINE}^{{commit}}"],
        ).decode("ascii").strip()
        tree = git_index_output(
            exact_repository,
            ["rev-parse", "--verify", f"{BASELINE}^{{tree}}"],
        ).decode("ascii").strip()
    except (SnapshotError, UnicodeDecodeError):
        failures.append("source object repository cannot resolve the baseline commit and tree")
        return
    if commit != BASELINE or tree != EXPECTED_SOURCE_TREE:
        failures.append("source object repository baseline commit or tree mismatch")
        return

    seen = set()
    for source in iter_manifest_source_records(manifest):
        if not isinstance(source, dict):
            continue
        source_path = source.get("source_path")
        source_blob = source.get("source_blob")
        if not is_safe_repo_path(source_path) or not is_hash(source_blob, SHA1_PATTERN):
            continue
        identity = (source_path, source_blob)
        if identity in seen:
            continue
        seen.add(identity)
        try:
            resolved_blob = git_index_output(
                exact_repository,
                ["rev-parse", "--verify", f"{BASELINE}:{source_path}"],
            ).decode("ascii").strip()
            raw = git_index_output(
                exact_repository,
                ["cat-file", "blob", f"{BASELINE}:{source_path}"],
            )
        except (SnapshotError, UnicodeDecodeError):
            failures.append(f"{source_path}: source object membership could not be resolved")
            continue
        if resolved_blob != source_blob or blob_sha1(raw) != source_blob:
            failures.append(f"{source_path}: source blob is not bound to the baseline tree path")
        source_sha256 = source.get("source_sha256")
        if source_sha256 is not None and sha256(raw) != source_sha256:
            failures.append(f"{source_path}: source object raw SHA-256 mismatch")
        source_normalized_sha256 = source.get("source_normalized_sha256")
        if source_normalized_sha256 is not None and normalized_sha256(raw) != source_normalized_sha256:
            failures.append(f"{source_path}: source object normalized SHA-256 mismatch")


def windows_profile_locator_matrix() -> list[tuple[str, str, str]]:
    backslash = "\\"
    forward = "/"
    label = "private Windows user-profile locator"
    ascii_space_profile = "Jane" + " " + "Doe"
    unicode_profile = chr(0x674E) + chr(0x534E)

    def drive_profile(separator: str, profile: str, child_separator=None) -> str:
        locator = "C:" + separator + "Users" + separator + profile
        return locator if child_separator is None else locator + child_separator + "project"

    return [
        ("private-user-profile-backslash-deeper", drive_profile(backslash, "alice", backslash), label),
        ("private-user-profile-forward-space-end", drive_profile(forward, ascii_space_profile), label),
        ("private-user-profile-forward-space-deeper", drive_profile(forward, ascii_space_profile, forward), label),
        ("private-user-profile-mixed-unicode-deeper", drive_profile(backslash, unicode_profile, forward), label),
        ("private-user-profile-forward-unicode-end", drive_profile(forward, unicode_profile), label),
        (
            "private-user-profile-device-question-backslash",
            backslash * 2 + "?" + backslash + drive_profile(backslash, ascii_space_profile, backslash),
            label,
        ),
        (
            "private-user-profile-device-question-forward",
            forward * 2 + "?" + forward + drive_profile(forward, unicode_profile, forward),
            label,
        ),
        (
            "private-user-profile-device-question-mixed",
            backslash * 2 + "?" + forward + drive_profile(backslash, unicode_profile, forward),
            label,
        ),
        (
            "private-user-profile-device-dot-backslash",
            backslash * 2 + "." + backslash + drive_profile(backslash, unicode_profile),
            label,
        ),
        (
            "private-user-profile-device-dot-forward",
            forward * 2 + "." + forward + drive_profile(forward, ascii_space_profile, forward),
            label,
        ),
        (
            "private-user-profile-device-dot-mixed",
            forward * 2 + "." + backslash + drive_profile(forward, unicode_profile, backslash),
            label,
        ),
    ]


def windows_private_locator_matrix() -> list[tuple[str, str, str]]:
    backslash = "\\"
    forward = "/"
    label = "private UNC locator"
    unicode_server = chr(0x670D) + chr(0x52A1) + chr(0x5668)
    unicode_share = chr(0x5171) + chr(0x4EAB)
    space_server = "build" + " " + "server"
    space_share = "team" + " " + "share"

    def unc(server: str, share: str, first_separator: str, child_separator=None) -> str:
        locator = first_separator * 2 + server + first_separator + share
        return locator if child_separator is None else locator + child_separator + "project"

    cases = [
        ("private-unc-backslash", unc("server", "share", backslash, backslash), label),
        ("private-unc-forward", unc("server", "share", forward, forward), label),
        ("private-unc-mixed", unc("server", "share", backslash, forward), label),
        ("private-unc-unicode-server", unc(unicode_server, "share", backslash, forward), label),
        ("private-unc-unicode-share", unc("server", unicode_share, forward, backslash), label),
        ("private-unc-space-server", unc(space_server, "share", backslash, forward), label),
        ("private-unc-space-share", unc("server", space_share, forward, backslash), label),
        (
            "private-device-question-backslash",
            backslash * 2 + "?" + backslash + "UNC" + backslash + backslash.join(("server", "share", "project")),
            label,
        ),
        (
            "private-device-question-forward",
            forward * 2 + "?" + forward + "UNC" + forward + forward.join(("server", unicode_share, "project")),
            label,
        ),
        (
            "private-device-question-mixed",
            backslash * 2 + "?" + forward + "UNC" + backslash + unicode_server + forward + "share" + backslash + "project",
            label,
        ),
        (
            "private-device-dot-backslash",
            backslash * 2 + "." + backslash + "UNC" + backslash + backslash.join((space_server, "share", "project")),
            label,
        ),
        (
            "private-device-dot-forward",
            forward * 2 + "." + forward + "UNC" + forward + forward.join(("server", space_share, "project")),
            label,
        ),
        (
            "private-device-dot-mixed",
            forward * 2 + "." + backslash + "UNC" + forward + "server" + backslash + unicode_share + forward + "project",
            label,
        ),
    ]
    for leading_separator_count in (3, 4, 5):
        cases.append(
            (
                f"private-unc-leading-separators-{leading_separator_count}",
                forward * leading_separator_count + forward.join(("server", "share", "project")),
                label,
            )
        )
    return cases


def file_uri_private_locator_matrix() -> list[tuple[str, str, str]]:
    backslash = "\\"
    forward = "/"
    profile_label = "private Windows user-profile locator"
    unc_label = "private UNC locator"
    ascii_space_profile = "Jane" + " " + "Doe"
    unicode_profile = chr(0x674E) + chr(0x534E)
    unicode_server = chr(0x670D) + chr(0x52A1) + chr(0x5668)
    unicode_share = chr(0x5171) + chr(0x4EAB)

    def drive_profile(profile: str, child=True) -> str:
        parts = ["C:", "Users", profile]
        if child:
            parts.append("project")
        return forward.join(parts)

    cases = [
        ("private-file-uri-triple-slash", "file:" + forward * 3 + drive_profile("alice"), profile_label),
        ("private-file-uri-single-slash", "file:" + forward + drive_profile(ascii_space_profile), profile_label),
        ("private-file-uri-common-opaque", "file:" + drive_profile(unicode_profile), profile_label),
        (
            "private-file-uri-localhost",
            "file:" + forward * 2 + "localhost" + forward + drive_profile(ascii_space_profile),
            profile_label,
        ),
        ("private-file-uri-drive-authority-upper", "file:" + forward * 2 + "C:" + forward + forward.join(("Users", ascii_space_profile, "project")), profile_label),
        ("private-file-uri-drive-authority-lower-end", "file:" + forward * 2 + "c:" + forward + forward.join(("Users", unicode_profile)), profile_label),
        ("private-file-uri-encoded-drive-authority", "file:" + forward * 2 + quote("C:", safe="") + forward + forward.join(("Users", quote(ascii_space_profile, safe=""))), profile_label),
        (
            "private-file-uri-encoded-full-drive-authority",
            "file:" + forward * 2 + quote(drive_profile("alice"), safe=""),
            profile_label,
        ),
        (
            "private-file-uri-encoded-full-drive-authority-backslash-unicode",
            "file:" + forward * 2 + quote(backslash.join(("c:", "Users", unicode_profile)), safe=""),
            profile_label,
        ),
        (
            "private-file-uri-encoded-drive-authority-plus-path",
            "file:" + forward * 2 + quote(forward.join(("C:", "Users", ascii_space_profile)), safe="") + forward + "project",
            profile_label,
        ),
        (
            "private-file-uri-uppercase-scheme",
            "FILE:" + forward * 3 + drive_profile(unicode_profile),
            profile_label,
        ),
        (
            "private-file-uri-percent-drive-colon",
            "file:" + forward * 3 + "C%3A" + forward + forward.join(("Users", "alice", "project")),
            profile_label,
        ),
        (
            "private-file-uri-percent-separators",
            "file:" + quote(drive_profile("alice"), safe=":"),
            profile_label,
        ),
        (
            "private-file-uri-percent-space",
            "file:" + forward * 3 + drive_profile(quote(ascii_space_profile, safe="")),
            profile_label,
        ),
        (
            "private-file-uri-percent-unicode",
            "file:" + forward * 3 + drive_profile(quote(unicode_profile, safe="")),
            profile_label,
        ),
        (
            "private-file-uri-unc-authority",
            "file:" + forward * 2 + "server" + forward + forward.join(("share", "project")),
            unc_label,
        ),
        ("private-file-uri-unicode-unc-authority", "file:" + forward * 2 + unicode_server + forward + forward.join((unicode_share, "project")), unc_label),
        ("private-file-uri-encoded-unicode-unc-authority", "file:" + forward * 2 + quote(unicode_server, safe="") + forward + forward.join((quote(unicode_share, safe=""), "project")), unc_label),
        ("private-file-uri-empty-authority-unc-path", "file:" + forward * 4 + forward.join((unicode_server, "team" + " " + "share", "project")), unc_label),
        (
            "private-file-uri-percent-unc-path",
            "file:" + forward * 2 + "server" + quote(forward + forward.join(("share", "project")), safe=""),
            unc_label,
        ),
        (
            "private-file-uri-device-question-drive",
            "file:" + quote(forward * 2 + "?" + forward + drive_profile(ascii_space_profile), safe=""),
            profile_label,
        ),
        (
            "private-file-uri-device-dot-drive",
            "file:" + quote(backslash * 2 + "." + backslash + drive_profile(unicode_profile), safe=""),
            profile_label,
        ),
    ]
    for leading_separator_count in (2, 3, 4, 5):
        decoded_path = forward * leading_separator_count + drive_profile("alice")
        cases.append(
            (
                f"private-file-uri-decoded-leading-separators-{leading_separator_count}",
                "file:" + quote(decoded_path, safe=""),
                profile_label,
            )
        )
    return cases


def ambiguous_locator_matrix() -> list[tuple[str, str, str]]:
    forward = "/"
    ambiguous_file = "ambiguous file URI locator"
    ambiguous_windows = "ambiguous Windows locator"
    profile_like_path = forward.join(("C:", "Users", "sample"))
    return [
        ("ambiguous-file-uri-device-query-drive", "file:" + forward * 2 + "?" + forward + profile_like_path, ambiguous_file),
        ("ambiguous-file-uri-device-query-unc", "file:" + forward * 2 + "?" + forward + forward.join(("UNC", "server", "share")), ambiguous_file),
        ("ambiguous-file-uri-empty-query", "file:" + forward * 3 + "C:" + forward + "ProgramData" + "?", ambiguous_file),
        ("ambiguous-file-uri-empty-fragment", "file:" + forward * 3 + "C:" + forward + "ProgramData" + "#", ambiguous_file),
        (
            "ambiguous-file-uri-raw-space-query-tail",
            "file:" + forward * 3 + forward.join(("C:", "Program" + " " + "Files")) + "?tail",
            ambiguous_file,
        ),
        (
            "ambiguous-file-uri-raw-space-fragment-tail",
            "file:" + forward * 3 + forward.join(("C:", "Program" + " " + "Files")) + "#tail",
            ambiguous_file,
        ),
        (
            "ambiguous-file-uri-space-before-locator",
            "file:" + " " + forward * 3 + profile_like_path,
            ambiguous_file,
        ),
        ("ambiguous-file-uri-double-encoded-drive", "file:" + forward * 2 + quote(quote(profile_like_path, safe=""), safe=""), ambiguous_file),
        ("ambiguous-file-uri-relative", "file:" + forward.join(("docs", "guide.md")), ambiguous_file),
        ("ambiguous-file-uri-malformed-authority", "file:" + forward * 2 + "[invalid", ambiguous_file),
        ("ambiguous-file-uri-invalid-utf8-path", "file:" + forward * 3 + "C:" + forward + "Us%FFers" + forward + "sample", ambiguous_file),
        ("ambiguous-file-uri-invalid-utf8-authority", "file:" + forward * 2 + "serv%FFer" + forward + "share", ambiguous_file),
        ("ambiguous-file-uri-invalid-drive-authority", "file:" + forward * 2 + quote("CC:" + forward + "Users" + forward + "sample", safe=""), ambiguous_windows),
        ("ambiguous-file-uri-incomplete-unc", "file:" + forward * 2 + "server" + forward, ambiguous_windows),
        ("ambiguous-direct-unc-empty-share", forward * 2 + "server" + forward, ambiguous_windows),
        ("ambiguous-direct-unc-server-only", forward * 2 + "server", ambiguous_windows),
        ("ambiguous-direct-unc-whitespace-share", forward * 2 + "server" + forward + " " * 3, ambiguous_windows),
        ("ambiguous-direct-unc-invalid-share", forward * 2 + forward.join(("server", "sha" + ":" + "re")), ambiguous_windows),
    ]


def windows_portable_near_neighbors() -> list[tuple[str, str]]:
    backslash = "\\"
    forward = "/"
    users_root = forward.join(("C:", "Users"))
    return [
        (
            "portable-https-url",
            "https:" + forward * 2 + forward.join(("server", "share", "project")),
        ),
        ("portable-double-slash-text", "Use " + forward * 2 + " in a syntax example."),
        ("portable-relative-path", forward.join(("docs", "guide.md"))),
        ("portable-host-like-relative", forward.join(("server", "share", "project"))),
        ("portable-publication-text", "Use a repository-relative path or an environment variable."),
        ("portable-profile-like-url", "https:" + forward * 2 + "example.test" + forward + users_root + forward + "sample"),
        ("portable-relative-users", forward.join(("Users", "sample", "project"))),
        ("portable-embedded-drive-token", "prefix" + users_root + forward + "sample"),
        ("portable-empty-profile", users_root + forward),
        ("portable-singular-user-root", "C:" + backslash + backslash.join(("User", "sample"))),
        ("portable-non-profile-root", forward.join(("C:", "Profiles", "sample"))),
    ]


def uri_portable_near_neighbors() -> list[tuple[str, str]]:
    forward = "/"
    profile_like_path = forward.join(("C:", "Users", "sample"))
    non_profile_path = forward.join(("C:", "ProgramData", "example"))
    empty_profile_path = forward.join(("C:", "Users")) + forward
    return [
        ("portable-http-profile-example", "http:" + forward * 2 + "example.test" + forward + profile_like_path),
        ("portable-https-profile-example", "https:" + forward * 2 + "example.test" + forward + profile_like_path),
        ("portable-https-unc-like-path", "https:" + forward * 2 + "example.test" + forward * 2 + forward.join(("server", "share"))),
        ("portable-other-uri-profile-example", "example:" + profile_like_path),
        ("portable-file-uri-non-profile-root", "file:" + forward * 3 + non_profile_path),
        ("portable-file-uri-localhost-non-profile", "file:" + forward * 2 + "localhost" + forward + non_profile_path),
        ("portable-file-uri-drive-authority-non-profile", "file:" + forward * 2 + "C:" + forward + non_profile_path),
        ("portable-file-uri-drive-authority-empty-profile", "file:" + forward * 2 + "C:" + forward + empty_profile_path),
        ("portable-file-uri-encoded-full-drive-authority-non-profile", "file:" + forward * 2 + quote(non_profile_path, safe="")),
        ("portable-file-uri-encoded-full-drive-authority-empty-profile", "file:" + forward * 2 + quote(empty_profile_path, safe="")),
        ("portable-file-uri-drive-root", "file:" + forward * 2 + "C:"),
        ("portable-file-uri-posix", "file:" + forward * 3 + forward.join(("var", "tmp", "example"))),
        ("portable-bare-file-scheme", "The " + "file:" + " scheme names local resources."),
        ("portable-file-uri-empty-profile", "file:" + forward * 3 + empty_profile_path),
    ]


def private_locator_matrix() -> list[tuple[str, str, str]]:
    return windows_profile_locator_matrix() + windows_private_locator_matrix() + file_uri_private_locator_matrix()


def rejected_locator_matrix() -> list[tuple[str, str, str]]:
    return private_locator_matrix() + ambiguous_locator_matrix()


def portable_locator_near_neighbors() -> list[tuple[str, str]]:
    return windows_portable_near_neighbors() + uri_portable_near_neighbors()


def check_generic_regression_matrix(failures: list[str]) -> None:
    prefix = "checker regression matrix"
    for name, locator, expected_label in rejected_locator_matrix():
        if expected_label not in private_labels(locator):
            failures.append(f"{prefix}: {name} was not rejected")
    for name, text in portable_locator_near_neighbors():
        if private_labels(text):
            failures.append(f"{prefix}: {name} was rejected")
    if normalized_sha256(b"\xff") is not None:
        failures.append(f"{prefix}: invalid UTF-8 was accepted for normalized hashing")

    schema_failures: list[str] = []
    validate_manifest_identity({}, schema_failures)
    if len(schema_failures) != 4:
        failures.append(f"{prefix}: incomplete manifest identity was not rejected")
    source_failures: list[str] = []
    validate_rewrite_source({}, "README.md", 0, source_failures)
    if len(source_failures) != 3:
        failures.append(f"{prefix}: incomplete rewrite source was not rejected")
    manifest_source_failures: list[str] = []
    validate_manifest_provenance(
        {
            "manifest_provenance": [
                {
                    "source_path": "docs/PROVENANCE.md" + chr(0x85) + "hidden",
                    "source_blob": "0" * 40,
                    "source_normalized_sha256": "0" * 64,
                }
            ]
        },
        manifest_source_failures,
    )
    if len(manifest_source_failures) != 1:
        failures.append(f"{prefix}: unsafe manifest_provenance source was not rejected")

    unsafe_paths = [
        "",
        "../outside",
        "/absolute",
        "drive:C",
        "back\\slash",
        "nul" + chr(0) + "path",
        "control" + chr(0x1F) + "path",
    ]
    if any(is_safe_repo_path(value) for value in unsafe_paths) or not is_safe_repo_path("docs/file.md"):
        failures.append(f"{prefix}: repository path containment matrix failed")
    control_code_points = tuple(range(0x20)) + (0x7F,) + tuple(range(0x80, 0xA0))
    if any(
        unicodedata.category(chr(code_point)) != "Cc"
        or is_safe_repo_path("docs/control-" + chr(code_point) + "-path.md")
        for code_point in control_code_points
    ):
        failures.append(f"{prefix}: Unicode General_Category Cc path boundary failed")
    non_control_category_samples = {
        "Cf": 0x200D,
        "Cs": 0xD800,
        "Co": 0xE000,
        "Cn": 0x0378,
        "Zs": 0x00A0,
    }
    if any(
        unicodedata.category(chr(code_point)) != category
        or not is_safe_repo_path("docs/non-control-" + chr(code_point) + "-path.md")
        for category, code_point in non_control_category_samples.items()
    ):
        failures.append(f"{prefix}: non-Cc Unicode path categories were rejected")
    missing, extra = inventory_differences({"mapped.txt"}, set())
    if missing != ["mapped.txt"] or extra:
        failures.append(f"{prefix}: missing mapped content was not detected")

    class Metadata:
        def __init__(self, attributes=None):
            if attributes is not None:
                self.st_file_attributes = attributes

    reparse_flag = 0x400
    if not legacy_windows_reparse_point(Path("probe"), lambda _: Metadata(reparse_flag), reparse_flag):
        failures.append(f"{prefix}: compatibility reparse branch did not reject a reparse point")
    if legacy_windows_reparse_point(Path("probe"), lambda _: Metadata(0), reparse_flag):
        failures.append(f"{prefix}: compatibility reparse branch rejected an ordinary path")
    if not legacy_windows_reparse_point(Path("probe"), lambda _: Metadata(), reparse_flag):
        failures.append(f"{prefix}: missing reparse metadata did not fail closed")
    traversal_probe = ROOT / "matrix-link" / "mapped.txt"
    if not has_link_like_component(traversal_probe, lambda path: path.name == "matrix-link"):
        failures.append(f"{prefix}: symlink or reparse traversal component was not rejected")
    source_repository_probe = Path("volume") / "linked-parent" / "repository"
    if not has_link_like_ancestor(source_repository_probe, lambda path: path.name == "linked-parent"):
        failures.append(f"{prefix}: linked source-repository ancestor was not rejected")
    if has_link_like_ancestor(source_repository_probe, lambda _: False):
        failures.append(f"{prefix}: ordinary source-repository ancestors were rejected")


def write_manifest(path: Path, manifest: dict) -> None:
    text = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_bytes(text.encode("utf-8"))


def run_adversarial_matrix() -> int:
    matrix_failures: list[str] = []
    case_results: list[dict] = []

    selector_failures = hostile_git_selector_isolation_proof()
    case_results.append(
        {
            "case": "hostile-git-selector-isolation",
            "result": "PASS" if not selector_failures else "FAIL",
        }
    )
    matrix_failures.extend(
        f"hostile-git-selector-isolation: {failure}" for failure in selector_failures
    )

    sentinel_failures, sentinel_proof = external_link_snapshot_sentinel_proof()
    case_results.append(
        {
            "case": "external-link-snapshot-sentinel",
            "proof": sentinel_proof,
            "result": "PASS" if not sentinel_failures else "FAIL",
        }
    )
    matrix_failures.extend(
        f"external-link-snapshot-sentinel: {failure}" for failure in sentinel_failures
    )

    def execute_case(name, mutate, expected_failure=None, preserve_suffix=None):
        with tempfile.TemporaryDirectory(prefix=f"{PRODUCT}-checker-matrix-") as temporary:
            copy_root = Path(temporary) / "repository"
            try:
                materialize_index_snapshot(ROOT, copy_root)
            except SnapshotError as error:
                case_results.append({"case": name, "result": "FAIL"})
                matrix_failures.append(f"{name}: safe Git-index snapshot failed: {error}")
                return
            mutate(copy_root)
            completed = subprocess.run(
                [sys.executable, "-B", str(copy_root / "scripts" / "check_repository.py"), "--json"],
                cwd=copy_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            try:
                payload = json.loads(completed.stdout)
            except json.JSONDecodeError as error:
                matrix_failures.append(f"{name}: checker did not return structured JSON: {error}")
                return
            if not isinstance(payload, dict):
                matrix_failures.append(f"{name}: checker JSON root was not an object")
                return
            observed = "\n".join(payload.get("failures", []))
            if expected_failure is None:
                passed = completed.returncode == 0 and payload.get("result") == "PASS"
            else:
                passed = completed.returncode != 0 and payload.get("result") == "FAIL" and expected_failure in observed
            if "Traceback" in completed.stderr:
                passed = False
                matrix_failures.append(f"{name}: checker emitted an uncaught traceback")
            if preserve_suffix is not None:
                target, suffix = preserve_suffix(copy_root)
                if not target.read_bytes().endswith(suffix):
                    passed = False
                    matrix_failures.append(f"{name}: offending bytes were not preserved")
            case_results.append({"case": name, "result": "PASS" if passed else "FAIL"})
            if not passed:
                matrix_failures.append(f"{name}: expected fail-closed outcome was not observed")

    no_change = lambda _: None
    execute_case("baseline", no_change)

    def append_locator(repo, locator):
        path = repo / "README.md"
        path.write_bytes(path.read_bytes() + ("\n" + locator + "\n").encode("utf-8"))

    def append_invalid_utf8(repo):
        path = repo / "README.md"
        path.write_bytes(path.read_bytes() + b"\xff")

    def mutate_manifest(repo, change):
        path = repo / "provenance" / "source-map.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        change(manifest)
        write_manifest(path, manifest)

    def inject_escaped_manifest_key(repo):
        path = repo / "provenance" / "source-map.json"
        private_key = "C:" + "\\" + "Users" + "\\" + "sample"
        escaped_key = "".join(f"\\u{ord(character):04x}" for character in private_key)
        text = path.read_text(encoding="utf-8")
        mutated = text.replace("{", "{\"" + escaped_key + "\": null,", 1)
        path.write_bytes(mutated.encode("utf-8"))

    def inject_unpaired_surrogate_manifest(repo):
        path = repo / "provenance" / "source-map.json"
        text = path.read_text(encoding="utf-8")
        marker = '"destination": ".gitattributes"'
        mutated = text.replace(marker, '"destination": "\\ud800"', 1)
        path.write_bytes(mutated.encode("utf-8"))

    def inject_duplicate_manifest_key(repo):
        path = repo / "provenance" / "source-map.json"
        private_value = "C:" + "\\" + "Users" + "\\" + "sample"
        escaped_value = "".join(f"\\u{ord(character):04x}" for character in private_value)
        text = path.read_text(encoding="utf-8")
        mutated = text.replace(
            "{",
            '{"matrix_note":"' + escaped_value + '","matrix_note":"portable",',
            1,
        )
        path.write_bytes(mutated.encode("utf-8"))

    for name, locator, expected_label in rejected_locator_matrix():
        execute_case(
            name,
            lambda repo, value=locator: append_locator(repo, value),
            expected_label,
        )
    execute_case(
        "invalid-normalized-utf8",
        append_invalid_utf8,
        "not valid UTF-8",
        lambda repo: (repo / "README.md", b"\xff"),
    )
    execute_case(
        "manifest-identity",
        lambda repo: mutate_manifest(repo, lambda manifest: manifest.pop("source_tree", None)),
        "provenance source tree mismatch",
    )
    execute_case(
        "manifest-source-commit",
        lambda repo: mutate_manifest(repo, lambda manifest: manifest.update({"source_commit": "0" * 40})),
        "provenance product or source commit mismatch",
    )
    execute_case(
        "manifest-source-mapping",
        lambda repo: mutate_manifest(
            repo,
            lambda manifest: next(
                entry for entry in manifest["entries"] if entry.get("kind") == "exact-git-blob"
            ).update({"source_blob": "0" * 40, "source_sha256": "0" * 64}),
        ),
        "provenance source mapping mismatch",
    )
    execute_case(
        "manifest-native-target-hash",
        lambda repo: mutate_manifest(
            repo,
            lambda manifest: next(
                entry for entry in manifest["entries"] if entry.get("kind") == "repository-native"
            ).update({"target_sha256": "0" * 64}),
        ),
        "provenance source mapping mismatch",
    )
    execute_case(
        "rewrite-source-schema",
        lambda repo: mutate_manifest(
            repo,
            lambda manifest: next(entry for entry in manifest["entries"] if entry.get("kind") == "standalone-normalized-text-rewrite").update({"sources": [{}]}),
        ),
        "unsafe or missing source_path",
    )
    execute_case(
        "manifest-provenance-schema",
        lambda repo: mutate_manifest(repo, lambda manifest: manifest.update({"manifest_provenance": [{}]})),
        "manifest_provenance: rewrite source 0 has unsafe or missing source_path",
    )
    execute_case(
        "manifest-provenance-c1-control-character",
        lambda repo: mutate_manifest(
            repo,
            lambda manifest: manifest["manifest_provenance"][0].update(
                {"source_path": "docs/PROVENANCE.md" + chr(0x85) + "hidden"}
            ),
        ),
        "manifest_provenance: rewrite source 0 has unsafe or missing source_path",
    )
    execute_case(
        "source-path-control-character",
        lambda repo: mutate_manifest(
            repo,
            lambda manifest: next(
                entry for entry in manifest["entries"] if entry.get("kind") == "exact-git-blob"
            ).update({"source_path": "README.md" + chr(0) + "hidden"}),
        ),
        "unsafe or missing source_path",
    )
    for case_name, code_point in (
        ("source-path-delete-control-character", 0x7F),
        ("source-path-c1-control-character", 0x85),
    ):
        execute_case(
            case_name,
            lambda repo, value=code_point: mutate_manifest(
                repo,
                lambda manifest: next(
                    entry for entry in manifest["entries"] if entry.get("kind") == "exact-git-blob"
                ).update({"source_path": "README.md" + chr(value) + "hidden"}),
            ),
            "unsafe or missing source_path",
        )
    execute_case(
        "exact-blob-source-sha256",
        lambda repo: mutate_manifest(
            repo,
            lambda manifest: next(
                entry for entry in manifest["entries"] if entry.get("kind") == "exact-git-blob"
            ).update({"source_sha256": "0" * 64}),
        ),
        "source SHA-256 mismatch",
    )
    execute_case(
        "manifest-publication-safety",
        lambda repo: mutate_manifest(
            repo,
            lambda manifest: manifest.update({"matrix_note": "\\" * 2 + "server" + "\\" + "share" + "\\" + "project"}),
        ),
        "private UNC locator",
    )
    execute_case(
        "manifest-publication-safety-escaped-key",
        inject_escaped_manifest_key,
        "private Windows user-profile locator",
    )
    execute_case(
        "manifest-unpaired-unicode-surrogate",
        inject_unpaired_surrogate_manifest,
        "unpaired Unicode surrogate",
    )
    execute_case(
        "manifest-duplicate-key",
        inject_duplicate_manifest_key,
        "duplicate JSON key",
    )
    execute_case(
        "unsafe-destination",
        lambda repo: mutate_manifest(repo, lambda manifest: manifest["entries"][0].update({"destination": "../outside.md"})),
        "unsafe provenance destination",
    )
    execute_case(
        "missing-mapped-content",
        lambda repo: (repo / "README.md").unlink(),
        "missing mapped files",
    )

    result = {
        "product": PRODUCT,
        "matrix_cases": case_results,
        "failures": matrix_failures,
        "result": "PASS" if not matrix_failures else "FAIL",
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if not matrix_failures else 1


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
    parser.add_argument("--adversarial", action="store_true")
    parser.add_argument("--source-repository", type=Path)
    args = parser.parse_args()
    if args.adversarial:
        return run_adversarial_matrix()
    failures: list[str] = []
    check_generic_regression_matrix(failures)

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
        manifest = json.loads(manifest_text, object_pairs_hook=reject_duplicate_json_keys)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, DuplicateJsonKeyError) as error:
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
    if contains_unpaired_unicode_surrogate(manifest):
        result = {
            "product": PRODUCT,
            "source_commit": BASELINE,
            "mapped_files": 0,
            "source_membership_check": "requested" if args.source_repository is not None else "not_requested",
            "failures": ["provenance/source-map.json: unpaired Unicode surrogate is not allowed"],
            "result": "FAIL",
        }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True) if args.json else f"{PRODUCT}: FAIL")
        return 1
    validate_manifest_identity(manifest, failures)
    validate_manifest_provenance(manifest, failures)

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
        elif kind == "repository-native":
            if not isinstance(entry.get("note"), str) or not entry["note"].strip():
                failures.append(f"{relative}: repository-native entry requires a note")
        else:
            failures.append(f"{relative}: unknown provenance kind")
    if args.source_repository is not None:
        verify_source_object_membership(args.source_repository, manifest, failures)
    valid_destinations = [value for value in destinations if isinstance(value, str)]
    if len(valid_destinations) != len(set(valid_destinations)):
        failures.append("duplicate provenance destination")
    expected_files = {value for value in valid_destinations if is_safe_repo_path(value)} | {"provenance/source-map.json"}
    actual_files = files_on_disk(failures)
    missing, extra = inventory_differences(expected_files, actual_files)
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
            if sha256(raw) != entry.get("source_sha256"):
                failures.append(f"{relative}: source SHA-256 mismatch")
            if blob_sha1(raw) != entry.get("source_blob"):
                failures.append(f"{relative}: source Git blob mismatch")
        elif entry.get("kind") == "standalone-normalized-text-rewrite":
            normalized_digest = normalized_sha256(raw)
            if normalized_digest is None:
                failures.append(f"{relative}: not valid UTF-8 for normalized-text hashing")
            elif normalized_digest != entry.get("target_normalized_sha256"):
                failures.append(
                    f"{relative}: normalized-text SHA-256 mismatch "
                    f"(expected {entry.get('target_normalized_sha256')}, got {normalized_digest})"
                )

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
        for label in private_labels(text):
            failures.append(f"{relative}: {label}")

    if manifest_raw.startswith(b"\xef\xbb\xbf"):
        failures.append("provenance/source-map.json: UTF-8 BOM is not allowed")
    for number, line in enumerate(manifest_text.splitlines(), start=1):
        if line.endswith((" ", "\t")):
            failures.append(f"provenance/source-map.json:{number}: trailing whitespace")
    manifest_private_labels = set(private_labels(manifest_text))
    for value in iter_text_values(manifest):
        manifest_private_labels.update(private_labels(value))
    for label in sorted(manifest_private_labels):
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
        "source_membership_check": "requested" if args.source_repository is not None else "not_requested",
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
