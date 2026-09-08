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
- Role owners and review route: `<primary owner, or O/P/E/R owners; stable checkpoint and finding/disposition routes>`
- Resolved execution metadata: `<for each newly resolved task/role: level,
  actual responsibility, provider/model/parameters or host-selection
  pass-through, object source, file source, requested values, and observable
  runtime identity>`
- Last material checkpoint and evidence: `<pointer, subject/revision, invalidation condition>`
- Reviewed input and coverage: `<baseline, actual change, semantic context, tests, docs, untracked inputs, graph/generated limits>`
- Findings and correction history: `<cumulative findings, dispositions, repairs, Reviewer continuity or replacement reason>`
- Last role result and returned disposition: `<checkpoint, verdict, return route, or awaiting verdict; one current Notice only>`
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
how hidden or external results are observed, verification owner, Reviewer and
review input when required, assessor, recording owner, and independently
acceptable checkpoints if any. Treat graph results as bounded coverage aids,
not semantic proof.>

## Stop, Decision, And Recovery

<State bounded recovery read order, next safe action, stop conditions, and
return route. Name one semantic owner for each pending user decision. Include
incomparable authority, a missing returned disposition, pending assessment
recording, evidence drift, writer conflict, and context-switch checkpoint when
applicable. Preserve approvals, findings, stops, and consumed evidence across
compaction, deliberate rotation, and successor Sessions.>

## Coordination

<State the least sufficient responsibility separation and applicable standing
policy without copying it. For role separation, state the Result Notice and
checkpoint-bound disposition routes; terminal dispositions require no
acknowledgement. Send one current Notice per checkpoint and retain cumulative
review history. Configuration choice does not enable a listed role or authorize
delivery or action.>

## Task Or Role Prompt

<Optional prompt scaffold, not a second authoritative contract. Shared contract:
locator/revision and material boundaries. Actual responsibility: primary or the
authorized O/P/E/R role. Current task: deliverable, inputs, required checks,
stop conditions, and return route. Necessary model adaptation: supported delta
and source, or none. Cold prompts supply missing context; warm prompts carry
only changed facts and the valid anchor; recovery preserves findings and
permission history. Keep effort in native runtime parameters.>
