# Batching Work

- Contract state: `approved`
- Run disposition: `active`
- Canonical owner: this file
- Planner: contract, review routing, correction, and acceptance owner
- Executor: current implementation session and sole writer
- Reviewer: one independent read-only technical Reviewer for each stable
  checkpoint, preferably reused after repair

## Outcome

`partition_batches(values, batch_size)` returns ordered lists of at most
`batch_size` values and retains a final partial batch.

## Boundaries

- Preserve input order and do not mutate the input.
- Reject a batch size below `1` with `ValueError`.
- Do not add persistence, concurrency, command-line behavior, or dependencies.

## Authorization

Implementation, focused tests, and existing status/evidence maintenance are
authorized. Role delivery, Git operations, project-governance changes, and
external effects are not authorized by this contract.

## Acceptance Evidence

The Executor runs the focused unit suite covering full batches, a final partial
batch, empty input, invalid size, and input preservation. An independent
Reviewer inspects the stable change and reports findings and coverage to the
Planner. Planner acceptance is required after review convergence.

## Stop And Recovery

Stop for a contract, permission, workspace, or writer mismatch. On recovery,
read this file, `STATUS.md`, `EVIDENCE.md`, actual Git state, implementation,
and tests before writing.
