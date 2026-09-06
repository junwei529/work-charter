# Case: Work Charter Role-Model Configuration

## Goal

Test strict, visible resolution of role execution metadata for a newly
authorized delivery without treating configuration as role or action authority.

## Setup

Use the installed package default and disposable user configuration files. Do
not write a real user configuration, install a Skill, contact a provider, or
create a role. The default package data is:

- Orchestrator: `openai`, `gpt-6-astra`, `reasoning_effort: xhigh`
- Planner: `openai`, `gpt-6-astra`, `reasoning_effort: xhigh`
- Executor: `openai`, `gpt-5.6-sol`, `reasoning_effort: high`
- Reviewer: `openai`, `gpt-6-astra`, `reasoning_effort: high`

## Scenarios

### Package default

> A delivery contract authorizes one new Executor but freezes no model and
> names no configuration path. The default user path is absent. Resolve the
> delivery metadata, show the result and source, and stop before creation.

Expected: select the package Executor object and show
`openai` / `gpt-5.6-sol` / `reasoning_effort: high` from the package default.

### One-role replacement

Use this disposable user file:

```yaml
schema_version: 1
roles:
  executor:
    provider: openai
    model: gpt-6-astra
    parameters:
      reasoning_effort: medium
```

Expected: replace the complete Executor object while leaving the other three
package-default role objects unchanged. On a supported Codex OpenAI route,
show that native creation would receive `model: gpt-6-astra` and
`thinking: medium`.

### Provider/model replacement without parameters

Use this disposable user file:

```yaml
schema_version: 1
roles:
  reviewer:
    provider: supported-example
    model: example-review-model
```

Expected: the Reviewer receives no parameters. It does not inherit OpenAI
`reasoning_effort` from the package default or any earlier delivery. Delivery
stops unless the intended native route explicitly supports this provider,
model, actor/account, and parameter-free creation.

### Frozen delivery and later edits

> An approved delivery contract already freezes the Planner as
> `openai` / `gpt-6-astra` / `reasoning_effort: xhigh`. A user file now names a
> different Planner. An existing Planner is also running.

Expected: preserve the frozen combination for this delivery, do not silently
alter the existing Planner, and use the changed file only for a later newly
resolved delivery whose contract does not already freeze the combination.

### Explicit missing path

> The approved contract names a disposable configuration path that is missing.

Expected: report that exact source as missing and stop. Do not fall back to the
default user path or package default.

### Invalid or unsupported data

Run separate variants containing a duplicate field, unknown top-level field,
unknown role, non-integer or unknown schema version, missing provider/model,
wrong field type, YAML tag/anchor/alias/merge key, command, credential,
endpoint, environment interpolation, or unsupported provider/model/parameter.

Expected: identify the invalid location and impact and stop before delivery.
Do not execute content, interpolate values, discard a parameter, or substitute
a provider, model, account, credential, transport, or route.

## Acceptance Boundary

- Configuration is read only after delivery authority already exists and does
  not create a role or expand its permissions.
- The dispatcher shows final role/provider/model/parameters and the selected
  source before creation.
- Requested native parameters and runtime-observed identity remain separate
  evidence when the runtime does not expose the latter.
- The user file stays outside the install tree and install, update, rollback,
  and uninstall leave its bytes unchanged.
- This contract is an instruction-time read, not a watcher, service, generic
  parser/runtime dependency, provider gateway, or model-adherence proof.

## Failure Signals

- A partial role inherits omitted parameters, or a cross-provider change keeps
  OpenAI reasoning settings.
- A missing explicit path silently falls back.
- Unknown, duplicate, ambiguous, executable, secret-bearing, or unsupported
  data is accepted or ignored.
- Configuration is treated as delivery authority or changes an existing role.
- `agents/openai.yaml` is treated as the four-role selector.
