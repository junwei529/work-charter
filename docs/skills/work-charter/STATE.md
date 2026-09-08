# Work Charter State

## Current implementation

Canonical editable source is the 6-file package under
[`skills/work-charter/`](../../../skills/work-charter/). It originated from
`80910a8b2375a11be897e9660c4b00a06d00dd13`; changed package, evaluation,
documentation, and checker files carry their recorded transformations and are bound to their
current hashes in the provenance manifest. Unchanged mapped material retains
its exact or normalized migration provenance. The working package is now
the local v0.6.2 candidate. It follows accepted v0.6.1 source and installer
correction commit `38dd18cb65b4afd24ef2139dcc63a014de1c5ccf`, independently
verified by the Planner. Historical acceptance does not qualify the new package.

## Current v0.6.2 local candidate

- Version: user-confirmed v0.6.2; schema 1 and six-file package shape retained
- Changes: Agent-derived guardrails explain concrete failure/consequence,
  needed protection strength, and why simpler existing methods are insufficient;
  expanding auxiliary work prompts the primary owner or Planner to compare
  remaining costs and simpler routes to the same protected user outcome
- Explicit user/project requirements retain existing authority; no extra
  role, form, or approval gate is added
- Candidate: [v0.6.2 descriptor](../../../release/v0.6.2-candidate.json),
  `PENDING_INDEPENDENT_REVIEW`; no committed-source receipt
- Package identity and required qualification: [Verification](VERIFICATION.md#current-v062-qualification)
- Source acceptance: R17 found no new blocking or material findings; Planner
  independently accepted the [frozen source checkpoint](#accepted-v062-source-checkpoint)
- Production installer, default models, schema, and metadata are unchanged;
  only the installer's self-test version constant follows v0.6.2
- The unstarted v0.6.1 installation retry remains suspended
- Accepted source commit: `21391c98197485494690050ce2a889745c10403c`
- Last verified installed copy: managed v0.6.2;
  [actual installation accepted](#accepted-v062-user-installation) by Planner
- Global consumer migration: `NOT_PERFORMED`; runtime/efficacy: `UNKNOWN`
- Existing candidate snapshots, R1-R17, findings, failures, and consumed
  operations remain historical evidence; no count or approval is reset

### Accepted v0.6.2 source checkpoint

R17 reviewed the complete 18-path difference and material unchanged context;
Planner independently verified the same 93-file index and working bytes and
accepted both portable additions. Baseline commit is
`38dd18cb65b4afd24ef2139dcc63a014de1c5ccf`; accepted staged diff SHA-256 is
`47fd0803259cb27766a35f0e5c56e5c7425a6fae37de1ab7f679071b9b9dd717`, and
indexed-content manifest SHA-256 is
`adb9e1043ef2a542ac203de6701153bf8613424b73f418d56704b1cd8c88980e`.
Package and qualification identities are in [Verification](VERIFICATION.md#current-v062-qualification).
This is independent technical review and frozen-source acceptance, not native
review, installation, publication, or runtime efficacy. The candidate retains
its immutable pre-review pending snapshot. Subsequent acceptance-record and
mapping changes receive separate final-input checks without changing the
accepted package or installer.

### Accepted v0.6.2 user installation

The managed user copy was updated from v0.4.0 using the existing production
installer and immutable accepted source commit
`21391c98197485494690050ce2a889745c10403c`. Planner independently verified
the source, six installed files, receipt, default-reader access, and bounded
permission preservation and accepted this exact installation. Detailed checks
and limits are in [Verification](VERIFICATION.md#accepted-v062-installation-verification).
Prior failed attempts remain historical evidence; this success does not imply
loaded-copy behavior, consumer migration, model adherence, publication, or
other lifecycle transitions.

## Historical v0.6.1 local candidate

- Version: v0.6.1; schema 1, six package files, approved default model/effort
  objects and role/permission/review contracts unchanged
- Changes: startup prompt reuses scoped authorization; prompts and handoffs
  retain necessary facts, decisions, material limits, and next action;
  configuration resolution has one required reference owner
- Candidate: [v0.6.1 descriptor](../../../release/v0.6.1-candidate.json),
  `PENDING_INDEPENDENT_REVIEW`; no committed-source receipt
- Package identity and input-bound qualification: [Verification](VERIFICATION.md#historical-v061-qualification)
- Current installer correction: `ACCEPTED_FROZEN_SOURCE_CHECKPOINT`; R16
  confirmed R15-F01 fixed with no new blocking/material findings, followed by
  Planner source acceptance; six-file package and candidate bytes unchanged
- The earlier v0.6.1 source was accepted and committed. Its authorized managed
  update stopped in fully inherited DACL preflight before target mutation.
  The SOURCE correction and synchronized records were committed as
  `38dd18cb65b4afd24ef2139dcc63a014de1c5ccf` and independently checked by the
  Planner. The unstarted installation retry was suspended; neither installation
  acceptance nor Git publication is established by that commit.
- Global consumer migration: `NOT_PERFORMED`; runtime/efficacy: `UNKNOWN`
- v0.6.0 descriptor and historical release objects remain byte-identical;
  previous checks and R12 do not prove this new installer input

The failed update and bounded diagnosis exposed a missing inheritance-parent
context in the old private replica. The correction uses an empty context model
and individually private real material, with a temporary private handoff before
moving old objects. Partial ACL failure requires recovery even with zero moves.
The supported permissions, owner/writer admission and recovery rules are owned
by [Design](DESIGN.md#windows-permission-context-and-private-handoff); current
SOURCE evidence requirements are owned by [Verification](VERIFICATION.md#historical-v061-qualification).
At that historical checkpoint the installed copy remained managed v0.4.0. Prior failed evidence
is retained and the SOURCE result does not establish a successful installation.

### Accepted installer source checkpoint

The accepted object is the complete 92-file index on baseline
`74b477d856b540e437ecb267dddf617dea5aa2`, with a 10-path staged diff SHA-256
`5eebc1eef646e180f37a64b5cdc52835594ea73a612494def86b7939d85fa7d5`.
Installer SHA-256 is
`e2c5d382144b120d9310fc0783b3fb0a7790866a6f6c1d1ff66a45010553c608`.
R15 reviewed the correction; R16 verified the non-Windows mkdir compatibility
fix and unchanged Windows branch. Planner independently matched the full index,
working bytes and diff before acceptance. Subsequent record synchronization
preserves that accepted installer/package identity and has its own final-index
checks; it does not rewrite the accepted checkpoint or pending candidate snapshot.
This acceptance addresses the reproduced inheritance defect within the existing
contract; it does not make every installer guarantee necessary for every Skill
installation. Native POSIX execution remains `UNKNOWN` / `NOT_PERFORMED`.

## Accepted v0.6.0 source checkpoint

- Source verdict: `ACCEPTED_FROZEN_SOURCE_CHECKPOINT`
- Independent technical review: cumulative R12 completed, `No new findings`;
  coverage was the complete 21-file source diff plus necessary unchanged
  semantic context. Read-only input identity held before and after review.
- Planner accepted the configuration capability, approved level defaults,
  prompt method, and that complete frozen input; P-C1/P-C2 are closed.
- Accepted baseline HEAD: `018ff69a26b70a3a490b57f3641b356739bb228f`
- Accepted staged-diff SHA-256:
  `237d7c0b0cf4318699c9e24d187e24843b76532700677ce9f343c7429da2b2bd`
- Accepted candidate SHA-256:
  `5890f3e7c73ed1d4046269a03b1385097a0596cca804a57e49a838d588aa96ff`
- Package shape: unchanged 6 files
- Configuration schema: backward-compatible `schema_version: 1` extension
- Package general defaults: unchanged O/P/E/R compatibility objects and values
- Package level defaults: 12 approved Astra objects in the canonical YAML
- Prompt method: contract + actual responsibility + current task + supported
  model delta; effort remains runtime metadata, model efficacy unverified
- Added configuration objects: optional general `primary` plus bounded
  `level_overrides` for the actual-responsibility matrix
- Resolution: frozen delivery, task-explicit confirmed combination, user level,
  user general, package level, package general, then host-selection
  pass-through only for a `primary` absent from both sources
- Actual-responsibility matrix: L0 primary plus separately triggered temporary
  R; L1/L2 primary plus optional R; L3 P/E/R; L4 O/P/E/R
- L0 activation: remains no active Charter
- Existing tasks/roles and role enablement: unchanged by configuration
- Package tree:
  `12fe4c65683a82d9d60295160681247b812efa0b` and package SHA-256
  `b73cf79466e8289fcb2d6eb441db91ce13def0cb2092e58bcbdfef14de08a50a`
- Candidate descriptor: [`../../../release/v0.6.0-candidate.json`](../../../release/v0.6.0-candidate.json)
- Current-input SOURCE, repository, staged adversarial, and lifecycle checks:
  see [Verification](VERIFICATION.md)
- Host/global task-start consumer integration: `NOT_PERFORMED`
- Commit/native commit gate, local release readiness, installation, and
  publication: not established or authorized by this source acceptance
- Runtime delivery, loaded-copy behavior, and broad efficacy: `UNKNOWN`
- Package version: v0.6.0; YAML schema version: 1 with optional field extensions

The candidate remains its original `PENDING_INDEPENDENT_REVIEW` snapshot,
including pending evidence fields. The later source acceptance above does not
rewrite that snapshot or require a committed-source receipt. No v0.6.0 commit
is claimed. Historical C5/C6, R1-R12, prior permission refusals, failed checks,
findings, and consumed authority remain part of the same work history.

The subsequent acceptance-record checkpoint also passed Planner verification.
Its 11-file delta comprised nine existing documents and mechanical provenance/
checker pins, with staged-diff SHA-256
`b1d5f69d15cff09c06c2e178718f1ded2b57ec7b22b38c5cd72749c1c35724c7`.
At that closeout, all six package files, candidate, historical release objects,
installer, and SOURCE checker stayed byte-identical to the source checkpoint.
Its own checks and acceptance remain distinct from later v0.6.1 work.

This development source does not rewrite or inherit the accepted v0.5.0 source
identity, review, or Planner acceptance below.

## Immutable accepted v0.5.0 source

- Version: `v0.5.0`
- Candidate descriptor: [`../../../release/v0.5.0-candidate.json`](../../../release/v0.5.0-candidate.json)
- Descriptor state: immutable `PENDING_INDEPENDENT_REVIEW` pre-review snapshot
- Accepted source commit: `8bf9f130598fbf1b9170dd0c082e3e8fb78d6c0d`
- Source acceptance receipt:
  [`../../../release/v0.5.0-local-release-receipt.json`](../../../release/v0.5.0-local-release-receipt.json)
- Package lineage: accepted v0.4.1 C4 source
  `59b4d91f46c2ac797c71c900e62dda87cf0cca60`
- Deterministic SOURCE, repository, adversarial, and lifecycle evidence:
  `VERIFIED` for the exact receipt-bound source checkpoint
- Independent technical review: ten completed rounds; R9 P2
  `WC-ROLE-CONFIG-R9-F01` fixed and closed by R10 with no new findings
- Planner source and committed-source acceptance: `ACCEPTED`
- Local source readiness: `VERIFIED`
- v0.5.0 installation and publication: `NOT_PERFORMED` and `NOT_AUTHORIZED`
- Actual v0.4.0 installed copy: remains managed v0.4.0 after the separately
  accepted ACL-only access repair; v0.4.1 and v0.5.0 were not installed
- `WC-INSTALL-POSTFLIGHT-F01`: closed only for that exact access repair
- Runtime role delivery, cross-provider execution, stable loaded-copy behavior,
  natural adherence, cross-Harness behavior, public release, and broad
  efficacy: `UNKNOWN` or separately authorized

The v0.5.0 candidate preserves the accepted v0.4.1 L0-L4 Reviewer, verification, acceptance,
evidence-first `UNKNOWN`, context recovery, callback, and graph boundaries. It
adds a strict role-model source hierarchy, whole-role replacement semantics,
closed schema and capability validation, visible native mapping, and a package
default for Orchestrator/Planner/Executor/Reviewer. Configuration never grants
role or action authority and never mutates existing roles. On Windows, the
lifecycle controller additionally supports exact allow-listed five-file and
six-file package transitions by projecting changed path membership on a private
replica while preserving every common descriptor. Unsupported path sets,
control states, inheritance results, or readback fail before any target move.

## Historical v0.4.0 candidate and failed installation

- Immutable candidate: [`../../../release/v0.4.0-candidate.json`](../../../release/v0.4.0-candidate.json)
- Accepted candidate commit: `30057490be21d869751854a51e9fafdfb535f206`
- Local-release receipt: [`../../../release/v0.4.0-local-release-receipt.json`](../../../release/v0.4.0-local-release-receipt.json)
- Receipt-bound independent review: five results through R5; two historical
  source findings closed and R5 P2 fixed pending R6 at that checkpoint
- Later R6 result and Planner source acceptance: `NO_FINDINGS` / `ACCEPTED`
- Accepted correction commit: `df674c773de6f915627af541f0eb37221da9adef`
- v0.3.0-to-v0.4.0 written bytes and elevated receipt/file postflight:
  `VERIFIED`
- Default sandbox reader access after original promotion: `FAILED`
- First authorized ACL-only repair: stopped before target mutation because
  `/restore` changed `D:P` to `D:PAI` and `D:` to `D:AI`
- Accepted v0.4.1 C4 source correction:
  `59b4d91f46c2ac797c71c900e62dda87cf0cca60`
- Later exact ACL-only repair: `ACCEPTED`; the managed v0.4.0 copy became
  default-readable and `WC-INSTALL-POSTFLIGHT-F01` closed for that repair
- Installed package version after repair: `v0.4.0`

The later control-state counterevidence does not erase R6 or its acceptance; it
invalidated the prior mechanism for the first repair attempt. The accepted C4
mechanism and later bounded repair preserved package bytes and version while
changing only the exact target's ACL. That evidence does not install v0.4.1 or
authorize another lifecycle action.

## Historical v0.3.0 release

- Version: `v0.3.0`
- Public identity: `junwei529/work-charter`
- Candidate descriptor: [`../../../release/v0.3.0-candidate.json`](../../../release/v0.3.0-candidate.json)
- Candidate state: `LOCAL_RELEASE_READY=VERIFIED`
- Accepted candidate C: `732e7efa6211d9aedeb133282ef28ce03f9bdfef`
- Acceptance receipt: [`../../../release/v0.3.0-local-release-receipt.json`](../../../release/v0.3.0-local-release-receipt.json)
- Release-note body: human review approved; immutable P's
  [`../../../CHANGELOG.md`](../../../CHANGELOG.md) carrier retains its pre-effect
  `PENDING` snapshot
- Public repository: `https://github.com/junwei529/work-charter`
- Public-source candidate: [`../../../release/v0.3.0-public-release-candidate.json`](../../../release/v0.3.0-public-release-candidate.json)
- Immutable public commit P: `b655c1aa42acc8c68b70e87c4c228445c5182d8b`
- Annotated tag: `v0.3.0`, fixed at P
- Public release state: `VERIFIED`
- Post-release evidence subject: [`../../../release/v0.3.0-public-release-evidence.json`](../../../release/v0.3.0-public-release-evidence.json), accepted as `B2-WC-PUBLIC-EVIDENCE-F-01` for exact F `4ba904808fe86e270ebd405db1866d41d1cc032e`

The immutable candidate identity is the clean commit containing the descriptor.
The descriptor deliberately does not contain its own commit hash and retains
its original pending snapshot. The separate receipt binds exact C, its tree,
the unchanged package tree, and the independent Planner acceptance without
rewriting that candidate.

## Repository ownership

This repository owns its Git history, documentation, checks, and future version,
evaluation, installation, and release decisions. It has no implicit dependency
on another Skill repository and begins with no configured remote.

## Evidence state

The migration proves historical source identities for mapped files. The current
manifest proves current target hashes, local link and publication-safety
constraints, and provenance classification. The v0.5.0 receipt-bound
deterministic qualification proves only that exact historical instruction text
and four-role default. The current checker separately reports the development
source's static selection/activation, authority, coordination/recovery,
review/acceptance, level-role resolution, Standard O/P/E/R, and unchanged
default-data clauses, and requires exact current-package binding to v0.6.2.
Neither result proves model adherence, host/global
consumer integration, runtime delivery, technical correctness, or acceptance
for the development source. R12 and Planner acceptance apply to the v0.6.0
checkpoint recorded above; R14/R16 and later Planner checks qualify the
accepted v0.6.1 source. R17 and Planner acceptance apply to the v0.6.2 frozen
source checkpoint above; later effects retain their separate gates.
The retained cases remain contract fixtures; they
do not create fresh model, efficacy, release, or installed-copy evidence.

Evidence states remain separate:

- Current v0.6.2 SOURCE identity: provenance-bound working bytes and a matching
  candidate descriptor. Input-bound deterministic results are recorded in
  [Verification](VERIFICATION.md). The earlier v0.6.1 R13 state-record finding was
  fixed and accepted after R14 before the prior source commit. The later
  installer correction has the separate accepted checkpoint above; its record
  synchronization is not an outstanding R13 source review.
- Historical v0.6.0 source and acceptance records: accepted at the checkpoints
  above. Its immutable descriptor retains the pre-review pending snapshot;
  that snapshot does not reopen the accepted history or qualify v0.6.2.
- Immutable v0.5.0 SOURCE identity and deterministic contract: `VERIFIED` for
  accepted commit `8bf9f130598fbf1b9170dd0c082e3e8fb78d6c0d`.
- Immutable v0.5.0 independent review and Planner acceptance: `VERIFIED` by the
  separate source receipt; the candidate descriptor retains its immutable
  pending snapshot.
- Immutable v0.5.0 local source readiness: `VERIFIED`.
- v0.5.0 installation and publication: `NOT_PERFORMED` and
  `NOT_AUTHORIZED`.
- v0.5.0 role-delivery runtime and cross-provider execution: `UNKNOWN`.
- Historical v0.4.0 source-candidate acceptance: `VERIFIED` for the immutable
  candidate and reviewed installer baseline; later control-state evidence and
  the accepted C4 correction remain separate from that history.
- Historical v0.4.0 original attempt: exact content and elevated receipt/five-
  file postflight are `VERIFIED`, while default-reader access was `FAILED`.
- Historical v0.4.0 exact ACL-only repair: `ACCEPTED`; the managed v0.4.0 copy
  became default-readable and the exact access finding was closed. This did not
  install v0.4.1 or authorize v0.5.0 effects.
- Historical v0.3.0 `LOCAL_RELEASE_READY`: `VERIFIED` by the exact-C acceptance
  receipt.
- Historical v0.3.0 `PUBLIC_RELEASE`: `VERIFIED` for exact P, annotated tag,
  and public Release.
- Historical v0.3.0 same-version install/update/rollback/uninstall/restoration:
  `VERIFIED`.
- Historical v0.3.0 `STABLE_INSTALLED_COPY`: `VERIFIED` for the evidenced Codex
  user installation at that checkpoint.
- Historical v0.3.0 installed-copy behavior: `VERIFIED` for the retained witnesses
  plus `B2-WC-SOLE-LOAD-02`, which observed exactly one catalog-visible managed
  `work-charter`.
- Retained predecessor bytes: preserved outside every Skill discovery root; the
  exact recovery locator is controller-side only.
- Broad product efficacy and untested selection/loading/negative contexts: `UNKNOWN`.

The immutable public-source candidate preserves its pre-effect snapshot. The
separate post-release evidence subject binds the later public and corrected
installed-copy facts without rewriting P. The attempted v0.3.0-to-v0.4.0
update verifies its written content and elevated postflight; its original
access failure and the later accepted ACL-only repair remain separately
attributed. Other cross-version transitions, cross-Harness behavior, untested
contexts, and broad efficacy remain `UNKNOWN`.

Lifecycle receipt validation is bounded to integrity and routing checks. It
refuses unreceipted, malformed or mismatched-receipt, wrong-tree, modified,
aliased, and drifted destinations, but does not prove cryptographic ownership
against a same-privilege local actor able to forge the complete receipt.
Repository-side lifecycle mutations now use a validated external, same-volume
task transaction root outside all declared Skill discovery roots. Planned
product operations supply it explicitly; legacy apply calls retain their prior
shape through a visibly marked `AUTO_COMPATIBILITY` root with the same guards.
The disposable self-test covers all four legacy apply forms, explicit-path
install/update/rollback/uninstall, pre-mutation path and volume refusal,
preservation when the initial backup move fails, and verified restoration after
a later replacement failure. The historical v0.4.1 Windows-specific correction
protects every random per-operation transaction directory for Owner Rights,
SYSTEM, and Administrators. New installs inherit the destination-parent DACL;
update/rollback/uninstall save the complete prior DACL tree and prove restore
capability on a private replica before mutation. AI-bearing records use a
single-record `/restore`; no-AI records use `SetFileSecurityW` without a child
propagation transition. Records are applied shallow-to-deep. The replica and
every promoted or recovered target are read back with the same bounded `/save`
representation; record order and newline form are ignored, while path
membership and exact DACL SDDL—including P, AI, AR and ACE order/content—must
match. A preflight mismatch produces zero target moves. A later mismatch enters
existing recovery and retains the original protected snapshot when recovery is
incomplete. Moved backup/tombstone trees inherit the private transaction DACL;
other platforms retain prior behavior. Historical five-file receipts and the
legacy candidate descriptor and the current six-file descriptor are two exact
allow-listed shapes. The legacy candidate may omit its redundant package
digest only while its actual tree matches a separate trusted tree; the current
shape requires the digest, and any supplied invalid or mismatched digest is
rejected. A changed-shape Windows update/rollback projects policy on a private
replica, preserves every
common descriptor, requires new paths to be auto-inherited and unprotected,
and exact-restores/readbacks the projected snapshot while retaining the
original for recovery. Unknown/self-declared sets, unsafe receipt paths,
missing/extra files, or identity mismatches fail closed. Lifecycle self-test
also proves that a disposable external user configuration remains byte-identical.
This correction creates a new six-file v0.5.0 source while leaving immutable
v0.4.1/v0.4.0/v0.3.0 objects unchanged. Exact qualification, ten completed
review rounds, and Planner acceptance are bound by the separate v0.5.0 receipt.

## Next gate

The accepted v0.6.2 source is committed and its exact managed user installation
is independently accepted. The remaining closeout work is minimal installation
record synchronization, final-input checks, an ordinary records commit, and
normal fast-forward publication to the intended repository's main branch.
Publication requires the actual Git authentication actor, exact target, write
capability, live ref/local ancestry, and outgoing-content checks. It has not
been performed. A material change or an operation-local permission requirement
still stops its dependent action. Package, installer and immutable candidate
bytes remain unchanged; installation qualification is not rerun for these
record-only changes.

Historical v0.6.0 acceptance and pending descriptor snapshots remain separate
from this current workflow. Host/global consumer migration, fresh role-delivery,
loaded-copy behavior, natural adherence, tags, Releases, other cross-version
transitions, cross-provider execution, and broader efficacy remain separate
gates. The exact historical v0.3.0
post-release evidence subject F remains accepted under
`B2-WC-PUBLIC-EVIDENCE-F-01` without moving its tag or rewriting P.

## Recovery entry

Read the root [`AGENTS.md`](../../../AGENTS.md),
[`PROVENANCE.md`](../../../PROVENANCE.md), [Design](DESIGN.md), this State, and
[Verification](VERIFICATION.md). Verify Git status, current branch, package
identity, and writer ownership before changing files.
