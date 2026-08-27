# Work Charter Design

## Product boundary

Bounds consequential Codex work by outcome, authority, evidence, recovery, and proportional coordination. The canonical installable source is
[`skills/work-charter/`](../../../skills/work-charter/). Package instructions, references,
assets, and metadata preserve the exact source blobs from `80910a8b2375a11be897e9660c4b00a06d00dd13`.

The repository owns one Skill product. Cross-Skill composition is optional and
cannot grant authority or create a hard dependency.

## Package contract

The package contains exactly 5 files. `SKILL.md` owns
selection and entry behavior; directly linked references and assets own detailed
guidance and templates. The repository checker fails if any package byte or
expected path differs from the recorded baseline mapping.

The independent `v0.3.0` candidate does not change those package bytes. Release
metadata, deterministic SOURCE qualification, and lifecycle tooling are
repository-owned surfaces outside the installable package.

Candidate C remains immutable. A separate local-release receipt binds its exact
commit, candidate tree, package tree, and independent Planner acceptance without
recording the receipt commit inside itself.

## Evaluation surface

- `evals/cases/cold-resume.md`
- `evals/cases/small-task-stays-flat.md`
- `evals/cases/work-charter-entry.md`
- `evals/cases/work-charter-midstream.md`
- `evals/cases/work-charter-planner-executor.md`
- `evals/cases/work-charter-recovery-integrity.md`
- `evals/cases/work-charter-selection.md`
- `evals/cases/work-charter-standard.md`

Cases and fixtures are exact source blobs. They define deterministic inputs and
expected boundaries; model runs, installation, and release remain separately
authorized evidence classes.

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
