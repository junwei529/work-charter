# Work Charter

[简体中文](README.zh-CN.md)

Release source: **v0.9.2**, with explicit cross-turn continuation and a retained mixed-design recovery path; arrangement-v1 and model schema v2 are unchanged.
See [publication state](docs/skills/work-charter/STATE.md#v092-publication).

Latest published release: **[v0.9.2](https://github.com/junwei529/work-charter/releases/tag/v0.9.2)**.
[Verified publication](docs/skills/work-charter/STATE.md#v092-publication).
The [v0.9.2 source candidate](release/v0.9.2-candidate.json) retains its
pre-effect snapshot; local review, managed-copy and bounded host-consumer status
is recorded in [State](docs/skills/work-charter/STATE.md#v092-local-source).

Keep complex AI projects moving across handoffs—and through to delivery.

Work Charter is a project collaboration Skill for Codex. It helps you choose
Direct, Team, or Phased work according to the result, real constraints, review
needs, and how you want to participate. An existing approved agreement remains
in force until its owner changes it.

It reuses known facts, inspects only authorized scope, and asks only questions
whose answers change the arrangement or a protected decision. Ordinary small
tasks need no Charter or extra questionnaire.

## Three ways to work

| Arrangement | How it works | When it helps |
|---|---|---|
| **Direct** | One primary owner completes the work; add a current-task agreement, durable recovery anchor, or independent review only when needed. | Everyday work, including a small high-risk change needing targeted review. |
| **Team** | A Planner owns the agreement and acceptance; an Executor implements; an independent Reviewer checks the actual product when requested or required. | Work that benefits from separated implementation and assessment. |
| **Phased** | An Orchestrator owns direction and phase acceptance above phase-local Planner, Executor and applicable Reviewer roles. | Consequential work across several dependent phases. |

New agreements directly describe the work arrangement and the conditions that
matter. You do not need to choose a level number. Use the least sufficient
coordination; more roles and handoffs have real cost.

## Conditional modules, one work agreement

First adoption, reassessment and migration use the same conditional choices.
Known answers are reused after checking that they still apply. Before adoption,
one concise agreement distinguishes confirmed/reused choices, recommendations
and unresolved decisions; it does not require a fixed questionnaire.
Conditional questions settle:

- **Continuity:** current-task context or a durable recovery anchor.
- **Review:** which actual result, plan or direction needs independent inspection.
- **Progression:** how far already-approved work continues without user intervention.
- **Execution boundaries:** real permission, workspace, data, cost and effect limits.

These are parts of one agreement, not arbitrary feature switches. Required review
and authority boundaries cannot be disabled. An approved same-scope repair can
go from R to the original author and back to the same valid R. P accepts stable
implementation results; planning products retain their designated approval
route. A preauthorized first E-to-R handoff also avoids routine relay.
Independent context and continuous progress are separate choices.

Continuous work covers execution, checks, review, repair, acceptance and the next
already-approved item. Cross-phase progression needs advance approval of a
bounded phase set and its transition conditions. A prompt cannot guarantee
background scheduling or reliable delivery. Name the recipient, supported
next-turn route and next authorized action; message arrival, activation,
completion and acceptance are separate. Recover a missing handoff without
repeating completed work or adding polling/ACK loops.

## Existing projects

At an authorized entry, recovery or stable work node, the Skill can suggest
reconsidering an old agreement. A stable node need not finish an entire Phase:
the product, remaining findings, writer, in-flight work and next action must be
clear enough to hand over. Reassess applicable choices rather than merely
patching the old level, models or carriers; reuse valid answers and approve one
complete migration delta. Existing contracts continue until that approval, with their findings,
consumed budgets, frozen models and protected gates preserved.

L0-L4 remain technical compatibility terms: ordinary/no Charter, current-task
Direct, durable Direct, Team and Phased respectively. They are not the internal
schema for new agreements. Personal model-file conversion is separate from
project adoption; installation performs neither migration automatically.

## Clear responsibilities for each role

Review products, Reviewer continuity and task/subagent carriers are separate
choices. Prefer one reliable continuing R for related direction, plan and
implementation reviews; use another only for a real independence, reliability,
expertise, access or authorized parallel-review need. Across independent O/P
tasks, an addressable R task can preserve continuity without depending on a
different parent's active turn. A bounded R subagent can serve an active parent;
cross-turn reuse also requires actual parent reactivation and recovery. Each review still names its product,
author and acceptance owner. Prior review is not authorship, but R must not
independently review a product or design decision it materially authored.
Context reuse is not a cache-hit or cost guarantee.

- **Direct primary:** Completes authorized work and its checks.
- **Orchestrator (Phased):** Owns project direction and phase acceptance.
- **Planner (Team or Phased):** Defines an executable agreement and accepts results. Team's Planner is its highest owner.
- **Executor:** Implements, checks, repairs, and delivers authorized work.
- **Reviewer:** Independently inspects an actual direction, plan, or implementation product against applicable instructions, the agreement, and evidence. The original author corrects findings; the same valid Reviewer rechecks.

Formal Team/Phased work that must continue after an upstream turn ends normally
uses independently addressable role tasks and an authorized route that starts
the recipient's next turn. Result arrival alone is insufficient. Direct short
review and bounded evidence subagents remain useful within an active parent.
Mixed carriers remain a supported design where actual host reactivation and
recovery fit; the current Codex cross-turn suspension and restoration conditions
are retained in [Design](docs/skills/work-charter/DESIGN.md#temporarily-suspended-mixed-design-and-restoration-conditions).
User-approved selection is still required; a new tool does not migrate work.
Use short recognizable titles and retain full identities/checkpoints in the
agreement. A work arrangement creates no tasks or permissions and guarantees
neither isolation nor recovery.

## Default models and customization

The package supplies complete provider, model, and reasoning-effort defaults.
They are recommendations by responsibility, not a claim of superior measured
performance or proof that an existing task has changed.

You can override a complete combination for an authorized new task or role.
Availability and parameters must be checked on the intended route.

User configuration takes priority over package defaults. Changes apply to tasks subsequently created using that configuration; existing tasks retain their settings.

| Responsibility | Package default |
|---|---|
| Direct primary; Team Planner; Phased Orchestrator | `gpt-6-astra` · `high` |
| Phased Planner; Team/Phased Executor | `gpt-6-sol` · `xhigh` |
| Any enabled independent Reviewer | `gpt-6-astra` · `medium` |

For a major planning tradeoff or difficult implementation judgment, an
authorized delivery may explicitly choose a complete `gpt-6-astra`/`high`
combination for P or E. A Reviewer default is used only when review is actually
enabled. A different provider needs supported parameters for that provider;
OpenAI effort names are not universal.

These are package presets. The task creation process must verify what is actually used; see the [default configuration file](skills/work-charter/assets/role-models.default.yaml) for the complete configuration.

## An example

For a task that must survive a handoff, Direct may need a durable recovery
anchor. If separate implementation and acceptance would help, consider Team.
If several phases need shared direction, consider Phased.

Independent review can cover an implementation, an executable plan, or an
overall direction when that product exists. Required review cannot be switched
off by preference. Keep valid decisions and ask about material changes before
dependent action.

## Get started

```text
$work-charter
This project will take several conversations to complete.
Recommend Direct, Team, or Phased work from what is already known.
Explain the outcome, roles, review, recovery, complete model defaults, and cost.
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

The released [`v0.6.5` candidate](release/v0.6.5-candidate.json) adjusts the approved
level-role defaults above and preserves the [v0.6.4 entry revision](release/v0.6.4-candidate.json). It keeps task-entry
assessment lightweight. An ordinary task without an applicable Charter or
material need stays at L0 without loading governance references or creating
roles. Applying roles load the shorter shared Skill body, then details only
for their decision, level and responsibility. An existing approved Charter is
reused. Material scope, permission, acceptance or recovery changes trigger a
reassessment and recommendation; the user still decides level adoption.
The package does not guarantee host-wide automatic loading or enforcement.
[State](docs/skills/work-charter/STATE.md#current-v065-local-candidate) and
[Verification](docs/skills/work-charter/VERIFICATION.md#current-v065-qualification)
record the candidate's scope and evidence limits. The accepted
[`v0.6.3` source and installation](docs/skills/work-charter/STATE.md#historical-v063-local-candidate)
remain historical evidence.

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
[accepted v0.6.3 installation](docs/skills/work-charter/STATE.md#accepted-v063-user-installation)
records that historical copy; [historical v0.6.5 state](docs/skills/work-charter/STATE.md#current-v065-local-candidate)
records that update. [Current state](docs/skills/work-charter/STATE.md#v092-local-source)
tracks the v0.9.2 source revision and separate installation state. Stable v0.5.0 loaded-copy behavior,
role-delivery adherence, cross-provider execution, cross-Harness behavior,
public release, and broad efficacy remain `UNKNOWN` or separately authorized.

## Role-model configuration

The [package YAML](skills/work-charter/assets/role-models.default.yaml) is the
single owner of complete default values. Model schema v2 has `roles`,
`arrangement_overrides` for `direct`/`team`/`phased`, and optional
`legacy_level_overrides` for unchanged old contracts. Arrangement maps select
actual responsibilities; there is no model table for every feature combination.
The Skill release version, `contract_format: arrangement-v1`, configuration
schema and frozen delivery values are distinct identities.

Use the contract's exact explicit file, else the existing
`~/.config/work-charter/role-models.yaml`, else package defaults. No user file is
needed to consume defaults. Every object repeats provider/model and optional
parameters; omitted parameters means none. Resolve frozen values, then confirmed
task values, then the selected user source, then package defaults. Within a v2
source use arrangement then general role, preceded by exact legacy level only
for an old contract. User general values beat package-specific defaults. Missing
primary values may preserve host selection; never borrow P or E values.

Schema v1 remains readable. New Team/Phased can interpret its l3/l4 candidates;
new Direct needs equal effective l0/l1/l2 candidates or all missing. Differing
objects or a present/missing mix require a decision, not silent fallback. A
separately authorized file conversion preserves every old level object in the
compatibility section and asks for an ambiguous new Direct default.

Validate the complete selected file, support and native parameters before
dispatch. Configuration does not create a role or prove runtime identity. An
install/update/rollback/uninstall never rewrites the user's external file or
existing tasks. The [configuration contract](skills/work-charter/references/coordination-and-recovery.md#role-model-configuration-at-dispatch)
owns the exact matrix, whole-object priority, v1 interpretation and stops.

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
python -B scripts/check_source_contract.py --json
python -B scripts/check_repository.py --json
```

Run the relevant checks against the final changed input. The SOURCE checker
separates static contract clauses from the required v0.9.2 tree/digest binding
and preserves historical descriptor identities, including v0.7.1.
Static wording and identity
checks do not prove model behavior. See
[Verification](docs/skills/work-charter/VERIFICATION.md) for current results.

Select additional checks for the mechanism changed: installer or permission
changes require affected lifecycle cases; provenance validation changes
require affected adversarial cases; selection/loading contract changes need focused correctness and compatibility
inspection. A fresh-loading claim needs its own runtime evidence; model or
efficacy evaluations require their separately agreed scope. A text or metadata change alone does not require rerunning the
complete lifecycle or staged-index matrix. Existing explicit frozen gates
retain their scope; the complete v0.6.3 qualification remains historical and
is not reported as a fresh run for a later revision. Actual installation still requires its
own identity, permission and postflight checks.

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
