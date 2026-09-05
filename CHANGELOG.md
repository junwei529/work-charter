# Changelog

## Work Charter v0.4.0

Candidate state: `PENDING_INDEPENDENT_REVIEW`

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

- The local descriptor binds the current five-file SOURCE candidate.
- Deterministic verification, independent technical review, and Planner
  acceptance are separate gates and do not yet establish
  `LOCAL_RELEASE_READY`.
- Installation, cross-version lifecycle, stable installed-copy behavior,
  public source, tag, Release, and broad efficacy remain `UNKNOWN` or separately
  authorized for v0.4.0.
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
