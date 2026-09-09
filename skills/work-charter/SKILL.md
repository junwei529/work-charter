---
name: work-charter
description: Bound Codex work by an applicable approved Charter, proportional L0-L4 assessment, authority, evidence, recovery, and independent review. Reuse a valid Charter and level for the same workstream without activation or level reselection, including small tasks. Use for direct assessment or reassessment requests and material continuity, writer, authorization, or recovery needs. First assessment recommends a user-owned level; reassessment starts from the existing contract. Load the full body before using this guidance and only relevant reference sections. Loading or assessment is not adoption or action authority. Without an applicable Charter or assessment request, do not select merely for small tasks, one failure, duration, documentation, shell diagnosis, or non-Codex adaptation.
---

# Work Charter

Keep the contract smaller than the work it protects. Work Charter is advisory:
it can recommend and stop its own work, but it cannot lock writers, reroute
other tasks, or enforce permissions.

## Enter With Progressive Authorization

Load the full Skill first when entering assessment, reassessment, or an
authorized continuation. Native catalog selection or body loading is an
instruction mechanism, not adoption or action authority. If the body cannot
load, report degraded loading and do not claim to apply Work Charter. Preserve
an unexposed loaded path or revision as `UNKNOWN`; do not invent exact-copy
proof or claim that this package forces every Harness to preload it.

Use supplied context and already-authorized bounded reads to distinguish:

1. **Applicable approved Charter:** reconcile its workstream, revision, level,
   authority, and live state. When they align, reuse the approved Charter and
   level without asking again to activate or select a level. Small-task
   exclusions do not cancel an applicable Charter. State the reused contract
   and next authorized action briefly. A new Thread alone does not require
   adoption again; use the existing re-entry routes for material drift.
2. **First assessment:** when no approved Charter applies, a new-work or manual
   assessment request evaluates L0-L4 and recommends the least sufficient
   level with its cost. The user chooses the level to adopt. A direct
   `$work-charter` invocation requests this assessment unless it explicitly
   requests reassessment or continues an applicable approved Charter.
3. **Manual reassessment:** start from the existing Charter and level, compare
   the requested change with that baseline, and recommend retaining or
   changing it. Keep valid authority; material level, permission, or contract
   changes require the user's decision before dependent work.

An assessment request is not adoption. `L0` has no active Charter. A Charter
is active only when its adopted L1-L4 contract applies and the full body is
available. Do not claim active, adopted, or in-force status from a symptom,
catalog entry, file presence, or mere invocation. An indirect match without an
applicable Charter may propose assessment; do not silently adopt a level,
establish roles, or impose new writer, pause, or handoff duties.

Before project inspection, identify the smallest useful scope: declared rules
and canonical owners, one declared Charter carrier (or one exact root fallback
check), relevant workspace/branch/dirty/writer facts, and named evidence.
Reuse existing read approval within its scope. An authorized bounded read-only
assessment needs no separate activation or repeated read approval, even before
adoption. If authority is missing, ask only for that exact read or material
decision. An explicit no-read instruction remains binding. Continue otherwise
authorized work that does not depend on a pending adoption decision.

Package loading never expands project-read or action authority. Read only the
reference sections needed by this level, responsibility, and next action;
those package reads do not consume target-project read approval. First
persistent adoption and the first Standard standing policy remain user-owned.
Assessment or read approval does not authorize adoption, writes, roles, Git,
installation, global changes, or external effects.

If an approved read cannot be completed through the approved route, preserve
the affected fact as `UNKNOWN` and stop its dependent work. Do not broaden the
scope, search neighboring or hidden sources, or change routes to compensate.
Propose any required broader read or different route explicitly.

## Recommend The Least Sufficient Protection

Explain the recommendation and its cost, then leave the choice to the user.
Use plain language first; the level codes are internal shorthand:

- ordinary flat task (`L0`): no active Charter; a separate review gate can
  still apply without activating or escalating Work Charter;
- current-task Charter (`L1`): one primary owner and a bounded contract in the
  current task, without a cold-recovery promise; a bounded independent
  Reviewer may inspect a stable checkpoint;
- durable single-owner Charter (`L2`): one primary owner plus one small
  persistent recovery anchor and the same optional review boundary;
- Planner/Executor/Reviewer separation (`L3`): durable recovery plus an
  independent Planner/assessor, sole-writer Executor, and read-only technical
  Reviewer; or
- Standard O/P/E/R (`L4`): `L3` plus Orchestrator responsibility, an
  applicable standing policy, and multi-phase governance.

Do not infer a level from model name, task length, file count, branch count, or
elapsed time. Inspect only environment capabilities the Harness exposes within
the approved scope, preserve `UNKNOWN`, explain material capability effects,
and do not silently auto-adapt. A level adds protection and cost, not action
authority.

## Resolve Role Models At The Delivery Boundary

Role-model configuration guides an already-authorized dispatcher; it never
authorizes creating a role, changing a responsibility, or widening any read,
write, Git, installation, network, provider, credential, or external-effect
boundary. The package's sole default data owner is
[the default role-model configuration](assets/role-models.default.yaml).
`agents/openai.yaml` remains Harness UI metadata and is not a role-model
selector.

Before resolving a newly authorized task or role, identify its protection level
and actual responsibility, then read
[Role-Model Configuration At Dispatch](references/coordination-and-recovery.md#role-model-configuration-at-dispatch).
That reference owns the complete priority, whole-object replacement, source
selection, schema validation, unknown-input rejection, and native mapping
contract. Follow it before reading configuration or creating the authorized
task; unavailable or incomparable required input stops dispatch.

Preserve frozen delivery combinations and existing tasks. Configuration
changes affect only later, newly resolved tasks or deliveries. Configuration
never creates roles or supplies action authority. `L0` remains no active
Charter, even when a host uses this interface. The package does not prove that
any host or global task-start consumer has integrated it. Installation lifecycle
operations do not own or mutate the external user configuration.

## Compose Prompts From Contract, Responsibility, And Task

Build one prompt from the shared contract, actual responsibility, current task,
and only necessary model adaptation. Keep authoritative constraints and result
routes explicit; use pointers to unchanged context instead of copied rules,
logs, or nested delegation envelopes. Add the receiving role's work and output,
not every other role's procedure. The detailed construction guidance is in
[Coordination And Recovery](references/coordination-and-recovery.md#task-and-role-prompt-construction).

Carry already-authorized work through its required checks and handoff. Routine
implementation choices, internal steps, and same-scope corrections do not need
another confirmation when the contract and guardrails still cover them.
Preserve genuine adoption, permission, review, and acceptance gates;
make a pending user decision concrete using authorized independent work, then
wait before the dependent action. A Working Proposal stays replaceable even
when it appears in a template or handoff.

Complete the required verification and checks appropriate to the changed
behavior. Broaden or repeat them only for changed inputs, failures, or unresolved
material risk; do not add repeated passes or model evaluations merely to make
the prompt look thorough. Preserve producer-before-consumer dependencies and
evidence identity. Keep reasoning effort in supported runtime parameters, not
in a separate prompt for each effort setting.

## Establish One Authoritative Carrier

Make these logical responsibilities discoverable without requiring fixed
headings or a separate file:

1. intended outcome and non-goals;
2. scope and hard boundaries;
3. authorization, including material writes and external effects;
4. acceptance evidence and verification expectations; and
5. stop, decision, and recovery conditions.

Every `L1` or stronger run needs a logical Charter locator. `L1` may keep it in
the current task. `L2`-`L4` require one discoverable durable anchor: a compact
pointer to applicability, authority/revision, responsibilities, workspace and
writer, checkpoint/evidence, next action, and reconfirmation conditions.
Prefer a suitable existing canonical owner and never maintain competing
normative copies. Adapt [the Work Charter asset](assets/work-charter.md) only
when no suitable carrier exists and a separate write is authorized.

`/plan` may help draft a Charter. `/goal` may optionally track an approved
objective and pointers. Neither is Work Charter, a canonical owner, execution
authority, verification, or acceptance.

## Protect The Contract, Keep The Proposal Flexible

When proposing consequential work, distinguish four layers:

1. **Confirmed Contract** — user-confirmed outcomes, acceptance, and exclusions;
2. **Necessary Guardrails** — safety, permission, reversibility, trust,
   irreversible-effect, and authoritative project-rule constraints, with the
   source or protected risk made clear;
3. **Working Proposal** — the Agent-proposed route, tools, sequence,
   implementation, and verification; and
4. **Assumptions / Open Decisions** — uncertainty, returning only material
   choices to the user.

For an Agent-derived guardrail, explain the concrete failure and consequence,
the protection strength needed, and why a simpler existing method is
insufficient. A guardrail label, tool promise, or general implementation
approval does not establish necessity. Explicit user or project requirements
remain valid under their existing contract without an extra burden of proof.

An Agent-proposed method does not silently become a hard requirement. Change
an ordinary Working Proposal without renewing the Charter when the Confirmed
Contract, Necessary Guardrails, interfaces, risk, permissions, external
effects, acceptance, workspace, and integration policy remain unchanged.
Remove or replace a rejected Agent invention instead of preserving it as a
durable non-goal. Read
[Coordination And Recovery](references/coordination-and-recovery.md) for the
material-change and convergence boundary.

## Separate Verification, Technical Review, And Acceptance

Keep three different responsibilities visible. The implementer verifies the
work it changed. An independent Reviewer inspects the stable change and its
necessary semantic context for defects, returns actionable findings plus
coverage limits, and does not modify the reviewed target. The designated
assessor decides whether the outcome and evidence satisfy the contract; tests,
Reviewer output, and an implementation report remain evidence rather than
acceptance by themselves.

Use an independent Reviewer when the user requests one, an applicable project
or delivery gate requires one, or a stable material change affects a protected
security, permission, data-loss, public-interface, core-decision, or similarly
consequential boundary. A bounded review at `L0` does not activate Work Charter,
and a temporary Reviewer at `L1` or `L2` does not create a Planner/Executor
workflow. Without a separate Planner, the primary owner dispositions findings,
repairs and verifies the work, and delivers it, but does not call its own
decision independent acceptance.

At `L3` and `L4`, the Executor implements and verifies, the Reviewer performs
read-only technical review, and the Planner owns target acceptance and the
same-scope correction loop. The Orchestrator at `L4` owns project direction and
phase acceptance without repeating technical review. Prefer the same reliable
Reviewer for repair rechecks within one work package, retain cumulative
findings and coverage, and replace that Reviewer only when context becomes
unreliable, the input, permission, or workspace changes materially, review
independence is breached, or an explicit blind review is required. Replacement
does not reset history, authority, or consumed evidence.

Give review the actual change, baseline, necessary surrounding source, tests,
documentation consumers, material untracked inputs, and explicitly excluded
generated or cached artifacts. Existing code or impact-graph results may guide
coverage only when their repository, baseline, checkpoint, freshness, changed
paths, and limitations are known. A read-only Reviewer does not silently build
or refresh such an index. Hash, graph, diff size, or a clean status cannot
replace semantic inspection.

When a result is `UNKNOWN`, the assessor or primary owner first checks the raw
terminal evidence and nearby counterexamples that are already inside its
authorized read scope. Escalate only when the missing fact requires broader
authority or would materially change the contract, permission, acceptance,
cost, or another user-owned boundary. Never rerun a command merely to replace
a missing terminal result when that rerun is separately consequential,
scarce, one-shot, or unauthorized.

## Reconcile Before Continuing

Each fresh Thread or role applying this guidance must load the full Skill
body, including its shared authority, safety, evidence, and recovery
boundaries. A handoff summary is not loaded-copy proof. Existing valid adoption
authorizes continuation without another activation question; loading does not
renew or expand the contract.

Use [Coordination And Recovery](references/coordination-and-recovery.md) by
section: minimum reconciliation, applicability and re-entry for first
assessment or continuation; durability for L2-L4; context-switch recovery when
recovering; and shared L3 role/writer/review boundaries for L3-L4. Read the
operating details needed by your own responsibility and its handoff interfaces,
not every other role's procedure. A dispatcher resolving a newly authorized
delivery reads the complete configuration section before using that interface;
other roles do not load configuration just because it is in the same file.

An L4 role also reads the shared entry and responsibility boundaries in
[Standard O/P/E/R](references/standard-ope.md), then the operating steps for
its own work and required interactions. Leave the Standard reference unloaded
for L0-L3 by default. A scoped evaluation of a transition to L4 may read the
needed sections without authorizing the transition. Do not skip a shared
permission, independent-review, writer, or recovery boundary to save context.

Match the named managed workstream, not the whole repository, and compare the
carrier revision with live workspace, writer, dirty ownership, evidence
freshness, and the latest applicable authority. An old task, marker, branch,
or elapsed time is not proof of conflict or adoption.

Return exactly one user-facing route, using this precedence:

1. **Stop safely** (`fail closed`) when authority or live state cannot be
   compared reliably.
2. **Revise the work contract** (`revise Charter`) when outcome, boundaries,
   acceptance, permission, material effects, or the canonical carrier change.
3. **Change how work is coordinated** (`change coordination`) when the
   contract remains stable but level, role, writer, workspace, delivery, or
   integration routing changes materially.
4. **Continue the existing plan** (`resume`) when the workstream, contract,
   coordination, authority, and live state still align.

Evidence refresh is a prerequisite to `resume`, not a fifth route. Request its
own authority when it writes, costs, uses sensitive data, crosses an external
boundary, consumes a budget, or repeats a one-shot operation.

Project Docs is an optional independent peer: consume reliable locators when
present, but do not require or automatically invoke it.

## Reload Changed Governing Rules

When a material governing instruction or Skill-package source changes, an old
Session may reread it for context and finish an already-permitted closeout, but
that reread is not proof that the Harness rebuilt or freshly loaded the changed
instruction chain. Before the next affected action relies on the new rules,
use a fresh Session or run, identify the applicable sources, record their
normalized-text identities, and requalify only the conditions affected by the
change. Do not treat a renamed task, refreshed summary, or manual reread as a
ruleset reload.

## Recover After A Context Switch

A context switch can be a summary or compaction inside one run, a deliberate
rotation to a fresh context, or a new or successor session. Treat those as
different mechanisms, but preserve the same work subject, role, contract,
writer boundary, findings, permissions, and evidence history whenever their
material identity remains unchanged. A product label or enabled setting does
not prove which mechanism occurred or that every fallback path was disabled.

Before a foreseeable switch, persist the smallest current checkpoint in the
existing authoritative carrier: contract and revision, role and writer,
workspace, reviewed input, open findings, evidence and invalidation condition,
returned disposition, and next authorized action. After the switch, reload the
current contract and that checkpoint, reconcile them with live state, and read
only the missing evidence needed to continue. Do not replay the whole prior
conversation, use memory as a substitute for authority, or treat a fresh
container as a reset of approvals, corrections, stops, or consumed evidence.

## Assess And Stop

When auxiliary repair or coordination keeps expanding, the current primary
owner or Planner reassesses the minimum sufficient user-visible outcome and
the remaining coordination, implementation, verification, and maintenance
cost. Compare simpler routes to the same protected outcome; a tool's own
promises do not become new user goals. Use the existing contract-change rules
for material decisions, without adding a role, form, or approval gate.

Create a separate technical review or assessment only when its governing gate
requires it. Keep the Reviewer and assessor distinct unless the contract
explicitly combines them without weakening independence. Record assessment
scope, owner, evidence pointers, material residual risks, return route, and
exactly one verdict: `ACCEPTED`, `CORRECTION_REQUIRED`, or
`DECISION_REQUIRED`. Passing tests, Reviewer output, Goal completion, a commit,
role delivery, or an Executor report is evidence, not acceptance.

Every Result Notice receives exactly one checkpoint-bound disposition back
through its declared return route. Name the notice recipient as part of that
route contract. When independent assessment is required, the assessment owner
produces that disposition; otherwise the named notice recipient does. The
allowed returns include terminal `ACCEPTED` with no next action and
`DECISION_REQUIRED`. A missing, wrong, duplicate, or stale return remains
awaiting verdict, not accepted. A terminal disposition grants no new action
and requires no acknowledgement.

Send at most one current Result Notice for one checkpoint. Do not resend the
same checkpoint, mirror a verdict, poll the other role, or require an
acknowledgement merely to keep the loop alive. A corrected or otherwise changed
input creates a new checkpoint and one new Notice while retaining the prior
finding and disposition history.

Give each material user decision one semantic owner. Other roles may relay the
exact question or answer and its authority anchor, but must not mirror the
question, reinterpret the answer, or consume the same approval again.
Reuse a still-valid authorization when the governed action, subject, and risk
boundary are unchanged. When the execution environment requires the task that
will perform an operation to obtain permission directly, that action task must
present the complete operation-local question and receive the answer itself;
an upper-role relay or status report cannot substitute for that direct gate.
Contract, scope, and higher-risk changes remain with their existing semantic
owner. A read-only Reviewer or evidence collector never solicits write
authority.

Before another session relies on a material decision or assessment, verify its
authoritative revision and required durable recording. Stop when contract,
permission, workspace, writer, evidence, delivery, or recovery state is
materially ambiguous.
