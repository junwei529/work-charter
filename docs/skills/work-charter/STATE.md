# Work Charter State

## Current implementation

Canonical editable source is the 5-file package under
[`skills/work-charter/`](../../../skills/work-charter/). It originated from
`80910a8b2375a11be897e9660c4b00a06d00dd13`; changed `v0.4.0` package,
evaluation, documentation, and checker files are repository-native and bound
to their current hashes in the provenance manifest. Unchanged mapped material
retains its exact or normalized migration provenance.

## Current v0.4.0 candidate

- Version: `v0.4.0`
- Candidate descriptor: [`../../../release/v0.4.0-candidate.json`](../../../release/v0.4.0-candidate.json)
- Candidate state: `PENDING_INDEPENDENT_REVIEW`
- Deterministic SOURCE, repository, adversarial, and lifecycle self-test
  evidence: `PASS` at the current review-ready checkpoint; any mapped source or
  checker change invalidates it
- Independent technical Reviewer verdict: pending
- Planner acceptance and `LOCAL_RELEASE_READY`: pending
- Installation, cross-version lifecycle, stable installed copy, and public
  release: `UNKNOWN` and separately authorized

The source update introduces portable independent Reviewer semantics across
L0-L4, explicit Executor verification / Reviewer findings / Planner or
Orchestrator acceptance boundaries, same-Reviewer repair re-review, cumulative
finding preservation, evidence-first `UNKNOWN` handling, context-switch
recovery, callback deduplication, and graph-evidence limits. The candidate
descriptor binds the current five-file package and retains its pre-review
evidence snapshot; it is not an acceptance receipt and does not authorize
installation or publication.

## Historical v0.3.0 release

- Version: `v0.3.0`
- Public identity: `junwei529/work-charter`
- Candidate descriptor: [`../../../release/v0.3.0-candidate.json`](../../../release/v0.3.0-candidate.json)
- Candidate state: `LOCAL_RELEASE_READY=VERIFIED`
- Accepted candidate C: `732e7efa6211d9aedeb133282ef28ce03f9bdfef`
- Acceptance receipt: [`../../../release/v0.3.0-local-release-receipt.json`](../../../release/v0.3.0-local-release-receipt.json)
- Release-note body: human review approved; immutable P's
  [`../../../CHANGELOG.md`](../../../CHANGELOG.md) carrier retains its pre-effect
  `PENDING` snapshot
- Public repository: `https://github.com/junwei529/work-charter`
- Public-source candidate: [`../../../release/v0.3.0-public-release-candidate.json`](../../../release/v0.3.0-public-release-candidate.json)
- Immutable public commit P: `b655c1aa42acc8c68b70e87c4c228445c5182d8b`
- Annotated tag: `v0.3.0`, fixed at P
- Public release state: `VERIFIED`
- Post-release evidence subject: [`../../../release/v0.3.0-public-release-evidence.json`](../../../release/v0.3.0-public-release-evidence.json), accepted as `B2-WC-PUBLIC-EVIDENCE-F-01` for exact F `4ba904808fe86e270ebd405db1866d41d1cc032e`

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

The migration proves historical source identities for mapped files. The current
manifest proves current target hashes, local link and publication-safety
constraints, and provenance classification. Fresh deterministic SOURCE
qualification is intended to prove that the `v0.4.0` instruction text contains
required selection/activation, authority non-expansion, coordination/recovery,
review/acceptance separation, and Standard O/P/E/R clauses. It does not prove
model adherence, technical correctness, or acceptance. The retained cases
remain contract fixtures; they do not create fresh model, efficacy, release, or
installed-copy evidence.

Evidence states remain separate:

- Current SOURCE identity and deterministic SOURCE contract: locally `PASS` at
  the current review-ready checkpoint, with re-verification required after any
  mapped source or checker change.
- Historical v0.3.0 `LOCAL_RELEASE_READY`: `VERIFIED` by the exact-C acceptance
  receipt; current v0.4.0 readiness is pending review and Planner acceptance.
- Historical v0.3.0 `PUBLIC_RELEASE`: `VERIFIED` for exact P, annotated tag,
  and public Release.
- Historical v0.3.0 same-version install/update/rollback/uninstall/restoration:
  `VERIFIED`.
- Historical v0.3.0 `STABLE_INSTALLED_COPY`: `VERIFIED` for the evidenced Codex
  user installation at that checkpoint.
- Historical v0.3.0 installed-copy behavior: `VERIFIED` for the retained witnesses
  plus `B2-WC-SOLE-LOAD-02`, which observed exactly one catalog-visible managed
  `work-charter`.
- Retained predecessor bytes: preserved outside every Skill discovery root; the
  exact recovery locator is controller-side only.
- Broad product efficacy and untested selection/loading/negative contexts: `UNKNOWN`.

The immutable public-source candidate preserves its pre-effect snapshot. The
separate post-release evidence subject binds the later public and corrected
installed-copy facts without rewriting P. Cross-version update/rollback,
cross-Harness behavior, untested contexts, and broad efficacy remain `UNKNOWN`.

Lifecycle receipt validation is bounded to integrity and routing checks. It
refuses unreceipted, malformed or mismatched-receipt, wrong-tree, modified,
aliased, and drifted destinations, but does not prove cryptographic ownership
against a same-privilege local actor able to forge the complete receipt.

## Next gate

Keep the v0.4.0 source frozen, obtain one independent read-only technical review
of the exact checkpoint, disposition any findings through the
Planner/Executor loop with focused re-verification, and obtain Planner
acceptance. Until then no v0.4.0 receipt, installation, public source, tag, or
Release may be claimed. The exact historical v0.3.0 post-release evidence subject F remains
accepted under `B2-WC-PUBLIC-EVIDENCE-F-01` without moving its tag or rewriting
P. Cross-version work, another Release, or broader efficacy remains separately
authorized.

## Recovery entry

Read the root [`AGENTS.md`](../../../AGENTS.md),
[`PROVENANCE.md`](../../../PROVENANCE.md), [Design](DESIGN.md), this State, and
[Verification](VERIFICATION.md). Verify Git status, current branch, package
identity, and writer ownership before changing files.
