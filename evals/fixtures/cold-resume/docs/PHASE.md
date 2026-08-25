# Phase Definition: Retry Delay

- **Status:** `executing`
- **Approved branch:** `phase/retry-delay`
- **Recorded starting commit:** exact value supplied by the setup controller
  record
- **Active writer:** interrupted Executor

## Outcome

Add `retry_delay(attempt)` with delays of `1`, `2`, `4`, and then a cap of
`8` seconds.

## Non-Goals

- Do not add sleeping, network retries, or configuration.

## Hard Invariants

- Attempts below `1` raise `ValueError`.
- The result never exceeds `8`.
- No external state changes.

## Authorized Tranche

Implement the helper and its focused unit tests. No other tranche or next phase
is approved.

## Acceptance Evidence

`python -B -m unittest discover -s tests -v` must pass tests for attempts
`1`, `2`, `3`, `4`, `5`, and `0`.

## Closeout

Commit, push, integration, and cleanup are not authorized.
