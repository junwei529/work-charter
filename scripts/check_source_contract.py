#!/usr/bin/env python3
import argparse
import hashlib
import json
import stat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "work-charter"
CURRENT_CANDIDATE = ROOT / "release" / "v0.4.1-candidate.json"
V040_CANDIDATE = ROOT / "release" / "v0.4.0-candidate.json"
V040_RECEIPT = ROOT / "release" / "v0.4.0-local-release-receipt.json"
HISTORICAL_CANDIDATE = ROOT / "release" / "v0.3.0-candidate.json"
RECEIPT = ROOT / "release" / "v0.3.0-local-release-receipt.json"
PUBLIC_RELEASE_CANDIDATE = ROOT / "release" / "v0.3.0-public-release-candidate.json"
PUBLIC_RELEASE_EVIDENCE = ROOT / "release" / "v0.3.0-public-release-evidence.json"
V030_PACKAGE_TREE = "0ac3cbb0f1fa8fa51d8f832c8127eabc9863ec9e"
V030_PACKAGE_SHA256 = "d445a3cd99c6d8f2ea2d9eee3be7c24781732617fedf08d4e9fd1b3d43ff88d1"
V030_RELEASE_NOTES_SHA256 = "e37631f77e9dd9a450e618c56967017e49a7c05618baa0b7a2cb838ccd01f12b"
V030_INSTALLED_PACKAGE_SHA256 = "7b67ea1f7073fa66ac91c36f3e39c735b54c04174e2fa3672068f8fa8948a5b2"
V040_PACKAGE_TREE = "fd5ceb5cb0fbef4a1974b40b4da05800433d5511"
V040_PACKAGE_SHA256 = "8ae542b9566415dfadd16108435735dc01406443dc84ee542fcf091ccec19076"
V040_INSTALLED_PACKAGE_SHA256 = "814fc88c4dae4a823461dc7339b8a83542258919e8374f2b1c280fb9d77157c8"
V040_PACKAGE_FILE_SHA256 = {
    "SKILL.md": "be3cf6ff88d2d2ae72209119c83bf9f27e2ff4d5afa917fc44aac30ca87eb6f5",
    "agents/openai.yaml": "f0032475e213d75ed17eb41c3424007ebc46c0ddb6739138c9908185beefdad6",
    "assets/work-charter.md": "821e907a9db2888e164e2bb0793fed949206455b496fb71581b610641985234d",
    "references/coordination-and-recovery.md": "a12a76e5c784e2ef1f54b1cbc5c8096ac64fabeccc947ff46cb97cc6969eda98",
    "references/standard-ope.md": "62c3da90b662fc4e489abfc32873a5ab92966a6326dd0b16c58285f0933fe48f",
}
V030_PACKAGE_FILE_SHA256 = {
    "SKILL.md": "c750d51940456b110bc7ed4b7d490690f42ca8ee9b555c23c8fe3d4d056b4dba",
    "agents/openai.yaml": "f0032475e213d75ed17eb41c3424007ebc46c0ddb6739138c9908185beefdad6",
    "assets/work-charter.md": "ca2ec792c0b0bf978e79a7e51cb5afd9b675e79b0daf7d0dc81917f77bfc7fa1",
    "references/coordination-and-recovery.md": "5565ef7d2db47847c570ae0ea0a0a307bc64c0ed8b61261d85177f4ef2da1f88",
    "references/standard-ope.md": "10a4d5b9c9239ac2f79544155e09ea230d99e6ca80049cd01ea624f16a72fd67",
}
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
        "authority.direct_operation_permission_gate": (
            contains_all(
                skill,
                [
                    "Reuse a still-valid authorization",
                    "that action task must present the complete operation-local question and receive the answer itself",
                    "A read-only Reviewer or evidence collector never solicits write authority.",
                ],
            )
            and contains_all(
                recovery,
                [
                    "Reuse valid authorization across role, task, Session, or Harness carriers",
                    "the action or permission-gate task becomes the semantic owner of the operation-local permission question",
                    "its relay, delegation, status report, or interpretation is not the required direct answer",
                    "does not transfer higher-level decisions",
                ],
            )
            and contains_all(
                standard,
                [
                    "the execution environment requires the action task to obtain operation-local permission directly",
                    "a Planner relay or status report is not a substitute",
                    "This does not transfer contract or scope ownership",
                    "The Reviewer reports technical unknowns and findings rather than asking for write authority.",
                ],
            )
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
                "Keep at most one Planner, one Executor, one Reviewer for the active package, one active execution lane, and one repository writer.",
                "Bind material evidence to its mutable subject, revision, and invalidation condition.",
                "silence is never acceptance",
            ],
        ),
        "review.levels_and_responsibility_separation": contains_all(
            skill,
            [
                "a separate review gate can still apply without activating or escalating Work Charter",
                "a bounded independent Reviewer may inspect a stable checkpoint",
                "Planner/Executor/Reviewer separation",
                "The implementer verifies the work it changed.",
                "An independent Reviewer inspects the stable change",
                "The designated assessor decides whether the outcome and evidence satisfy the contract",
            ],
        ),
        "review.same_reviewer_and_input_limits": contains_all(
            skill,
            [
                "Prefer the same reliable Reviewer for repair rechecks within one work package",
                "retain cumulative findings and coverage",
                "Give review the actual change, baseline, necessary surrounding source, tests, documentation consumers, material untracked inputs",
                "A read-only Reviewer does not silently build or refresh such an index.",
                "Hash, graph, diff size, or a clean status cannot replace semantic inspection.",
            ],
        ),
        "review.unknown_context_and_callback_boundaries": contains_all(
            skill,
            [
                "When a result is `UNKNOWN`",
                "A context switch can be a summary or compaction inside one run, a deliberate rotation to a fresh context, or a new or successor session.",
                "Send at most one current Result Notice for one checkpoint.",
                "A corrected or otherwise changed input creates a new checkpoint and one new Notice",
            ],
        ),
        "standard.role_separation_and_hierarchy": contains_all(
            standard,
            [
                "Orchestrator -> Phase Mandate",
                "Planner -> Phase Definition",
                "Planner -> Executor execution tranche or work package",
                "Executor -> internal steps or slices",
                "Planner -> Reviewer stable review checkpoint",
                "Reviewer -> Planner findings and coverage limits",
                "Keep one active lane, one repository writer, at most one Planner, at most one Executor, and one reliable Reviewer for the active package.",
            ],
        ),
        "standard.callback_and_recording_boundary": contains_all(
            standard,
            [
                "returns one review-ready Result Notice to the Planner for a named stable checkpoint",
                "freezes the review input and exclusions, and routes it to the Reviewer",
                "the same reliable Reviewer re-reviews the affected and cumulative material surface",
                "returns exactly one checkpoint-bound",
                "the next authorized governance writer records and verifies the verdict",
                "send at most one current Notice per checkpoint and one returned disposition",
            ],
        ),
    }

    current_candidate_error = None
    current_candidate = {}
    actual_package_tree = None
    try:
        current_candidate = json.loads(CURRENT_CANDIDATE.read_text(encoding="utf-8"))
        if not isinstance(current_candidate, dict) or not isinstance(
            current_candidate.get("package"), dict
        ):
            raise ValueError("current candidate descriptor must be an object with an object package")
        actual_package_tree = git_tree_hash(PACKAGE)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        current_candidate_error = str(error)
    current_package_sha256 = package_digest(actual_files) if actual_files == EXPECTED_FILES else None
    checks["candidate.v041_identity"] = (
        current_candidate.get("schema") == "work-charter-local-release-candidate/v1"
        and current_candidate.get("product") == "work-charter"
        and current_candidate.get("version") == "0.4.1"
        and current_candidate.get("public_identity") == "junwei529/work-charter"
        and current_candidate.get("candidate_state") == "PENDING_INDEPENDENT_REVIEW"
        and current_candidate.get("package", {}).get("file_count") == 5
        and current_candidate.get("package", {}).get("path") == "skills/work-charter"
        and current_candidate.get("package", {}).get("tree") == actual_package_tree
        and current_candidate.get("package", {}).get("sha256") == current_package_sha256
        and current_candidate.get("evidence_states", {}).get("independent_review") == "PENDING"
        and current_candidate.get("evidence_states", {}).get("planner_acceptance") == "PENDING"
        and current_candidate.get("evidence_states", {}).get("local_release_ready")
        == "PENDING_REVIEW_AND_PLANNER_ACCEPTANCE"
        and current_candidate.get("evidence_states", {}).get("public_release") == "UNKNOWN"
        and current_candidate.get("evidence_states", {}).get("stable_installed_copy") == "UNKNOWN"
        and current_candidate.get("evidence_states", {}).get("cross_version_lifecycle")
        == "REQUIRES_FRESH_QUALIFICATION"
        and current_candidate.get("lineage")
        == {
            "historical_package_tree": V040_PACKAGE_TREE,
            "previous_candidate": "release/v0.4.0-candidate.json",
            "previous_local_release_receipt": "release/v0.4.0-local-release-receipt.json",
            "source_commit": "df674c773de6f915627af541f0eb37221da9adef",
        }
        and current_candidate.get("human_release_notes_review") == "PENDING"
    )

    v040_candidate_error = None
    v040_candidate = {}
    try:
        v040_candidate = json.loads(V040_CANDIDATE.read_text(encoding="utf-8"))
        if not isinstance(v040_candidate, dict) or not isinstance(
            v040_candidate.get("package"), dict
        ):
            raise ValueError("v0.4.0 candidate descriptor must be an object with an object package")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        v040_candidate_error = str(error)
    checks["candidate.v040_historical_identity"] = (
        v040_candidate.get("schema") == "work-charter-local-release-candidate/v1"
        and v040_candidate.get("product") == "work-charter"
        and v040_candidate.get("version") == "0.4.0"
        and v040_candidate.get("public_identity") == "junwei529/work-charter"
        and v040_candidate.get("candidate_state") == "PENDING_INDEPENDENT_REVIEW"
        and v040_candidate.get("package")
        == {
            "file_count": 5,
            "path": "skills/work-charter",
            "sha256": V040_PACKAGE_SHA256,
            "tree": V040_PACKAGE_TREE,
        }
        and v040_candidate.get("human_release_notes_review") == "PENDING"
    )

    historical_candidate_error = None
    historical_candidate = {}
    try:
        historical_candidate = json.loads(HISTORICAL_CANDIDATE.read_text(encoding="utf-8"))
        if not isinstance(historical_candidate, dict) or not isinstance(
            historical_candidate.get("package"), dict
        ):
            raise ValueError("historical candidate descriptor must be an object with an object package")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        historical_candidate_error = str(error)
    checks["candidate.v030_historical_identity"] = (
        historical_candidate.get("schema") == "work-charter-local-release-candidate/v1"
        and historical_candidate.get("product") == "work-charter"
        and historical_candidate.get("version") == "0.3.0"
        and historical_candidate.get("public_identity") == "junwei529/work-charter"
        and historical_candidate.get("candidate_state") == "PENDING_PLANNER_ACCEPTANCE"
        and historical_candidate.get("package", {}).get("file_count") == 5
        and historical_candidate.get("package", {}).get("path") == "skills/work-charter"
        and historical_candidate.get("package", {}).get("tree") == V030_PACKAGE_TREE
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
        and receipt.get("candidate", {}).get("package_tree") == V030_PACKAGE_TREE
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
        and receipt.get("source_forward_behavior", {}).get("package_tree") == V030_PACKAGE_TREE
    )

    current_receipt_error = None
    current_receipt = {}
    try:
        parsed_current_receipt = json.loads(V040_RECEIPT.read_text(encoding="utf-8"))
        if not isinstance(parsed_current_receipt, dict):
            raise ValueError("current local release receipt must be an object")
        for field in (
            "candidate",
            "evidence_states",
            "independent_review",
            "installation",
            "installer",
            "pending_source_correction",
            "policy_preservation_finding",
            "planner_acceptance",
            "restore_verification_finding",
            "runtime_finding",
            "trust",
        ):
            if not isinstance(parsed_current_receipt.get(field), dict):
                raise ValueError(f"current local release receipt field {field!r} must be an object")
        if not isinstance(parsed_current_receipt["independent_review"].get("findings"), list):
            raise ValueError("current local release receipt findings must be a list")
        if not isinstance(parsed_current_receipt["installation"].get("transaction"), dict):
            raise ValueError("current local release receipt transaction must be an object")
        if not isinstance(
            parsed_current_receipt["pending_source_correction"].get("actual_repair_route"),
            dict,
        ):
            raise ValueError("current local release receipt repair route must be an object")
        current_receipt = parsed_current_receipt
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        current_receipt = {}
        current_receipt_error = str(error)
    checks["receipt.v040_identity_and_readiness"] = (
        current_receipt.get("schema") == "work-charter-local-release-receipt/v1"
        and current_receipt.get("product") == "work-charter"
        and current_receipt.get("version") == "0.4.0"
        and current_receipt.get("candidate")
        == {
            "commit": "30057490be21d869751854a51e9fafdfb535f206",
            "descriptor": "release/v0.4.0-candidate.json",
            "package_sha256": V040_PACKAGE_SHA256,
            "package_tree": V040_PACKAGE_TREE,
            "tree": "a746f2eb4dc54db71f6ebd627da5f184929c9428",
        }
        and current_receipt.get("installer")
        == {
            "commit": "08f72b404b1e127d6c461ac337a4e570c2c6800c",
            "tree": "899f7ec700516a2feb3121e7062dbd5bdab37065",
        }
        and current_receipt.get("planner_acceptance")
        == {
            "access_correction": {
                "checkpoint": "WC-INSTALL-ACCESS-REVIEW-READY-01",
                "finding": "WC-INSTALL-ACCESS-P01",
                "verdict": "CORRECTION_REQUIRED",
            },
            "dacl_readback_correction": {
                "checkpoint": "WC-INSTALL-ACCESS-R5-RESULT-01",
                "finding": "WC-INSTALL-ACCESS-R5-F01",
                "verdict": "CORRECTION_REQUIRED",
            },
            "postflight": {
                "checkpoint": "WC-SOURCE-INSTALL-AND-RECORDS-READY-01",
                "finding": "WC-INSTALL-POSTFLIGHT-F01",
                "verdict": "CORRECTION_REQUIRED",
            },
            "source": {"checkpoint": "SOURCE_CANDIDATE_03", "verdict": "ACCEPTED"},
            "tool": {"checkpoint": "WC-INSTALL-ACCEPTANCE-02", "verdict": "ACCEPTED"},
        }
        and current_receipt.get("independent_review")
        == {
            "completed_rounds": 5,
            "final_result": "CORRECTION_REQUIRED",
            "final_round": "WC-INSTALL-ACCESS-R5-RESULT-01",
            "findings": [
                {
                    "disposition": "FALSE_POSITIVE_CLOSED",
                    "id": "WC-SOURCE-R1-F01",
                    "severity": "P1",
                },
                {
                    "disposition": "FIXED_CLOSED",
                    "id": "WC-SOURCE-R1-F02",
                    "severity": "P2",
                },
                {
                    "disposition": "FIXED_PENDING_R6_REVIEW_AND_PLANNER_ACCEPTANCE",
                    "id": "WC-INSTALL-ACCESS-R5-F01",
                    "parent_finding": "WC-INSTALL-ACCESS-P01",
                    "severity": "P2",
                },
            ],
            "model": "gpt-5.6-terra",
            "reasoning_effort": "high",
        }
        and current_receipt.get("installation", {}).get("action") == "update"
        and current_receipt.get("installation", {}).get("from_version") == "0.3.0"
        and current_receipt.get("installation", {}).get("result")
        == "CONTENT_VERIFIED_DEFAULT_READER_FAILED"
        and current_receipt.get("installation", {}).get("overall_acceptance")
        == "NOT_ACCEPTED"
        and current_receipt.get("installation", {}).get("default_reader")
        == "ACCESS_DENIED"
        and current_receipt.get("installation", {}).get("postflight_scope")
        == "ELEVATED_CONTENT_AND_RECEIPT_ONLY"
        and current_receipt.get("installation", {}).get("receipt_schema")
        == "work-charter-install-receipt/v1"
        and current_receipt.get("installation", {}).get("receipt_raw_sha256")
        == "c562b4ecc71c0b1d96b4f1b6d7465e7057479cbca3aade7a738fc7121b9be338"
        and current_receipt.get("installation", {}).get("package_sha256")
        == V040_INSTALLED_PACKAGE_SHA256
        and current_receipt.get("installation", {}).get("package_tree")
        == V040_PACKAGE_TREE
        and current_receipt.get("installation", {}).get("files")
        == V040_PACKAGE_FILE_SHA256
        and current_receipt.get("installation", {}).get("destination_class")
        == "managed Codex user Skill installation"
        and current_receipt.get("installation", {}).get("transaction")
        == {
            "cleanup": "REMOVED_EMPTY_TASK_ROOT",
            "disposition": "EXTERNAL_CANONICAL_NON_REPARSE_SAME_VOLUME",
            "mode": "EXPLICIT",
        }
        and current_receipt.get("trust")
        == {
            "record_sha256": "06ec69d391a33ac0e5c3cd0d4ee02d3b29b6c8d45f61f3907927496366845db8",
            "target_package_tree": V040_PACKAGE_TREE,
        }
        and current_receipt.get("evidence_states")
        == {
            "broad_product_efficacy": "UNKNOWN",
            "cross_harness_behavior": "UNKNOWN",
            "cross_version_lifecycle": (
                "CONTENT_AND_ELEVATED_POSTFLIGHT_VERIFIED_WITH_ACCESS_REGRESSION_OPEN"
            ),
            "local_release_ready": "BLOCKED_BY_INSTALLED_COPY_ACCESS_REGRESSION",
            "managed_installation": "NOT_ACCEPTED_DEFAULT_READER_ACCESS_FAILED",
            "natural_adherence": "UNKNOWN",
            "public_release": "UNKNOWN",
            "source_candidate_acceptance": "VERIFIED",
            "stable_installed_copy": "FAILED_DEFAULT_READER_ACCESS",
        }
        and current_receipt.get("runtime_finding")
        == {
            "discovered_by": "PLANNER_POSTFLIGHT",
            "id": "WC-INSTALL-POSTFLIGHT-F01",
            "issue": (
                "PROMOTED_DESTINATION_RETAINED_PRIVATE_TRANSACTION_ACL_AND_"
                "DEFAULT_READER_ACCESS_WAS_DENIED"
            ),
            "review_history": (
                "SEPARATE_FROM_FIVE_COMPLETED_REVIEW_RESULTS_AND_TWO_HISTORICAL_"
                "SOURCE_FINDINGS"
            ),
            "status": "OPEN",
        }
        and current_receipt.get("restore_verification_finding")
        == {
            "discovered_by": "WC-INSTALL-ACCESS-R5-RESULT-01",
            "id": "WC-INSTALL-ACCESS-R5-F01",
            "issue": (
                "RESTORE_SUCCESS_WAS_NOT_FOLLOWED_BY_TARGET_DACL_READBACK_"
                "COMPARISON"
            ),
            "parent_finding": "WC-INSTALL-ACCESS-P01",
            "severity": "P2",
            "status": "FIXED_PENDING_R6_REVIEW_AND_PLANNER_ACCEPTANCE",
        }
        and current_receipt.get("policy_preservation_finding")
        == {
            "discovered_by": "PLANNER_AFTER_R4_NO_FINDINGS",
            "id": "WC-INSTALL-ACCESS-P01",
            "issue": (
                "PARENT_RESET_DID_NOT_PRESERVE_EXISTING_EXPLICIT_OR_PROTECTED_"
                "DACL_POLICY"
            ),
            "review_history": "R4_NO_FINDINGS_RETAINED_WITHOUT_PLANNER_ACCEPTANCE",
            "severity": "P2",
            "status": "OPEN",
        }
        and current_receipt.get("pending_source_correction")
        == {
            "actual_installed_copy_repair": "NOT_PERFORMED",
            "actual_repair_route": {
                "effect": (
                    "ACL_ONLY_RESET_TO_VERIFIED_DESTINATION_PARENT_WITH_ROLLBACK_SNAPSHOT"
                ),
                "preconditions": [
                    "REVIEWED_SOURCE_AND_PLANNER_ACCEPTANCE_AND_LOCAL_COMMIT_COMPLETE",
                    "INSTALLED_V040_CONTENT_AND_RECEIPT_MATCH_INDEPENDENT_TRUST",
                    "CURRENT_DACL_MATCHES_RECORDED_PRIVATE_TRANSACTION_POLICY",
                    "DESTINATION_PARENT_DACL_MATCHES_SEPARATELY_VERIFIED_READER_POLICY",
                ],
                "state": "PROPOSED_NOT_EXECUTED",
            },
            "non_windows_behavior": "UNCHANGED_PLATFORM_DEFAULT",
            "state": "PENDING_R6_INDEPENDENT_REVIEW_AND_PLANNER_ACCEPTANCE",
            "windows_mechanism": (
                "PRIVATE_TRANSACTION_RECOVERY_MATERIAL_AND_PREMUTATION_DACL_SNAPSHOT_"
                "WITH_POSTRESTORE_SEMANTIC_READBACK_INSTALL_PARENT_INHERITANCE_AND_"
                "UPDATE_ROLLBACK_UNINSTALL_RECOVERY_POLICY_PRESERVATION"
            ),
        }
        and current_receipt.get("human_release_notes_review") == "PENDING"
    )

    public_candidate_error = None
    public_candidate = {}
    try:
        parsed_public_candidate = json.loads(PUBLIC_RELEASE_CANDIDATE.read_text(encoding="utf-8"))
        if not isinstance(parsed_public_candidate, dict):
            raise ValueError("public release candidate must be an object")
        for field in ("github_release", "lineage", "package", "public_repository"):
            if not isinstance(parsed_public_candidate.get(field), dict):
                raise ValueError(f"public release candidate field {field!r} must be an object")
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
        == V030_RELEASE_NOTES_SHA256
        and public_candidate.get("tag") == "v0.3.0"
        and public_candidate.get("tag_type") == "annotated"
        and public_candidate.get("github_release")
        == {"draft": False, "prerelease": False}
        and public_candidate.get("lineage", {}).get("local_release_receipt")
        == "release/v0.3.0-local-release-receipt.json"
        and public_candidate.get("lineage", {}).get("local_release_receipt_commit")
        == "193be0edcb95dac5b3ddfc95a935d06165ffa446"
        and public_candidate.get("package", {}).get("path") == "skills/work-charter"
        and public_candidate.get("package", {}).get("tree") == V030_PACKAGE_TREE
        and public_candidate.get("package", {}).get("sha256")
        == V030_PACKAGE_SHA256
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
            "planner_acceptance",
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
        and public_evidence.get("evidence_state") == "VERIFIED"
        and public_evidence.get("planner_acceptance")
        == {
            "evidence_id": "B2-WC-PUBLIC-EVIDENCE-F-01",
            "subject_commit": "4ba904808fe86e270ebd405db1866d41d1cc032e",
            "subject_tree": "03307594f66dfb92e262b73546fc4ec0ddb6d720",
            "verdict": "ACCEPTED",
        }
        and public_evidence.get("public_source", {}).get("commit")
        == "b655c1aa42acc8c68b70e87c4c228445c5182d8b"
        and public_evidence.get("public_source", {}).get("tree")
        == "0b5166b402d98df041589d378a739a5fa9757ba5"
        and public_evidence.get("public_source", {}).get("package_tree") == V030_PACKAGE_TREE
        and public_evidence.get("public_source", {}).get("package_sha256")
        == V030_PACKAGE_SHA256
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
        == V030_INSTALLED_PACKAGE_SHA256
        and public_evidence.get("persistent_lifecycle", {}).get("final_package_tree")
        == V030_PACKAGE_TREE
        and public_evidence.get("installed_copy_behavior", {}).get("package_tree")
        == V030_PACKAGE_TREE
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
        == V030_PACKAGE_FILE_SHA256
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
    if current_candidate_error:
        failures.append(f"candidate.v041_unreadable: {current_candidate_error}")
    if v040_candidate_error:
        failures.append(f"candidate.v040_unreadable: {v040_candidate_error}")
    if historical_candidate_error:
        failures.append(f"candidate.v030_unreadable: {historical_candidate_error}")
    if receipt_error:
        failures.append(f"receipt.unreadable: {receipt_error}")
    if current_receipt_error:
        failures.append(f"receipt.v040_unreadable: {current_receipt_error}")
    if public_candidate_error:
        failures.append(f"public_release_candidate.unreadable: {public_candidate_error}")
    if public_evidence_error:
        failures.append(f"public_release_evidence.unreadable: {public_evidence_error}")
    result = {
        "checks": checks,
        "failures": failures,
        "package_sha256": current_package_sha256,
        "proof_class": "deterministic-source-contract",
        "result": "PASS" if not failures else "FAIL",
        "scope_limits": [
            "no model execution",
            "no live installed-copy recheck",
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
