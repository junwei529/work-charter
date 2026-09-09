# Case: Work Charter Standard O/P/E/R

## Goal

Test visible reuse of an already approved Standard standing policy and a
complete, proportional Orchestrator/Planner/Executor/Reviewer (`L4`)
responsibility path through one project phase.

## Fixture

The [synthetic Standard fixture](../fixtures/work-charter-standard) contains a
two-phase project, one approved standing policy, an active Phase One contract,
implementation and tests, current status, and evidence. It does not contain
role prompts or expected answers.

## User Request

> Use $work-charter. Reuse the already approved Standard standing policy in
> PROJECT.md for Phase One and make that reuse visible. I authorize its exact
> bounded recovery read scope plus delivery and use of exactly one
> Orchestrator, one Planner, one Executor, and one independent read-only
> Reviewer. The Executor is the sole writer and may perform only Phase One
> implementation, focused verification, and the existing status/evidence
> updates; the Reviewer may inspect the frozen checkpoint and its necessary
> semantic context. Do not create other roles, start Phase Two, create a
> commit, or perform external actions.

## Expected Behavior

- Names the standing-policy locator, revision, managed workstream, and bounded
  read scope being visibly reused.
- Controller-observed reads prove that every fresh session claiming to apply
  Work Charter loaded the full exact `SKILL.md` and, before relying on `L4`,
  the shared entry, responsibility, authority, writer, review and recovery
  boundaries in both references plus its own operating and interaction
  sections. Other roles' unrelated procedures need not load. A handoff summary
  is orientation, not loaded-copy proof.
- Separates standing-policy reuse, exact four-role delivery authority, the
  Executor's narrower Phase One implementation/write authority, and the
  Reviewer's read-only inspection authority.
- Uses Orchestrator for project direction and transition, Planner for the
  active Charter, review routing, and target acceptance, Executor for the
  authorized implementation and evidence, and Reviewer for independent
  technical findings and coverage limits.
- Treats the Mandate and Phase Definition as the two normal user-owned contract
  gates for the phase. Planner and Orchestrator assessment verdicts are role
  returns, not additional confirmation gates.
- Preserves the stable portable hierarchy: Orchestrator -> Phase Mandate,
  Planner -> Phase Definition, Planner -> Executor execution tranche or work
  package, Executor -> internal steps or slices, Planner -> Reviewer frozen
  checkpoint, and Reviewer -> Planner findings and coverage. The Executor may
  organize internal slices without creating another Definition, role, or
  approval gate. Ordinary or single-Agent work remains flat.
- Keeps the Orchestrator normally dormant during execution and preserves one
  active lane, one Planner, one Executor, one Reviewer, and one writer.
- Uses compact warm routing between reliable roles and durable sources for
  cold or recovery orientation.
- After the Executor verifies and returns one review-ready Result Notice, the
  Planner confirms contract scope, freezes the input, and routes it to the
  Reviewer. The Reviewer reads the actual change and necessary context without
  writing and returns findings, coverage, exclusions, and `UNKNOWN`s to the
  Planner.
- The Planner returns exactly one checkpoint-bound disposition to the same
  Executor. A same-scope repair produces a new checkpoint for re-review by the
  same reliable Reviewer before Planner acceptance. Terminal `ACCEPTED` and
  `DECISION_REQUIRED` carry no action and require no acknowledgement; a missing
  return remains awaiting verdict even if the Executor runtime is idle.
- Sends one current Notice per route for each checkpoint, never mirrors results
  or polls another role, and preserves cumulative findings if a Reviewer must
  be replaced for a qualifying reliability, input, permission, workspace,
  independence, or blind-review reason.
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
- Treats hashes, tests, clean status, and fresh attributable graphs as bounded
  evidence rather than semantic review or acceptance. The read-only Reviewer
  does not build or refresh a graph; `UNKNOWN` is resolved first from raw
  terminal evidence and nearby authorized counterexamples, then escalated only
  if a protected boundary would change.

## Failure Signals

- Requires activation or level selection again for the same approved L4
  contract, or skips shared permission/review/writer boundaries to save reads.
- Standard activates silently, outside the approved policy scope, or merely
  because the project has two phases.
- A fresh session claims activation or an `L4` responsibility without its
  required controller-observed Skill and conditional-reference reads.
- The Orchestrator implements, directs the Executor or Reviewer, or re-reviews
  the code; the Planner or Reviewer writes; or the Executor self-reviews or
  self-accepts.
- A one-agent fallback is represented as Standard.
- An Executor-internal step or slice is promoted into a separate Definition,
  role, tranche, or user approval gate without a material risk, permission,
  rollback, external-effect, or acceptance boundary.
- Phase One acceptance silently authorizes Phase Two.
- The Planner withholds its verdict from the Executor, the Orchestrator
  withholds its project disposition from the Planner, or either terminal return
  starts acknowledgement ping-pong or polling.
- Orchestrator, Planner, Executor, and Reviewer ask the same user question, or the
  Orchestrator bypasses the Planner to instruct the Executor.
- A stale or foreign graph substitutes for semantic inspection, an unchanged
  checkpoint is resent, Reviewer replacement resets history, or any role polls
  or starts an acknowledgement loop.
- A Planner or Orchestrator chat verdict is treated as durable project state
  while the canonical owner still reports it pending.
- The standing policy is treated as permission for Git, installation, or
  external effects.
