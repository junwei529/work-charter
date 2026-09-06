# Work Charter Design

## Product boundary

Bounds consequential Codex work by outcome, authority, evidence, recovery,
independent review, and proportional coordination. The canonical installable source is
[`skills/work-charter/`](../../../skills/work-charter/). Package instructions, references,
assets, and metadata originated from `80910a8b2375a11be897e9660c4b00a06d00dd13`.
The source map preserves exact historical origin while classifying changed
`v0.5.0` files as repository-native rather than exact migration blobs.

The repository owns one Skill product. Cross-Skill composition is optional and
cannot grant authority or create a hard dependency.

## Package contract

The package contains exactly 6 files. `SKILL.md` owns selection, entry, and the
portable verification/review/acceptance split; directly linked references and
assets own detailed coordination, recovery, Standard O/P/E/R, and template
guidance. The repository checker fails if any package byte or expected path
differs from its current recorded mapping.

`assets/role-models.default.yaml` is the sole default-data owner for role model
selection. An authorized dispatcher resolves a frozen delivery combination,
an explicitly selected file, the default user file, or the package default in
that order; validates a closed schema and native route support; then displays
the final role/provider/model/parameters and source before delivery. A partial
user file replaces each supplied role as a whole and never inherits omitted
parameters. Configuration is data and cannot authorize role creation or any
action. It does not create a parser dependency, watcher, service, provider
gateway, credential store, or automatic change to an existing role.

`L0` remains no active Charter even when an external review gate applies.
`L1` and `L2` retain one primary owner and may add one bounded read-only
Reviewer. `L3` separates Planner target acceptance, Executor implementation and
verification, and Reviewer technical inspection. `L4` adds Orchestrator project
direction and phase acceptance without duplicating technical review.

Review is bound to an actual stable checkpoint, baseline, necessary semantic
context, tests, documentation consumers, material untracked inputs, and stated
graph/generated-artifact limits. Repair normally returns to the same reliable
Reviewer, with cumulative findings preserved. One checkpoint has at most one
current Notice per route; terminal returns require no acknowledgement. Context
switches preserve contract, authority, role/writer, finding, stop, and evidence
history unless a material identity changes.

Authorization remains bound to its action, subject, actor class, effect, and
risk rather than to a carrier task. A still-valid authorization may therefore
be reused, but an environment-mandated direct operation permission is owned by
the action task that will perform it and cannot be satisfied by an upstream
relay or status report. This operation-local gate does not transfer Phase or
project contract ownership. Read-only Reviewers and evidence collectors do not
solicit write authority.

The current `v0.5.0` candidate adds role-model configuration to the accepted
v0.4.1 source. Its descriptor is a new pending pre-review snapshot, not a
receipt. The immutable v0.4.0 candidate and receipt remain the historical
owners of the accepted candidate, reviewed lifecycle-controller baseline, five
recorded independent-review results, Planner source/tool acceptances, external
trust identity, and failed update attempt. R6 later returned `NO_FINDINGS`, the
Planner accepted that source correction, and commit
`df674c773de6f915627af541f0eb37221da9adef` recorded it. An authorized repair
preflight then proved that whole-tree `icacls /restore` changed automatic-
inheritance control state while preserving paths and ACE text, and stopped
before target mutation. The v0.4.1 C4 source corrected that mechanism and was
independently accepted at `59b4d91f46c2ac797c71c900e62dda87cf0cca60`.
A later ACL-only repair restored default-reader access to the exact managed
v0.4.0 copy and closed that exact access finding without installing v0.4.1.
The v0.5.0 candidate creates no installation, publication, runtime-delivery,
or stable-behavior claim. Historical release metadata and evidence remain
immutable for their versions.

Historical v0.3.0 candidate C remains immutable. Its separate local-release
receipt binds the exact commit, candidate tree, package tree, and independent
Planner acceptance without recording the receipt commit inside itself. The
v0.4.0 candidate and receipt use the same non-circular structure: the receipt
binds the already immutable candidate and later evidence, while neither object
attempts to predict the receipt's eventual commit.

The public release uses the same non-circular pattern. A distinct immutable
public-source candidate commit P carries final repository content and the
human-reviewable release notes without embedding P's commit hash. Later public
ref and release evidence may bind exact P while the annotated `v0.3.0` tag stays
fixed at P.

## Evaluation surface

- `evals/cases/cold-resume.md`
- `evals/cases/small-task-stays-flat.md`
- `evals/cases/work-charter-entry.md`
- `evals/cases/work-charter-midstream.md`
- `evals/cases/work-charter-planner-executor.md`
- `evals/cases/work-charter-recovery-integrity.md`
- `evals/cases/work-charter-role-model-configuration.md`
- `evals/cases/work-charter-selection.md`
- `evals/cases/work-charter-standard.md`

Unchanged cases and fixtures retain exact source-blob provenance; files revised
for `v0.5.0` are repository-native and individually hashed. Together they define
deterministic inputs and expected boundaries. The accepted candidate and the
attempted update have separate review, acceptance, postflight, and access
evidence; exact installed bytes do not override a failed default-reader check.
Model adherence, stable loaded-copy behavior, publication, and broad efficacy
remain separately authorized evidence classes.

## Standalone constraints

- No other Skill package is included.
- Verification uses only repository-local files and standard host tools.
- Source provenance is explicit in [`../../../provenance/source-map.json`](../../../provenance/source-map.json).
- Historical monorepo state is not a runtime dependency or acceptance condition.
- Install lifecycle operations use an explicit immutable source checkout and a
  receipt. Planned product mutations use an existing absolute external
  transaction root on the destination volume and outside the destination,
  source, and every declared Skill discovery root. Legacy apply calls without
  that argument remain compatible through a visibly reported, unique automatic
  root that satisfies the same path and volume guards and is removed after a
  clean result; it is not the accepted route for a planned install or release.
  Per-operation stage, backup, tombstone, and recovery material remains under
  the validated root; missing, aliased, link-like, overlapping, or cross-volume
  explicit routes fail before destination mutation. The
  tool refuses unreceipted, malformed or mismatched-receipt, wrong-tree,
  modified, aliased, and drifted destinations. A failed initial backup move
  never deletes the old destination; failures after that move restore and
  verify the old managed copy or retain an explicit recovery path. On Windows,
  each random per-operation transaction directory is first protected for Owner
  Rights, SYSTEM, and Administrators. A genuinely new install inherits the
  destination parent's existing DACL. Before update, rollback, or uninstall
  mutation, the controller saves the complete existing DACL tree inside the
  private transaction and restores it path by path to a private replica.
  AI-bearing snapshot records use a one-record `icacls /restore`; records
  without AI use `SetFileSecurityW` with DACL and, when required, protected-DACL
  information. The latter setter is used for its documented non-propagating
  directory behavior. Records are applied shallow-to-deep and then read back
  through the same bounded `/save` representation. Enumeration order and
  newline serialization are ignored; managed-path membership and exact
  per-path DACL SDDL—including P, AI, AR and ACE order/content—must match.
  Missing capability, an unsupported control state, or any mismatch therefore
  fails before a target move. The promoted or recovered target receives the
  saved policy and passes the same readback before success is reported; moved
  backup and tombstone trees inherit the protected transaction DACL. A later
  mismatch enters the same recovery path, which retains the original snapshot
  when recovery is incomplete. Other platforms retain the existing platform-
  default permission behavior. Historical five-file receipts and the current
  six-file descriptor map only to two exact allow-listed path sets. The legacy
  five-file candidate shape may omit its redundant package digest while its
  actual tree remains bound to a separate trusted tree. The six-file shape
  requires the digest; any explicitly supplied invalid or mismatched digest is
  rejected. When a Windows update or rollback changes between them, the
  controller restores the
  original snapshot to a private replica, transforms only that replica to the
  target shape, resets only new paths to inherited ACLs, proves every common
  descriptor is unchanged and every new path is auto-inherited and unprotected,
  then exact-restores and reads back the projected snapshot. The original
  snapshot remains the recovery authority. The receipt
  provides integrity and routing evidence, not cryptographic ownership proof
  against a same-privilege local actor capable of forging the complete receipt.
- SOURCE contract qualification checks instruction and exact default-data
  coverage only. Model adherence, actual role delivery, live installed-copy
  behavior, publication, and broad efficacy
  require separate evidence. Receipt validation is static and does not re-read
  the live installation.

## Cross-version trust distribution

The lifecycle CLI carries the accepted v0.3.0 package tree as a built-in trust anchor. Future update and rollback operations remain executable without trusting the candidate descriptor itself: the operator supplies the target package-tree identity from a separately reviewed, candidate-external trust record through `--trusted-target-package-tree`; `--trusted-current-package-tree` supplies an independently retained current identity when it is not built into the selected tool. Deriving either value from the candidate source would collapse the trust boundary and is not an accepted route. The recorded v0.3.0-to-v0.4.0 attempt used that external route and verified written content, but its default-reader access regression left the overall transition unaccepted. A later separately accepted ACL-only repair restored the exact managed v0.4.0 copy's default-reader access without accepting that installation transition. These observations do not verify other cross-version transitions.
