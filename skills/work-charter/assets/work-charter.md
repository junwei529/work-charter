# Work Charter: <Name>

Use this optional durable carrier only when no suitable existing canonical
owner exists. It is never auto-created and its presence is not adoption proof.
For one authoritative checkout, root `WORK_CHARTER.md` is a possible fallback.
With multiple worktrees, record one explicit control location all required
roles can read at the same revision; do not copy authoritative files into each
worktree. Remove unused prompts and keep pointers instead of copied content.

- Managed workstream and exclusions: `<bounded line of work and what it does not cover>`
- Protection and responsibilities: `<plain-language shape; internal L1 | L2 | L3 | L4 if useful>`
- Contract state: `<draft | proposed | approved | superseded>`
- Run disposition: `<active | paused | closed>`
- Canonical locator and revision: `<portable locator and comparable freshness marker>`
- Standing-policy locator: `<if applicable; otherwise none>`
- Intended workspace and writer: `<workspace/worktree and one-writer boundary>`
- Last material checkpoint and evidence: `<pointer, subject/revision, invalidation condition>`
- Last role result and returned disposition: `<checkpoint, verdict, return route, or awaiting verdict>`
- Next approved action or pending decision: `<bounded action and its authority, or decision locator and semantic owner>`
- Reconfirmation and return conditions: `<material change, stop, and return route>`

## Proposal Layers

- **Confirmed Contract:** `<user-confirmed outcomes, acceptance, and exclusions>`
- **Necessary Guardrails:** `<safety, permission, reversibility, trust,
  irreversible-effect, and authoritative project-rule constraints; name the
  source or protected risk>`
- **Working Proposal:** `<current Agent-proposed route, tools, sequence,
  implementation, and verification; replaceable while contract and guardrails
  remain intact>`
- **Assumptions / Open Decisions:** `<uncertainty; identify only the material
  choices that require the user>`

Do not promote the Working Proposal into a hard requirement. When a proposed
method is rejected, remove or replace it unless an independently justified
durable boundary remains.

## Outcome And Non-Goals

<State the observable result and adjacent work that remains excluded.>

## Scope And Hard Boundaries

<State the bounded work and the conditions that require a new decision.>

## Authorization And Material Effects

<State which reads, writes, role delivery, Git operations, installation,
external effects, costs, or sensitive-data actions are authorized or
prohibited.>

## Acceptance Evidence

<State checks, evidence pointers, mutable subjects and invalidation conditions,
how hidden or external results are observed, assessor when required, recording
owner, and independently acceptable checkpoints if any.>

## Stop, Decision, And Recovery

<State bounded recovery read order, next safe action, stop conditions, and
return route. Name one semantic owner for each pending user decision. Include
incomparable authority, a missing returned disposition, pending assessment
recording, evidence drift, or writer conflict when applicable.>

## Coordination

<State the least sufficient responsibility separation and applicable standing
policy without copying it. For role separation, state the Result Notice and
checkpoint-bound disposition routes; terminal dispositions require no
acknowledgement. Profile choice does not authorize delivery or action.>
