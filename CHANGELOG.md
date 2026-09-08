# Changelog

## Work Charter v0.6.1

Local candidate: [release/v0.6.1-candidate.json](release/v0.6.1-candidate.json)

Independent source review and Planner acceptance: verified at the
[installer checkpoint](docs/skills/work-charter/STATE.md#accepted-installer-source-checkpoint).
The candidate retains its pre-review snapshot; human release-note review is `PENDING`.

- Reuses scoped authorization in the default startup prompt, asking only for
  missing project-read or adoption decisions.
- Keeps prompts and handoffs proportionate and complete for the receiver's
  next decision/action, removing repeated background before material content.
- Routes entrypoint and Standard configuration lookups to one required
  coordination reference. Priority, whole-object replacement, validation,
  native mapping, approved defaults, and authority boundaries are unchanged.
- Binds fresh package qualification to v0.6.1 and preserves the frozen v0.6.0
  descriptor and prior evidence. Installation and publication require their
  own completed gates; neither is claimed by this candidate.
- Corrects repository-side Windows installer preflight for fully inherited
  targets using an empty model with the original parent's inheritance context.
  Real transaction material is individually private; old objects become private
  before moving, with verified restoration after partial ACL failures. Uninstall
  recovery unpacks privately before promotion. The package, version, candidate
  and receipt schema are unchanged. Corrected source is accepted; actual retry
  and installation acceptance remain subsequent gates.

## Work Charter v0.6.0

Local candidate: [`release/v0.6.0-candidate.json`](release/v0.6.0-candidate.json)

Descriptor snapshot: `PENDING_INDEPENDENT_REVIEW`

Human release-note review: `PENDING`

R12 completed with no new findings; Planner source verdict:
`ACCEPTED_FROZEN_SOURCE_CHECKPOINT` for the uncommitted input recorded in
[State](docs/skills/work-charter/STATE.md#accepted-v060-source-checkpoint). The
pre-review descriptor is unchanged. Later acceptance-record edits are checked
separately; no commit, local release readiness, installation, or global adoption
follows from this verdict.

- Adds optional general `primary` and `level_overrides` to schema version 1,
  preserving legacy four-role YAML and exact general compatibility defaults.
  Adds 12 approved Astra level objects; canonical YAML owns their values.
- Resolves a frozen delivery, a task-explicit confirmed combination, user
  level, user general, package level, then package general objects.
  Every selected object is complete; omitted parameters never carry over.
- Represents L0/L1/L2 primary owners without borrowing Planner or Executor
  metadata. Only a primary absent from both sources preserves host selection. Entries do not
  create roles, L0 does not activate Charter, and active tasks do not change.
- Builds prompts from contract, actual responsibility, current task, and
  supported model delta. Reuses valid authority, keeps real gates, and avoids
  redundant microsteps/checks. Effort stays native runtime metadata.
- Requires the current package tree and digest to match the v0.6.0 descriptor
  and directs lifecycle qualification to that source version. Historical
  candidates, receipts, failures, and acceptance remain attached to their bytes.
- Defines a task-start and dispatch interface; host/global consumers are not
  integrated. Deterministic checks do not prove model efficacy or runtime
  adoption. Installation, real user configuration, global rules, model runs,
  commit, and publication remain separate authorization boundaries.

## Work Charter v0.5.0

Descriptor snapshot: `PENDING_INDEPENDENT_REVIEW`

Local source readiness: `VERIFIED`

Acceptance receipt:
[`release/v0.5.0-local-release-receipt.json`](release/v0.5.0-local-release-receipt.json)

Accepted source commit: `8bf9f130598fbf1b9170dd0c082e3e8fb78d6c0d`

Human release-note review: `PENDING`

### Highlights

- Adds the package-owned `assets/role-models.default.yaml` with approved initial
  defaults: Orchestrator and Planner use `gpt-6-astra/xhigh`, Executor uses
  `gpt-5.6-sol/high`, and Reviewer uses `gpt-6-astra/high`.
- Resolves role metadata at the authorized delivery boundary: a frozen delivery
  wins, otherwise an explicit contract path, the default user path, or the
  package default is selected in that order. The resolved role/provider/model/
  parameters and source are shown before native creation.
- Makes partial user files replace complete named role objects. Provider and
  model are required; omitted parameters mean none, so values never leak from
  a prior model or provider. Unknown, duplicate, ambiguous, executable,
  secret-bearing, or unsupported data fails closed.
- Keeps configuration outside authority: it cannot create roles or widen
  permissions, does not alter existing/frozen deliveries, adds no watcher,
  service, parser dependency, or generic provider gateway, and is never mutated
  by install/update/rollback/uninstall.
- Extends the lifecycle controller from one fixed package set to exact
  allow-listed historical five-file and current six-file identities. Windows
  path-set changes are projected on a private replica; common DACL descriptors
  remain exact, new paths must inherit, and both target and recovery snapshots
  retain exact readback guarantees.
- Preserves the real historical five-file candidate format, whose trusted tree
  can stand without a redundant package digest. The current six-file format
  still requires its digest, and any explicitly supplied invalid or mismatched
  digest fails closed.
- Carries forward independently accepted v0.4.1 C4 source. The separately
  accepted ACL-only repair made the exact managed v0.4.0 installed copy
  default-readable without installing v0.4.1.

### Evidence boundaries

- The immutable descriptor retains its pending pre-review snapshot. The
  separate receipt binds ten completed review rounds, final R10 no-new-finding
  result, Planner acceptance, the accepted commit, and exact deterministic
  qualification without rewriting the candidate.
- Static checks and the role-configuration evaluation case do not prove Agent
  adherence, role creation, runtime identity, cross-provider execution, or a
  live user configuration.
- The six-file source, independent review, Planner acceptance, and local commit
  are complete and receipt-bound. Installation and runtime evidence remain
  distinct gates.
- v0.5.0 grants no persistent installation, user-config write, global-rule
  migration, provider/account/credential/network change, push, tag, release,
  or publication authority.

## Work Charter v0.4.1

Descriptor snapshot: `PENDING_INDEPENDENT_REVIEW`

Local release state: `PENDING_REVIEW_AND_PLANNER_ACCEPTANCE`

Human release-note review: `PENDING`

### Highlights

- Replaces the v0.4.0 whole-tree `icacls /restore` path after an authorized
  actual-policy preflight proved that it added AI while preserving paths and
  ACE text. The preflight stopped before target mutation, so the installed
  v0.4.0 access finding remains open.
- Restores saved Windows DACLs path by path. Records already carrying AI use a
  single-record `/restore`; records without AI use `SetFileSecurityW`, whose
  directory setter does not propagate policy to children. Every path is still
  read back through `/save` and must exactly retain P, AI, AR, ACE type, flags,
  SID, rights, and order. Unsupported states fail before a target move.
- Adds focused Windows proof for both AI-bearing and deliberately no-AI DACL
  round trips, path escape refusal, control-flag drift, missing paths, ACE
  ordering, promotion recovery, and protected snapshot retention.
- Reuses valid authorization across carrier tasks while requiring an action or
  permission-gate task to ask and receive any environment-mandated direct
  operation permission itself. Upstream relay does not replace that gate;
  higher-level contract ownership remains unchanged, and read-only reviewers
  do not solicit write authority.
- Introduces a new five-file candidate derived from committed v0.4.0 source
  `df674c773de6f915627af541f0eb37221da9adef`. It creates no v0.4.1 receipt,
  installation, publication, or acceptance claim.

### Evidence boundaries

- The v0.4.0 R6 no-finding result and Planner source acceptance remain
  historical facts. The later actual-policy preflight is new counterevidence
  that requires this v0.4.1 source checkpoint and fresh review.
- At this descriptor snapshot, `WC-INSTALL-POSTFLIGHT-F01` remained open and
  the actual installed copy, its parent ACL, and all retained v0.4.0 repair
  snapshots were unchanged. A later separately accepted ACL-only repair closed
  that finding for the exact managed v0.4.0 copy without installing v0.4.1.
- v0.4.1 deterministic checks and disposable Windows proof are source
  qualification only. They do not authorize a new actual repair, commit,
  installation, release, or cleanup.

## Work Charter v0.4.0

Descriptor snapshot: `PENDING_INDEPENDENT_REVIEW` (retained without rewriting)

Source-candidate acceptance: `VERIFIED`

Local release state: `BLOCKED_BY_INSTALLED_COPY_ACCESS_REGRESSION`

Human release-note review: `PENDING`

### Highlights

- Adds portable independent Reviewer semantics without forcing Work Charter at
  `L0` or Planner/Executor separation at `L1` and `L2`.
- Separates Executor verification, Reviewer technical findings, Planner target
  acceptance, and Orchestrator project direction/phase acceptance across
  Standard O/P/E/R.
- Routes stable Executor checkpoints through Planner scope freeze to a read-only
  Reviewer, then back through Planner correction and acceptance; repair reuses
  the same reliable Reviewer and preserves cumulative findings.
- Treats `UNKNOWN` as an evidence question first, limits graph results to
  attributable coverage guidance, and never treats hashes, tests, status, or
  graphs as semantic review or acceptance.
- Distinguishes compaction, deliberate context rotation, and successor Sessions
  while preserving contract, authority, role/writer, finding, stop, and
  evidence history.
- Enforces one current Result Notice per route and checkpoint, with no mirrored
  verdicts, polling, or acknowledgement loop.

### Evidence boundaries

- The immutable local descriptor binds the accepted five-file SOURCE candidate;
  a separate non-circular receipt binds the later review and acceptance facts.
- The immutable receipt binds five independent technical-review rounds and
  Planner source/tool acceptance for its exact recorded identities. R6 later
  returned `NO_FINDINGS`, and Planner accepted the source correction.
- One explicit-root v0.3.0-to-v0.4.0 attempt wrote exact bytes and passed
  elevated receipt/five-file postflight, but the promoted directory retained
  the private transaction ACL and failed default-reader access. Managed
  installation and `LOCAL_RELEASE_READY` are not accepted.
- R4 returned `NO_FINDINGS`, but Planner acceptance found open P2
  `WC-INSTALL-ACCESS-P01`: unconditional parent reset did not preserve a managed
  target's explicit or protected DACL policy.
- R5 opened P2 `WC-INSTALL-ACCESS-R5-F01`: `/restore` process success alone did
  not prove the target DACL was restored. The readback correction later passed
  R6 and Planner acceptance and was committed as
  `df674c773de6f915627af541f0eb37221da9adef`.
- The revised bounded Windows correction protects each random transaction and
  its recovery material, snapshots the complete existing DACL tree and proves
  it can be restored and semantically read back before update/rollback/uninstall
  mutation, preserves and rechecks that policy on the new or recovered target,
  and uses parent inheritance only for a genuinely new install. Record order
  and newline form are non-semantic; path membership and exact DACL SDDL,
  including flags and ACE order/content, must match. A later actual-policy
  preflight exposed the AI transition recorded under v0.4.1 and made no target
  mutation; at that checkpoint the actual installed copy remained unrepaired.
  A later separately accepted ACL-only repair restored default-reader access
  without accepting the v0.3.0-to-v0.4.0 installation transition.
- Stable loaded-copy behavior, natural adherence, other cross-version
  lifecycle effects, cross-Harness behavior, public source, tag, Release, and
  broad efficacy remain failed, `UNKNOWN`, or separately authorized as
  recorded for v0.4.0.
- Historical v0.3.0 receipts and public evidence remain unchanged and apply
  only to that version.

## Work Charter v0.3.0

Human release-note review: `PENDING`

First independent release of Work Charter, a Codex Skill for bounding
consequential work by outcome, authority, evidence, recovery, and proportional
coordination.

### Highlights

- Publishes the independently versioned `junwei529/work-charter` repository.
- Preserves the installable 5-file Work Charter package byte for byte from the
  recorded migration source.
- Includes deterministic SOURCE qualification for selection and activation,
  authority non-expansion, coordination and recovery, and Standard O/P/E.
- Includes an explicit-destination lifecycle tool with dry-run defaults and
  disposable install, update, rollback, uninstall, and recovery checks.

### Evidence boundaries

- Local release readiness is verified for the accepted immutable candidate.
- The release does not by itself prove stable installed-copy behavior,
  cross-Harness behavior, untested selection or loading contexts, persistent
  lifecycle effects, or broad product efficacy.
- Lifecycle receipts provide integrity and routing evidence, not cryptographic
  ownership against a same-privilege local actor able to forge a complete
  receipt.
