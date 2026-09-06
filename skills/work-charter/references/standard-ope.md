# Standard Orchestrator/Planner/Executor/Reviewer (`L4`)

Use Standard O/P/E/R for consequential multi-phase project governance only when
an applicable approved standing policy, active Charter, and discoverable
durable control location support it. `L4` is internal shorthand; Standard
O/P/E/R is the public name.

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

Before each newly authorized Standard role delivery, the dispatcher applies
the strict source priority, whole-role replacement, schema validation, native
capability check, and visible resolved-value requirements in
[Role-Model Configuration At Dispatch](coordination-and-recovery.md#role-model-configuration-at-dispatch).
The package [default configuration](../assets/role-models.default.yaml) is the
sole default data owner. A frozen approved delivery combination remains in
force, and configuration never supplies delivery or action authority. Existing
roles do not change when a configuration file changes.

## Responsibilities

| Role | Owns | Does not do |
|---|---|---|
| Orchestrator | Project direction, phase order, mandates, project-level acceptance, and transitions | Implement work, direct the Executor or Reviewer, or repeat technical review |
| Planner | Active Charter, execution boundaries, Executor and Reviewer routing, correction direction, and target acceptance | Implement, repair, or technically review the work under assessment |
| Executor | Authorized implementation, verification, evidence, and implementation documentation | Expand scope, select a new phase, review its own work, or approve its own result |
| Reviewer | Read-only semantic inspection of a stable checkpoint, actionable findings, and explicit coverage limits | Modify the reviewed target, direct project scope, or decide target or phase acceptance |

The Orchestrator normally remains dormant during phase execution. Keep one
active lane, one repository writer, at most one Planner, at most one Executor,
and one reliable Reviewer for the active package.

The portable responsibility hierarchy is:

```text
Orchestrator -> Phase Mandate
Planner -> Phase Definition
Planner -> Executor execution tranche or work package
Executor -> internal steps or slices
Planner -> Reviewer stable review checkpoint
Reviewer -> Planner findings and coverage limits
```

Executor-internal steps or slices are not separate Definitions, roles, or
approval gates. Standard normally has two user-owned contract gates per phase:
the Mandate and the Phase Definition. This hierarchy applies only when Standard
is already applicable and approved; ordinary and single-Agent work remains
flat.

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
4. The Executor implements only that work, may organize it into internal steps
   or slices without another Definition or approval gate, verifies it, and
   returns one review-ready Result Notice to the Planner for a named stable
   checkpoint. It then stops polling and remains idle.
5. The Planner confirms that checkpoint matches the contract, freezes the
   review input and exclusions, and routes it to the Reviewer. The Reviewer
   inspects the actual change, necessary semantic context, tests,
   documentation consumers, material untracked inputs, and declared graph or
   generated-artifact limits, then returns findings and coverage to the
   Planner without modifying the target.
6. The Planner returns exactly one checkpoint-bound `ACCEPTED`,
   `CORRECTION_REQUIRED`, or `DECISION_REQUIRED` disposition to the Executor.
   Same-scope corrections or a listed next tranche may continue there;
   terminal acceptance or decision-required sends a no-action disposition and
   requires no acknowledgement. When correction is required, the Executor
   repairs and verifies a new checkpoint and the same reliable Reviewer
   re-reviews the affected and cumulative material surface before Planner
   acceptance. Reviewer replacement requires an unreliable context, material
   input/permission/workspace change, breached independence, or an explicit
   blind-review rule and never resets history.
7. Before the Orchestrator relies on Planner acceptance, the next authorized
   governance writer records and verifies the verdict and evidence pointer in
   the target project's canonical owner. Otherwise report recording as pending
   and stop.
8. The Planner returns its phase-level Result Notice to the Orchestrator. The
   Orchestrator assesses project direction and transition without duplicating
   implementation review, then returns exactly one checkpoint-bound
   disposition to the Planner. It never contacts the Executor directly.
   Record and verify that read-only assessment before another session or phase
   transition relies on it.
9. An unapproved phase, material replan, permission change, or residual-risk
   decision returns to the user.

Use durable state for cold or recovery entry and compact warm handoffs while
role sessions remain reliable. Work Charter cannot guarantee role delivery,
writer locking, message finality, graph completeness, or compliance. Treat
`UNKNOWN` as an evidence question first: inspect raw terminal evidence and
nearby counterexamples already within scope, then escalate only if the missing
fact requires broader authority or changes a protected boundary. Report
capability degradation honestly and stop for material control, delivery,
writer, review-input, or evidence ambiguity. For every route, send at most one
current Notice per checkpoint and one returned disposition; never poll, mirror
the result, or require acknowledgement.
