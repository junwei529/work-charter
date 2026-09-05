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
- Descriptor snapshot: `PENDING_INDEPENDENT_REVIEW`, retained without rewriting
- Accepted immutable candidate: `30057490be21d869751854a51e9fafdfb535f206`
- Local-release receipt: [`../../../release/v0.4.0-local-release-receipt.json`](../../../release/v0.4.0-local-release-receipt.json)
- Deterministic SOURCE, repository, adversarial, and lifecycle self-test
  evidence: `PASS` for the accepted inputs, with Windows lifecycle cases run
  under a DACL-restore-capable token; any relevant source or checker change
  invalidates the corresponding evidence
- Independent technical review: five completed results; two historical source
  findings closed; R4 `NO_FINDINGS`; R5 P2
  `WC-INSTALL-ACCESS-R5-F01` fixed pending R6 and Planner acceptance
- Planner source and reviewed-installer baseline acceptance: `VERIFIED`
- v0.3.0-to-v0.4.0 written bytes and elevated receipt/file postflight:
  `VERIFIED`
- Default sandbox reader access after promotion: `FAILED`
- Managed installation acceptance and `LOCAL_RELEASE_READY`:
  `BLOCKED_BY_INSTALLED_COPY_ACCESS_REGRESSION`
- Current source DACL-preservation/readback correction: pending R6 independent
  review and Planner acceptance; actual installed-copy repair not performed
- `WC-INSTALL-ACCESS-P01`: P2 / `OPEN`; parent reset did not preserve a managed
  target's explicit or protected DACL policy
- `WC-INSTALL-ACCESS-R5-F01`: P2 /
  `FIXED_PENDING_R6_REVIEW_AND_PLANNER_ACCEPTANCE`;
  `/restore` success lacked a target DACL readback; remains under P01
- Stable loaded-copy behavior, natural adherence, cross-Harness behavior,
  public release, and broad efficacy: failed or `UNKNOWN` as recorded

The source update introduces portable independent Reviewer semantics across
L0-L4, explicit Executor verification / Reviewer findings / Planner or
Orchestrator acceptance boundaries, same-Reviewer repair re-review, cumulative
finding preservation, evidence-first `UNKNOWN` handling, context-switch
recovery, callback deduplication, and graph-evidence limits. The candidate
descriptor binds the current five-file package and retains its pre-review
evidence snapshot; it is not rewritten into an acceptance receipt. The
separate local-release receipt binds the accepted candidate commit, reviewed
installer baseline commit, cumulative static-review dispositions,
candidate-external trust identity, exact content/elevated postflight, and the
later open default-reader access finding without claiming installation
acceptance, publication, or natural adherence.

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
  the accepted checkpoint, with re-verification required after any relevant
  source or checker change.
- Current v0.4.0 source-candidate acceptance: `VERIFIED` for the immutable
  candidate and reviewed installer baseline.
- Current v0.4.0 attempt: exact content and elevated receipt/five-file
  postflight are `VERIFIED`, but default-reader access is `FAILED`; managed
  installation and `LOCAL_RELEASE_READY` are not accepted.
- Historical v0.3.0 `LOCAL_RELEASE_READY`: `VERIFIED` by the exact-C acceptance
  receipt.
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
installed-copy facts without rewriting P. The attempted v0.3.0-to-v0.4.0
update verifies only its written content and elevated postflight, not an
accepted transition. Other cross-version transitions, cross-Harness behavior,
untested contexts, and broad efficacy remain `UNKNOWN`.

Lifecycle receipt validation is bounded to integrity and routing checks. It
refuses unreceipted, malformed or mismatched-receipt, wrong-tree, modified,
aliased, and drifted destinations, but does not prove cryptographic ownership
against a same-privilege local actor able to forge the complete receipt.
Repository-side lifecycle mutations now use a validated external, same-volume
task transaction root outside all declared Skill discovery roots. Planned
product operations supply it explicitly; legacy apply calls retain their prior
shape through a visibly marked `AUTO_COMPATIBILITY` root with the same guards.
The disposable self-test covers all four legacy apply forms, explicit-path
install/update/rollback/uninstall, pre-mutation path and volume refusal,
preservation when the initial backup move fails, and verified restoration after
a later replacement failure. The current Windows-specific correction also
protects every random per-operation transaction directory for Owner Rights,
SYSTEM, and Administrators. New installs inherit the destination-parent DACL;
update/rollback/uninstall save the complete prior DACL tree and prove restore
capability on a private replica before mutation. The replica and every promoted
or recovered target are read back with the same bounded `/save` representation;
record order and newline form are ignored, while path membership and exact DACL
SDDL—including inheritance/protection flags and ACE order/content—must match.
A preflight mismatch produces zero target moves. A later mismatch enters
existing recovery and retains the original protected snapshot when recovery is
incomplete. Moved backup/tombstone trees inherit the private transaction DACL;
other platforms retain prior behavior. This source correction leaves the
five-file v0.4.0 candidate package and all historical v0.3.0 objects unchanged
and is pending independent review and acceptance.

## Next gate

The DACL-preservation/readback correction and corrected attempt record follow
the same R6 independent review, Planner acceptance, and local commit gate as other
evidence-bearing changes. Only after those gates may the exact current
installed copy be repaired through the separately authorized exact ACL-only
route. That route first verifies the trusted v0.4.0 content/receipt, recorded
private current DACL, and independently verified destination-parent reader
policy; it saves and preflights a rollback snapshot before resetting only that
target to parent inheritance. Default-reader status/read/hash/ACL postflight is
required. Fresh loaded-copy or natural-adherence
evidence, any global migration, public source, tag, Release, other cross-version
transition, or broader efficacy claim remains a separate gate. The exact historical v0.3.0
post-release evidence subject F remains accepted under
`B2-WC-PUBLIC-EVIDENCE-F-01` without moving its tag or rewriting P.

## Recovery entry

Read the root [`AGENTS.md`](../../../AGENTS.md),
[`PROVENANCE.md`](../../../PROVENANCE.md), [Design](DESIGN.md), this State, and
[Verification](VERIFICATION.md). Verify Git status, current branch, package
identity, and writer ownership before changing files.
