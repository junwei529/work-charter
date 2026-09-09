# Work Charter

[简体中文](README.zh-CN.md)

Keep complex AI projects moving across handoffs—and through to delivery.

Work Charter is a project collaboration Skill for Codex. It offers five levels, L0–L4, with role responsibilities and model configurations to help you move from everyday tasks to projects spanning conversations, roles, and phases.

It recommends a suitable level based on the project's continuity, division of responsibilities, and acceptance needs, explains the benefits and costs, and leaves adoption to you. Existing working agreements can continue when they still apply.

## Five collaboration levels for different needs

| Level | How it works | Default roles | What it helps with |
|---|---|---|---|
| L0: Direct execution | Complete the current task without establishing a Charter | Primary owner | Keep everyday tasks simple |
| L1: Task agreement | Define goals, boundaries, and completion criteria in the current conversation | Primary owner, with an optional Reviewer | Give the current task a clear agreement |
| L2: Durable continuity | Add a persistent work record and recovery entry point | Primary owner, with an optional Reviewer | Pick up existing work in a new conversation |
| L3: Separate responsibilities | Separate planning, execution, and technical review | Planner, Executor, Reviewer | Make implementation and assessment responsibilities clear |
| L4: Project coordination | Add coordination across phases to L3 | Orchestrator, Planner, Executor, Reviewer | Coordinate project direction, phase goals, and overall acceptance |

An L1 agreement stays in the current conversation. For reliable recovery across conversations, use L2 or above. Higher levels require more coordination information to maintain, so start with the least sufficient level.

## Clear responsibilities for each role

- **Orchestrator — project coordination:** Owns project direction, phase planning, and project-level acceptance.
- **Planner — planning and acceptance:** Defines phase goals, work boundaries, and completion criteria, then assesses the results.
- **Executor — implementation and verification:** Implements authorized work, completes the necessary checks, and delivers results.
- **Reviewer — independent technical review:** Inspects implementation issues and provides traceable findings and evidence.

At L0–L2, the primary owner is directly responsible for the current task. A role arrangement does not itself create tasks or expand permissions.

## Default models and customization

The author built a private evaluation set from multiple real code repositories, organized around the responsibilities of the Orchestrator, Planner, Executor, and Reviewer. The current L0–L4 model and reasoning defaults were selected using those evaluation results.

These defaults provide a starting point. You can adjust models and reasoning settings for each level and role based on your project, available models, cost, and observed performance.

User configuration takes priority over package defaults. Changes apply to tasks subsequently created using that configuration; existing tasks retain their settings.

| Scope | Package default |
|---|---|
| L0 primary owner | Astra · medium |
| L1–L2 primary owner and optional Reviewer | Astra · medium |
| L3 Planner; L4 Orchestrator and Planner | Astra · max |
| L3–L4 Executor and Reviewer | Astra · medium |

Astra means `gpt-6-astra`; `medium` and `max` are reasoning effort settings. If a separate rule triggers a temporary Reviewer at L0, the current general fallback is Astra · high.

These are package presets. The task creation process must verify what is actually used; see the [default configuration file](skills/work-charter/assets/role-models.default.yaml) for the complete configuration.

## An example

For a project that spans several conversations, first assess whether L2 is appropriate to preserve key decisions, current state, verification evidence, and the next step.

When the project needs independent planning and technical review, assess the coordination cost of L3. When several phases need shared direction, consider L4. Throughout, retain valid decisions and make explicit adjustments for material changes.

## Get started

```text
$work-charter
This project will take several conversations to complete.
Recommend a suitable collaboration level from L0–L4.
Explain the default roles, model configuration, benefits, and maintenance cost.
```

If a working agreement is already in place:

```text
Continue the project under the existing approved Work Charter.
Check the current state, then proceed with the next authorized action.
```

[Design](docs/skills/work-charter/DESIGN.md) · [Current state](docs/skills/work-charter/STATE.md) · [Verification](docs/skills/work-charter/VERIFICATION.md) · [Evaluation scenarios](evals/README.md)

<details>
<summary>Technical reference, installation and recovery, version history, and historical evidence</summary>

Bounds consequential Codex work by outcome, authority, evidence, recovery,
independent review, and proportional coordination.

This repository is the independent product repository for `work-charter`. Its
installable package is [`skills/work-charter/`](skills/work-charter/). It was
materialized from source commit `80910a8b2375a11be897e9660c4b00a06d00dd13`;
files changed for the current repository-native version are identified in the
source map rather than represented as unchanged migration blobs.

The accepted `v0.5.0` source is described by the immutable pre-review snapshot
[`release/v0.5.0-candidate.json`](release/v0.5.0-candidate.json). The separate
[`release/v0.5.0-local-release-receipt.json`](release/v0.5.0-local-release-receipt.json)
binds accepted source commit `8bf9f130598fbf1b9170dd0c082e3e8fb78d6c0d`,
ten completed review rounds, Planner acceptance, and the exact deterministic
qualification. Local source readiness is `VERIFIED`; no v0.5.0 installation,
runtime role-delivery, or public-release claim follows from that receipt.

The current [`v0.6.3` candidate](release/v0.6.3-candidate.json) reuses an
applicable approved Charter and level, including small tasks and continuation
in a new Thread. First assessment recommends L0-L4 for user adoption; manual
reassessment starts from the existing contract. Authorized bounded assessment
needs no separate activation or repeated read question. Every applying fresh
role loads the full Skill and shared boundaries, then only reference sections
needed by its responsibility and next action. Loading is not adoption or action
authority. [State](docs/skills/work-charter/STATE.md#current-v063-local-candidate)
and [Verification](docs/skills/work-charter/VERIFICATION.md#current-v063-qualification)
record this source candidate's scope and evidence limits.

The prior [`v0.6.2` candidate](release/v0.6.2-candidate.json) asks Agents to
justify the failure, required strength, and lack of simpler alternatives behind
their own guardrails. When auxiliary work keeps growing, the primary owner or
Planner compares the remaining cost with simpler routes to the same protected
user outcome. Explicit requirements keep their existing authority. The
[contract guidance](skills/work-charter/references/coordination-and-recovery.md#contract-and-proposal-changes)
owns these two additions; schema 1, the six-file shape, defaults, and production
installation behavior are unchanged. The accepted v0.6.1 source and candidate
remain historical; fresh v0.6.2 checks, review, installation, and publication
have their own input and action boundaries.

The prior local `v0.6.0` candidate adds backward-compatible
level-by-actual-responsibility resolution and is bound by
[`release/v0.6.0-candidate.json`](release/v0.6.0-candidate.json).
R12 completed independent technical review with no new findings; Planner
accepted the uncommitted frozen source checkpoint. The [acceptance record](docs/skills/work-charter/STATE.md#accepted-v060-source-checkpoint)
identifies its scope and limits. The candidate remains its pre-review snapshot;
this is not committed source, local release readiness, installation, or global
adoption. The immutable
v0.5.0 candidate and receipt remain historical evidence for their exact bytes.

The immutable v0.4.0 receipt binds its accepted candidate, five review results,
and the failed v0.3-to-v0.4 update at that checkpoint:
[`release/v0.4.0-local-release-receipt.json`](release/v0.4.0-local-release-receipt.json).
The later sixth result, R6, found no source issue and Planner accepted the prior
correction, which was committed as
`df674c773de6f915627af541f0eb37221da9adef`. A first authorized repair preflight
then stopped because `icacls /restore` changed automatic-inheritance control
state. The v0.4.1 C4 correction replaced that path with exact control-aware
restore and readback and was independently accepted at
`59b4d91f46c2ac797c71c900e62dda87cf0cca60`. A later ACL-only repair restored
default-reader access to the exact managed v0.4.0 copy and closed
`WC-INSTALL-POSTFLIGHT-F01` for that repair. At that repair checkpoint the package remained
managed v0.4.0; v0.4.1 was not installed. The later
[accepted v0.6.2 installation](docs/skills/work-charter/STATE.md#accepted-v062-user-installation)
records the current verified user copy. Stable v0.5.0 loaded-copy behavior,
role-delivery adherence, cross-provider execution, cross-Harness behavior,
public release, and broad efficacy remain `UNKNOWN` or separately authorized.

## Role-model configuration

The package defaults are owned by
[`skills/work-charter/assets/role-models.default.yaml`](skills/work-charter/assets/role-models.default.yaml):

General compatibility fallbacks:

| Role | Provider | Model | Reasoning effort |
|---|---|---|---|
| Orchestrator | OpenAI | `gpt-6-astra` | `xhigh` |
| Planner | OpenAI | `gpt-6-astra` | `xhigh` |
| Executor | OpenAI | `gpt-5.6-sol` | `high` |
| Reviewer | OpenAI | `gpt-6-astra` | `high` |

Approved level defaults use OpenAI `gpt-6-astra`:

| Level | Responsibility and reasoning effort |
|---|---|
| L0 | primary `medium` |
| L1/L2 | primary and reviewer `medium` |
| L3 | planner `max`; executor and reviewer `medium` |
| L4 | orchestrator and planner `max`; executor and reviewer `medium` |

No L0 Reviewer override is supplied; its general fallback remains applicable.
These configured choices are not evidence of optimality or runtime adoption.

To customize later task starts or role deliveries, copy that file to
`~/.config/work-charter/role-models.yaml` and edit it, or have an approved
delivery contract name another exact file. Schema v1 still accepts the legacy
four-role file. A partial file may add a general `primary`, replace changed
general roles, and/or add bounded `level_overrides` for `l0` through `l4`.
Every supplied object is a whole replacement and must repeat `provider` and
`model`; omitted `parameters` means none. Missing user objects fall through to package objects. No user file is needed
to consume package level defaults.

Resolution is: an already frozen complete delivery combination; then a complete
combination explicitly confirmed for the new task or role; then its applicable
user level object; user general object; package level object; package general
object. User general configuration beats package level defaults. A host `main`
label normalizes to `primary`. If an `L0`/`L1`/`L2` primary has neither a level
override nor a general `primary` in either source, the boundary sends no model override and
preserves host selection—it never borrows Planner or Executor defaults.

The valid lookup matrix is `L0` primary plus separately triggered temporary R;
`L1`/`L2` primary plus optional R; `L3` P/E/R; and `L4` O/P/E/R. Entries do not
enable roles, and `L0` still does not activate Work Charter. Before creation,
the boundary shows level, actual responsibility, provider/model/parameters,
object source, and file source and verifies native support. Codex OpenAI maps
`model` to native `model` and `reasoning_effort` to `thinking`. Unsupported or
ambiguous data fails closed. Existing tasks and roles do not change when the
file changes. The package defines this interface; global and host task-start
consumers have not yet been migrated, so the source and fixtures are not proof
of effective local delivery. Install, update, rollback, and uninstall never
mutate the external user file.

Prompts use the [shared contract, actual responsibility, current task, and
necessary model adaptation](skills/work-charter/references/coordination-and-recovery.md#task-and-role-prompt-construction).
Reuse valid authority for continuation, retain material gates, and adapt to an
actual model only with relevant guidance or attributable evidence. Effort stays
in runtime metadata. Each prompt and handoff retains the facts, decisions,
material limits, and next action its receiver needs; remove repeated
background and unrelated prose before essential information. Global migration follows separate Skill acceptance and
an approved applicable-copy switch; it is not performed by this candidate.

## Historical v0.3.0 evidence

The first independent version is `v0.3.0`. Its historical local candidate is
described by [`release/v0.3.0-candidate.json`](release/v0.3.0-candidate.json);
its public identity is `junwei529/work-charter`. Exact candidate C was accepted
and is bound by [`release/v0.3.0-local-release-receipt.json`](release/v0.3.0-local-release-receipt.json),
so `LOCAL_RELEASE_READY` is `VERIFIED`. `PUBLIC_RELEASE` is `VERIFIED` for
immutable public commit `b655c1aa42acc8c68b70e87c4c228445c5182d8b`, annotated
tag `v0.3.0`, and the public GitHub Release.
The immutable candidate descriptor retains its original
`PENDING_PLANNER_ACCEPTANCE` snapshot rather than rewriting C.

The immutable public-source candidate is described by
[`release/v0.3.0-public-release-candidate.json`](release/v0.3.0-public-release-candidate.json).
It preserves the package bytes and records the intended public repository,
default branch, tag, and human release-note gate without containing its own
commit hash. An exact public ref and later release receipt must bind that commit;
the annotated tag and GitHub Release were later created after explicit human
approval.

The post-release evidence subject is recorded in
[`release/v0.3.0-public-release-evidence.json`](release/v0.3.0-public-release-evidence.json).
It binds the public objects, bounded same-version persistent lifecycle effects,
the two historical projectless witnesses, and a fresh sole-discovery loaded-copy
witness. The retained predecessor bytes are preserved outside every Skill
discovery root, so the managed user installation is the only catalog-visible
`work-charter`. Planner acceptance `B2-WC-PUBLIC-EVIDENCE-F-01` verifies exact
subject F `4ba904808fe86e270ebd405db1866d41d1cc032e`; cross-version lifecycle
behavior, cross-Harness behavior, untested contexts, and broad efficacy remain
`UNKNOWN`.

## Repository contents

- Product package: [`skills/work-charter/`](skills/work-charter/)
- Product design and state: [`docs/skills/work-charter/`](docs/skills/work-charter/)
- Evaluation cases and fixtures: [`evals/`](evals/README.md)
- Standalone verification: [`scripts/check_repository.py`](scripts/check_repository.py)
- SOURCE contract qualification: [`scripts/check_source_contract.py`](scripts/check_source_contract.py)
- Install lifecycle tool: [`scripts/manage_install.py`](scripts/manage_install.py)
- Source mapping: [`PROVENANCE.md`](PROVENANCE.md) and
  [`provenance/source-map.json`](provenance/source-map.json)
- Release notes: [`CHANGELOG.md`](CHANGELOG.md)

## Verify

```powershell
python -B scripts/check_repository.py --json
python -B scripts/check_source_contract.py --json
python -B scripts/manage_install.py self-test --source .
```

The SOURCE checker reports the static selection, assessment/adoption, authority,
recovery, independent-review, level-role, and Standard O/P/E/R clauses
separately from the required current-package identity gate. The v0.6.3
descriptor must bind the actual current tree and digest; any mismatch makes
the command fail. The immutable v0.5.0 descriptor is checked only against its
historical values. Current-input results are recorded in
[Verification](docs/skills/work-charter/VERIFICATION.md).

The lifecycle self-test is a required gate for the current v0.6.3 package and
first binds its source to the matching descriptor. An older exact-release
checkout is not coverage for the current input. The staged adversarial
repository matrix likewise does not cover an unstaged working-tree delta.
Neither missing gate may be reported as passed or inapplicable.
These checks still do not execute a model, create a task or
role, exercise a host/global consumer, read a live user configuration, re-read
the installed copy, prove publication, or establish broad efficacy.

## Future immutable-source lifecycle

Use an exact immutable checkout of `junwei529/work-charter` as `--source` and
an explicit destination. Commands are dry-run plans unless `--apply` is added:

```powershell
python -B scripts/manage_install.py status --destination <skill-destination> [--trusted-current-package-tree <git-tree-sha1>]
python -B scripts/manage_install.py install --source <v0.3.0-immutable-checkout> --destination <skill-destination> --expected-version 0.3.0
python -B scripts/manage_install.py update --source <new-immutable-checkout> --destination <skill-destination> --expected-version <new-version>
python -B scripts/manage_install.py rollback --source <old-immutable-checkout> --destination <skill-destination> --expected-version <old-version>
python -B scripts/manage_install.py uninstall --destination <skill-destination> [--trusted-current-package-tree <git-tree-sha1>]
```

For any planned product mutation, first create an absolute task-scoped
transaction directory on the same filesystem volume as the destination,
outside every Skill discovery root, then add
`--apply --transaction-root <external-task-directory>`. The tool automatically
protects the destination parent and the source checkout's `skills` directory;
repeat `--discovery-root <absolute-path>` for every additional active Skill
discovery root. It rejects missing, relative, aliased, link-like, overlapping,
or cross-volume explicit paths before changing the destination.

Existing `--apply` calls that omit `--transaction-root` remain behaviorally
compatible: the tool creates a unique validated same-volume directory outside
the destination discovery root, reports `AUTO_COMPATIBILITY`, and removes that
directory after a clean result. This fallback does not authorize or replace the
explicit path required by a planned installation or release operation. In both
modes, stage, backup, tombstone, and recovery-archive material stays under the
external per-operation transaction directory. On Windows, every content-bearing
object and permission snapshot is individually protected for Owner Rights,
SYSTEM, and Administrators before bytes are written. A new install inherits the
destination parent's existing DACL. Before updating, rolling back, or uninstalling,
the tool qualifies the original DACL on a zero-byte model with an isolated copy
of the parent's inheritance context. This includes an original-policy/private-
policy/original-policy roundtrip. Records whose snapshot already
contains AI use a one-record `icacls /restore`; records without AI use
`SetFileSecurityW` with DACL and, when required, protected-DACL information so
the setter does not propagate a directory policy to children. Shallow-to-deep
application is followed by the same bounded `/save` readback. The comparison
ignores record enumeration order and newline serialization, but requires the
same managed path set and exact DACL SDDL for each path, including P, AI, AR,
and ACE order/content. Unsupported control states or any preflight mismatch fail
before target ACL changes or moves. After those checks, the exact old managed
objects become private before the first move to backup or tombstone. Readers can
temporarily lose access during this handoff. Even a failed move can therefore
require restoring changed ACLs. Promotion and recovery restore the original
policy at the real destination parent and verify it before reporting success.
Incomplete recovery retains the original snapshot and complete old content.
Uninstall archive recovery is unpacked privately before promotion. Untrusted
writers, unsupported owners/ACE forms, hard-linked managed files, or context
drift are refused. The [design](docs/skills/work-charter/DESIGN.md#windows-permission-context-and-private-handoff)
defines these bounds; other platforms retain their prior permission behavior.

Historical five-file receipts and candidate descriptors and the current six-
file descriptor are recognized only as exact allow-listed package shapes. A
legacy five-file candidate may omit the redundant package digest because its
actual tree must still match an independent trusted tree; the current six-file
shape requires the digest, and any supplied invalid or mismatched digest fails
closed. For a Windows update or rollback whose path set changes, the tool first
proves the original recovery
snapshot on the same empty context model, transforms only that model to the target path
shape, resets only newly introduced paths to parent inheritance, verifies that
every common descriptor is unchanged and every new path is auto-inherited and
unprotected, and proves an exact readback of the projected snapshot. The
original snapshot remains the recovery authority. Unknown or self-declared
path sets, unsafe receipt keys, missing or extra paths, and tree mismatches fail
closed.

The install example is deliberately bound to an immutable v0.3.0 checkout,
whose package tree is already in the bundled trust map. Do not substitute this
working checkout into that historical command. The v0.4.0 package was reviewed,
accepted, externally trust-bound, and written through
the explicit route recorded in its local-release receipt, but the promoted
directory retained the transaction ACL and failed default-reader access. The
committed v0.4.0 correction still failed its first later actual-policy
preflight because `/restore` changed AI. The accepted v0.4.1 C4 source replaces
that restore path and also tightens permission-question routing. Its later
ACL-only application restored the exact v0.4.0 installed copy's default-reader
access; it did not install the v0.4.1 package. Neither v0.4 package tree is
added to the tool's historical built-in map, so later status or mutation must
continue to receive the independently retained trust identity.

The repair for that exact failed v0.4.0 copy remained ACL-only, not a generic
update that discards arbitrary policy. Its first authorized attempt stopped
before target mutation; the later bounded attempt used accepted C4 source,
reverified trusted content/receipt and rollback inputs, changed only the target
DACL, and passed default-identity status, direct-read, hash, and ACL postflight.
That result does not authorize another repair, package update, or installation.

The tool refuses destinations that are unreceipted, have a malformed or
mismatched receipt, use the wrong package tree, are locally modified or aliased,
or otherwise drift from the receipt. The receipt is an integrity and routing
record, not cryptographic ownership proof: a same-privilege local actor capable
of forging the complete receipt is outside this mechanism's protection.
For v0.3.0, the separately authorized persistent same-version lifecycle,
publication, tag, GitHub Release, and stable installed-copy evidence are
verified as recorded above. For v0.4.0, the original promotion failure and the
later exact ACL-only access repair remain separate evidence; the repair left that copy
managed and default-readable at v0.4.0 before the later accepted update. Other cross-version
transitions and stable loaded behavior still require separate evidence.

### Future update and rollback trust

The bundled trust map authorizes the v0.3.0 package tree only. A later immutable release must publish its human-reviewed package-tree identity independently of the candidate checkout. Supply that external trust anchor with `--trusted-target-package-tree <git-tree-sha1>` when updating or rolling back to a version not bundled in this tool. If the currently installed version is also absent from the bundled map, supply its independently retained identity with `--trusted-current-package-tree <git-tree-sha1>` for update, rollback, status, and uninstall. Never copy either trust value from the source tree being installed; future-version public release and cross-version lifecycle evidence remain `UNKNOWN` until separately established.

</details>
