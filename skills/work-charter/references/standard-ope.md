# Standard Orchestrator/Planner/Executor/Reviewer (`L4`)

Use Standard O/P/E/R for consequential multi-phase project governance only when
an applicable approved standing policy, active Charter, and discoverable
durable control location support it. `L4` is internal shorthand; Standard
O/P/E/R is the public name.

A fresh L4 role loads the complete slim shared Skill body and this reference's shared entry,
responsibility, single-writer and permission boundaries, then its own operating
steps and handoff interfaces. It does not load every other role's procedures
or repeat adoption merely because it is a new Thread. Manual reassessment uses
the current Charter and policy as its baseline; material changes remain
user-owned. Valid continuity never implies automatic role creation.

Initial persistent adoption and the first Standard standing policy are
user-owned decisions. Later reuse must name the policy and exact bounded read
scope being reused, remain visible to the user, and stay subordinate to
Harness and project instructions. Policy or level selection does not authorize
role delivery, writes, project-document or `AGENTS.md` changes, worktrees,
Git, integration, installation, cleanup, publication, or external effects.

If governing instructions require fresh selection, the control location or
revision cannot be reconciled, or separate role delivery is unavailable or
uncertain, propose the smallest transition and stop. Do not represent a
one-agent fallback as Standard.

Before each newly authorized Standard role delivery, identify `L4` and the
actual responsibility, then read and apply
[Role-Model Configuration At Dispatch](coordination-and-recovery.md#role-model-configuration-at-dispatch).
That section is the sole owner of configuration resolution and validation;
do not reconstruct a parallel lookup here. Preserve frozen combinations,
require native support, and keep requested values separate from runtime
identity. Configuration never authorizes delivery or action, enables a role,
or changes an existing task.

## Responsibilities

| Role | Owns | Does not do |
|---|---|---|
| Orchestrator | Project direction, phase order, mandates, project-level acceptance, and transitions | Implement work, direct the Executor or Reviewer, or repeat technical review |
| Planner | Active Charter, execution boundaries, Executor and Reviewer routing, correction direction, and target acceptance | Implement, repair, or technically review the work under assessment |
| Executor | Authorized implementation, verification, evidence, and implementation documentation | Expand scope, select a new phase, review its own work, or approve its own result |
| Reviewer | Read-only semantic inspection of a stable checkpoint, actionable findings, and explicit coverage limits | Modify the reviewed target, direct project scope, or decide target or phase acceptance |

The Orchestrator normally remains dormant during phase execution, handling
only direction, cross-phase dependencies, material project risk and phase
acceptance. The Planner owns in-phase decisions and stable acceptance; preauthorized
ordinary repairs close through E and R without per-round Planner intervention. Keep one
active lane, one repository writer, at most one Planner, at most one Executor,
and one reliable Reviewer for the active package.

The portable responsibility hierarchy is:

```text
Orchestrator -> Phase Mandate
Planner -> Phase Definition
Planner -> Executor execution tranche or work package
Executor -> internal steps or slices
Planner -> Reviewer stable review checkpoint
Reviewer -> Executor preauthorized same-scope findings; otherwise Planner
Reviewer -> Planner stable findings and coverage limits
```

Executor-internal steps or slices are not separate Definitions, roles, or
approval gates. The user approves the Mandate. It may explicitly delegate
in-bound Definition finalization and specified E/R delivery to P; otherwise
the Definition remains a separate user gate. Missing material choices keep
the Mandate planning-only. Existing approvals are not expanded retrospectively.
See [Delegated Decisions And Escalation](coordination-and-recovery.md#delegated-decisions-and-escalation).
This hierarchy applies only to approved Standard work; ordinary work remains flat.

Build role prompts from the
[shared contract, actual responsibility, current task, and necessary model adaptation](coordination-and-recovery.md#task-and-role-prompt-construction).
Include only the receiver's authorized responsibilities and current work.
Warm continuations reuse a valid contract and send the delta without another
prompt approval or role for an internal step. Model and effort selection never
changes O/P/E/R permissions, independent review, or acceptance boundaries.

Reviewer findings are technical evidence, while Planner and Orchestrator
assessments are role verdicts rather than extra user confirmation gates. The
Orchestrator owns questions about project
direction, cross-phase risk, the next phase, or a Mandate. The Planner owns
questions about the active Phase contract, workspace, acceptance, and residual
risk. The Executor reports a permission blocker to the Planner unless the
execution environment requires the action task to obtain operation-local
permission directly. In that case the action task presents the complete
permission question and receives the answer itself; a Planner relay or status
report is not a substitute. This does not transfer contract or scope ownership,
and a changed Phase boundary still returns to the Planner. The Reviewer reports
technical unknowns and findings rather than asking for write authority. A
separately governed specialist likewise owns only a directly required
operation-local permission question. Non-owners relay an exact question or
answer once and never mirror it.

## Operating Path

1. Reconcile the one authoritative control location, its standing-policy and
   Charter revisions, managed workstream, workspace/writer boundary, and named
   evidence using [Coordination And Recovery](coordination-and-recovery.md).
2. The Orchestrator bounds project direction and the current phase outcome.
3. The Planner makes the active Charter implementation-ready and identifies
   authorized execution tranches or work packages, writer, evidence, and stop
   conditions.
4. The Executor continuously completes that work, necessary checks and
   implementation documentation. Preparation, individual checks and ordinary
   repairs do not create acceptance checkpoints. It may organize internal steps
   or slices and choose ordinary files, tools and check order within the approved
   outcome, domain, environment, effects and cost without another Definition or
   approval gate. Explicit dependencies, frozen evidence and protected effects
   still bind. It verifies the package, and
   returns one review-ready Result Notice to the Planner for a named stable
   checkpoint. It then stops polling and remains idle.
5. The Planner confirms that checkpoint matches the contract, freezes the
   review input and exclusions, and routes it to the Reviewer. R inspects the
   actual change, necessary semantic context, tests, documentation consumers,
   material untracked inputs and graph/generated limits without writing.
6. Follow the approved correction route in
   [Planner, Executor, And Reviewer](coordination-and-recovery.md#planner-executor-and-reviewer).
   Preauthorized ordinary same-scope findings go from R to the original E;
   E repairs and verifies, and the same reliable Reviewer re-reviews the
   affected and cumulative material surface. No per-round P approval is needed.
   Without preauthorization, or for disputes, nonconvergence, uncertain
   authority or material risk, return to P. At convergence or an exception,
   P checks independence, coverage and contract fit without repeating technical
   review, then returns exactly one checkpoint-bound `ACCEPTED`,
   `CORRECTION_REQUIRED`, or `DECISION_REQUIRED` disposition to E. Acceptance
   stays with P; R never repairs or accepts. Terminal dispositions need no ACK.
   Reviewer replacement requires a material reliability, independence or
   contract reason and never resets cumulative history.

7. Keep the formed verdict and its recording state separate. With governance
   write authority, the Planner records its verdict after assessment and the
   Executor's writer relinquishment. If only the Executor may write, include
   that mechanical record update and its checks in the disposition or closeout.
   Before another session relies on durable acceptance, the authorized writer
   records and verifies the verdict and evidence pointer in the canonical owner;
   otherwise report recording as pending. The Executor never prewrites a future
   verdict. Fix record errors as records, returning to the relevant gate only
   for changes to contract, risk or acceptance meaning. Git review still applies.
8. The Planner returns its phase-level Result Notice to the Orchestrator. The
   Orchestrator assesses project direction and transition without duplicating
   implementation review, then returns exactly one checkpoint-bound
   disposition to the Planner. It never contacts the Executor directly.
   Record and verify that assessment through the same authorized writer rule
   before another session or phase transition relies on its durable state.
   Define the final records, checks, remaining authorized actions and writer
   state; a factual recording-complete notice does not start another acceptance
   loop. Cross-project status receipt alone adds no acceptance layer; an explicit
   existing layer changes only through the user's contract decision.
9. An unapproved phase or change beyond delegated outcome, permission, cost,
   effect, risk or acceptance authority returns to the user through its owner.
   In-bound P choices do not automatically require O or user approval.

Use durable state for cold or recovery entry and compact warm handoffs while
role sessions remain reliable. Work Charter cannot guarantee role delivery,
writer locking, message finality, graph completeness, or compliance. Treat
`UNKNOWN` as an evidence question first: inspect raw terminal evidence and
nearby counterexamples already within scope, then escalate only if the missing
fact requires broader authority or changes a protected boundary. Report
capability degradation honestly and stop for material control, delivery,
writer, review-input, or evidence ambiguity. Return a disposition for a required
decision to the role that acts on it; factual and evidence notices need no pure
acceptance receipt. Do not relabel a decision to bypass its gate. Never poll,
mirror the result or require acknowledgement. Recover current rules only before
the next affected work; idle roles are not broadcast-woken by text changes.
Harness loading proof and explicit frozen fresh-run contracts retain their
separate requirements under the shared recovery boundary.
