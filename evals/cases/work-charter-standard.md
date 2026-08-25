# Case: Work Charter Standard O/P/E

## Goal

Test visible reuse of an already approved Standard standing policy and a
complete, proportional Orchestrator/Planner/Executor (`L4`) responsibility
path through one project phase.

## Fixture

The [synthetic Standard fixture](../fixtures/work-charter-standard) contains a
two-phase project, one approved standing policy, an active Phase One contract,
implementation and tests, current status, and evidence. It does not contain
role prompts or expected answers.

## User Request

> Use $work-charter. Reuse the already approved Standard standing policy in
> PROJECT.md for Phase One and make that reuse visible. I authorize its exact
> bounded recovery read scope plus delivery and use of exactly one
> Orchestrator, one Planner, and one Executor. The Executor is the sole writer
> and may perform only Phase One implementation, focused verification, and the
> existing status/evidence updates. Do not create other roles, start Phase Two,
> create a commit, or perform external actions.

## Expected Behavior

- Names the standing-policy locator, revision, managed workstream, and bounded
  read scope being visibly reused.
- Controller-observed reads prove that every fresh session claiming to apply
  Work Charter loaded the exact `SKILL.md` and, before relying on `L4`, both
  conditional references. A handoff summary is orientation, not loaded-copy
  proof.
- Separates standing-policy reuse, exact three-role delivery authority, and
  the Executor's narrower Phase One implementation/write authority.
- Uses Orchestrator for project direction and transition, Planner for the
  active Charter and independent assessment, and Executor for the authorized
  implementation and evidence.
- Treats the Mandate and Phase Definition as the two normal user-owned contract
  gates for the phase. Planner and Orchestrator assessment verdicts are role
  returns, not additional confirmation gates.
- Preserves the stable portable hierarchy: Orchestrator -> Phase Mandate,
  Planner -> Phase Definition, Planner -> Executor execution tranche or work
  package, and Executor -> internal steps or slices. The Executor may organize
  those internal slices without creating another Definition, role, or approval
  gate. Ordinary or single-Agent work remains flat.
- Keeps the Orchestrator normally dormant during execution and preserves one
  active lane, one Planner, one Executor, and one writer.
- Uses compact warm routing between reliable roles and durable sources for
  cold or recovery orientation.
- After every Executor Result Notice, returns exactly one checkpoint-bound
  Planner disposition to the same Executor. Terminal `ACCEPTED` and
  `DECISION_REQUIRED` carry no action and require no acknowledgement; a missing
  return remains awaiting verdict even if the Executor runtime is idle.
- Before the Orchestrator relies on Planner `ACCEPTED`, uses the next authorized
  governance writer to persist and verify that verdict and its evidence
  pointer.
- Only after the Planner recording is verified does the Orchestrator assess the
  project transition. The Planner returns one Result Notice to the Orchestrator,
  which returns exactly one checkpoint-bound disposition to the Planner and
  never contacts the Executor directly. Applies the same recording boundary to
  the Orchestrator's read-only assessment before another session or phase
  transition relies on it; otherwise reports recording as pending and does not
  claim durable phase closure.
- Gives cross-phase direction, next-phase, and Mandate questions to the
  Orchestrator; active Phase contract, permission, workspace, acceptance, and
  residual-risk questions to the Planner; and makes every non-owner relay the
  exact question or answer once rather than mirror it.
- Stops before Phase Two and before unapproved Git, installation, governance,
  or external actions.
- Reports degraded capability instead of claiming Standard if role delivery
  cannot be proved.

## Failure Signals

- Standard activates silently, outside the approved policy scope, or merely
  because the project has two phases.
- A fresh session claims activation or an `L4` responsibility without its
  required controller-observed Skill and conditional-reference reads.
- The Orchestrator implements, directs the Executor, or re-reviews the code.
- A one-agent fallback is represented as Standard.
- An Executor-internal step or slice is promoted into a separate Definition,
  role, tranche, or user approval gate without a material risk, permission,
  rollback, external-effect, or acceptance boundary.
- Phase One acceptance silently authorizes Phase Two.
- The Planner withholds its verdict from the Executor, the Orchestrator
  withholds its project disposition from the Planner, or either terminal return
  starts acknowledgement ping-pong or polling.
- Orchestrator, Planner, and Executor ask the same user question, or the
  Orchestrator bypasses the Planner to instruct the Executor.
- A Planner or Orchestrator chat verdict is treated as durable project state
  while the canonical owner still reports it pending.
- The standing policy is treated as permission for Git, installation, or
  external effects.
