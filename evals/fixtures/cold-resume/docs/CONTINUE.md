# Recovery Snapshot

## Recorded Workspace

- Branch: `phase/retry-delay`
- Baseline commit: exact value supplied by the setup controller record
- Owned dirty file: `src/retry_policy.py`
- Writer: interrupted Executor

## Last Verified Checkpoint

The pre-phase baseline unit suite passed two unrelated worker tests at the
recorded commit. It does not verify retry delay behavior.

## Next Safe Action

Revalidate the repository root, branch, controller-recorded baseline commit,
dirty state, and writer ownership. If they match this workstream, recommend
continuing only after the authorized focused evidence is refreshed.

Stop and report recovery drift before writing if the branch, commit, ownership,
or approved contract does not match. An unrelated task or branch is not a
conflict unless it changed this protected state.
