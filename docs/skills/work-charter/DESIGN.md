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
