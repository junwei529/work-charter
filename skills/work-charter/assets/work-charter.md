# Work Charter: <Name>

Use this optional durable carrier only when no suitable existing canonical
owner exists. It is never auto-created and its presence is not adoption proof.
For one authoritative checkout, root `WORK_CHARTER.md` is a possible fallback.
With multiple worktrees, record one explicit control location all required
roles can read at the same revision; do not copy authoritative files into each
worktree. Remove unused prompts and keep pointers instead of copied content.

- Managed workstream and exclusions: `<bounded line of work and what it does not cover>`
- Contract format: `arrangement-v1` for a newly approved contract; retain an old contract until its authorized migration
- Work arrangement and responsibilities: `<Direct | Team | Phased; reason and real coordination cost>`
- Continuity: `<current-task | durable, applicable existing anchor; Team/Phased need common recoverable control>`
- Contract state: `<draft | proposed | approved | superseded>`
- Run disposition: `<active | paused | closed>`
- Canonical locator and revision: `<portable locator and comparable freshness marker>`
- Standing-policy locator: `<if applicable; otherwise none>`
- Intended workspace and writer: `<workspace/worktree and one-writer boundary>`
- Role owners, carriers and review route: `<primary or actual O/P/E/R responsibilities; selected carriers, parent/recipient lifetime, next-turn activation where required, stable checkpoint and finding/disposition routes>`
- Review product and timing: `<actual result, implementation plan or overall direction; required gate, applicable instructions/contract, input, original author and assessor>`
- Reviewer continuity and carrier: `<one reliable continuing R for related products where supported; real reason for another R; exact request/return route across the selected carriers>`
- Resolved execution metadata: `<for each newly resolved task/role: arrangement, contract format (legacy level only if applicable),
  actual responsibility, provider/model/parameters or host-selection
  pass-through, object source, file source, requested values, and observable
  runtime identity>`
- Last material checkpoint and evidence: `<pointer, subject/revision, invalidation condition>`
- Reviewed input and coverage: `<baseline, actual change, semantic context, tests, docs, untracked inputs, graph/generated limits>`
- Findings and correction history: `<cumulative findings, dispositions, repairs, Reviewer continuity or replacement reason>`
- Last material result and decision: `<checkpoint, named assessor and action recipient; returned verdict or awaiting verdict only when a decision is required; factual notice otherwise>`
- Decision recording and closeout: `<formed verdict, canonical recording state, authorized writer window, required final records/checks and endpoint>`
- Next approved action or pending decision: `<bounded action and its authority, or decision locator and semantic owner>`
- Reconfirmation and return conditions: `<material change, stop, and return route>`

## Proposal Layers

- **Confirmed Contract:** `<user-confirmed outcomes, functional domain,
  environment, permitted effects, real cost, acceptance, and exclusions>`
- **Necessary Guardrails:** `<safety, permission, reversibility, trust,
  irreversible-effect, and authoritative project-rule constraints; name the
  source or protected risk; for Agent-derived guards, give the concrete
  failure/consequence, needed strength, and why simpler existing methods do
  not suffice; explicit user/project requirements need no new justification>`
- **Working Proposal:** `<current Agent-proposed route, ordinary file list,
  tools, sequence, implementation, and verification; replaceable while contract
  and guardrails remain intact>`
- **Assumptions / Open Decisions:** `<uncertainty; identify only the material
  choices that require the user>`

Before presenting this agreement as ready for adoption, distinguish confirmed
and still-valid reused answers from recommendations and unresolved user choices.
Explain actual roles/carriers, review products, acceptance and progression in
one concise view; omit inapplicable branches instead of adding a questionnaire.

Do not promote the Working Proposal into a hard requirement. When a proposed
method is rejected, remove or replace it unless an independently justified
durable boundary remains.
An approved general route does not fix every ordinary implementation step or
authorize an unlisted external effect. Keep explicit one-shot, human-review,
frozen-evidence and consumed-limit boundaries.

If auxiliary work keeps expanding, the current primary owner or Planner
compares simpler routes to the same protected outcome against remaining
coordination, implementation, verification, and maintenance cost. Keep the
minimum sufficient user-visible result in view; tool promises add no user goal.

## Outcome And Non-Goals

<State the observable result and adjacent work that remains excluded.>

## Scope And Hard Boundaries

<State fixed outcomes, interfaces, acceptance floor and real guardrails;
P's delegated in-phase choices and whether Definition finalization/dispatch
is authorized; E's replaceable methods and same-scope correction authority;
and the concrete exceptions that require P, O or the user. Planning-only
authority remains explicit when execution has not been delegated.>

## Authorization And Material Effects

<State which reads, writes, role delivery, Git operations, installation,
external effects, costs, or sensitive-data actions are authorized or
prohibited.>

## Acceptance Evidence

<State checks, evidence pointers, mutable subjects and invalidation
conditions, how hidden or external results are observed, verification
owner, Reviewer and review input when required, assessor, recording owner,
and independently acceptable checkpoints if any. For material evidence
claims, identify the agreed inspection scope, actual coverage and
remaining gaps. Treat graph results and acquisition counts as bounded
coverage aids, not semantic proof.>

## Authorized Progression

<Name the approved work package, next items, dependency/acceptance transitions,
aggregate cost/effect budget, intervention preference and exception stops.
State whether first E-to-R review and same-scope original-author repair/same-R
re-review are preauthorized; P receives the stable or exception result and
retains acceptance. Name the exact recipient, supported next-turn activation
route and next authorized action for each dependent handoff; distinguish
permission, message arrival, activation, completion and acceptance.
For cross-phase continuation, cite advance approval of the bounded phase set,
outcomes, transition conditions and total limits; otherwise the next unapproved
Phase remains a user gate. Preserve explicit old gates until amended.>

## Stop, Decision, And Recovery

<State bounded recovery read order, next safe action, stop conditions, and
return route. Name one semantic owner for each pending user decision.
Include incomparable authority, a missing required disposition, pending
recording that blocks reliance on durable state, evidence drift, writer
conflict, and the next affected recovery action. For ongoing evidence
work, retain usable source locators, obtained versus examined material,
and remaining gaps. Do not wake idle roles for text changes or claim
fresh loading from rereading, hashes or a new task alone. Preserve explicit
fresh-run contracts, approvals, findings, stops and consumed evidence
across compaction, deliberate rotation and successor Sessions.>

## Coordination

<State the least sufficient responsibility separation and applicable standing
policy without copying it. Name the assessor and action recipient for material
decisions; factual, evidence and mechanical-recording notices need no acceptance
reply. Required dispositions still reach the dependent role; terminal ones need
no acknowledgement. Complete the authorized package before stable review unless
a material boundary intervenes. Name any preauthorized R-to-E same-scope repair
and E-to-original-R re-review route, its stops and read-only review windows.
Otherwise findings return to P; in Direct they return to the primary.
Planning findings return to their original P or O author and designated approval
route. For implementation, P receives the cumulative stable or exception result
and returns its acceptance/correction/decision disposition to E. Record only formed verdicts
within the authorized single-writer window; mechanical closeout does not recurse
into acceptance of its records. Retain cumulative review history. Configuration
choice does not enable a listed role or authorize delivery or action. Distinct
responsibilities that outlive an upstream turn normally use separate addressable
tasks with a supported next-turn route. Bounded subagents may return within an
active parent turn. Cross-turn mixed carriers require actual host reactivation,
addressing/recovery and approved selection; keep a suspended design in its
existing design owner, not as a competing active default. Use short task labels;
full identities and checkpoints remain in the contract.>

## Task Or Role Prompt

<Optional prompt scaffold, not a second authoritative contract. Shared
contract: locator/revision and material boundaries. Actual responsibility:
primary or the authorized O/P/E/R role. Current task: deliverable, inputs,
required checks, stop conditions, and return route. For evidence-only
work, include the bounded question, allowed source/data scope and actual
coverage/gaps required in the result. Necessary model adaptation:
supported delta and source, or none. Cold prompts supply missing context;
warm prompts carry only changed facts and the valid anchor; recovery
preserves findings, permission history and material inspection progress.
Keep effort in native runtime parameters.>
