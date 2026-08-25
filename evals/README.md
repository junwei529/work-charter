# Work Charter Evaluations

These retained cases and fixtures are exact Git blobs from source commit
`80910a8b2375a11be897e9660c4b00a06d00dd13`. They define the repository-local evaluation surface without
importing another Skill or the former monorepo evaluation envelope.

## Cases

- [`cold-resume.md`](cases/cold-resume.md)
- [`small-task-stays-flat.md`](cases/small-task-stays-flat.md)
- [`work-charter-entry.md`](cases/work-charter-entry.md)
- [`work-charter-midstream.md`](cases/work-charter-midstream.md)
- [`work-charter-planner-executor.md`](cases/work-charter-planner-executor.md)
- [`work-charter-recovery-integrity.md`](cases/work-charter-recovery-integrity.md)
- [`work-charter-selection.md`](cases/work-charter-selection.md)
- [`work-charter-standard.md`](cases/work-charter-standard.md)

## Fixtures

- [`cold-resume`](fixtures/cold-resume/)
- [`small-task-stays-flat`](fixtures/small-task-stays-flat/)
- [`work-charter-entry`](fixtures/work-charter-entry/)
- [`work-charter-loop`](fixtures/work-charter-loop/)
- [`work-charter-recovery-integrity`](fixtures/work-charter-recovery-integrity/)
- [`work-charter-standard`](fixtures/work-charter-standard/)

## Deterministic verification

Run `python -B scripts/check_repository.py --json` from the repository root.
Case execution that invokes a model, installs a Skill, or uses an external
provider remains a separately authorized evidence action.
