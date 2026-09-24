#!/usr/bin/env python3
import argparse
import hashlib
import json
import stat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "work-charter"
CURRENT_CANDIDATE = ROOT / "release" / "v0.7.1-candidate.json"
V070_CANDIDATE = ROOT / "release" / "v0.7.0-candidate.json"
V070_CANDIDATE_SHA256 = "656f021a2af4b8af6683a32b60a9c6e08fa8f1e7bd44611ad7f23cc33ed235b7"
V070_PACKAGE_TREE = "9bc03ec6f1ac081b738da2ca316b18b22a356aea"
V068_CANDIDATE = ROOT / "release" / "v0.6.8-candidate.json"
V068_CANDIDATE_SHA256 = "5477e80a235e77b09ca8afb93ff3dbe5bb880c17ca2786474f4e780d8ab1130d"
V068_PACKAGE_TREE = "03b4053d61b6b55877c4fb1401c42bc34b1cc89c"
V067_CANDIDATE = ROOT / "release" / "v0.6.7-candidate.json"
V067_CANDIDATE_SHA256 = "1a8fb41f176038412b08aa57cac9b9e0f5bfcc0c5f122e0f78090e8a3695dbca"
V067_PACKAGE_TREE = "b1171c73a4e4c243b982a701c4790d181524b6c2"
V066_CANDIDATE = ROOT / "release" / "v0.6.6-candidate.json"
V066_CANDIDATE_SHA256 = "d61c43225dc919486ff78d0edc8d85d3a45b04eceeb9e1fa5ce815983ae85660"
V066_PACKAGE_TREE = "d5018129b990686515c91e40184ebf9e5abfc546"
V065_CANDIDATE = ROOT / "release" / "v0.6.5-candidate.json"
V065_CANDIDATE_SHA256 = "64596e7ae47ed9abcd4fe90b9fbfe042d6351ab0f57f0627edb45a9f6e7cb236"
V065_PACKAGE_TREE = "d0df02a81471c2b9e157c9f6faebc65948cb4b54"
V064_CANDIDATE = ROOT / "release" / "v0.6.4-candidate.json"
V064_CANDIDATE_SHA256 = "fd561fd8b90441cb5bba8ee6f791d79b043cfee26d34e48e0152439642c7f27a"
V064_PACKAGE_TREE = "a4974a1fa9b6f4f01437c4db17110db47bbf32b1"
V063_CANDIDATE = ROOT / "release" / "v0.6.3-candidate.json"
V063_CANDIDATE_SHA256 = "ee7cbe69cb7614f15c2611306c86539120b023b93d4f120de0f29d8c61737767"
V063_PACKAGE_TREE = "40d454daa3dbf50421508860b0f4b5e4542d4052"
V062_CANDIDATE = ROOT / "release" / "v0.6.2-candidate.json"
V062_CANDIDATE_SHA256 = "9a379f98e384eb08b040bf776cd2cddc115dd27c124cd311e90a1d79466b6981"
V062_PACKAGE_TREE = "d0f3148a17f5d6c7bcec22df214a19a8ec75a62d"
V061_CANDIDATE = ROOT / "release" / "v0.6.1-candidate.json"
V061_CANDIDATE_SHA256 = "e03b2a6781b0b156679568e08b9df114770de1ebec904f2bdf126491bf18ed1a"
V061_PACKAGE_TREE = "08689a9706fa15dbe6889eec1572e7c8943c1f1c"
V060_CANDIDATE = ROOT / "release" / "v0.6.0-candidate.json"
V060_CANDIDATE_SHA256 = "5890f3e7c73ed1d4046269a03b1385097a0596cca804a57e49a838d588aa96ff"
V060_PACKAGE_TREE = "12fe4c65683a82d9d60295160681247b812efa0b"
V050_CANDIDATE = ROOT / "release" / "v0.5.0-candidate.json"
V050_RECEIPT = ROOT / "release" / "v0.5.0-local-release-receipt.json"
V041_CANDIDATE = ROOT / "release" / "v0.4.1-candidate.json"
V040_CANDIDATE = ROOT / "release" / "v0.4.0-candidate.json"
V040_RECEIPT = ROOT / "release" / "v0.4.0-local-release-receipt.json"
HISTORICAL_CANDIDATE = ROOT / "release" / "v0.3.0-candidate.json"
RECEIPT = ROOT / "release" / "v0.3.0-local-release-receipt.json"
PUBLIC_RELEASE_CANDIDATE = ROOT / "release" / "v0.3.0-public-release-candidate.json"
PUBLIC_RELEASE_EVIDENCE = ROOT / "release" / "v0.3.0-public-release-evidence.json"
ROLE_MODEL_CASE = ROOT / "evals" / "cases" / "work-charter-role-model-configuration.md"
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
V050_COMMIT = "8bf9f130598fbf1b9170dd0c082e3e8fb78d6c0d"
V050_TREE = "1985606f58d560cb21f06e85207eaae99c1f99d1"
V050_CANDIDATE_SHA256 = "ab91fa3f8dea0deeaa0fea94d7f74dc20fd43a7983dac855351097e955ed547e"
V050_PACKAGE_TREE = "413584a6a5968e60a2663ef7554181327180531f"
V050_PACKAGE_SHA256 = "b15c479518101d522c3ba27f1b32c2406e4586115622ad8fbcd35a00a38e874a"
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
    "assets/role-models.default.yaml",
    "assets/work-charter.md",
    "references/coordination-and-recovery.md",
    "references/standard-ope.md",
}
EXPECTED_DEFAULT_ROLE_MODELS = """schema_version: 1
roles:
  orchestrator:
    provider: openai
    model: gpt-6-astra
    parameters:
      reasoning_effort: high
  planner:
    provider: openai
    model: gpt-6-astra
    parameters:
      reasoning_effort: high
  executor:
    provider: openai
    model: gpt-6-sol
    parameters:
      reasoning_effort: xhigh
  reviewer:
    provider: openai
    model: gpt-6-astra
    parameters:
      reasoning_effort: medium
level_overrides:
  l0:
    primary:
      provider: openai
      model: gpt-6-sol
      parameters:
        reasoning_effort: xhigh
    reviewer:
      provider: openai
      model: gpt-6-sol
      parameters:
        reasoning_effort: xhigh
  l1:
    primary:
      provider: openai
      model: gpt-6-sol
      parameters:
        reasoning_effort: xhigh
    reviewer:
      provider: openai
      model: gpt-6-sol
      parameters:
        reasoning_effort: xhigh
  l2:
    primary:
      provider: openai
      model: gpt-6-sol
      parameters:
        reasoning_effort: xhigh
    reviewer:
      provider: openai
      model: gpt-6-sol
      parameters:
        reasoning_effort: xhigh
  l3:
    planner:
      provider: openai
      model: gpt-6-astra
      parameters:
        reasoning_effort: high
    executor:
      provider: openai
      model: gpt-6-sol
      parameters:
        reasoning_effort: xhigh
    reviewer:
      provider: openai
      model: gpt-6-astra
      parameters:
        reasoning_effort: medium
  l4:
    orchestrator:
      provider: openai
      model: gpt-6-astra
      parameters:
        reasoning_effort: high
    planner:
      provider: openai
      model: gpt-6-astra
      parameters:
        reasoning_effort: high
    executor:
      provider: openai
      model: gpt-6-sol
      parameters:
        reasoning_effort: xhigh
    reviewer:
      provider: openai
      model: gpt-6-astra
      parameters:
        reasoning_effort: medium
"""


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
    role_models = texts.get("assets/role-models.default.yaml", "")
    charter_asset = texts.get("assets/work-charter.md", "")
    ui_metadata = texts.get("agents/openai.yaml", "")
    role_model_case_error = None
    try:
        role_model_case = ROLE_MODEL_CASE.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        role_model_case = ""
        role_model_case_error = str(error)

    checks = {
        "prompts.contract_role_task_layers": contains_all(recovery, [
            "shared contract, actual responsibility, current task, and necessary model adaptation",
            "| Primary (`L0`-`L2`)", "| Orchestrator (`L4`)",
            "| Planner (`L3`/`L4`)", "| Executor (`L3`/`L4`)", "| Reviewer (when enabled)",
            "Cold prompts", "Warm continuations", "Recovery restores",
        ]) and "## Task Or Role Prompt" in charter_asset,
        "prompts.continuation_and_real_gates": contains_all(recovery, [
            "Complete authorized work through required checks and its result route",
            "Silence never approves the dependent action",
            "adoption, material replan, operation permission, independent review, and acceptance gates",
            "Repeat verification only when its input changed, it failed, or an unresolved material concern requires it",
        ]),
        "prompts.startup_and_complete_expression": (
            contains_all(ui_metadata, [
                "Use $work-charter",
                "continue an applicable approved Charter and level",
                "reusing authorized reads and asking only for missing permissions or material adoption changes",
            ])
            and "then ask before inspecting project details" not in ui_metadata
            and contains_all(recovery, [
                "every prompt and handoff proportionate and complete",
                "receiver's next decision or action",
                "Preserve key facts, decisions, material limitations, and the next step",
                "First remove repeated background, preambles, reassurance, and unrelated content",
                "not only to the final result",
                "no fixed word limit or extra mandatory message templates",
            ])
        ),
        "prompts.model_delta_and_effort": contains_all(recovery, [
            "actual selected Astra, Sol, Terra, or Luna model",
            "Record the source and supported delta",
            "package requires no other Skill or private reference path",
            "Reasoning effort is a supported runtime parameter and evaluation variable",
            "Editing a prompt does not authorize model evaluation",
        ]),
        "package.exact_six_file_shape": actual_files == EXPECTED_FILES,
        "role_models.default_exact": role_models == EXPECTED_DEFAULT_ROLE_MODELS,
        "role_models.entrypoint_routing": (
            (
            "references/coordination-and-recovery.md#role-model-configuration-at-dispatch" in skill
            and "coordination-and-recovery.md#role-model-configuration-at-dispatch" in standard
            and "## Role-Model Configuration At Dispatch" in recovery
            and contains_all(skill, ["identify level and responsibility first", "read the complete section before reading configuration or dispatching"])
            and "then read and apply" in " ".join(standard.split())
        )
        ),
        "role_models.priority_and_replacement": contains_all(recovery, [
            "Preserve a complete provider/model/parameters combination already frozen",
            "Otherwise, use a complete combination explicitly confirmed for this new task or role",
            "selected explicit or user file: `level_overrides.<level>.<responsibility>`",
            "selected explicit or user file: `roles.<responsibility>`",
            "package default: `level_overrides.<level>.<responsibility>`",
            "package default: `roles.<responsibility>`",
            "only for `primary`, when neither source supplies an object",
            "Never borrow the `executor` or `planner` object for a primary owner",
            "Missing or unreadable input stops delivery",
            "Every supplied object is a whole-object replacement",
            "it must repeat `provider` and `model`",
            "omitted `parameters` means no parameters for that combination",
        ]),
        "role_models.schema_matrix_and_native_mapping": contains_all(
            recovery,
            [
                "top-level mapping has integer `schema_version: 1`, at least one of `roles` or `level_overrides`, and no other field",
                "`roles`, when present, contains only `primary`, `orchestrator`, `planner`, `executor`, and `reviewer`",
                "| `l0` | `primary`, `reviewer` |",
                "| `l1` | `primary`, `reviewer` |",
                "| `l2` | `primary`, `reviewer` |",
                "| `l3` | `planner`, `executor`, `reviewer` |",
                "| `l4` | `orchestrator`, `planner`, `executor`, `reviewer` |",
                "Validate the complete selected file before using any entry",
                "tags, anchors, aliases, merge keys",
                "map `model` to the native `model` field",
                "`parameters.reasoning_effort` to `thinking`",
                "Stop rather than substitute a different route or value.",
            ],
        ),
        "role_models.authority_lifecycle_and_existing_roles": (
            (contains_all(skill, [
            'Role-model configuration guides an already-authorized dispatcher',
            'it neither creates roles nor changes existing tasks',
            'Preserve frozen combinations and external user configuration.',
        ])
            and contains_all(recovery, [
            'Configuration changes affect only later, newly resolved tasks or deliveries.',
            '`L0` remains no active Charter',
            'does not prove that any host or global task-start consumer has integrated it',
            'Installation lifecycle operations do not own or mutate the external user configuration.',
        ])
            and contains_all(standard, [
            'Preserve frozen combinations',
            'require native support',
            'Configuration never authorizes delivery or action, enables a role, or changes an existing task.',
        ]))
        ),
        "role_models.evaluation_boundary": contains_all(
            role_model_case,
            [
                "Legacy four-role package default",
                "General role replacement remains whole-object",
                "General primary and level override",
                "Frozen then task-explicit then configured priority",
                "Unconfigured low-level primary preserves host selection",
                "Listed but unenabled role",
                "Explicit missing path",
                "Invalid or unsupported data",
                "The user file stays outside the install tree",
                "host/global consumer integration",
            ],
        ),
        "role_models.carrier_evidence_boundary": contains_all(
            charter_asset,
            [
                "Resolved execution metadata",
                "level, actual responsibility, provider/model/parameters or host-selection pass-through",
                "object source, file source, requested values",
                "Configuration choice does not enable a listed role or authorize delivery or action.",
            ],
        ),
        "selection.assessment_and_adoption_are_distinct": contains_all(
            skill,
            [
                "Load the full Skill first",
                "First assessment",
                "evaluates L0-L4",
                "The user chooses the level to adopt.",
                "An assessment request is not adoption.",
                "`L0` has no active Charter.",
            ],
        ),
        "selection.applicable_charter_precedes_new_adoption": contains_all(skill, [
            'reuse the approved Charter and level without asking again',
            'A small task or new Thread does not cancel that Charter.',
            'Manual reassessment',
            'start from the existing Charter and level',
            "Material level, permission, or contract changes require the user's decision",
        ]),
        "selection.references_follow_role_and_level": contains_all(skill, [
            'this shared entry is the required body',
            'Read only what supports the current decision or action',
            "do not read every other role's procedure",
            'Leave the Standard reference unloaded for L0-L3 by default',
            'Do not skip shared permission, independent-review, writer or recovery boundaries.',
        ]),
        "selection.lightweight_entry_and_material_reassessment": contains_all(skill, [
            "At task entry, use supplied context",
            "continue ordinary authorized work as `L0`",
            "Do not load references, inspect a project, create a Charter or roles",
            "Before the next affected action, proactively reassess",
            "do not silently adopt or upgrade it",
            "Continue independent work already covered by authority.",
        ]),
        "authority.loading_and_assessment_do_not_expand_authority": contains_all(skill, [
            'Package loading never expands project-read or action authority.',
            'Reuse an authorized bounded read without a new activation or read question.',
            'An explicit no-read instruction remains binding',
            'Loading this package grants no Git, installation, global configuration, publication, provider or other external effect.',
        ]),
        "authority.direct_operation_permission_gate": (
            (contains_all(skill, [
            'Give each material user decision one owner. Reuse valid approval',
            'complete question/answer linkage, authorized scope and target',
            'An operation-local permission gate belongs to the action task',
            'a relay cannot replace required direct consent',
            'A read-only Reviewer or evidence collector never solicits write authority.',
        ])
            and contains_all(recovery, [
            'Reuse valid authorization across role, task, Session, or Harness carriers',
            'the action or permission-gate task becomes the semantic owner of the operation-local permission question',
            'its relay, delegation, status report, or interpretation is not the required direct answer',
            'does not transfer higher-level decisions',
        ])
            and contains_all(standard, [
            'the execution environment requires the action task to obtain operation-local permission directly',
            'a Planner relay or status report is not a substitute',
            'This does not transfer contract or scope ownership',
            'The Reviewer reports technical unknowns and findings rather than asking for write authority.',
        ]))
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
        "review.levels_and_responsibility_separation": contains_all(skill, [
            'A separate review gate may still apply.',
            'Independent review at `L0`-`L2` does not by itself adopt or raise a level, or create P/E roles.',
            'Planner/Executor/Reviewer separation',
            'The implementer verifies the work it changed.',
            'An independent Reviewer inspects the stable change',
            'The designated assessor decides whether outcome and evidence satisfy the contract.',
        ]),
        "review.same_reviewer_and_input_limits": contains_all(recovery, [
            'Prefer the same reliable Reviewer for re-review after repair.',
            'Replacement retains the cumulative findings, authority, and evidence-consumption history.',
            'Give the Reviewer the actual change and baseline, necessary surrounding source, tests, documentation consumers, material untracked inputs',
            'A read-only Reviewer does not silently build or refresh an index.',
            'none replaces semantic review or acceptance.',
        ]),
        "review.unknown_context_and_callback_boundaries": contains_all(recovery, [
            'When a finding or result is `UNKNOWN`',
            'Distinguish a summary or compaction inside one run',
            'Send at most one current Result Notice per route for one checkpoint.',
            'A corrected stable review input or other material handoff creates a new checkpoint and one new Notice',
        ]),
        "standard.role_separation_and_hierarchy": contains_all(
            standard,
            [
                "Orchestrator -> Phase Mandate",
                "Planner -> Phase Definition",
                "Planner -> Executor execution tranche or work package",
                "Executor -> internal steps or slices",
                "Planner -> Reviewer stable review checkpoint",
                "Reviewer -> Planner stable findings and coverage limits",
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
                "the authorized writer records and verifies the verdict",
                "Return a disposition for a required decision to the role that acts on it",
            ],
        ),
        "review.decision_closure_not_message_receipts": contains_all(recovery, [
            "For a material result requiring acceptance or permission to continue",
            "Pure factual, evidence or mechanical-recording completion notices do not automatically create an acceptance checkpoint or a reply obligation.",
            "never rename a material decision as a notice to bypass approval",
            "Using the Reviewer's report does not require an `ACCEPTED` or no-action reply to the Reviewer.",
            "ordinary internal repairs and individual checks are not separate acceptance checkpoints.",
        ]),
        "review.formed_verdict_and_recording_endpoint": contains_all(recovery, [
            "the execution writer has relinquished the workspace",
            "The Executor never prewrites a future Planner or Orchestrator verdict.",
            "Mechanical persistence of a formed verdict is not a new technical acceptance package.",
            "Independent Git review requirements still apply",
            "Define the closeout endpoint in the disposition",
        ]),
        "recovery.next_affected_action_and_loading_owner": contains_all(recovery, [
            "before the next action that depends on them",
            "Do not broadcast a reload to idle roles.",
            "the Harness or an explicit special contract owns loading proof and any required fresh-run mechanism.",
            "Existing frozen fresh-run qualifications, stop conditions, failures and consumed evidence remain binding",
        ]),
    }

    current_candidate_error = None
    current_candidate = {}
    current_package_sha256 = package_digest(actual_files) if actual_files == EXPECTED_FILES else None
    package_identity_error = None
    actual_package_tree = None
    try:
        actual_package_tree = git_tree_hash(PACKAGE)
    except (OSError, ValueError) as error:
        package_identity_error = str(error)
    try:
        current_candidate = json.loads(V050_CANDIDATE.read_text(encoding="utf-8"))
        if not isinstance(current_candidate, dict) or not isinstance(
            current_candidate.get("package"), dict
        ):
            raise ValueError("v0.5.0 candidate descriptor must be an object with an object package")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        current_candidate_error = str(error)
    checks["candidate.v050_historical_identity"] = (
        current_candidate.get("schema") == "work-charter-local-release-candidate/v1"
        and current_candidate.get("product") == "work-charter"
        and current_candidate.get("version") == "0.5.0"
        and current_candidate.get("public_identity") == "junwei529/work-charter"
        and current_candidate.get("candidate_state") == "PENDING_INDEPENDENT_REVIEW"
        and current_candidate.get("package", {}).get("file_count") == 6
        and current_candidate.get("package", {}).get("files") == sorted(EXPECTED_FILES)
        and current_candidate.get("package", {}).get("path") == "skills/work-charter"
        and current_candidate.get("package", {}).get("tree") == V050_PACKAGE_TREE
        and current_candidate.get("package", {}).get("sha256") == V050_PACKAGE_SHA256
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
            "historical_package_tree": "a2281edf51b624271cd5675ca02a7f4d5ae4acbb",
            "previous_candidate": "release/v0.4.1-candidate.json",
            "previous_local_release_receipt": "release/v0.4.0-local-release-receipt.json",
            "source_commit": "59b4d91f46c2ac797c71c900e62dda87cf0cca60",
        }
        and current_candidate.get("human_release_notes_review") == "PENDING"
    )
    v060_candidate_error = None
    try:
        v060_candidate_bytes = V060_CANDIDATE.read_bytes()
        checks["candidate.v060_historical_identity"] = (
            hashlib.sha256(v060_candidate_bytes).hexdigest() == V060_CANDIDATE_SHA256
        )
    except OSError as error:
        checks["candidate.v060_historical_identity"] = False
        v060_candidate_error = str(error)

    v062_candidate_error = None
    try:
        checks["candidate.v062_historical_identity"] = (
            hashlib.sha256(V062_CANDIDATE.read_bytes()).hexdigest() == V062_CANDIDATE_SHA256
        )
    except OSError as error:
        checks["candidate.v062_historical_identity"] = False
        v062_candidate_error = str(error)

    v061_candidate_error = None
    try:
        v061_candidate_bytes = V061_CANDIDATE.read_bytes()
        checks["candidate.v061_historical_identity"] = (
            hashlib.sha256(v061_candidate_bytes).hexdigest() == V061_CANDIDATE_SHA256
        )
    except OSError as error:
        checks["candidate.v061_historical_identity"] = False
        v061_candidate_error = str(error)

    v063_candidate_error = None
    try:
        checks["candidate.v063_historical_identity"] = (
            hashlib.sha256(V063_CANDIDATE.read_bytes()).hexdigest() == V063_CANDIDATE_SHA256
        )
    except OSError as error:
        checks["candidate.v063_historical_identity"] = False
        v063_candidate_error = str(error)

    v066_candidate_error = None
    try:
        checks["candidate.v066_historical_identity"] = (
            hashlib.sha256(V066_CANDIDATE.read_bytes()).hexdigest() == V066_CANDIDATE_SHA256
        )
    except OSError as error:
        checks["candidate.v066_historical_identity"] = False
        v066_candidate_error = str(error)

    v065_candidate_error = None
    try:
        checks["candidate.v065_historical_identity"] = (
            hashlib.sha256(V065_CANDIDATE.read_bytes()).hexdigest() == V065_CANDIDATE_SHA256
        )
    except OSError as error:
        checks["candidate.v065_historical_identity"] = False
        v065_candidate_error = str(error)

    v064_candidate_error = None
    try:
        checks["candidate.v064_historical_identity"] = (
            hashlib.sha256(V064_CANDIDATE.read_bytes()).hexdigest() == V064_CANDIDATE_SHA256
        )
    except OSError as error:
        checks["candidate.v064_historical_identity"] = False
        v064_candidate_error = str(error)

    v067_candidate_error = None
    try:
        checks["candidate.v067_historical_identity"] = (
            hashlib.sha256(V067_CANDIDATE.read_bytes()).hexdigest() == V067_CANDIDATE_SHA256
        )
    except OSError as error:
        checks["candidate.v067_historical_identity"] = False
        v067_candidate_error = str(error)

    checks["candidate.v068_historical_identity"] = (
        hashlib.sha256(V068_CANDIDATE.read_bytes()).hexdigest() == V068_CANDIDATE_SHA256
    )
    checks["candidate.v070_historical_identity"] = (
        hashlib.sha256(V070_CANDIDATE.read_bytes()).hexdigest() == V070_CANDIDATE_SHA256
    )
    successor_error = None
    successor = {}
    try:
        parsed_successor = json.loads(CURRENT_CANDIDATE.read_text(encoding="utf-8"))
        if not isinstance(parsed_successor, dict) or any(
            not isinstance(parsed_successor.get(field), dict)
            for field in ("package", "evidence_states", "lineage")
        ):
            raise ValueError("v0.7.1 candidate requires object package, evidence_states, and lineage")
        successor = parsed_successor
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        successor_error = str(error)
    checks["candidate.v071_identity"] = (
        successor.get("schema") == "work-charter-local-release-candidate/v1"
        and successor.get("product") == "work-charter"
        and successor.get("version") == "0.7.1"
        and successor.get("public_identity") == "junwei529/work-charter"
        and successor.get("candidate_state") == "PENDING_INDEPENDENT_REVIEW"
        and successor.get("human_release_notes_review") == "PENDING"
        and successor.get("release_notes") == "CHANGELOG.md"
        and successor.get("package", {}).get("file_count") == 6
        and successor.get("package", {}).get("files") == sorted(EXPECTED_FILES)
        and successor.get("package", {}).get("path") == "skills/work-charter"
        and successor.get("lineage") == {
            "historical_package_tree": V070_PACKAGE_TREE,
            "previous_candidate": "release/v0.7.0-candidate.json",
            "source_commit": "1f9697a5f1c1fd9c454fdaa21952f63ab6eaa052",
        }
        and successor.get("evidence_states") == {
            "broad_product_efficacy": "UNKNOWN",
            "cross_provider_runtime": "UNKNOWN",
            "cross_version_lifecycle": "NOT_RERUN_UNCHANGED_MECHANISM",
            "independent_review": "PENDING",
            "local_release_ready": "NOT_AUTHORIZED",
            "planner_acceptance": "NOT_APPLICABLE",
            "public_release": "NOT_AUTHORIZED",
            "role_delivery_runtime": "UNKNOWN",
            "source_contract": "REQUIRES_FRESH_DETERMINISTIC_CHECK",
            "stable_installed_copy": "PENDING_AUTHORIZED_UPDATE",
        }
    )
    checks["candidate.current_package_binding"] = (
        checks["candidate.v071_identity"]
        and actual_package_tree is not None
        and current_package_sha256 is not None
        and successor.get("package", {}).get("tree") == actual_package_tree
        and successor.get("package", {}).get("sha256") == current_package_sha256
    )

    v050_receipt_error = None
    v050_receipt = {}
    try:
        parsed_v050_receipt = json.loads(V050_RECEIPT.read_text(encoding="utf-8"))
        if not isinstance(parsed_v050_receipt, dict):
            raise ValueError("v0.5.0 local source receipt must be an object")
        for field in (
            "authorization_boundaries",
            "candidate",
            "evidence_states",
            "historical_runtime",
            "independent_review",
            "planner_acceptance",
            "verification",
        ):
            if not isinstance(parsed_v050_receipt.get(field), dict):
                raise ValueError(f"v0.5.0 local source receipt field {field!r} must be an object")
        if not isinstance(parsed_v050_receipt["candidate"].get("package"), dict):
            raise ValueError("v0.5.0 local source receipt package must be an object")
        if not isinstance(parsed_v050_receipt["independent_review"].get("findings"), list):
            raise ValueError("v0.5.0 local source receipt findings must be a list")
        v050_receipt = parsed_v050_receipt
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        v050_receipt_error = str(error)
    checks["receipt.v050_source_readiness"] = (
        v050_receipt.get("schema") == "work-charter-local-release-receipt/v1"
        and v050_receipt.get("product") == "work-charter"
        and v050_receipt.get("version") == "0.5.0"
        and v050_receipt.get("candidate")
        == {
            "commit": V050_COMMIT,
            "descriptor": "release/v0.5.0-candidate.json",
            "descriptor_raw_sha256": V050_CANDIDATE_SHA256,
            "package": {
                "file_count": 6,
                "files": sorted(EXPECTED_FILES),
                "path": "skills/work-charter",
                "sha256": V050_PACKAGE_SHA256,
                "tree": V050_PACKAGE_TREE,
            },
            "tree": V050_TREE,
        }
        and v050_receipt.get("authorization_boundaries")
        == {
            "actual_installation": "NOT_AUTHORIZED",
            "global_rule_migration": "NOT_AUTHORIZED",
            "publication": "NOT_AUTHORIZED",
            "remote_integration": "NOT_AUTHORIZED",
            "user_role_model_configuration_write": "NOT_AUTHORIZED",
        }
        and v050_receipt.get("evidence_states")
        == {
            "actual_installation": "NOT_PERFORMED",
            "broad_product_efficacy": "UNKNOWN",
            "cross_harness_behavior": "UNKNOWN",
            "cross_provider_runtime": "UNKNOWN",
            "local_source_ready": "VERIFIED",
            "natural_adherence": "UNKNOWN",
            "public_release": "NOT_PERFORMED",
            "role_delivery_runtime": "UNKNOWN",
            "source_candidate_acceptance": "VERIFIED",
            "stable_installed_copy_v050": "UNKNOWN",
            "user_role_model_configuration": "NOT_READ_OR_WRITTEN",
        }
        and v050_receipt.get("historical_runtime")
        == {
            "installed_version": "0.4.0",
            "v040_access_repair": "ACCEPTED_FOR_EXACT_ACL_ONLY_EFFECT",
            "v041_installed": False,
            "v050_installed": False,
        }
        and v050_receipt.get("independent_review")
        == {
            "completed_rounds": 10,
            "final_result": "NO_NEW_FINDINGS",
            "final_round": "WC-ROLE-CONFIG-SOURCE-V050-R10-RESULT-01",
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
                    "disposition": "FIXED_CLOSED",
                    "id": "WC-INSTALL-ACCESS-P01",
                    "severity": "P2",
                },
                {
                    "disposition": "FIXED_CLOSED",
                    "id": "WC-INSTALL-ACCESS-R5-F01",
                    "parent_finding": "WC-INSTALL-ACCESS-P01",
                    "severity": "P2",
                },
                {
                    "disposition": "FIXED_CLOSED",
                    "id": "WC-ROLE-CONFIG-R9-F01",
                    "severity": "P2",
                },
            ],
            "fresh_reviewer": {
                "model": "gpt-6-astra",
                "reasoning_effort": "high",
                "rounds": [
                    "WC-ROLE-CONFIG-SOURCE-V050-R9-RESULT-01",
                    "WC-ROLE-CONFIG-SOURCE-V050-R10-RESULT-01",
                ],
            },
            "historical_reviewer": {
                "model": "gpt-5.6-terra",
                "reasoning_effort": "high",
                "rounds": 8,
            },
            "non_findings": {
                "r7_acl_hypothesis": "UNCONFIRMED_NOT_A_FINDING",
                "r8_result": "NO_CONFIRMED_DEFECT",
            },
        }
        and v050_receipt.get("planner_acceptance")
        == {
            "commit": {
                "checkpoint": "WC-ROLE-CONFIG-SOURCE-V050-COMMIT-01",
                "disposition": "WC-ROLE-CONFIG-SOURCE-V050-COMMIT-DISPOSITION-01",
                "verdict": "ACCEPTED_COMMITTED_SOURCE_V050",
            },
            "source": {
                "checkpoint": "WC-ROLE-CONFIG-SOURCE-V050-ACCEPTED-COMMIT-HANDOFF-01",
                "review_checkpoint": "WC-ROLE-CONFIG-SOURCE-V050-R10-RESULT-01",
                "verdict": "ACCEPTED_SOURCE_V050",
            },
        }
        and v050_receipt.get("verification")
        == {
            "adversarial_repository_matrix": {
                "cases": 92,
                "result": "PASS",
                "subject": "RECEIPT_AND_CANONICAL_CONSUMERS",
                "terminal_exit_code": 0,
            },
            "repository": {
                "mapped_files": 89,
                "result": "PASS",
                "subject": "RECEIPT_AND_CANONICAL_CONSUMERS",
                "terminal_exit_code": 0,
            },
            "source_contract": {
                "checks": 26,
                "result": "PASS",
                "subject": "RECEIPT_AND_CANONICAL_CONSUMERS",
                "terminal_exit_code": 0,
            },
            "windows_lifecycle": {
                "default_token": "DACL_PREFLIGHT_PERMISSION_DENIED",
                "disposition": "DISPOSABLE_SOURCE_QUALIFICATION_ONLY",
                "elevated_token": "PASS",
                "persistent_effect": False,
                "subject": "ACCEPTED_SOURCE_COMMIT_C5",
                "terminal_exit_code": 0,
            },
        }
        and v050_receipt.get("human_release_notes_review") == "PENDING"
    )

    v041_candidate_error = None
    v041_candidate = {}
    try:
        v041_candidate = json.loads(V041_CANDIDATE.read_text(encoding="utf-8"))
        if not isinstance(v041_candidate, dict) or not isinstance(
            v041_candidate.get("package"), dict
        ):
            raise ValueError("v0.4.1 candidate descriptor must be an object with an object package")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        v041_candidate_error = str(error)
    checks["candidate.v041_historical_identity"] = (
        v041_candidate.get("schema") == "work-charter-local-release-candidate/v1"
        and v041_candidate.get("product") == "work-charter"
        and v041_candidate.get("version") == "0.4.1"
        and v041_candidate.get("public_identity") == "junwei529/work-charter"
        and v041_candidate.get("candidate_state") == "PENDING_INDEPENDENT_REVIEW"
        and v041_candidate.get("package")
        == {
            "file_count": 5,
            "path": "skills/work-charter",
            "sha256": "1fbffa78e7dfdc9509dc8a4b003da1c35b0b11151d09838ebe89d2be6e8bdaf1",
            "tree": "a2281edf51b624271cd5675ca02a7f4d5ae4acbb",
        }
        and v041_candidate.get("lineage")
        == {
            "historical_package_tree": V040_PACKAGE_TREE,
            "previous_candidate": "release/v0.4.0-candidate.json",
            "previous_local_release_receipt": "release/v0.4.0-local-release-receipt.json",
            "source_commit": "df674c773de6f915627af541f0eb37221da9adef",
        }
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
    if role_model_case_error:
        failures.append(f"role_models.case_unreadable: {role_model_case_error}")
    if current_candidate_error:
        failures.append(f"candidate.v050_unreadable: {current_candidate_error}")
    if successor_error:
        failures.append(f"candidate.v071_unreadable: {successor_error}")
    if v067_candidate_error:
        failures.append(f"candidate.v067_unreadable: {v067_candidate_error}")
    if v066_candidate_error:
        failures.append(f"candidate.v066_unreadable: {v066_candidate_error}")
    if v065_candidate_error:
        failures.append(f"candidate.v065_unreadable: {v065_candidate_error}")
    if v064_candidate_error:
        failures.append(f"candidate.v064_unreadable: {v064_candidate_error}")
    if v063_candidate_error:
        failures.append(f"candidate.v063_unreadable: {v063_candidate_error}")
    if v062_candidate_error:
        failures.append(f"candidate.v062_unreadable: {v062_candidate_error}")
    if v061_candidate_error:
        failures.append(f"candidate.v061_unreadable: {v061_candidate_error}")
    if v060_candidate_error:
        failures.append(f"candidate.v060_unreadable: {v060_candidate_error}")
    if package_identity_error:
        failures.append(f"package.identity: {package_identity_error}")
    if v050_receipt_error:
        failures.append(f"receipt.v050_unreadable: {v050_receipt_error}")
    if v041_candidate_error:
        failures.append(f"candidate.v041_unreadable: {v041_candidate_error}")
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
    static_clause_prefixes = (
        "authority.",
        "recovery.",
        "review.",
        "prompts.",
        "role_models.",
        "selection.",
        "standard.",
    )
    static_clause_checks = {
        name: passed
        for name, passed in checks.items()
        if name.startswith(static_clause_prefixes)
    }
    current_package_bound = checks.get("candidate.current_package_binding", False)
    result = {
        "checks": checks,
        "current_package_differs_from_v050": (
            current_package_sha256 is not None
            and current_package_sha256 != V050_PACKAGE_SHA256
        ),
        "current_package_tree": actual_package_tree,
        "failures": failures,
        "package_sha256": current_package_sha256,
        "proof_class": "deterministic-source-contract",
        "required_identity_gate": (
            "SATISFIED" if current_package_bound else "BLOCKED_CURRENT_PACKAGE_UNBOUND"
        ),
        "result": "PASS" if not failures else "FAIL",
        "source_release_identity": (
            "BOUND_TO_V071_CANDIDATE"
            if current_package_bound
            else "UNBOUND_PENDING_SUCCESSOR_VERSION_AND_DESCRIPTOR"
        ),
        "static_clause_checks_passed": sum(static_clause_checks.values()),
        "static_clause_checks_total": len(static_clause_checks),
        "static_clause_result": (
            "PASS" if all(static_clause_checks.values()) else "FAIL"
        ),
        "scope_limits": [
            "no model execution",
            "no task or role creation or runtime identity proof",
            "no host or global task-start consumer execution",
            "no live user-configuration read",
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
