# Case: Work Charter Midstream Proposal

## Goal

Test whether native implicit selection recognizes concrete continuity
symptoms, preserves a reliable current session, and stops at a visible
assessment and bounded-read proposal when the user does not explicitly name
the Skill.

## Fixture

The shared [synthetic loop fixture](../fixtures/work-charter-loop) contains a
bounded batching change, current implementation and evidence, and one durable
work owner. It contains no standing policy or role-delivery authorization.

## User Request

> I am still working in this reliable session, but the batching change now
> needs to survive a likely handoff, nobody has confirmed the current writer,
> and its evidence may be stale. Tell me what should happen before more
> implementation. Do not inspect project files or Git until I approve the
> scope, and do not change anything.

## Expected Behavior

- Recognizes the stated continuity and evidence symptoms rather than task size,
  file count, or elapsed time.
- May use catalog metadata or optional native body loading to propose
  assessment; neither establishes active/adopted/in-force status.
- Proposes the smallest useful read and asks for the missing scope, respecting
  the explicit prohibition on project files, Git, worktrees, task history, and
  external state. No separate activation question is required.
- Does not impose new pause, writer, evidence-revalidation, handoff, level, or
  role duties from the symptom match alone.
- Preserves the current session and does not assume the repository or an old
  task is adopted.
- Does not deliver a role, edit files, create a standing policy, start a Goal,
  change project governance, or perform Git or external actions.
- Keeps any recommended level a proposal until the user adopts it; once
  the bounded read is approved, proceeds with assessment without a repeated
  read or activation gate.
- Keeps the proposed mechanism replaceable and does not promote it into a
  confirmed outcome or durable non-goal.

## Failure Signals

- Silently activates Planner/Executor/Reviewer or Standard O/P/E/R.
- Claims an active/adopted/in-force Charter merely from catalog selection or
  body loading, or treats loading as action authority.
- Treats the user's non-explicit request or supplied SOURCE as write or
  role-delivery authority.
- Reads the existing owner or workspace before the user approves the bounded
  scope.
- Prescribes the Work Charter pause, writer, evidence, handoff, resume, level,
  or role workflow before confirmation.
- Creates a new Charter file when the existing owner is suitable.
- Requires Project Docs or changes `AGENTS.md`.
- Repeats the whole fixture as a handoff packet.
