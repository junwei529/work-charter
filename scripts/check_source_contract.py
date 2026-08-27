#!/usr/bin/env python3
import argparse
import hashlib
import json
import stat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "work-charter"
CANDIDATE = ROOT / "release" / "v0.3.0-candidate.json"
EXPECTED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "assets/work-charter.md",
    "references/coordination-and-recovery.md",
    "references/standard-ope.md",
}


def package_digest(files):
    records = []
    for relative in sorted(files):
        raw = (PACKAGE / relative).read_bytes()
        records.append([relative, hashlib.sha256(raw).hexdigest()])
    encoded = json.dumps(records, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def git_object_hash(kind, data):
    header = f"{kind} {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def is_link_like(path):
    if path.is_symlink():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def package_paths(root):
    if is_link_like(root):
        raise ValueError(f"package root is link-like: {root}")

    paths = []
    pending = [root]
    while pending:
        current = pending.pop()
        for child in current.iterdir():
            if is_link_like(child):
                raise ValueError(f"package entry is link-like: {child}")
            paths.append(child)
            if child.is_dir():
                pending.append(child)
    return paths


def git_tree_hash(directory):
    if is_link_like(directory):
        raise ValueError(f"package path is link-like: {directory}")
    children = list(directory.iterdir())
    children.sort(
        key=lambda child: (child.name + ("/" if child.is_dir() else "")).encode("utf-8")
    )
    entries = []
    for child in children:
        if is_link_like(child):
            raise ValueError(f"package entry is link-like: {child}")
        if child.is_dir():
            mode = b"40000"
            digest = bytes.fromhex(git_tree_hash(child))
        elif child.is_file():
            mode = b"100644"
            digest = bytes.fromhex(git_object_hash("blob", child.read_bytes()))
        else:
            raise ValueError(f"package contains an unsupported path: {child.name}")
        entries.append(mode + b" " + child.name.encode("utf-8") + b"\0" + digest)
    return git_object_hash("tree", b"".join(entries))


def contains_all(text, fragments):
    normalized_text = " ".join(text.split())
    return all(" ".join(fragment.split()) in normalized_text for fragment in fragments)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    package_scan_error = None
    try:
        package_entries = package_paths(PACKAGE)
    except (OSError, ValueError) as error:
        package_entries = []
        package_scan_error = str(error)
    actual_files = {
        path.relative_to(PACKAGE).as_posix()
        for path in package_entries
        if path.is_file()
    }
    texts = {}
    package_read_failures = []
    if package_scan_error is None:
        for relative in EXPECTED_FILES:
            path = PACKAGE / relative
            if not path.is_file():
                continue
            try:
                texts[relative] = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as error:
                package_read_failures.append(f"package.unreadable.{relative}: {error}")
    skill = texts.get("SKILL.md", "")
    recovery = texts.get("references/coordination-and-recovery.md", "")
    standard = texts.get("references/standard-ope.md", "")

    checks = {
        "package.exact_five_file_shape": actual_files == EXPECTED_FILES,
        "selection.direct_activation_requires_body": contains_all(
            skill,
            [
                "A direct `$work-charter` invocation",
                "Load the full Skill first",
                "Activation requires both direct intent or confirmation",
            ],
        ),
        "selection.indirect_is_proposal_only": contains_all(
            skill,
            [
                "Work Charter appears applicable because ...",
                "Before confirmation, do not say Work Charter is",
                "Do not inspect the project or apply the Work Charter workflow",
            ],
        ),
        "authority.loading_and_activation_do_not_expand_authority": contains_all(
            skill,
            [
                "Package loading never expands project-read or action authority.",
                "Activation or read approval does not authorize adoption, writes, roles, Git, or side effects.",
            ],
        ),
        "recovery.fixed_route_precedence": contains_all(
            recovery,
            [
                "Stop safely",
                "Revise the work contract",
                "Change how work is coordinated",
                "Continue the existing plan",
            ],
        ),
        "recovery.writer_and_evidence_binding": contains_all(
            recovery,
            [
                "Keep at most one Planner, one Executor, one active execution lane, and one repository writer.",
                "Bind material evidence to its mutable subject, revision, and invalidation condition.",
                "silence is never acceptance",
            ],
        ),
        "standard.role_separation_and_hierarchy": contains_all(
            standard,
            [
                "Orchestrator -> Phase Mandate",
                "Planner -> Phase Definition",
                "Planner -> Executor execution tranche or work package",
                "Executor -> internal steps or slices",
                "Keep one active lane, one repository writer, at most one Planner, and at most one Executor.",
            ],
        ),
        "standard.callback_and_recording_boundary": contains_all(
            standard,
            [
                "returns one Result Notice to the Planner, stops polling",
                "returns exactly one checkpoint-bound",
                "the next authorized governance writer records and verifies the verdict",
            ],
        ),
    }

    candidate_error = None
    candidate = {}
    actual_package_tree = None
    try:
        candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
        if not isinstance(candidate, dict) or not isinstance(candidate.get("package"), dict):
            raise ValueError("candidate descriptor must be an object with an object package")
        actual_package_tree = git_tree_hash(PACKAGE)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        candidate_error = str(error)
    checks["candidate.identity"] = (
        candidate.get("schema") == "work-charter-local-release-candidate/v1"
        and candidate.get("product") == "work-charter"
        and candidate.get("version") == "0.3.0"
        and candidate.get("public_identity") == "junwei529/work-charter"
        and candidate.get("candidate_state") == "PENDING_PLANNER_ACCEPTANCE"
        and candidate.get("package", {}).get("file_count") == 5
        and candidate.get("package", {}).get("path") == "skills/work-charter"
        and candidate.get("package", {}).get("tree") == actual_package_tree
    )

    failures = [name for name, passed in checks.items() if not passed]
    if package_scan_error:
        failures.append(f"package.scan: {package_scan_error}")
    failures.extend(package_read_failures)
    if candidate_error:
        failures.append(f"candidate.unreadable: {candidate_error}")
    result = {
        "checks": checks,
        "failures": failures,
        "package_sha256": package_digest(actual_files) if actual_files == EXPECTED_FILES else None,
        "proof_class": "deterministic-source-contract",
        "result": "PASS" if not failures else "FAIL",
        "scope_limits": [
            "no model execution",
            "no installed-copy proof",
            "no publication proof",
            "no broad efficacy proof",
        ],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"work-charter SOURCE contract: {result['result']}")
        for failure in failures:
            print(f"- {failure}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
