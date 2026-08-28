#!/usr/bin/env python3
import argparse
import hashlib
import json
import stat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "work-charter"
CANDIDATE = ROOT / "release" / "v0.3.0-candidate.json"
RECEIPT = ROOT / "release" / "v0.3.0-local-release-receipt.json"
PUBLIC_RELEASE_CANDIDATE = ROOT / "release" / "v0.3.0-public-release-candidate.json"
PUBLIC_RELEASE_EVIDENCE = ROOT / "release" / "v0.3.0-public-release-evidence.json"
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

    receipt_error = None
    receipt = {}
    try:
        parsed_receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        if not isinstance(parsed_receipt, dict):
            raise ValueError("local release receipt must be an object")
        for field in ("candidate", "planner_acceptance", "evidence_states", "source_forward_behavior"):
            if not isinstance(parsed_receipt.get(field), dict):
                raise ValueError(f"local release receipt field {field!r} must be an object")
        receipt = parsed_receipt
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        receipt = {}
        receipt_error = str(error)
    checks["receipt.identity_and_readiness"] = (
        receipt.get("schema") == "work-charter-local-release-receipt/v1"
        and receipt.get("product") == "work-charter"
        and receipt.get("version") == "0.3.0"
        and receipt.get("candidate", {}).get("commit")
        == "732e7efa6211d9aedeb133282ef28ce03f9bdfef"
        and receipt.get("candidate", {}).get("descriptor")
        == "release/v0.3.0-candidate.json"
        and receipt.get("candidate", {}).get("tree")
        == "cc09ec16f85b05ed2287afd68ac6051dd800d287"
        and receipt.get("candidate", {}).get("package_tree") == actual_package_tree
        and receipt.get("planner_acceptance", {}).get("checkpoint")
        == "B1-WC-CANDIDATE-C-01"
        and receipt.get("planner_acceptance", {}).get("verdict") == "ACCEPTED"
        and receipt.get("evidence_states", {}).get("local_release_ready") == "VERIFIED"
        and receipt.get("evidence_states", {}).get("public_release") == "UNKNOWN"
        and receipt.get("evidence_states", {}).get("stable_installed_copy") == "UNKNOWN"
        and receipt.get("evidence_states", {}).get("persistent_lifecycle") == "UNKNOWN"
        and receipt.get("evidence_states", {}).get("broad_product_efficacy") == "UNKNOWN"
        and receipt.get("human_release_notes_review") == "PENDING"
        and receipt.get("source_forward_behavior", {}).get("evidence_id") == "Q06"
        and receipt.get("source_forward_behavior", {}).get("model") == "gpt-5.6-sol"
        and receipt.get("source_forward_behavior", {}).get("reasoning_effort") == "high"
        and receipt.get("source_forward_behavior", {}).get("result") == "ACCEPTED"
        and receipt.get("source_forward_behavior", {}).get("scope")
        == "fresh projectless read-only no-tool exact-SOURCE"
        and receipt.get("source_forward_behavior", {}).get("package_tree") == actual_package_tree
    )

    public_candidate_error = None
    public_candidate = {}
    release_notes_sha256 = None
    try:
        parsed_public_candidate = json.loads(PUBLIC_RELEASE_CANDIDATE.read_text(encoding="utf-8"))
        if not isinstance(parsed_public_candidate, dict):
            raise ValueError("public release candidate must be an object")
        for field in ("github_release", "lineage", "package", "public_repository"):
            if not isinstance(parsed_public_candidate.get(field), dict):
                raise ValueError(f"public release candidate field {field!r} must be an object")
        release_notes_sha256 = hashlib.sha256((ROOT / "CHANGELOG.md").read_bytes()).hexdigest()
        public_candidate = parsed_public_candidate
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        public_candidate = {}
        public_candidate_error = str(error)
    checks["public_release_candidate.identity"] = (
        public_candidate.get("schema") == "work-charter-public-release-candidate/v1"
        and "commit" not in public_candidate
        and public_candidate.get("product") == "work-charter"
        and public_candidate.get("version") == "0.3.0"
        and public_candidate.get("public_release_state") == "PENDING_HUMAN_APPROVAL"
        and public_candidate.get("human_release_notes_review") == "PENDING"
        and public_candidate.get("release_title") == "Work Charter v0.3.0"
        and public_candidate.get("release_notes") == "CHANGELOG.md"
        and public_candidate.get("release_notes_sha256")
        == release_notes_sha256
        and public_candidate.get("tag") == "v0.3.0"
        and public_candidate.get("tag_type") == "annotated"
        and public_candidate.get("github_release")
        == {"draft": False, "prerelease": False}
        and public_candidate.get("lineage", {}).get("local_release_receipt")
        == "release/v0.3.0-local-release-receipt.json"
        and public_candidate.get("lineage", {}).get("local_release_receipt_commit")
        == "193be0edcb95dac5b3ddfc95a935d06165ffa446"
        and public_candidate.get("package", {}).get("path") == "skills/work-charter"
        and public_candidate.get("package", {}).get("tree") == actual_package_tree
        and public_candidate.get("package", {}).get("sha256")
        == (package_digest(actual_files) if actual_files == EXPECTED_FILES else None)
        and public_candidate.get("public_repository", {}).get("full_name")
        == "junwei529/work-charter"
        and public_candidate.get("public_repository", {}).get("url")
        == "https://github.com/junwei529/work-charter"
        and public_candidate.get("public_repository", {}).get("default_branch") == "main"
        and public_candidate.get("public_repository", {}).get("visibility") == "public"
    )

    public_evidence_error = None
    public_evidence = {}
    try:
        parsed_public_evidence = json.loads(PUBLIC_RELEASE_EVIDENCE.read_text(encoding="utf-8"))
        if not isinstance(parsed_public_evidence, dict):
            raise ValueError("public release evidence must be an object")
        for field in (
            "discovery_correction",
            "evidence_states",
            "github_release",
            "installed_copy_behavior",
            "persistent_lifecycle",
            "public_source",
            "tag",
        ):
            if not isinstance(parsed_public_evidence.get(field), dict):
                raise ValueError(f"public release evidence field {field!r} must be an object")
        if not isinstance(parsed_public_evidence["installed_copy_behavior"].get("evidence"), list):
            raise ValueError("public release evidence witnesses must be a list")
        if not isinstance(
            parsed_public_evidence["installed_copy_behavior"].get("package_file_sha256"), dict
        ):
            raise ValueError("public release evidence package hashes must be an object")
        if not isinstance(parsed_public_evidence["persistent_lifecycle"].get("operations"), list):
            raise ValueError("public release evidence lifecycle operations must be a list")
        public_evidence = parsed_public_evidence
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        public_evidence = {}
        public_evidence_error = str(error)
    checks["public_release_evidence.identity"] = (
        public_evidence.get("schema") == "work-charter-public-release-evidence/v1"
        and public_evidence.get("product") == "work-charter"
        and public_evidence.get("version") == "0.3.0"
        and public_evidence.get("evidence_state") == "PENDING_PLANNER_ACCEPTANCE"
        and public_evidence.get("planner_acceptance") == "PENDING"
        and public_evidence.get("public_source", {}).get("commit")
        == "b655c1aa42acc8c68b70e87c4c228445c5182d8b"
        and public_evidence.get("public_source", {}).get("tree")
        == "0b5166b402d98df041589d378a739a5fa9757ba5"
        and public_evidence.get("public_source", {}).get("package_tree") == actual_package_tree
        and public_evidence.get("public_source", {}).get("package_sha256")
        == (package_digest(actual_files) if actual_files == EXPECTED_FILES else None)
        and public_evidence.get("public_source", {}).get("repository")
        == "junwei529/work-charter"
        and public_evidence.get("tag", {}).get("name") == "v0.3.0"
        and public_evidence.get("tag", {}).get("type") == "annotated"
        and public_evidence.get("tag", {}).get("annotation") == "Work Charter v0.3.0"
        and public_evidence.get("tag", {}).get("object")
        == "81675840fe586e4f8960404210b1985d70ae4940"
        and public_evidence.get("tag", {}).get("peeled_commit")
        == "b655c1aa42acc8c68b70e87c4c228445c5182d8b"
        and public_evidence.get("github_release", {}).get("id") == 378244052
        and public_evidence.get("github_release", {}).get("title") == "Work Charter v0.3.0"
        and public_evidence.get("github_release", {}).get("url")
        == "https://github.com/junwei529/work-charter/releases/tag/v0.3.0"
        and public_evidence.get("github_release", {}).get("draft") is False
        and public_evidence.get("github_release", {}).get("prerelease") is False
        and public_evidence.get("github_release", {}).get("body_normalized_lf_sha256")
        == "4a02c5cce79f3aaee545eca1c7f0a2330563618782a7126946dfdf786b0bb7d8"
        and public_evidence.get("persistent_lifecycle", {}).get("final_state") == "MANAGED"
        and public_evidence.get("persistent_lifecycle", {}).get("source_identity")
        == "junwei529/work-charter"
        and public_evidence.get("persistent_lifecycle", {}).get("source_ref") == "v0.3.0"
        and public_evidence.get("persistent_lifecycle", {}).get("version") == "0.3.0"
        and public_evidence.get("persistent_lifecycle", {}).get("foreign_copy_refusal")
        == "VERIFIED"
        and public_evidence.get("persistent_lifecycle", {}).get("foreign_copy_retained") is True
        and public_evidence.get("persistent_lifecycle", {}).get("foreign_copy_discovery_state")
        == "PRESERVED_OUTSIDE_SKILL_DISCOVERY_ROOT"
        and public_evidence.get("persistent_lifecycle", {}).get(
            "managed_uninstall_target_is_sole_discoverable_copy"
        )
        is True
        and public_evidence.get("persistent_lifecycle", {}).get("operations")
        == [
            "install",
            "same-version update",
            "same-version rollback",
            "origin-aware uninstall",
            "public-source restoration",
        ]
        and public_evidence.get("persistent_lifecycle", {}).get("final_package_sha256")
        == "7b67ea1f7073fa66ac91c36f3e39c735b54c04174e2fa3672068f8fa8948a5b2"
        and public_evidence.get("persistent_lifecycle", {}).get("final_package_tree")
        == actual_package_tree
        and public_evidence.get("installed_copy_behavior", {}).get("package_tree")
        == actual_package_tree
        and public_evidence.get("installed_copy_behavior", {}).get("evidence")
        == [
            {
                "evidence_id": "B2-WC-LOAD-01",
                "result": "ACCEPTED",
                "scope": "fresh projectless read-only loaded-copy behavior",
            },
            {
                "evidence_id": "B2-WC-RESTORE-01",
                "result": "ACCEPTED",
                "scope": "fresh projectless read-only restored-copy recovery behavior",
            },
            {
                "evidence_id": "B2-WC-SOLE-LOAD-02",
                "result": "ACCEPTED",
                "scope": "fresh projectless sole-discovery loaded-copy behavior",
            },
        ]
        and public_evidence.get("discovery_correction", {}).get("prior_discovery_ambiguity")
        == "CORRECTED"
        and public_evidence.get("discovery_correction", {}).get("retained_copy")
        == "PRESERVED_OUTSIDE_SKILL_DISCOVERY_ROOT"
        and public_evidence.get("discovery_correction", {}).get("recovery_locator")
        == "CONTROLLER_SIDE_ONLY"
        and public_evidence.get("discovery_correction", {}).get("current_same_name_catalog_count")
        == 1
        and public_evidence.get("discovery_correction", {}).get("current_witness")
        == "B2-WC-SOLE-LOAD-02"
        and public_evidence.get("discovery_correction", {}).get("historical_evidence_preserved")
        == ["B2-WC-LOAD-01", "B2-WC-RESTORE-01"]
        and public_evidence.get("discovery_correction", {}).get("supersedes_evidence_commit")
        == "651d9decd9bb3b9532fa41eb55b2ceeffe19ccc0"
        and public_evidence.get("installed_copy_behavior", {}).get("package_file_sha256")
        == {
            "SKILL.md": "c750d51940456b110bc7ed4b7d490690f42ca8ee9b555c23c8fe3d4d056b4dba",
            "agents/openai.yaml": "f0032475e213d75ed17eb41c3424007ebc46c0ddb6739138c9908185beefdad6",
            "assets/work-charter.md": "ca2ec792c0b0bf978e79a7e51cb5afd9b675e79b0daf7d0dc81917f77bfc7fa1",
            "references/coordination-and-recovery.md": "5565ef7d2db47847c570ae0ea0a0a307bc64c0ed8b61261d85177f4ef2da1f88",
            "references/standard-ope.md": "10a4d5b9c9239ac2f79544155e09ea230d99e6ca80049cd01ea624f16a72fd67",
        }
        and public_evidence.get("evidence_states", {}).get("public_release") == "VERIFIED"
        and public_evidence.get("evidence_states", {}).get("stable_installed_copy")
        == "VERIFIED"
        and public_evidence.get("evidence_states", {}).get("sole_installed_copy_discovery")
        == "VERIFIED"
        and public_evidence.get("evidence_states", {}).get("cross_version_lifecycle")
        == "UNKNOWN"
        and public_evidence.get("evidence_states", {}).get("broad_product_efficacy")
        == "UNKNOWN"
    )

    failures = [name for name, passed in checks.items() if not passed]
    if package_scan_error:
        failures.append(f"package.scan: {package_scan_error}")
    failures.extend(package_read_failures)
    if candidate_error:
        failures.append(f"candidate.unreadable: {candidate_error}")
    if receipt_error:
        failures.append(f"receipt.unreadable: {receipt_error}")
    if public_candidate_error:
        failures.append(f"public_release_candidate.unreadable: {public_candidate_error}")
    if public_evidence_error:
        failures.append(f"public_release_evidence.unreadable: {public_evidence_error}")
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
