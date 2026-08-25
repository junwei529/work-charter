# Work Charter State

## Current implementation

Canonical editable source is the 5-file package under
[`skills/work-charter/`](../../../skills/work-charter/). Every package file and retained
case or fixture is an exact Git blob from `80910a8b2375a11be897e9660c4b00a06d00dd13`.

## Repository ownership

This repository owns its Git history, documentation, checks, and future version,
evaluation, installation, and release decisions. It has no implicit dependency
on another Skill repository and begins with no configured remote.

## Evidence state

The migration proves current package byte identity, mapped case and fixture byte
identity, local link and publication-safety checks, and repository-local
verification. The retained cases are deterministic contract fixtures; they do not create fresh product, efficacy, release, or installed-copy evidence.

## Next gate

Any remote, installation, tag, release, publication, or behavior-evaluation
action requires its own authority and fresh evidence. Ordinary local changes
must preserve the provenance record or explicitly supersede the mapped baseline.

## Recovery entry

Read the root [`AGENTS.md`](../../../AGENTS.md),
[`PROVENANCE.md`](../../../PROVENANCE.md), [Design](DESIGN.md), this State, and
[Verification](VERIFICATION.md). Verify Git status, current branch, package
identity, and writer ownership before changing files.
