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
evaluation/documentation surfaces. Its deterministic SOURCE qualification,
independent technical review, Planner acceptance, installation, and publication
are separate evidence or authority gates. Historical `v0.3.0` release metadata
and lifecycle evidence remain immutable evidence for that version only.

Historical v0.3.0 candidate C remains immutable. A separate local-release receipt binds its exact
commit, candidate tree, package tree, and independent Planner acceptance without
recording the receipt commit inside itself.

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
deterministic inputs and expected boundaries; model runs, independent review,
acceptance, installation, and release remain separately authorized evidence
classes.

## Standalone constraints

- No other Skill package is included.
- Verification uses only repository-local files and standard host tools.
- Source provenance is explicit in [`../../../provenance/source-map.json`](../../../provenance/source-map.json).
- Historical monorepo state is not a runtime dependency or acceptance condition.
- Install lifecycle operations use an explicit immutable source checkout and a
  receipt. The tool refuses unreceipted, malformed or mismatched-receipt,
  wrong-tree, modified, aliased, and drifted destinations. The receipt provides
  integrity and routing evidence, not cryptographic ownership proof against a
  same-privilege local actor capable of forging the complete receipt.
- SOURCE contract qualification checks instruction coverage only. Model
  adherence, installed-copy behavior, publication, and broad efficacy require
  separate evidence.

## Cross-version trust distribution

The lifecycle CLI carries the accepted v0.3.0 package tree as a built-in trust anchor. Future update and rollback operations remain executable without trusting the candidate descriptor itself: the operator supplies the target package-tree identity from separately reviewed immutable release notes through `--trusted-target-package-tree`; `--trusted-current-package-tree` supplies an independently retained current identity when it is not built into the selected tool. Deriving either value from the candidate source would collapse the trust boundary and is not an accepted route.
