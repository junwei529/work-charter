# Changelog

## Work Charter v0.4.0

Descriptor snapshot: `PENDING_INDEPENDENT_REVIEW` (retained without rewriting)

Source-candidate acceptance: `VERIFIED`

Local release state: `BLOCKED_BY_INSTALLED_COPY_ACCESS_REGRESSION`

Human release-note review: `PENDING`

### Highlights

- Adds portable independent Reviewer semantics without forcing Work Charter at
  `L0` or Planner/Executor separation at `L1` and `L2`.
- Separates Executor verification, Reviewer technical findings, Planner target
  acceptance, and Orchestrator project direction/phase acceptance across
  Standard O/P/E/R.
- Routes stable Executor checkpoints through Planner scope freeze to a read-only
  Reviewer, then back through Planner correction and acceptance; repair reuses
  the same reliable Reviewer and preserves cumulative findings.
- Treats `UNKNOWN` as an evidence question first, limits graph results to
  attributable coverage guidance, and never treats hashes, tests, status, or
  graphs as semantic review or acceptance.
- Distinguishes compaction, deliberate context rotation, and successor Sessions
  while preserving contract, authority, role/writer, finding, stop, and
  evidence history.
- Enforces one current Result Notice per route and checkpoint, with no mirrored
  verdicts, polling, or acknowledgement loop.

### Evidence boundaries

- The immutable local descriptor binds the accepted five-file SOURCE candidate;
  a separate non-circular receipt binds the later review and acceptance facts.
- Deterministic verification, five independent technical-review rounds, and
  Planner source/tool acceptance are `VERIFIED` for the exact recorded
  identities.
- One explicit-root v0.3.0-to-v0.4.0 attempt wrote exact bytes and passed
  elevated receipt/five-file postflight, but the promoted directory retained
  the private transaction ACL and failed default-reader access. Managed
  installation and `LOCAL_RELEASE_READY` are not accepted.
- R4 returned `NO_FINDINGS`, but Planner acceptance found open P2
  `WC-INSTALL-ACCESS-P01`: unconditional parent reset did not preserve a managed
  target's explicit or protected DACL policy.
- R5 opened P2 `WC-INSTALL-ACCESS-R5-F01`: `/restore` process success alone did
  not prove the target DACL was restored. The correction is implemented but
  remains open pending R6 and Planner acceptance under the parent P01 finding.
- The revised bounded Windows correction protects each random transaction and
  its recovery material, snapshots the complete existing DACL tree and proves
  it can be restored and semantically read back before update/rollback/uninstall
  mutation, preserves and rechecks that policy on the new or recovered target,
  and uses parent inheritance only for a genuinely new install. Record order
  and newline form are non-semantic; path membership and exact DACL SDDL,
  including flags and ACE order/content, must match. It is pending R6 and
  Planner acceptance; the actual installed copy has not been repaired.
- Stable loaded-copy behavior, natural adherence, other cross-version
  lifecycle effects, cross-Harness behavior, public source, tag, Release, and
  broad efficacy remain failed, `UNKNOWN`, or separately authorized as
  recorded for v0.4.0.
- Historical v0.3.0 receipts and public evidence remain unchanged and apply
  only to that version.

## Work Charter v0.3.0

Human release-note review: `PENDING`

First independent release of Work Charter, a Codex Skill for bounding
consequential work by outcome, authority, evidence, recovery, and proportional
coordination.

### Highlights

- Publishes the independently versioned `junwei529/work-charter` repository.
- Preserves the installable 5-file Work Charter package byte for byte from the
  recorded migration source.
- Includes deterministic SOURCE qualification for selection and activation,
  authority non-expansion, coordination and recovery, and Standard O/P/E.
- Includes an explicit-destination lifecycle tool with dry-run defaults and
  disposable install, update, rollback, uninstall, and recovery checks.

### Evidence boundaries

- Local release readiness is verified for the accepted immutable candidate.
- The release does not by itself prove stable installed-copy behavior,
  cross-Harness behavior, untested selection or loading contexts, persistent
  lifecycle effects, or broad product efficacy.
- Lifecycle receipts provide integrity and routing evidence, not cryptographic
  ownership against a same-privilege local actor able to forge a complete
  receipt.
