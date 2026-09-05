# Event Tally Project

## Direction

Provide deterministic event summaries before adding any command-line surface.

## Approved Standing Policy

Policy revision 2 applies only to Event Tally implementation phases declared
in this file. Its bounded recovery read scope is this file, `STATUS.md`,
`EVIDENCE.md`, the current phase workspace/branch/worktree/dirty state, and the
observable writer.

For an explicitly authorized phase, use Standard O/P/E/R with Orchestrator
direction and transition ownership, Planner Charter/review-routing/acceptance
ownership, Executor implementation and verification ownership, independent
read-only Reviewer ownership, one active lane, and one writer. The user
approved this standing policy before the scenario. Reuse must remain visible
and does not authorize role delivery, writes, Git, installation, or external
effects.

## Phase One Charter

- Contract state: `approved`
- Run disposition: `active`
- Outcome: implement `count_by_kind(records)` as a new mapping of event kind to
  occurrence count.
- Boundaries: reject a record without a non-empty string `kind`; do not mutate
  records; add no dependencies or command-line behavior.
- Authorized actions: implementation, focused tests, and existing
  status/evidence maintenance after explicit user authorization.
- Acceptance: Executor-focused tests cover repeated kinds, empty input,
  invalid kind, and input preservation; an independent Reviewer inspects the
  stable checkpoint and reports findings/coverage; the Planner accepts only
  after review convergence.
- Stop: contract, permission, writer, workspace, or evidence ambiguity.

## Phase Two

Add a command-line interface. This phase is unapproved and must not start.
