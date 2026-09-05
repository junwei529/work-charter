# Work Charter Design

## Product boundary

Bounds consequential Codex work by outcome, authority, evidence, recovery,
independent review, and proportional coordination. The canonical installable source is
[`skills/work-charter/`](../../../skills/work-charter/). Package instructions, references,
assets, and metadata originated from `80910a8b2375a11be897e9660c4b00a06d00dd13`.
The source map preserves exact historical origin while classifying changed
`v0.4.0` files as repository-native rather than exact migration blobs.

The repository owns one Skill product. Cross-Skill composition is optional and
cannot grant authority or create a hard dependency.

## Package contract

The package contains exactly 5 files. `SKILL.md` owns selection, entry, and the
portable verification/review/acceptance split; directly linked references and
assets own detailed coordination, recovery, Standard O/P/E/R, and template
guidance. The repository checker fails if any package byte or expected path
differs from its current recorded mapping.

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

The current `v0.4.0` candidate changes the package semantics and selected
evaluation/documentation surfaces. Its descriptor remains the immutable
pre-review snapshot. A separate receipt binds the accepted candidate, reviewed
lifecycle-controller baseline, cumulative independent-review dispositions,
Planner source/tool acceptances, external trust identity, and the later update
attempt and five completed independent review results. That attempt wrote exact
bytes and passed elevated content postflight,
but its final directory retained the private transaction ACL and failed
default-reader access. Overall installation and local-release readiness are
therefore blocked. R4 returned `NO_FINDINGS`, but Planner acceptance opened P2
`WC-INSTALL-ACCESS-P01`: recursive parent reset did not preserve an existing
explicit or protected DACL. R5 then opened P2
`WC-INSTALL-ACCESS-R5-F01`: process-level restore success was not followed by a
target DACL readback. The readback correction is implemented pending R6 and
Planner acceptance under P01. Publication and stable behavior remain separate
evidence or authority gates. Historical `v0.3.0` release metadata and lifecycle
evidence remain immutable evidence for that version only.

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
- `evals/cases/work-charter-selection.md`
- `evals/cases/work-charter-standard.md`

Unchanged cases and fixtures retain exact source-blob provenance; files revised
for `v0.4.0` are repository-native and individually hashed. Together they define
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
  private transaction, restores that snapshot to a private replica, and reads
  the replica back before destination mutation. Enumeration order and newline
  serialization are ignored; managed-path membership and exact per-path DACL
  SDDL—including inheritance/protection flags and ACE order/content—must match.
  Missing restore/readback capability or a mismatch therefore fails before any
  target move. The promoted or recovered target receives the saved policy and
  passes the same readback before success is reported; moved backup and
  tombstone trees inherit the protected transaction DACL. A later mismatch
  enters the same recovery path, which retains the original snapshot when
  recovery is incomplete. Other platforms retain the existing platform-default
  permission behavior. The receipt
  provides integrity and routing evidence, not cryptographic ownership proof
  against a same-privilege local actor capable of forging the complete receipt.
- SOURCE contract qualification checks instruction coverage only. Model
  adherence, live installed-copy behavior, publication, and broad efficacy
  require separate evidence. Receipt validation is static and does not re-read
  the live installation.

## Cross-version trust distribution

The lifecycle CLI carries the accepted v0.3.0 package tree as a built-in trust anchor. Future update and rollback operations remain executable without trusting the candidate descriptor itself: the operator supplies the target package-tree identity from a separately reviewed, candidate-external trust record through `--trusted-target-package-tree`; `--trusted-current-package-tree` supplies an independently retained current identity when it is not built into the selected tool. Deriving either value from the candidate source would collapse the trust boundary and is not an accepted route. The recorded v0.3.0-to-v0.4.0 attempt used that external route and verified written content, but its default-reader access regression leaves the overall transition unaccepted. This observation does not verify other cross-version transitions.
