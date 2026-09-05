# Work Charter Verification

## Historical migration baseline and current local release

- Source commit: `80910a8b2375a11be897e9660c4b00a06d00dd13`
- Package path: `skills/work-charter/`
- Package files: 5
- Provenance manifest: [`../../../provenance/source-map.json`](../../../provenance/source-map.json)
- Current candidate: [`../../../release/v0.4.1-candidate.json`](../../../release/v0.4.1-candidate.json)
- Candidate descriptor state: `PENDING_INDEPENDENT_REVIEW`
- Candidate lineage commit: `df674c773de6f915627af541f0eb37221da9adef`
- Historical v0.4.0 local-release receipt:
  [`../../../release/v0.4.0-local-release-receipt.json`](../../../release/v0.4.0-local-release-receipt.json)
- v0.4.1 source-candidate acceptance: `PENDING`
- v0.4.0 local-release state:
  `BLOCKED_BY_INSTALLED_COPY_ACCESS_REGRESSION`

## Repository check

```powershell
python -B scripts/check_repository.py --json
```

This verifies exact Git-blob identity for unchanged mapped inputs, current
hashes and honest provenance classification for revised/native files, expected
package and evaluation shape, UTF-8/BOM and Markdown-link boundaries, and
publication safety.
The default standalone route preserves a checker-pinned source-identity map;
it does not assume the former source repository is present.

When the exact source Git object store is available during migration audit, run:

```powershell
python -B scripts/check_repository.py --json --source-repository <source-git-repository>
```

That explicit route resolves the recorded commit/tree and proves every mapped
source path, Git blob, and raw or normalized SHA-256 directly from Git objects;
it never reads source working-tree bytes.

## Adversarial checker matrix

```powershell
python -B scripts/check_repository.py --adversarial
```

This builds every disposable repository strictly from staged Git-index blobs;
working-tree, ignored, untracked, cache, and link-target bytes are not copied.
Before treating its result as evidence for a candidate, stage the complete
intended candidate—including new files—and verify that
`git diff --cached --name-status` matches the declared review input. Unstaged
or untracked changes are outside the matrix snapshot, so a passing command run
against an old index proves only that older indexed input.
The admitted publication-classifier input domain is the UTF-8 text of mapped
repository files plus every string value consumed from the v2 provenance
manifest. Manifest paths remain strict POSIX repository-relative paths. Within
that domain, the locator grammar is limited to direct absolute Windows drive
profiles, direct/device UNC locators, and `file:` URIs that resolve to those
forms after exactly one percent-decoding pass. One separator/prefix
canonicalization handles equivalent slash forms and repeated leading
separators in direct and `file:` representations; explicit non-`file:` URIs,
repository-relative paths, POSIX
`file:` paths, and non-profile Windows roots remain portable. Locator-like
`file:` or UNC forms that cannot be classified unambiguously after that pass
fail closed, including `file:` candidates whose raw query or fragment
delimiter or raw-space token boundary would make the local path representation
ambiguous, and candidates whose percent escapes are not valid UTF-8. Direct UNC
forms with a server but no share also fail closed; the
portable `//` syntax-text partition requires no server token. This policy
protects the existing no-private-locator publication
contract; it does not promise another URI or filesystem grammar.
The finite fail-closed matrix covers drive-rooted private Windows profiles with
backslash, forward-slash, and mixed separators; ASCII-space and Unicode profile
names; end-of-string and deeper paths; and recognized device-drive prefixes.
It also covers ordinary, device, and extended UNC locators after one canonical
separator/prefix normalization. A shared structured UNC parser requires
nonempty server and share components, accepts Unicode and internal spaces, and
rejects controls and Windows-invalid component characters. Portable explicit
non-file URI, relative, embedded-drive, empty-profile, singular-root,
syntax-text, POSIX, and non-profile-root partitions remain accepted. A
URI-aware standard-library layer parses `file:` candidates,
decodes percent escapes once, and routes local-drive, `localhost`, UNC-authority,
drive-authority (including a once-decoded drive-rooted authority remainder),
and encoded device-drive representations through the same path predicates;
HTTP/HTTPS, other schemes, non-profile Windows roots, POSIX paths, bare schemes,
and empty-profile forms remain portable. Git-index snapshots remove inherited
`GIT_*` selectors case-insensitively, reintroduce only disabled optional locks,
and use an explicit repository route; a disposable hostile-selector matrix
proves both `ls-files` and `cat-file` stay bound to the intended repository.
The matrix also covers invalid UTF-8 and unpaired-Unicode-surrogate structured failure, manifest
identity and rewrite-source schema, exact-blob source SHA-256 verification,
top-level source-commit/source-tree identity, and a checker-pinned canonical
digest of every destination-to-source identity mapping. Exact tree membership
is established only by the explicit source-object audit above;
manifest duplicate-key rejection, top-level `manifest_provenance` source-record
schema/path validation, decoded-key/value publication safety, unsafe
destinations, source paths free of Unicode General_Category `Cc` controls
(covering C0, DEL, and C1 while preserving other admitted Unicode categories),
missing mapped content, the legacy
reparse fallback, and rejection of link-like source-repository ancestors. An external-link
sentinel proves that a link entry is rejected before its target blob is read or
copied; the result identifies whether the current host also created a real
disposable symlink or used the deterministic index-link-mode branch.

## Focused check

Run the deterministic SOURCE contract check:

```powershell
python -B scripts/check_source_contract.py --json
```

It verifies the exact 5-file package shape, the `v0.4.1` candidate binding, the
separate immutable v0.4.0 local-release receipt, and the instruction clauses needed for
direct and indirect selection/activation,
authority non-expansion, context recovery, independent review/acceptance
separation, same-Reviewer repair re-review, callback deduplication,
evidence-first `UNKNOWN` handling, graph limitations, Standard O/P/E/R, and
direct operation-local permission ownership without higher-contract transfer.
It also verifies the immutable v0.4.0 candidate/receipt and v0.3.0 release
objects against fixed historical package and release-note identities rather
than comparing them with current bytes. The v0.4.0 receipt qualification binds
its five recorded review results, source/tool acceptance, exact written
content, elevated postflight, open default-reader and policy-preservation
findings, and the R5 readback finding. Later R6 acceptance, the failed
control-state repair preflight, and the v0.4.1 candidate remain separate facts.
The checker does not re-read the live installed copy or accept the new
correction. It is static source evidence, not a
fresh model run, review, acceptance, publication proof, or stable loaded-copy
proof.

Run the install lifecycle self-test:

```powershell
python -B scripts/manage_install.py self-test --source .
```

On Windows, run the complete self-test with a token capable of `icacls /save`,
single-record `/restore`, and `SetFileSecurityW`. The production lifecycle
performs the same control-aware restore-and-readback preflight against a private
replica and fails before destination mutation when the token or filesystem
cannot preserve and verify the existing DACL tree.

The self-test uses disposable temporary directories to exercise install,
status, update, rollback, unreceipted/mismatched/wrong-tree/modified/aliased/
drifted-destination refusal, uninstall, and recovery behavior. Mutating cases
exercise the legacy install/update/rollback/uninstall apply shape through
reported automatic external roots, then exercise the explicit external
same-volume route. They verify update/rollback routing, missing/overlapping/
declared-discovery-root/alias/reparse/cross-volume refusal before destination
mutation, old-copy preservation when the first backup move fails, and verified
restoration when a later stage move fails. On Windows they additionally verify
that each random per-operation transaction directory is protected before
staging, a new install inherits the destination-parent DACL, and a parent-wide
reader policy does not replace a narrower protected managed-target policy.
Raw `/save` snapshots of the root, package directories, all five files, and the
receipt must match after normal update, rollback, injected post-handoff failure
recovery, and partial-uninstall recovery. AI-bearing records use a one-record
`/restore`; deliberately no-AI records exercise `SetFileSecurityW`. Both paths
must round-trip exact control flags and ACE content. Injected snapshot and restore-preflight
failures must each produce zero move calls. A second focused path simulates a
successful `/restore` that changes nothing: semantic readback mismatch during
preflight must also produce zero move calls. Missing readback records must fail;
record reordering and LF/CRLF differences must compare equal; escaped paths,
changed P/AI/AR flags, and changed ACE order/content must not. An injected
mismatch after promotion must not report success and must
verify the recovered old target. If both promotion and recovery readbacks
mismatch, the operation must report incomplete recovery and retain the original
snapshot inside the protected transaction. Moved backup and tombstone trees
inherit the protected transaction DACL. Other platforms report
`PLATFORM_DEFAULT` and preserve the prior permission behavior. The reparse case is reported as
`UNAVAILABLE` when the host cannot create a disposable directory symlink or
junction; the deterministic production guard remains present. The self-test
does not install or remove a persistent Skill copy. Receipt checks establish
integrity and routing consistency, not cryptographic ownership against a
same-privilege local actor capable of forging the complete receipt.

The historical v0.3.0 local-release receipt binds accepted candidate C
`732e7efa6211d9aedeb133282ef28ce03f9bdfef`, candidate tree
`cc09ec16f85b05ed2287afd68ac6051dd800d287`, and historical package tree
`0ac3cbb0f1fa8fa51d8f832c8127eabc9863ec9e`. The SOURCE checker verifies that
fixed binding and the historical `LOCAL_RELEASE_READY=VERIFIED` transition.
Accepted Q06 provides
fresh projectless, read-only, no-tool, exact-SOURCE forward-behavior evidence
with `gpt-5.6-sol/high`; it does not prove installed-copy behavior,
publication, stable installation, cross-Harness behavior, or broad efficacy.

The historical v0.3.0 public-source descriptor
[`../../../release/v0.3.0-public-release-candidate.json`](../../../release/v0.3.0-public-release-candidate.json)
records the exact repository identity, default branch, intended annotated tag,
release-note owner, B1 receipt lineage, and historical package identity. The
SOURCE checker verifies that descriptor against its recorded release-note and
package identities. It does not prove the
public ref, tag, GitHub Release, or any persistent installation effect; those
require live public-object and installed-copy evidence tied to exact P.

The post-release evidence subject
[`../../../release/v0.3.0-public-release-evidence.json`](../../../release/v0.3.0-public-release-evidence.json)
binds exact public commit P, the annotated tag object and peeled commit, exact
human-approved Release title/body hash, bounded same-version persistent
lifecycle effects, final managed package identity, and two fresh projectless
installed-copy behavior witnesses. Those two remain historical evidence. After
the retained predecessor was preserved outside every Skill discovery root,
`B2-WC-SOLE-LOAD-02` freshly observed exactly one catalog-visible managed copy,
verified its receipt and five historical file hashes, and loaded the Skill body plus its
coordination/recovery and Standard O/P/E references. The recovery locator stays
controller-side. This evidence does not prove cross-version update/rollback,
cross-Harness behavior, untested contexts, or broad efficacy.

Planner acceptance `B2-WC-PUBLIC-EVIDENCE-F-01` verifies the exact post-release
evidence subject F `4ba904808fe86e270ebd405db1866d41d1cc032e` and tree
`03307594f66dfb92e262b73546fc4ec0ddb6d720`. The successor acceptance record
does not alter P, tag `v0.3.0`, the GitHub Release, package bytes, installed
copy, retained recovery copy, or the evidence limitations above.

The v0.4.0 local-release receipt binds accepted candidate commit
`30057490be21d869751854a51e9fafdfb535f206`, candidate tree
`a746f2eb4dc54db71f6ebd627da5f184929c9428`, package tree
`fd5ceb5cb0fbef4a1974b40b4da05800433d5511`, and the reviewed lifecycle
controller commit `08f72b404b1e127d6c461ac337a4e570c2c6800c`. It records five completed
independent-review results, both historical source finding dispositions, Planner source and
tool acceptance, the candidate-external trust-record digest, and one
explicit-root update attempt from v0.3.0 to v0.4.0. Elevated postflight matched
the installed receipt and all five package files, observed no residual
transaction entry, and removed the empty task transaction root. A subsequent
default-sandbox status and direct file read both failed with access denied. The
receipt records this as open runtime finding `WC-INSTALL-POSTFLIGHT-F01`,
separate from the five completed review results and two historical source
findings. R4 `WC-INSTALL-ACCESS-R4-RESULT-01` returned `NO_FINDINGS`, but Planner
acceptance opened P2 `WC-INSTALL-ACCESS-P01` because parent reset did not retain
explicit or protected DACL policy. R5
`WC-INSTALL-ACCESS-R5-RESULT-01` then opened P2
`WC-INSTALL-ACCESS-R5-F01` because `/restore` process success was not followed
by a target DACL readback. The receipt records the readback implementation as
fixed pending R6/Planner acceptance under P01 and confirms that no actual
installed-copy repair has been performed. The receipt deliberately omits
private path and task identifiers. This evidence verifies exact written content
and elevated postflight, not an accepted installation or transition.

After that immutable receipt checkpoint, R6 returned `NO_FINDINGS`, the Planner
accepted the source correction, and local commit
`df674c773de6f915627af541f0eb37221da9adef` recorded it. A later authorized
ACL-only repair captured and protected a rollback snapshot, then stopped before
target mutation because its private replica readback differed only in automatic-
inheritance control state: root `D:P` became `D:PAI` and the other records'
`D:` became `D:AI`. Exact path membership and ACE order/content were unchanged.
That counterevidence does not erase R6, but it invalidates whole-tree
`icacls /restore` as the accepted mechanism for a new repair attempt. The
actual target, parent ACL, content, receipt, and retained rollback evidence were
left unchanged.

A same-host disposable Windows probe exercised the superseded R4 correction without
touching the actual installed copy. Its outer transaction parent deliberately
carried the existing default-reader `ReadAndExecute` policy; the installer
itself removed inheritance from the random per-operation transaction directory
and restricted it to Owner Rights, SYSTEM, and Administrators before an
elevated process promoted the exact five files. The default sandbox identity
then read all five files and the receipt and obtained `MANAGED` status. After an injected
post-handoff failure, the old v0.4.0 target was restored, re-inherited the
destination-parent policy, and remained readable. A separate simulated backup
cleanup failure left the new target readable while exact-path access to the
retained backup was denied; ACL inspection showed the outer transaction parent
was reader-accessible, the random transaction directory had protected private
rules, the retained backup inherited only those rules, and the target inherited
the destination parent's reader access. The disposable tree was then removed.
That evidence proved installed-copy readability and recovery-material privacy,
but it did not test a narrower pre-existing target policy and therefore did not
close `WC-INSTALL-ACCESS-P01`. It remains historical R4 input only. This host evidence is
bounded to Windows/Python 3.12.10 and does not accept the correction or repair
the actual installation.

A later same-host R5 disposable probe directly targeted
`WC-INSTALL-ACCESS-P01`. Its destination parent carried the existing sandbox
reader `ReadAndExecute` rule, while the managed target root was protected for
Owner Rights, SYSTEM, and Administrators and one package file further limited
Owner Rights to read. The complete root/directory/five-file/receipt DACL
snapshot had SHA-256
`1e8fbde6f8b9d6402f0d2307b653b4904c738558e6a8e3b43a3e8c6367b97daf`.
Normal update reported `PRESERVED_FROM_PREVIOUS_DESTINATION`; its DACL snapshot
matched byte-for-byte. An injected failure after the promoted-target DACL
restore caused two restore calls, returned the prior managed version, and again
matched the baseline snapshot. Partial-uninstall recovery also returned the
managed version with an exact DACL match. The default sandbox reader was denied
receipt access after every phase, proving the wider parent policy did not
replace the narrower target policy. ACL inspection also confirmed the retained
recovery snapshot and partial tombstone remained behind a protected random
transaction directory. Cleanup of the exact disposable root was rejected by
the permission boundary, so that private task-scoped residue remains outside
all Skill discovery roots; the helper was removed. This evidence does not
close P01, satisfy the later R5 readback finding, or repair the actual
installation. The R5 finding does not invalidate these observed exact matches;
it requires the production lifecycle to perform that check on every restore.

The repair of the exact failed v0.4.0 installed copy remains ACL-only. Its first
authorized attempt stopped at the control-state preflight and made no target
mutation. A new attempt requires reviewed and accepted v0.4.1 source, any
separately required local commit, and separate execution authority. It must
again verify trusted v0.4.0 content/receipt, current and parent DACLs, and a
protected rollback snapshot before resetting only that exact target to parent
inheritance. Any failure restores and verifies the snapshot. Default-identity
status, all five file and receipt reads, hashes, and ACL inspection remain the
required postflight.

## Evidence limits

The retained cases are deterministic contract fixtures; they do not create
fresh model, efficacy, release, or installed-copy evidence. SOURCE qualification
proves clause coverage only. For v0.4.0, the accepted source candidate, six
completed independent-review results including later R6, and Planner source/tool
acceptance remain distinct completed evidence. The update attempt has exact
content and elevated postflight evidence but failed default-reader access, so
managed installation and `LOCAL_RELEASE_READY` remain blocked. The control-
state counterevidence and v0.4.1 disposable proof require fresh v0.4.1 review
and Planner acceptance; they do not prove an actual installed-copy repair or
post-repair result. The receipt does not prove
publication, stable installed-copy behavior, natural adherence, other
cross-version lifecycle effects, cross-Harness behavior, or broad product
efficacy.

## Future-version lifecycle boundary

The lifecycle command accepts `--trusted-target-package-tree` and `--trusted-current-package-tree` for versions outside its built-in trust map. These values are explicit external trust inputs, not candidate-derived metadata. B2 verifies same-version effects from exact public `v0.3.0`; the v0.4.0 receipt additionally verifies only the content and elevated postflight of the failed-access update attempt. Other cross-version behavior remains `UNKNOWN`. Dry runs and legacy apply calls retain their existing call shape. A legacy apply call without `--transaction-root` reports `AUTO_COMPATIBILITY` and uses a unique external same-volume root with the same overlap and reparse guards. Planned product installation, update, rollback, and uninstall commands supply `--transaction-root` explicitly; the operator repeats `--discovery-root` for active roots beyond the automatically protected destination parent and source `skills` directory. If recovery-archive cleanup fails after a successful uninstall, the command reports `ABSENT`, retains and identifies the archive and transaction path, and returns a warning instead of misreporting the completed uninstall as failed.
