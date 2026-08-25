# Multi-worktree Carrier Snapshot

A recovery agent must determine which Charter controls one managed release
workstream spanning two worktrees.

## Worktree Observations

- Worktree A: `WORK_CHARTER.md`, revision `5`, next action `package`
- Worktree B: `WORK_CHARTER.md`, revision `6`, next action `retest`
- Both files claim to be authoritative for `release-2`
- Common control location: `UNKNOWN`
- Revision finality relation: `UNKNOWN`
- Active writer: `UNKNOWN`
- Dirty ownership: incomparable between the two worktrees
- Authority to copy, synchronize, commit, integrate, or select either file:
  none
