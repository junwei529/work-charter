# Work Charter

[简体中文](README.zh-CN.md)

Bounds consequential Codex work by outcome, authority, evidence, recovery,
independent review, and proportional coordination.

This repository is the independent product repository for `work-charter`. Its
installable package is [`skills/work-charter/`](skills/work-charter/). It was
materialized from source commit `80910a8b2375a11be897e9660c4b00a06d00dd13`;
files changed for the current repository-native version are identified in the
source map rather than represented as unchanged migration blobs.

The current source candidate is `v0.4.0`, described by
[`release/v0.4.0-candidate.json`](release/v0.4.0-candidate.json). It adds
portable L0-L4 independent Reviewer semantics, separates Reviewer technical
findings from Executor verification and Planner/Orchestrator acceptance,
preserves the same Reviewer and cumulative findings across repair re-review,
defines evidence-first `UNKNOWN` handling and context-switch recovery, and
limits callback and graph claims. The descriptor remains the immutable
pre-review snapshot. The accepted source candidate, five completed independent
review rounds, reviewed lifecycle-controller baseline, and attempted v0.3-to-v0.4 update
are bound separately by
[`release/v0.4.0-local-release-receipt.json`](release/v0.4.0-local-release-receipt.json),
but the update is not accepted: its exact bytes and receipt passed elevated
postflight while the default sandbox reader could not read the promoted copy.
Source-candidate acceptance remains `VERIFIED`; `LOCAL_RELEASE_READY` and the
managed installation are blocked pending review, acceptance, and application
of the bounded ACL correction. R4 returned `NO_FINDINGS`, but Planner acceptance
opened `WC-INSTALL-ACCESS-P01` because the reviewed parent-reset route did not
preserve an existing explicit or protected DACL policy. R5 then opened P2
`WC-INSTALL-ACCESS-R5-F01` because command success was not followed by a target
DACL readback; the implementation below is fixed pending R6 and Planner
acceptance. Stable loaded-copy behavior, natural adherence, cross-Harness
behavior, public release, and broad efficacy remain failed, `UNKNOWN`, or
separately authorized as recorded.

## Historical v0.3.0 evidence

The first independent version is `v0.3.0`. Its historical local candidate is
described by [`release/v0.3.0-candidate.json`](release/v0.3.0-candidate.json);
its public identity is `junwei529/work-charter`. Exact candidate C was accepted
and is bound by [`release/v0.3.0-local-release-receipt.json`](release/v0.3.0-local-release-receipt.json),
so `LOCAL_RELEASE_READY` is `VERIFIED`. `PUBLIC_RELEASE` is `VERIFIED` for
immutable public commit `b655c1aa42acc8c68b70e87c4c228445c5182d8b`, annotated
tag `v0.3.0`, and the public GitHub Release.
The immutable candidate descriptor retains its original
`PENDING_PLANNER_ACCEPTANCE` snapshot rather than rewriting C.

The immutable public-source candidate is described by
[`release/v0.3.0-public-release-candidate.json`](release/v0.3.0-public-release-candidate.json).
It preserves the package bytes and records the intended public repository,
default branch, tag, and human release-note gate without containing its own
commit hash. An exact public ref and later release receipt must bind that commit;
the annotated tag and GitHub Release were later created after explicit human
approval.

The post-release evidence subject is recorded in
[`release/v0.3.0-public-release-evidence.json`](release/v0.3.0-public-release-evidence.json).
It binds the public objects, bounded same-version persistent lifecycle effects,
the two historical projectless witnesses, and a fresh sole-discovery loaded-copy
witness. The retained predecessor bytes are preserved outside every Skill
discovery root, so the managed user installation is the only catalog-visible
`work-charter`. Planner acceptance `B2-WC-PUBLIC-EVIDENCE-F-01` verifies exact
subject F `4ba904808fe86e270ebd405db1866d41d1cc032e`; cross-version lifecycle
behavior, cross-Harness behavior, untested contexts, and broad efficacy remain
`UNKNOWN`.

## Repository contents

- Product package: [`skills/work-charter/`](skills/work-charter/)
- Product design and state: [`docs/skills/work-charter/`](docs/skills/work-charter/)
- Evaluation cases and fixtures: [`evals/`](evals/README.md)
- Standalone verification: [`scripts/check_repository.py`](scripts/check_repository.py)
- SOURCE contract qualification: [`scripts/check_source_contract.py`](scripts/check_source_contract.py)
- Install lifecycle tool: [`scripts/manage_install.py`](scripts/manage_install.py)
- Source mapping: [`PROVENANCE.md`](PROVENANCE.md) and
  [`provenance/source-map.json`](provenance/source-map.json)
- Release notes: [`CHANGELOG.md`](CHANGELOG.md)

## Verify

```powershell
python -B scripts/check_repository.py --json
python -B scripts/check_source_contract.py --json
python -B scripts/manage_install.py self-test --source .
```

The SOURCE check proves that the current candidate instructions contain the
required selection, activation, authority, recovery, independent-review, and
Standard O/P/E/R boundaries while preserving fixed historical v0.3 identities
and validating the exact v0.4 attempt receipt, open access finding, and pending
source correction. It does not execute a model, re-read the live installed
copy, accept that correction, prove publication, or establish broad efficacy.

## Future immutable-source lifecycle

Use an exact immutable checkout of `junwei529/work-charter` as `--source` and
an explicit destination. Commands are dry-run plans unless `--apply` is added:

```powershell
python -B scripts/manage_install.py status --destination <skill-destination> [--trusted-current-package-tree <git-tree-sha1>]
python -B scripts/manage_install.py install --source <v0.3.0-immutable-checkout> --destination <skill-destination> --expected-version 0.3.0
python -B scripts/manage_install.py update --source <new-immutable-checkout> --destination <skill-destination> --expected-version <new-version>
python -B scripts/manage_install.py rollback --source <old-immutable-checkout> --destination <skill-destination> --expected-version <old-version>
python -B scripts/manage_install.py uninstall --destination <skill-destination> [--trusted-current-package-tree <git-tree-sha1>]
```

For any planned product mutation, first create an absolute task-scoped
transaction directory on the same filesystem volume as the destination,
outside every Skill discovery root, then add
`--apply --transaction-root <external-task-directory>`. The tool automatically
protects the destination parent and the source checkout's `skills` directory;
repeat `--discovery-root <absolute-path>` for every additional active Skill
discovery root. It rejects missing, relative, aliased, link-like, overlapping,
or cross-volume explicit paths before changing the destination.

Existing `--apply` calls that omit `--transaction-root` remain behaviorally
compatible: the tool creates a unique validated same-volume directory outside
the destination discovery root, reports `AUTO_COMPATIBILITY`, and removes that
directory after a clean result. This fallback does not authorize or replace the
explicit path required by a planned installation or release operation. In both
modes, stage, backup, tombstone, and recovery-archive material stays under the
external per-operation transaction directory. A failure to move the old
destination to backup leaves that destination untouched; a later replacement
failure restores and verifies the old managed copy or reports the preserved
recovery path. The pending Windows correction first removes inheritance from
each random per-operation transaction directory and grants access only to Owner
Rights, SYSTEM, and Administrators. A new install inherits the destination
parent's existing DACL. Before update, rollback, or uninstall mutation, the tool
saves the complete existing DACL tree inside the private transaction, restores
it to a private replica as a capability preflight, reads the replica back with
the same bounded `/save` representation, and fails closed if that cannot
complete or match. The comparison ignores record enumeration order and newline
serialization, but requires the same managed path set and exact DACL SDDL for
each path, including inheritance/protection flags and ACE order/content. The
saved policy is then applied to the promoted or recovered target and read back
under the same rule before success is reported; backup and tombstone trees
inherit the private transaction DACL. A preflight mismatch occurs before any
target move. A later mismatch enters existing recovery, and the original
snapshot remains in the protected transaction when recovery is incomplete.
Other platforms retain their prior platform-default permission behavior. On
Windows, the full lifecycle self-test must run with a token capable of
`icacls /restore` and `/save`; an incapable token is rejected before destination
mutation.

The install example is deliberately bound to an immutable v0.3.0 checkout,
whose package tree is already in the bundled trust map. Do not substitute this
working checkout into that historical command. The current v0.4.0 package was
subsequently reviewed, accepted, externally trust-bound, and written through
the explicit route recorded in its local-release receipt, but the promoted
directory retained the transaction ACL and failed default-reader access. The
working source contains a bounded Windows DACL-preservation and post-restore
readback correction that still requires R6 independent review and Planner
acceptance before it may repair the installed copy. The v0.4 package tree is
not added to the tool's historical built-in map, so later status or mutation
must continue to receive the independently retained v0.4 trust identity.

The proposed repair for that exact failed v0.4.0 copy is ACL-only, not a generic
update that discards arbitrary policy. After source review, Planner acceptance,
and local commit, it first verifies the independently trusted v0.4.0 content and
receipt, the recorded private current DACL, and the separately verified
destination-parent reader policy. It then saves and preflights a rollback DACL
snapshot before resetting only that exact target to parent inheritance; any
failure restores the snapshot. Default-identity status, direct reads, hashes,
and ACL inspection are required postflight. This route is not yet executed.

The tool refuses destinations that are unreceipted, have a malformed or
mismatched receipt, use the wrong package tree, are locally modified or aliased,
or otherwise drift from the receipt. The receipt is an integrity and routing
record, not cryptographic ownership proof: a same-privilege local actor capable
of forging the complete receipt is outside this mechanism's protection.
For v0.3.0, the separately authorized persistent same-version lifecycle,
publication, tag, GitHub Release, and stable installed-copy evidence are
verified as recorded above. For v0.4.0, only the written bytes and elevated
receipt/file postflight from the v0.3-to-v0.4 attempt are verified; default
reader access failed, so the overall transition is not accepted. Other
cross-version transitions and stable loaded behavior still require separate
evidence.

### Future update and rollback trust

The bundled trust map authorizes the v0.3.0 package tree only. A later immutable release must publish its human-reviewed package-tree identity independently of the candidate checkout. Supply that external trust anchor with `--trusted-target-package-tree <git-tree-sha1>` when updating or rolling back to a version not bundled in this tool. If the currently installed version is also absent from the bundled map, supply its independently retained identity with `--trusted-current-package-tree <git-tree-sha1>` for update, rollback, status, and uninstall. Never copy either trust value from the source tree being installed; future-version public release and cross-version lifecycle evidence remain `UNKNOWN` until separately established.
