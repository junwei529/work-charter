# Work Charter State

## Current implementation

Canonical editable source is the 5-file package under
[`skills/work-charter/`](../../../skills/work-charter/). Every package file and retained
case or fixture is an exact Git blob from `80910a8b2375a11be897e9660c4b00a06d00dd13`.

## Independent candidate

- Version: `v0.3.0`
- Public identity: `junwei529/work-charter`
- Candidate descriptor: [`../../../release/v0.3.0-candidate.json`](../../../release/v0.3.0-candidate.json)
- Candidate state: `LOCAL_RELEASE_READY=VERIFIED`
- Accepted candidate C: `732e7efa6211d9aedeb133282ef28ce03f9bdfef`
- Acceptance receipt: [`../../../release/v0.3.0-local-release-receipt.json`](../../../release/v0.3.0-local-release-receipt.json)
- Release notes: [`../../../CHANGELOG.md`](../../../CHANGELOG.md), human review pending

The immutable candidate identity is the clean commit containing the descriptor.
The descriptor deliberately does not contain its own commit hash and retains
its original pending snapshot. The separate receipt binds exact C, its tree,
the unchanged package tree, and the independent Planner acceptance without
rewriting that candidate.

## Repository ownership

This repository owns its Git history, documentation, checks, and future version,
evaluation, installation, and release decisions. It has no implicit dependency
on another Skill repository and begins with no configured remote.

## Evidence state

The migration proves current package byte identity, mapped case and fixture byte
identity, local link and publication-safety checks, and repository-local
verification. Deterministic SOURCE qualification additionally proves that the
candidate instruction text contains required selection/activation, authority
non-expansion, coordination/recovery, and Standard O/P/E clauses. It does not
prove model adherence. The retained cases remain contract fixtures; they do not
create fresh model, efficacy, release, or installed-copy evidence.

Evidence states remain separate:

- SOURCE identity and deterministic SOURCE contract: locally verifiable.
- `LOCAL_RELEASE_READY`: `VERIFIED` by the exact-C acceptance receipt.
- `PUBLIC_RELEASE`: `UNKNOWN`.
- `STABLE_INSTALLED_COPY`: `UNKNOWN`.
- Broad product efficacy and untested selection/loading/negative contexts: `UNKNOWN`.

Lifecycle receipt validation is bounded to integrity and routing checks. It
refuses unreceipted, malformed or mismatched-receipt, wrong-tree, modified,
aliased, and drifted destinations, but does not prove cryptographic ownership
against a same-privilege local actor able to forge the complete receipt.

## Next gate

The next release gate is the separately authorized immutable public source and
publication route. Any remote, installation, tag, Release, publication,
persistent lifecycle effect, or installed-copy behavior evaluation still
requires its own authority and fresh evidence. Ordinary local changes must
preserve the provenance record or explicitly supersede the mapped baseline.

## Recovery entry

Read the root [`AGENTS.md`](../../../AGENTS.md),
[`PROVENANCE.md`](../../../PROVENANCE.md), [Design](DESIGN.md), this State, and
[Verification](VERIFICATION.md). Verify Git status, current branch, package
identity, and writer ownership before changing files.
