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

`L1` keeps one primary owner and its logical Charter locator in the reliable
current task. It promises no cold recovery. `L2` adds one discoverable durable
anchor for bounded cold re-entry; if no trustworthy anchor is available, do
not claim `L2` readiness. Either level may use one bounded read-only Reviewer
without creating Planner/Executor separation. The primary owner remains the
writer, dispositions findings, verifies repairs, and delivers the result.
Update durable state only at material checkpoints, not after every message.

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
that the Planner, Executor, Reviewer, and—at `L4`—Orchestrator can read at the
same revision. Do not copy an authoritative file into every worktree. If
common readability, writer ownership, review independence, or finality cannot
be proved, stop safely. Any commit, integration, or synchronization needed to
expose the carrier remains separately authorized.

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

## Context-Switch Recovery

Distinguish a summary or compaction inside one run, a deliberate rotation to a
fresh context, and creation of a new or successor Session. A product label or
enabled setting does not prove which mechanism occurred or that every fallback
path was disabled. None of these mechanisms creates a new work subject or
resets approvals, findings, correction history, permissions, stop conditions,
or consumed evidence when the material contract and checkpoint are unchanged.

Before a foreseeable switch, preserve the smallest sufficient checkpoint in
the existing authoritative carrier: Charter locator and revision, role and
writer, workspace, reviewed input, open findings, evidence and invalidation
condition, last returned disposition, and next authorized action. After the
switch, reload the current contract and checkpoint, compare them with live
workspace and writer state, then retrieve only missing evidence. Memory or a
conversation summary may locate evidence but cannot replace current authority,
raw terminal proof, or durable state. If role, ruleset, input, or workspace
identity is incomparable, stop safely and use the applicable re-entry route.

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

For a guardrail derived by the Agent, distinguish the protected outcome from
the chosen mechanism and its strength. Identify the concrete failure and its
consequence, the strength needed to address it, and why simpler existing
methods do not suffice. The Necessary Guardrail label, a documented tool
promise, or general implementation approval alone proves none of these.
Explicit user and project requirements retain their authority under the
existing contract; do not require the user to justify them again.

If auxiliary repair or coordination keeps expanding, the current primary
owner or Planner determines the minimum sufficient user-visible outcome and
compares the remaining coordination, implementation, verification, and
maintenance cost with simpler viable routes to the same protected outcome.
Sunk effort and findings about a tool's own promises do not turn that tool
into a new user goal. Reuse these four layers and the existing decision owner;
this assessment adds no role, required form, or approval gate. Preserve real
defects, evidence, explicit requirements, and applicable verification while
replacing a proposal.

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

## Task And Role Prompt Construction

Compose prompts from shared contract, actual responsibility, current task, and
necessary model adaptation. These are logical inputs, not mandatory headings
or copied instruction sets. An ordinary L0 host task can use this shape without
selecting or activating Work Charter.

- Shared contract: identify the authoritative outcome, scope, permissions,
  acceptance, revision, and stop conditions. Restate only boundaries the
  receiving context needs to act unambiguously.
- Actual responsibility: include only the receiver's authorized work below.
  Model names never grant responsibility or permission.
- Current task: give the bounded deliverable, relevant inputs and evidence,
  remaining work, required verification, and result route. Prescribe internal
  steps only for a dependency, protected risk, or explicit contract requirement.
- Necessary model adaptation: include only a supported difference relevant to
  the actual model and task, with its source; otherwise use adaptation `none`.

| Actual responsibility | Prompt addition |
| --- | --- |
| Primary (`L0`-`L2`) | Complete authorized implementation, required verification, and delivery; at L1/L2 retain the applicable record and disposition independently required Reviewer findings. Do not create P/E separation or claim independent self-acceptance. |
| Orchestrator (`L4`) | Frame project outcome, Mandate, phase direction, and Planner return route; assess project-level results without directing the Executor or repeating technical review. |
| Planner (`L3`/`L4`) | Supply the executable contract, acceptance criteria, and E/R routes; assess returned evidence and direct corrections while remaining read-only on implementation and routing technical review to R. |
| Executor (`L3`/`L4`) | Complete authorized work and required checks, preserve findings and evidence, and return the stable checkpoint to the Planner; do not expand scope or accept the result. |
| Reviewer (when enabled) | Inspect frozen input and necessary semantic context read-only; return actionable findings, coverage, and unknowns to the designated assessor or primary owner without repair or self-granted authority. |

Cold prompts provide sufficient authoritative pointers and hard boundaries to
start without a conversation search. Warm continuations retain the contract
anchor, changed task/evidence, next authorized action, and return route; omit
unchanged instructions already reliable in context. Recovery restores missing
contract, writer, checkpoint, findings, and permission history. Do not nest an
old delegation envelope inside a new one. Use the optional
[prompt scaffold](../assets/work-charter.md#task-or-role-prompt) without creating
a second authority file.

Keep every prompt and handoff proportionate and complete for the receiver's
next decision or action. Preserve key facts, decisions, material limitations,
and the next step. First remove repeated background, preambles, reassurance,
and unrelated content. Brevity must not hide a constraint, unresolved decision,
or evidence needed to act. Apply this throughout the exchange, not only to the
final result; use no fixed word limit or extra mandatory message templates.

Complete authorized work through required checks and its result route. Ask only
for a missing material decision or permission; resolve routine choices within
the existing contract. Make a required decision concrete with independent
authorized work first. Silence never approves the dependent action. Preserve
activation/adoption, material replan, operation permission, independent review,
and acceptance gates. Remove duplicate warnings and arbitrary step counts, not
those boundaries. Repeat verification only when its input changed, it failed,
or an unresolved material concern requires it; complete all required checks.

### Model Adaptation On Demand

For the actual selected Astra, Sol, Terra, or Luna model, consult current
official guidance only when a model-specific adjustment is needed, or use
relevant attributable behavioral evidence already authorized for this work.
Record the source and supported delta; do not routinely load or copy four
guides. A host documentation Skill may help, but this package requires no other
Skill or private reference path. Missing guidance never justifies invented
model stereotypes; unresolved native parameter support still stops dispatch.
A source claim does not prove runtime identity or model efficacy.

The [official Astra prompting guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices),
checked on 2026-09-07, supports explicit in-scope continuation, clear instruction
priority, and testing proportional to demonstrated need. Where relevant, use
the common continuation and verification rule above without another approval
loop or copied guide. This grants no new roles or relaxed evidence gates.
Consult another model's own guidance before applying model-specific claims.

Reasoning effort is a supported runtime parameter and evaluation variable,
not a responsibility or prose replacement such as "think harder". Keep the
shared contract/role/task prompt stable across effort settings; do not copy a
full prompt for each setting or change an active task's model. If evaluation is
separately authorized, distinguish prompt, model, and effort changes for
attributable evidence. Editing a prompt does not authorize model evaluation.

## Role-Model Configuration At Dispatch

Apply this section only when the governing contract has authorized a new task
or delivery and identified its protection level and actual responsibility.
Configuration selects execution metadata for that start or delivery; it grants
no task, role, action, read, write, Git, installation, provider, credential,
network, or external-effect authority. A level describes coordination and
governance, not task difficulty or a monotonic model-investment scale; never
infer the level from a model name or the model from a level alone.

First resolve the delivery inputs in this order:

1. Preserve a complete provider/model/parameters combination already frozen
   for this delivery. Do not reread configuration to replace it.
2. Otherwise, use a complete combination explicitly confirmed for this new
   task or role. This task-local value is contract input, not another YAML
   source, and omitted `parameters` means no parameters.
3. Otherwise, resolve from configuration using source priority first and
   level-before-general priority within each source, as defined below.

For step 3, select at most one override file. When the contract names an
explicit configuration file, read exactly that file. Missing or unreadable
input stops delivery; do not fall back and hide the failure. Otherwise read
`~/.config/work-charter/role-models.yaml` when it exists. If neither exists,
use only the package [default configuration](../assets/role-models.default.yaml).
The selected explicit or user file supplies higher-priority complete objects;
the package supplies fallback objects. Do not merge fields across them or
introduce another directory source.

The user path is outside Skill discovery and installation roots. Never search
project directories or other user paths for alternatives. Install, update,
rollback, and uninstall must not create, modify, move, or delete the user file.

The package default retains its four general objects and existing values as
compatibility fallbacks, and adds the approved L0-L4 level overrides. It has no
general `primary` or `l0.reviewer` override; the latter uses the general
Reviewer fallback unless explicitly configured. Missing user entries may use
package level defaults, including for primary owners. Accept configuration
only in this bounded data shape:

- the top-level mapping has integer `schema_version: 1`, at least one of
  `roles` or `level_overrides`, and no other field;
- `roles`, when present, contains only `primary`, `orchestrator`, `planner`,
  `executor`, and `reviewer`;
- `level_overrides`, when present, contains only `l0`, `l1`, `l2`, `l3`, and
  `l4`; each level may contain only the actual responsibilities in this matrix:

  | Level | Configurable actual responsibilities |
  | --- | --- |
  | `l0` | `primary`, `reviewer` |
  | `l1` | `primary`, `reviewer` |
  | `l2` | `primary`, `reviewer` |
  | `l3` | `planner`, `executor`, `reviewer` |
  | `l4` | `orchestrator`, `planner`, `executor`, `reviewer` |

- each supplied general or level-specific object has exactly nonempty
  plain-string `provider` and `model`, plus optional mapping `parameters`; and
- each parameter name and value must be explicitly supported by the selected
  provider/model and the current native creation route.

Reject duplicate or unknown fields and roles, unknown schema versions, wrong
types, ambiguous YAML, tags, anchors, aliases, merge keys, executable or
instruction-like content, credentials, endpoints, commands, and environment
interpolation. Treat the file as data only. Do not add a parser dependency,
start a service, evaluate content, interpolate values, or silently discard an
unsupported parameter.

An explicit or user file may supply only the general roles and level-role
combinations it changes. Every supplied object is a whole-object replacement:
it must repeat `provider` and `model`, and omitted `parameters` means no
parameters for that combination. Do not inherit parameters from a package
object, another level, a previous model, or a different provider. Missing
objects fall through to the next object in the lookup order; they do not
invent values or merge parameters. The same rule applies to task-local
explicit combinations unless the contract already froze the complete delivery.

At the task-start or role-dispatch boundary, normalize a host label `main` to
the canonical actual responsibility `primary`; do not accept both spellings as
YAML keys. Validate the complete selected file before using any entry, so an
unknown or invalid entry is not silently ignored merely because its role is not
enabled. Validate the package defaults as well when consulting them. Then
resolve the identified level and actual responsibility:

1. selected explicit or user file: `level_overrides.<level>.<responsibility>`;
2. selected explicit or user file: `roles.<responsibility>`;
3. package default: `level_overrides.<level>.<responsibility>`;
4. package default: `roles.<responsibility>`; or
5. only for `primary`, when neither source supplies an object, preserve the host's existing
   selection by sending no provider, model, or parameter override. Record the
   requested combination as `UNSPECIFIED`, the source as `host selection`, and
   runtime identity as `UNKNOWN` unless the host exposes it. Never borrow the
   `executor` or `planner` object for a primary owner.

Use the first present complete object; with no selected user file, start at
the package level lookup. An explicit/user general object wins over a package
level override, preserving legacy four-role user files. For example, a user
general Executor configured as Sol/high still wins for L3 or L4 even though
the package level default is Astra/medium. If that user file omits Executor,
the applicable package level override wins before the package general fallback.
The current package supplies every valid primary lookup, so host pass-through
is a defensive compatibility rule rather than the current no-user-file result.

The matrix defines which objects may be selected, not which roles are enabled.
An `l0.reviewer`, `l1.reviewer`, or `l2.reviewer` entry never creates a Reviewer
or activates a review gate. `L0` remains no active Charter; its local
task-selection consumer may reuse this input contract without loading or
activating Work Charter. Until a host or global task-start consumer actually
implements the interface, package text and deterministic fixtures prove only
the source contract, not local adoption or effective runtime delivery.

The authorized boundary resolves the named level and actual responsibility
before creation, then shows the final level, responsibility, provider, model,
parameters, object source, and configuration-file source. It verifies provider,
model, parameter, account/actor, and target support through the intended native
route. On a supported Codex OpenAI route, map `model` to the native `model`
field and `parameters.reasoning_effort` to `thinking`; use another provider or
parameter only when that exact route supports it. Stop rather than substitute
a different route or value. Record requested delivery values separately from
runtime-observed identity when the runtime does not expose the latter.

A later file edit affects only a later, newly resolved task or delivery. It does
not change an existing primary task or role, a frozen delivery, or
same-combination recovery. This contract is an instruction-time read, not a
file watcher, background component, or general model gateway.

## Planner, Executor, And Reviewer (`L3`)

Use `L3` only after approval when independent contract ownership or assessment
materially protects implementation. The Planner owns the active Charter,
clarification, review routing, correction direction, and target acceptance and
remains read-only while assessing. The Executor owns only authorized
implementation, verification, evidence, and implementation documentation. The
Reviewer independently inspects a stable checkpoint and its necessary semantic
context, reports actionable findings and coverage limits, and never modifies
the reviewed target.

Keep at most one Planner, one Executor, one Reviewer for the active package,
one active execution lane, and one repository writer. Reuse reliable role
sessions; do not create roles for implementation slices, documentation sync,
verification reruns, or ordinary repairs. Prefer the same reliable Reviewer
for re-review after repair. Replace it only when its context is unreliable,
the input, permission, or workspace changes materially, independence is
breached, or an explicit blind review is required. Replacement retains the
cumulative findings, authority, and evidence-consumption history.

For a warm handoff, include only receiving role and writer/authority boundary,
changed facts and evidence pointers, bounded action, active stop condition,
and return route. Do not persist it as a competing contract.

Writer ownership is advisory. Before handoff, confirm the prior writer stopped
and capture the dirty boundary. Concurrent or unexplained changes pause
writing, require a delta inventory and one-writer restoration, and invalidate
affected evidence until rechecked.

The normal review path is:

1. the Executor verifies its work and sends one review-ready Result Notice to
   the Planner for a named stable checkpoint;
2. the Planner confirms contract scope, freezes the review input, and routes
   that checkpoint to the Reviewer;
3. the Reviewer returns findings, inspected coverage, exclusions, and
   unresolved `UNKNOWN` facts to the Planner without writing the target;
4. the Planner returns one checkpoint-bound disposition to the Executor;
5. when correction is required, the Executor repairs and verifies a new
   checkpoint, and the same Reviewer re-reviews the affected and cumulative
   material surface; and
6. only after review convergence does the Planner decide target acceptance.

Give the Reviewer the actual change and baseline, necessary surrounding
source, tests, documentation consumers, material untracked inputs, and explicit
generated or cached exclusions. A code or impact graph may guide inspection
only when its repository, baseline, checkpoint, freshness, changed paths, and
limitations are known. A read-only Reviewer does not silently build or refresh
an index. Hashes, graphs, diff size, clean status, tests, and implementation
reports are evidence; none replaces semantic review or acceptance.

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
checks, failures, and residual risks. The Reviewer returns technical findings
and coverage limits to the Planner. The Planner returns exactly `ACCEPTED`,
`CORRECTION_REQUIRED`, or `DECISION_REQUIRED` to the Executor and owns the
acceptance decision. Bind review and correction history to the same logical
Charter subject and material contract/acceptance revision, and bind each
finding and verdict to the stable checkpoint it assessed. Task, Session, root,
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

Send at most one current Result Notice per route for one checkpoint. Do not
resend an unchanged checkpoint, mirror a finding or verdict, poll another role,
or require an acknowledgement to keep the loop alive. A correction or other
material input change creates a new checkpoint and one new Notice while the
prior Notice, findings, and disposition remain part of cumulative history.

When a finding or result is `UNKNOWN`, the Planner or primary owner first
examines the raw terminal result and nearby counterexamples already inside its
authorized read scope. Ask the Reviewer to clarify its existing evidence when
that does not broaden scope or mutate state. Escalate only when resolving the
unknown requires broader authority or would materially change contract,
permission, acceptance, cost, risk, or another user-owned boundary. Never
rerun consequential, scarce, one-shot, or unauthorized evidence merely to
replace a missing terminal result.

Assign each material user question one semantic owner at a stable decision
locator and revision. A non-owner may forward that exact question or relay the
user's exact answer and authority anchor once to the owner. It must not ask a
parallel version, reinterpret the answer, claim a second approval, or create a
fresh decision merely because the carrier task changed. Transfer ownership
only when authority or reliable context changes, and preserve the predecessor
locator. A materially changed question supersedes the old revision and returns
to the user once through the new owner.

Reuse valid authorization across role, task, Session, or Harness carriers only
while the authorized action, subject, actor class, effect, and material risk
boundary remain unchanged. A carrier change does not invalidate authority, but
neither does an upstream approval bypass a direct permission gate imposed by
the environment that will perform the operation. When that environment
requires direct consent, the action or permission-gate task becomes the
semantic owner of the operation-local permission question: it presents the
complete actor, target, action, effect, recovery, and exclusion boundary to the
user and receives the answer directly before acting. An upper role may supply
the governing contract and authority anchor, but its relay, delegation, status
report, or interpretation is not the required direct answer.

This operation-local ownership does not transfer higher-level decisions. Any
change to contract, scope, acceptance, workspace, external effect, cost, or
material risk still returns to the corresponding Planner, Orchestrator, or
user-owned decision locator. Reporting that permission is blocked does not
transfer the question, and receiving operation-local permission does not grant
a replan. A read-only Reviewer or evidence collector reports the need and
evidence boundary; it never asks for or receives write, mutation, installation,
publication, or other execution authority.

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
