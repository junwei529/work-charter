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
limits callback and graph claims. Independent review, Planner acceptance,
installation, and public release remain pending and separately authorized.

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
Standard O/P/E/R boundaries while preserving fixed historical v0.3 identities.
It does not prove model compliance, installed-copy behavior, acceptance,
publication, or broad efficacy.

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
recovery path.

The install example is deliberately bound to an immutable v0.3.0 checkout,
whose package tree is already in the bundled trust map. Do not substitute this
working v0.4.0 candidate checkout: v0.4.0 still requires independent review,
Planner acceptance, and a trusted package-tree identity published outside the
candidate before installation can use the later-version trust route.

The tool refuses destinations that are unreceipted, have a malformed or
mismatched receipt, use the wrong package tree, are locally modified or aliased,
or otherwise drift from the receipt. The receipt is an integrity and routing
record, not cryptographic ownership proof: a same-privilege local actor capable
of forging the complete receipt is outside this mechanism's protection.
For v0.3.0, the separately authorized persistent same-version lifecycle,
publication, tag, GitHub Release, and stable installed-copy evidence are
verified as recorded above. Future-version and cross-version lifecycle effects
still require separate authorization and evidence.

### Future update and rollback trust

The bundled trust map authorizes the v0.3.0 package tree only. A later immutable release must publish its human-reviewed package-tree identity independently of the candidate checkout. Supply that external trust anchor with `--trusted-target-package-tree <git-tree-sha1>` when updating or rolling back to a version not bundled in this tool. If the currently installed version is also absent from the bundled map, supply its independently retained identity with `--trusted-current-package-tree <git-tree-sha1>` for update, rollback, status, and uninstall. Never copy either trust value from the source tree being installed; future-version public release and cross-version lifecycle evidence remain `UNKNOWN` until separately established.
