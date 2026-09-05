# Work Charter State

## Current implementation

Canonical editable source is the 5-file package under
[`skills/work-charter/`](../../../skills/work-charter/). It originated from
`80910a8b2375a11be897e9660c4b00a06d00dd13`; changed `v0.4.1` package,
evaluation, documentation, and checker files are repository-native and bound
to their current hashes in the provenance manifest. Unchanged mapped material
retains its exact or normalized migration provenance.

## Current v0.4.1 candidate

- Version: `v0.4.1`
- Candidate descriptor: [`../../../release/v0.4.1-candidate.json`](../../../release/v0.4.1-candidate.json)
- Descriptor state: `PENDING_INDEPENDENT_REVIEW`
- Package lineage: committed v0.4.0 source
  `df674c773de6f915627af541f0eb37221da9adef`
- Deterministic SOURCE, repository, adversarial, and lifecycle evidence:
  requires fresh qualification for this exact checkpoint
- Independent technical review and Planner acceptance: `PENDING`
- Local-release receipt, installation, and publication: not created or claimed
- Actual v0.4.0 installed-copy repair: not authorized by this candidate and not
  performed
- `WC-INSTALL-POSTFLIGHT-F01`: `OPEN`
- Stable loaded-copy behavior, natural adherence, cross-Harness behavior,
  public release, and broad efficacy: failed or `UNKNOWN` as recorded

The candidate preserves the v0.4.0 L0-L4 Reviewer, verification, acceptance,
evidence-first `UNKNOWN`, context recovery, callback, and graph boundaries. It
adds direct operation-local permission ownership without transferring higher
contract ownership. On Windows it replaces whole-tree restore with a
control-aware, path-by-path mechanism: AI-bearing records use one-record
`icacls /restore`, while records without AI use the non-propagating directory
behavior of `SetFileSecurityW`. Exact P, AI, AR, ACE order/content, and managed
path membership remain required by post-restore readback. Unsupported states
fail in the private replica preflight before any target move.

## Historical v0.4.0 candidate and failed installation

- Immutable candidate: [`../../../release/v0.4.0-candidate.json`](../../../release/v0.4.0-candidate.json)
- Accepted candidate commit: `30057490be21d869751854a51e9fafdfb535f206`
- Local-release receipt: [`../../../release/v0.4.0-local-release-receipt.json`](../../../release/v0.4.0-local-release-receipt.json)
- Receipt-bound independent review: five results through R5; two historical
  source findings closed and R5 P2 fixed pending R6 at that checkpoint
- Later R6 result and Planner source acceptance: `NO_FINDINGS` / `ACCEPTED`
- Accepted correction commit: `df674c773de6f915627af541f0eb37221da9adef`
- v0.3.0-to-v0.4.0 written bytes and elevated receipt/file postflight:
  `VERIFIED`
- Default sandbox reader access after promotion: `FAILED`
- First authorized ACL-only repair: stopped before target mutation because
  `/restore` changed `D:P` to `D:PAI` and `D:` to `D:AI`
- Managed installation acceptance and `LOCAL_RELEASE_READY`:
  `BLOCKED_BY_INSTALLED_COPY_ACCESS_REGRESSION`

The later control-state counterevidence does not erase R6 or its acceptance; it
invalidates the prior mechanism for a new repair attempt. The actual target,
parent ACL, source commit, and retained v0.4.0 repair snapshots remain unchanged.

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
qualification is intended to prove that the `v0.4.1` instruction text contains
required selection/activation, authority non-expansion, coordination/recovery,
review/acceptance separation, and Standard O/P/E/R clauses. It does not prove
model adherence, technical correctness, or acceptance. The retained cases
remain contract fixtures; they do not create fresh model, efficacy, release, or
installed-copy evidence.

Evidence states remain separate:

- Current v0.4.1 SOURCE identity and deterministic contract: requires fresh
  verification for the exact candidate checkpoint.
- Current v0.4.1 independent review and Planner acceptance: `PENDING`.
- Historical v0.4.0 source-candidate acceptance: `VERIFIED` for the immutable
  candidate and reviewed installer baseline; the later control-state evidence
  requires a new mechanism rather than erasing that history.
- Historical v0.4.0 attempt: exact content and elevated receipt/five-file
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
accepted transition. The first ACL-only repair attempt made no target mutation.
Other cross-version transitions, cross-Harness behavior, untested contexts, and
broad efficacy remain `UNKNOWN`.

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
capability on a private replica before mutation. AI-bearing records use a
single-record `/restore`; no-AI records use `SetFileSecurityW` without a child
propagation transition. Records are applied shallow-to-deep. The replica and
every promoted or recovered target are read back with the same bounded `/save`
representation; record order and newline form are ignored, while path
membership and exact DACL SDDL—including P, AI, AR and ACE order/content—must
match. A preflight mismatch produces zero target moves. A later mismatch enters
existing recovery and retains the original protected snapshot when recovery is
incomplete. Moved backup/tombstone trees inherit the private transaction DACL;
other platforms retain prior behavior. This source correction creates a new
five-file v0.4.1 candidate while leaving immutable v0.4.0/v0.3.0 release objects
unchanged, and is pending independent review and acceptance.

## Next gate

The v0.4.1 source checkpoint requires fresh independent review and Planner
acceptance. Any local commit is a later explicit gate. Only after those gates
may a separately authorized ACL-only attempt repair the exact current installed
copy. That route re-verifies trusted v0.4.0 content/receipt, current and parent
DACLs, and its protected rollback snapshot before resetting only that target to
parent inheritance. Default-reader status/read/hash/ACL postflight is required.
Fresh loaded-copy or natural-adherence
evidence, any global migration, public source, tag, Release, other cross-version
transition, or broader efficacy claim remains a separate gate. The exact historical v0.3.0
post-release evidence subject F remains accepted under
`B2-WC-PUBLIC-EVIDENCE-F-01` without moving its tag or rewriting P.

## Recovery entry

Read the root [`AGENTS.md`](../../../AGENTS.md),
[`PROVENANCE.md`](../../../PROVENANCE.md), [Design](DESIGN.md), this State, and
[Verification](VERIFICATION.md). Verify Git status, current branch, package
identity, and writer ownership before changing files.
