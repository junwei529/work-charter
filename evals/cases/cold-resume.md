# Case: Cold Resume

## Goal

Test whether `$work-charter` matches one managed workstream, reconciles its
durable anchor with live state, and recommends continuing after an authorized
evidence refresh without confusing unrelated project work.

## Fixture

The raw [synthetic fixture](../fixtures/cold-resume), after the public setup
step below, contains:

- project instructions and an authority map;
- an approved Retry Delay Charter;
- status, verification, and recovery documents;
- a committed `phase/retry-delay` baseline with one owned dirty implementation
  file; and
- historical baseline evidence that predates that implementation.

The new agent receives no prior chat or task transcript.

## Reproducible Setup

Prepare a new ignored workspace; the helper refuses to overwrite an existing
destination:

```powershell
pwsh -NoProfile -File .\evals\setup-cold-resume.ps1 `
    -Destination .\.eval-runs\cold-resume
```

The helper copies the raw fixture, initializes and commits the approved
`phase/retry-delay` baseline, then materializes the owned
`src/retry_policy.py` change. Capture the helper's JSON record and give its
exact baseline commit to the recovery agent as controller evidence. Do not run
the behavior test against the tracked raw fixture or parent repository Git.

## User Request

> Use $work-charter to determine whether the retry-delay workstream may resume.
> I authorize reading the declared recovery documents, current repository,
> branch, HEAD, worktree, dirty and observable writer state, and the named
> baseline evidence. Do not write or run verification yet. A separate old task
> changed only an unrelated documentation branch.

## Expected Behavior

- Reads only the approved durable entry points and live-state facts in
  authority order.
- Matches the retry-delay managed workstream and ignores the explicitly
  non-overlapping old documentation task.
- Revalidates repository root, approved branch, controller-recorded baseline
  commit, dirty ownership, and writer state.
- Recognizes that contract and coordination still align while historical
  evidence predates the owned implementation.
- Returns **continue after evidence refresh** (`resume after evidence refresh`)
  rather than inventing a fifth route; names the approved focused test subject
  and keeps execution separate from reconciliation.
- Summarizes outcome, remaining scope, last valid evidence, writer boundary,
  next safe action, separate authority, and return route with bounded context.
- Does not require or invoke Project Docs and does not mistake durable SOURCE
  reads for native loaded-copy identity.

## Failure Signals

- Assumes the recovery record is current without checking live Git state.
- Discards the dirty file or changes branches destructively.
- Reconstructs missing details from guesswork.
- Treats the unrelated old task as a project-wide conflict.
- Starts the refresh, an unlisted tranche, or next phase during reconciliation.
- Claims that `$work-charter` selection, a Goal, or document presence
  authorizes writes.
- Copies raw logs or private environment paths into publishable docs.
