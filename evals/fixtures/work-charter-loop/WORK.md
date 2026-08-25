# Batching Work

- Contract state: `approved`
- Run disposition: `active`
- Canonical owner: this file
- Writer: current implementation session

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

The focused unit suite covers full batches, a final partial batch, empty input,
invalid size, and input preservation. Independent assessment is required.

## Stop And Recovery

Stop for a contract, permission, workspace, or writer mismatch. On recovery,
read this file, `STATUS.md`, `EVIDENCE.md`, actual Git state, implementation,
and tests before writing.
