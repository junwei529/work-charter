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
Run `python -B scripts/check_source_contract.py --json` for candidate SOURCE
clause coverage. The latter validates the package source against the material
selection/activation, authority, recovery, and Standard O/P/E boundaries in
this evaluation surface; it does not execute a model or claim adherence.
Case execution that invokes a model, installs a Skill, or uses an external
provider remains a separately authorized evidence action.

Accepted Q06 is bounded fresh exact-SOURCE forward-behavior evidence from a
projectless, read-only, no-tool `gpt-5.6-sol/high` run. It does not establish
installed-copy behavior, publication, stable installation, cross-Harness
behavior, or broad efficacy.

Lifecycle receipt checks cover unreceipted, malformed or mismatched-receipt,
wrong-tree, modified, aliased, and drifted destinations. They do not establish
cryptographic ownership against a same-privilege local receipt forger.
