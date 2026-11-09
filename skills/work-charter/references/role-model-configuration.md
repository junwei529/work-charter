# Role-Model Configuration

Read this file only for a selected Charter model policy. Model defaults remain
in [role-models.default.yaml](../assets/role-models.default.yaml).
This policy selects delivery inputs; role and effect authority follow the agreement.

## Resolution Order

1. Keep the complete provider/model/parameters combination frozen for this delivery.
2. Otherwise use a complete explicitly confirmed task/role combination.
3. Otherwise use the contract's exact override file, else an existing
   ~/.config/work-charter/role-models.yaml, else the package defaults.

A selected missing or unreadable file stops that delivery. Validate the entire
selected file, including unused entries, before using it; validate package defaults
when consulted. Load configuration as data.

For arrangement-v2, select by actual responsibility:

| Responsibility | Selector |
|---|---|
| Direct D (primary), standalone or under O, and its R | direct.primary / direct.reviewer |
| Selected Team P, E and its R | team.planner / team.executor / team.reviewer |
| O and R reviewing O's planning product | phased.orchestrator / phased.reviewer |

D maps to primary; host main is normalized to primary at the boundary.
Arrangement-v1 Phased P/E/R retain their phased selector. Frozen combinations
take precedence over a later source change.

## Complete Objects And Schema v2

A complete object contains nonempty provider and model strings and optionally
a parameters mapping. Each object replaces the whole previous object.
Omitted or empty parameters means no parameters; fields never merge across objects.

Schema v2 requires integer schema_version: 2 and at least one complete object.
Only roles, arrangement_overrides and legacy_level_overrides are additional keys.
General roles are primary, orchestrator, planner, executor, reviewer.
Allowed arrangement roles: direct primary/reviewer; team planner/executor/reviewer;
phased orchestrator/planner/executor/reviewer. Supplied empty maps are allowed
alongside at least one complete object.

Reject duplicate/unknown keys, wrong types, unsupported schema versions, tags,
anchors, aliases, merge keys, expressions, credentials, endpoints, commands and
environment interpolation. This preserves data-only selection. main is a host
alias, not an accepted YAML key.

## Source Priority And Lookup

Exhaust the selected user source before consulting package defaults. In each v2
source use arrangement_overrides.<arrangement>.<role>, then roles.<role>.
An applicable old contract checks its legacy_level_overrides.<level>.<role> first.
A user general-role object outranks a package arrangement object.

Use the first present complete object. Only primary may fall back to the host
selection if neither source supplies an object and no compatibility ambiguity
remains. Record requested combination UNSPECIFIED and runtime UNKNOWN until
observed. A required non-primary role without an object stops delivery.
Use the primary's own object rather than borrowing executor/planner.

## Schema v1 And Old-Level Compatibility

Load this section for an actual v1 source or old-level contract.

Schema v1 has integer schema_version: 1 and only roles and level_overrides;
at least one must be present. Its historically empty role maps fall through.
Both v1 level_overrides and v2 legacy_level_overrides use this matrix:

| Level | Roles |
|---|---|
| l0, l1, l2 | primary, reviewer |
| l3 | planner, executor, reviewer |
| l4 | orchestrator, planner, executor, reviewer |

For a schema v1 old contract, use its exact level object then its general role
in each source. For a schema v2 old contract, use the level, arrangement, general
order in Source Priority And Lookup above. With a v1 source, a new Team selector
uses l3; O/O-product R and arrangement-v1 Phased P/E/R use l4.
For a new Direct selector, compare effective l0/l1/l2 objects in that source:
level override, else general role, else missing. Continue only when all three are
structurally equal in provider/model/parameters or all missing. All missing moves
to the next source. A difference or present/missing mix needs one consolidated
user decision for the affected roles, before package fallback.

Keep each old value. For an explicitly authorized v1 conversion, preserve general
roles and every old level object, derive only unambiguous arrangement objects,
and compare all effective old selections including inherited fallback values.
Where new arrangement objects would shadow an old fallback, preserve that old
selection as a complete compatibility object in the approved conversion.
Alternatively retain v1 and use task-local choices. Project adoption and package
install, update, rollback or uninstall leave the user's model file intact.

## Native Delivery And Evidence

Use the actual host schema to express the complete required combination.
An unsupported required value stops the dispatch; do not omit it or substitute
a model. Record source and selector, requested pair, tool acceptance and separately
the runtime identity actually exposed.

New source settings apply to newly resolved deliveries. Existing tasks keep
their settings and frozen combinations. The host owns loading and native effects.
