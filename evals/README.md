# Work Charter Evaluations

These cases and fixtures originated from source commit
`80910a8b2375a11be897e9660c4b00a06d00dd13`. Files revised for `v0.4.0` are
repository-native and hash-bound in the source map; unchanged fixtures remain
exact Git blobs. They define the repository-local evaluation surface without
importing another Skill or the former monorepo evaluation envelope.

## Cases

- [`cold-resume.md`](cases/cold-resume.md)
- [`small-task-stays-flat.md`](cases/small-task-stays-flat.md)
- [`work-charter-entry.md`](cases/work-charter-entry.md)
- [`work-charter-midstream.md`](cases/work-charter-midstream.md)
- [`work-charter-planner-executor.md`](cases/work-charter-planner-executor.md)
- [`work-charter-recovery-integrity.md`](cases/work-charter-recovery-integrity.md)
- [`work-charter-role-model-configuration.md`](cases/work-charter-role-model-configuration.md)
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
Run `python -B scripts/check_source_contract.py --json` for static SOURCE clause
coverage and the required current-package candidate binding. The static result
validates the package source against the material
selection/activation, authority, recovery, independent-review/acceptance,
same-Reviewer re-review, callback deduplication, graph limits, context-switch,
level-by-actual-role model resolution, and Standard O/P/E/R boundaries in this
evaluation surface; it also binds the exact general compatibility fallbacks, approved level
defaults, contract/role/task/model-delta prompt clauses, scoped startup
authorization, complete expression, and required reference reachability.
Current candidate identity is v0.6.2; the v0.6.0 and v0.6.1 descriptors remain
fixed historical snapshots. The new guardrail/cost prose is inspected in
independent source review; phrase matching is not evidence of its behavioral
effectiveness. The checker does not execute a model, create a task or role, read a live user
configuration, exercise a host/global consumer, or claim adherence. Static
clause success does not make an unbound package a qualified candidate; without
a matching descriptor the overall command must fail.
Case execution that invokes a model, installs a Skill, or uses an external
provider remains a separately authorized evidence action.

Accepted Q06 is bounded fresh exact-SOURCE forward-behavior evidence from a
projectless, read-only, no-tool `gpt-5.6-sol/high` run. It does not establish
installed-copy behavior, publication, stable installation, cross-Harness
behavior, or broad efficacy.

Lifecycle receipt checks cover unreceipted, malformed or mismatched-receipt,
wrong-tree, modified, aliased, and drifted destinations. They do not establish
cryptographic ownership against a same-privilege local receipt forger.
