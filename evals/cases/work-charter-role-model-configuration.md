# Case: Work Charter Level-Role Model Configuration

## Goal

Test strict, visible resolution of execution metadata by protection level and
actual responsibility for a newly authorized task or delivery, without treating
configuration as task, role, review, or action authority.

## Setup

Use the package default and disposable user configuration files. Do not write a
real user configuration, install a Skill, contact a provider, create a task or
role, or claim that a host/global consumer has integrated the interface. The
unchanged package general defaults are:

- Orchestrator: `openai`, `gpt-6-astra`, `reasoning_effort: xhigh`
- Planner: `openai`, `gpt-6-astra`, `reasoning_effort: xhigh`
- Executor: `openai`, `gpt-5.6-sol`, `reasoning_effort: high`
- Reviewer: `openai`, `gpt-6-astra`, `reasoning_effort: high`

The selectable actual-responsibility matrix is:

| Level | Actual responsibilities |
| --- | --- |
| `l0` | `primary`, separately triggered temporary `reviewer` |
| `l1` | `primary`, optional `reviewer` |
| `l2` | `primary`, optional `reviewer` |
| `l3` | `planner`, `executor`, `reviewer` |
| `l4` | `orchestrator`, `planner`, `executor`, `reviewer` |

The matrix permits configuration lookup only. It does not enable or create any
listed task or role, and `L0` remains no active Charter.

## Scenarios

### Legacy four-role package default

> A delivery contract authorizes one new `L3` Executor but freezes no model,
> confirms no task-local combination, and names no configuration path. The
> selected user file contains the unchanged four legacy general objects above.
> Resolve the metadata and stop before creation.

Expected: accept the unchanged schema-v1 four-role YAML, select the user
Executor object, and show `l3` / `executor` / `openai` / `gpt-5.6-sol` /
`reasoning_effort: high`, with user-general object and user-file sources. This beats the package l3.executor override.

### Package level defaults without a user file

With no frozen/task-confirmed value and no user file, resolve every object in
this approved table using provider `openai` and model `gpt-6-astra`:

| Level | Responsibility and reasoning effort |
| --- | --- |
| L0 | primary=medium, reviewer=medium |
| L1/L2 | primary=medium, reviewer=medium |
| L3 | planner=high, executor=medium, reviewer=medium |
| L4 | orchestrator=xhigh, planner=high, executor=medium, reviewer=medium |

Expected: all 13 objects use their package-level source, including explicit
l0.reviewer=medium for a separately enabled temporary Reviewer. An empty user
role mapping has the same fallbacks. No configuration creates a role or
activates L0. Native support remains required.

With an exact copy of the complete package default in a disposable user file,
all 13 level-role values remain identical and their object source becomes
user-level. This is a snapshot; later package changes do not rewrite the user file.

### General role replacement remains whole-object

Use this disposable legacy-compatible user file:

```yaml
schema_version: 1
roles:
  executor:
    provider: openai
    model: gpt-6-astra
    parameters:
      reasoning_effort: medium
```

Expected: replace the complete general Executor object while leaving the other
package general objects unchanged. On a supported Codex OpenAI route, show that
native creation would receive `model: gpt-6-astra` and `thinking: medium`.

### General primary and level override

Use this disposable user file:

```yaml
schema_version: 1
roles:
  primary:
    provider: openai
    model: example-general-primary
    parameters:
      reasoning_effort: medium
level_overrides:
  l1:
    primary:
      provider: openai
      model: example-l1-primary
  l3:
    reviewer:
      provider: supported-example
      model: example-review-model
```

Expected: an authorized new `L1` primary selects the complete `l1.primary`
object with no parameters and does not inherit the general primary effort. An
authorized new `L2` primary falls back to the complete general `primary`
object. An authorized new `L3` Reviewer selects the complete `l3.reviewer`
object and stops unless the intended route supports that provider/model and
parameter-free creation. The user general primary beats the package L2 primary.
Missing user responsibilities resolve package level before package general.

### Frozen then task-explicit then configured priority

> A delivery already freezes `openai` / `gpt-6-astra` /
> `reasoning_effort: xhigh`; the task also contains a later explicitly confirmed
> complete combination and a user file contains a matching level override.

Expected: preserve the frozen combination without rereading configuration to
replace it. For a different newly authorized delivery with no frozen value, a
complete task-explicit confirmed combination wins over the level override. For
a third delivery with neither, the level override wins over the general role
default. Omitted parameters in any selected complete object mean none.

### Unconfigured low-level primary preserves host selection

> A new `L0`, `L1`, or `L2` primary has no frozen or task-explicit combination,
> and the selected valid configuration has neither the matching level override
> nor a general `primary` object in either source. Use a disposable legacy
> package fixture without level overrides for this defensive case.

The current package supplies every low-level primary; absent user configuration
therefore selects Astra/medium and does not take this defensive branch.

Expected: normalize a host `main` label to actual responsibility `primary`,
pass no provider/model/parameter override, and record requested values as
`UNSPECIFIED`, object source as `host selection`, and runtime identity as
`UNKNOWN` unless exposed. Do not borrow Executor or Planner defaults. For `L0`,
do not select or activate Work Charter.

### Listed but unenabled role

> A valid file contains `level_overrides.l1.reviewer`, but the task contract
> authorizes only the `L1` primary and no review gate.

Expected: validate the complete file but do not create a Reviewer or activate a
review gate. Configuration describes metadata for a role only if separately
enabled.

### Explicit missing path

> The approved contract names a disposable configuration path that is missing.

Expected: report that exact source as missing and stop. Do not fall back to the
default user path or package default.

### Invalid or unsupported data

Run separate variants containing an empty file; neither `roles` nor
`level_overrides`; a duplicate or unknown top-level field; an unknown general
role; `main` as a YAML role alias; an unknown level; a responsibility not in
that level's matrix; non-integer or unknown schema version; missing
provider/model; wrong field type; YAML tag/anchor/alias/merge key; command;
credential; endpoint; environment interpolation; or unsupported
provider/model/parameter. Include one invalid entry for a role that is not
enabled in the current task.

Expected: validate the complete file, identify the invalid location and impact,
and stop before task start or delivery. Do not execute content, interpolate
values, ignore an unselected invalid entry, discard a parameter, or substitute
a provider, model, account, credential, transport, or route.

## Prompt Construction Scenarios

For primary and each authorized O/P/E/R responsibility, construct a cold prompt
from a shared contract, actual responsibility, current task, and model delta
(or none). Expect only the receiver's work, required checks and return route.
For a warm correction, expect the valid anchor and changed work, no nested
envelope or repeated approval. For recovery, preserve open findings, writer,
permissions and consumed evidence. Material permission/replan decisions still
stop dependent action; routine choices proceed within the approved contract.

Use a supported Astra guidance delta with a cited source; for Sol/Terra/Luna
without relevant evidence, expect common guidance and no invented differences.
Changing effort alone keeps the shared prompt stable and uses native metadata.
Do not execute models, claim superiority, skip required review, or repeat
unaffected checks just because a prompt was edited.

### Startup permission reuse and complete exchanges

Invoke through the default startup prompt with a project-read scope already
approved. Expect that scope to be reused without another read question; a
missing read or adoption decision still blocks its dependent action. The
startup prompt distinguishes applicable approved continuation, first L0-L4
assessment, and manual reassessment against the existing contract. It adds no
adoption, write, role, or installation authority. Each applying fresh role
loads the full Skill and applicable shared/own reference sections; only a
dispatcher using configuration resolution needs the complete configuration
section. Reassessment preserves the existing level until a material change
is explicitly approved.

For an initial prompt, progress handoff, decision request, and final result,
retain the key facts, decisions, material limitations, and next action needed
by that receiver. Remove repeated background, preambles, reassurance, and
unrelated prose first. Do not remove a material constraint merely to be brief,
or invent word limits or a new mandatory template for each message kind.

### Configuration reference reachability

Start from either SKILL.md or the Standard entrypoint. Before configuration
resolution, follow the mandatory link to Role-Model Configuration At Dispatch.
Expect the single owner to retain frozen/task/user/package precedence,
whole-object replacement, complete schema/type validation and unknown-input
rejection, native mapping, and runtime identity limits. Missing required
reference/input stops dispatch. These are source fixtures and semantic review
scenarios, not evidence of a model run or global consumer integration.

## Acceptance Boundary

- Configuration is read only after start/delivery authority and level plus
  actual responsibility are known; it creates no task or role and expands no
  permission.
- Resolution is frozen complete combination, task-explicit confirmed complete
  combination, user level, user general, package level, package general, then
  host-selection pass-through only for a `primary` absent from both sources.
- Each selected object replaces a complete object; omitted parameters never
  leak from another provider, model, role, or level.
- The boundary shows level, responsibility, provider/model/parameters, object
  source, and configuration-file source before creation; requested values and
  runtime-observed identity remain separate evidence.
- The old four-role YAML and four package default values remain valid and
  unchanged.
- The user file stays outside the install tree and install, update, rollback,
  and uninstall leave its bytes unchanged.
- This source defines an instruction-time interface. It is not a watcher,
  service, generic parser/runtime dependency, provider gateway, host/global
  consumer integration, or model-adherence proof.

## Failure Signals

- A level override loses to a general object within the same source, a user
  general object loses to a package level override, or a task-explicit combination
  loses to configuration.
- A selected object inherits omitted parameters, including across providers or
  levels.
- An unconfigured primary borrows Executor or Planner metadata instead of
  preserving host selection.
- A listed but unenabled role is created, or `L0` configuration activates Work
  Charter.
- A missing explicit path silently falls back.
- Unknown, duplicate, ambiguous, executable, secret-bearing, invalid but
  currently unselected, or unsupported data is accepted or ignored.
- Configuration is treated as authority, changes an existing task/role, or is
  claimed effective without an integrated consumer.
- `agents/openai.yaml` is treated as the level-role selector.
