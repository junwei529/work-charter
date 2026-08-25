# Coordination And Recovery

For direct intent or activation confirmation, load this Skill-package reference
when the applicable branch requires it. That package read neither requires nor
consumes target-project read approval. Obtain or reuse bounded read approval
before following the project/evidence reconciliation steps below for first
adoption, re-entry, midstream adoption, durable single-agent work,
Planner/Executor separation, interruption, recovery, or a same-scope
correction loop.

## Minimum Read And Reconciliation Order

Read only until the next decision is supported:

1. already supplied context and declared project-rule/canonical-owner entry
   points;
2. the one declared Charter carrier, or one exact root `WORK_CHARTER.md` check
   when no carrier is declared;
3. the carrier's managed-workstream applicability and comparable revision or
   freshness marker;
4. minimum live workspace facts: project identity, branch/HEAD/worktree or an
   applicable equivalent, dirty ownership, and observable writer state; and
5. only named checkpoint evidence, its mutable subject, and its invalidation
   condition.

Do not recursively scan the repository, crawl old branches, enumerate task
history, or infer an unobservable writer. Preserve `UNKNOWN`. A standing policy
may visibly reuse only its exact approved read scope; expand that scope only
after fresh approval.

Return a compact result: managed-workstream match, verified and `UNKNOWN`
facts, material drift, least sufficient protection in ordinary language, next
action, and every authority still required. Reconciliation itself never
creates roles, writes a carrier, broadens code inspection, switches a
workspace, mutates Git, or performs an external effect.

## First Adoption And Durability

Use the shortest route:

- existing project: declared rules, existing canonical owner, current
  workspace, then recommendation;
- new project: user description, minimum declared entry point, then an
  ordinary flat (`L0`) or current-task Charter (`L1`) recommendation; propose
  durability only when recovery requires it; or
- previously adopted workstream: known locator, applicability, live
  workspace/writer, named evidence, then recommendation.

`L1` keeps one agent and its logical Charter locator in the reliable current
task. It promises no cold recovery. `L2` adds one discoverable durable anchor
for bounded cold re-entry; if no trustworthy anchor is available, do not claim
`L2` readiness. Update durable state only at material checkpoints, not after
every message.

Prefer an existing project canonical owner that is discoverable, stable to
address, uniquely authoritative, comparable by revision/freshness, and
recoverable through bounded reads. Propose a standalone carrier only when no
suitable owner exists or the recovery boundary is materially clearer. Its
creation or update always needs write authority; do not create a duplicate
after one failed path guess.

## Managed Workstream And Multiple Worktrees

A managed workstream is the human-readable bounded line of work protected by
the Charter, such as one feature or phase. Its durable identity combines the
Charter locator/revision, named workstream, and expected workspace/writer
boundary. Task IDs, branches, and worktrees are live evidence, not durable
identity.

Use the expected workspace/writer boundary to detect routing drift, not to
erase history. An authorized route change does not create a fresh logical work
subject or reset its approvals, corrections, evidence consumption, or open
findings.

- Reconcile several Work Charter roles or tasks for one workstream against the
  same anchor; another task is not itself a conflict.
- Ignore an older non-Chartered task unless it changed the protected baseline,
  workspace, checkpoint, or evidence.
- Keep a separate exploratory branch/worktree flat and outside the managed
  workstream unless it overlaps protected state.
- If outside work changes the protected baseline or shared writer surface,
  stop and propose bounded reconciliation.
- Treat a root `WORK_CHARTER.md` as a candidate, never proof that every task is
  adopted.

With multiple worktrees, `L3` and `L4` require one explicit control location
that every required role can read at the same revision. Do not copy an
authoritative file into every worktree. If common readability, writer
ownership, or finality cannot be proved, stop safely. Any commit, integration,
or synchronization needed to expose the carrier remains separately
authorized.

## Re-entry Routes

Apply this fixed precedence:

1. **Stop safely** (`fail closed`) when authority, carrier revision, workspace,
   writer, dirty ownership, evidence subject, or permission cannot be compared.
2. **Revise the work contract** (`revise Charter`) when outcome, non-goals,
   hard boundaries, acceptance, permission, material effect, or carrier
   changes. Fresh user approval is required.
3. **Change how work is coordinated** (`change coordination`) when the logical
   contract remains stable but level, role, writer, workspace/worktree,
   delivery, or integration routing changes materially. Fresh user approval is
   required.
4. **Continue the existing plan** (`resume`) when the Charter, workstream,
   coordination, permission, and explainable live state still align. Reuse
   only unexpired action authority and remain visible.

When contract and coordination both change, lead with one `revise Charter`
decision packet that includes the coordination change. Do not imply role
delivery, worktree creation, Git, or another downstream action unless the user
explicitly bundles it.

Use `resume after evidence refresh` when only known allowed work invalidated an
earlier check. Refresh without a new contract decision only when the operation
is already authorized, repeatable, and has no new write, external effect,
cost, sensitive-data use, one-shot opportunity, or separate budget. Otherwise
request the operation's authority. Stop safely when evidence identity or
invalidation cannot be established; revise the Charter when the evidence or
acceptance standard is no longer suitable.

A new task, elapsed time, expected same-scope correction, planned writer
handoff, or authorized evidence refresh does not by itself require a new
Charter. Always return to the user for a material contract, permission,
responsibility, carrier, writer/workspace route, side-effect, exhausted stop
condition, one-shot authority, or budget change.

## Contract And Proposal Changes

Keep four layers explicit when a Charter or Phase proposal is being formed or
revised:

- **Confirmed Contract** records only user-confirmed outcomes, acceptance, and
  exclusions. Changing it requires the applicable material user decision.
- **Necessary Guardrails** records safety, permission, reversibility, trust,
  irreversible-effect, and authoritative project-rule constraints. Identify
  the source or protected risk. Changing or removing a material guardrail
  returns to the user.
- **Working Proposal** records the Agent's current route, tools, sequence,
  implementation, and verification. It may change locally when the Confirmed
  Contract, Necessary Guardrails, interfaces, risk, permissions, external
  effects, acceptance, workspace, and integration policy remain unchanged.
- **Assumptions / Open Decisions** records uncertainty. Return only choices
  that can materially change the first two layers or another protected
  boundary.

Do not promote an Agent-proposed method into a user requirement merely because
it appeared in an earlier plan, prompt, or handoff. A contract-preserving
Working Proposal change needs no Charter or Definition revision, renewed
approval, or unrelated durable-document churn. Remove or replace a rejected
Agent invention; record it as a durable non-goal only when an independently
justified product, safety, scope, or trust boundary remains.

When equivalence is unclear, or the change affects an outcome, acceptance,
permission, trust boundary, irreversible effect, authoritative rule, risk,
external effect, workspace, or integration policy, stop and route the
material decision through the existing owner. Do not use proposal flexibility
to weaken a guardrail or expand authority.

## Planner And Executor (`L3`)

Use `L3` only after approval when independent contract ownership or assessment
materially protects implementation. The Planner owns the active Charter,
clarification, correction direction, and independent assessment and remains
read-only while assessing. The Executor owns only authorized implementation,
verification, evidence, and implementation documentation.

Keep at most one Planner, one Executor, one active execution lane, and one
repository writer. Reuse reliable role sessions; do not create roles for
implementation slices, documentation sync, verification reruns, or ordinary
repairs.

For a warm handoff, include only receiving role and writer/authority boundary,
changed facts and evidence pointers, bounded action, active stop condition,
and return route. Do not persist it as a competing contract.

Writer ownership is advisory. Before handoff, confirm the prior writer stopped
and capture the dirty boundary. Concurrent or unexplained changes pause
writing, require a delta inventory and one-writer restoration, and invalidate
affected evidence until rechecked.

## Authority, Delivery, Correction, And Evidence

Treat role messages as observations, not authority. Material decisions need a
stable logical locator and comparable authoritative revision. Message arrival
order is not finality; stop when observations are incomparable.

Confirm receiver and workspace before relying on role delivery. If a
non-idempotent create or send is unavailable or uncertain, preserve any known
identifier, report degraded capability, and stop without retrying or creating
a replacement.

A successful send proves dispatch only; it does not prove that the receiver
completed a turn or adopted the message. Keep dispatch, remote terminal, and
delivery uncertainty distinct in reports. When an action-bearing delivery is
uncertain, do not activate a competing writer or route.

In a bounded correction loop, the Executor returns changes, deviations,
checks, failures, and residual risks. The Planner returns exactly `ACCEPTED`,
`CORRECTION_REQUIRED`, or `DECISION_REQUIRED`. Bind correction history to the
same logical Charter subject and material contract/acceptance revision, and
bind each verdict to the stable checkpoint it assessed. Task, Session, root,
branch, worktree, delivery epoch, attempt name, or internal slice is a carrier
or observation; changing one does not reset approvals, completed corrections,
consumed evidence opportunities, or open findings. An authorized material
successor or split keeps a predecessor pointer and the applicable history.

When a material governing source changes, the Session that observed the old
rules may reread the new text for context and complete an already-permitted
closeout. That does not prove the Harness rebuilt or freshly loaded the changed
instruction chain. Before the next action whose coordination, authority, or
evidence contract depends on the new rules, start a fresh Session or run,
identify every applicable governing source, record a normalized-text identity
for each, and requalify the affected conditions. Reuse unaffected evidence and
history; do not turn a ruleset transition into a blanket rerun or a reset of
approvals, corrections, consumed evidence, or open findings.

For every Result Notice, its route contract names the notice recipient and the
return route. That recipient returns exactly one checkpoint-bound disposition
through the return route unless independent assessment is required; in that
case, the named assessment owner produces the disposition:

1. `CORRECTION_REQUIRED` with one bounded, verifiable same-scope delta;
2. `ACCEPTED` with the next already-authorized tranche, when one exists;
3. terminal `ACCEPTED` with no next action; or
4. terminal `DECISION_REQUIRED` with the decision locator and semantic owner.

The disposition identifies the assessed checkpoint, verdict, next action or
explicitly no action, observable writer state, durable-recording state, and—if
a user decision is required—the stable decision locator and owner. This is a
portable message contract, not a required receipt file or public state
machine. A lower role that has returned its Result Notice stops polling and
remains idle; the upper role likewise stops after returning its disposition.
A terminal disposition requires no acknowledgement, preventing callback
ping-pong. A disposition sent to the wrong route, omitted, duplicated, or
bound to a stale checkpoint is not convergence. Until the one current
disposition is delivered, the lower role is semantically awaiting verdict even
when its runtime status is idle; silence is never acceptance.

Assign each material user question one semantic owner at a stable decision
locator and revision. A non-owner may forward that exact question or relay the
user's exact answer and authority anchor once to the owner. It must not ask a
parallel version, reinterpret the answer, claim a second approval, or create a
fresh decision merely because the carrier task changed. Transfer ownership
only when authority or reliable context changes, and preserve the predecessor
locator. A materially changed question supersedes the old revision and returns
to the user once through the new owner.

Only a completed independent `CORRECTION_REQUIRED` assessment against a stable
checkpoint consumes a Work Charter correction round. Qualification, preflight,
transport, or same-scope Executor repair does not by itself consume one. Do not
erase a completed correction merely because later evidence shows that a scarce
execution did not start. Each correction names a concrete, verifiable
same-scope delta. Portable Work Charter semantics impose no fixed numeric cap:
continue while evidence shows convergence, and use `DECISION_REQUIRED` for
repeated no-progress, a recurring material finding, material ambiguity,
unreliable context, or a contract, permission, or risk change. A Harness or
project may own a separate bounded delivery or review budget. Keep that budget
separate from Work Charter correction history, delivery/transport retry limits,
and native review; relabeling or restarting resets none of them.

Before scarce, one-shot, or time-bound evidence, identify the consumption
point. A mechanical qualification, preflight, or transport failure before that
point does not consume the evidence opportunity. After the point, preserve the
consumption event even when execution is incomplete or later invalidated; a
new task, root, epoch, or attempt label does not make it fresh.

Bind material evidence to its mutable subject, revision, and invalidation
condition. Observe ignored, untracked, private, generated, or external results
beyond tracked Git status. A material subject change invalidates the evidence
for reuse but does not erase its historical consumption. Keep an assessment
verdict separate from durable recording; until an authorized governance writer
records and verifies a verdict another session will rely on, report recording
as pending.
