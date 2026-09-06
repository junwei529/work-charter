# Work Charter

[简体中文](README.zh-CN.md)

Bounds consequential Codex work by outcome, authority, evidence, recovery,
independent review, and proportional coordination.

This repository is the independent product repository for `work-charter`. Its
installable package is [`skills/work-charter/`](skills/work-charter/). It was
materialized from source commit `80910a8b2375a11be897e9660c4b00a06d00dd13`;
files changed for the current repository-native version are identified in the
source map rather than represented as unchanged migration blobs.

The current source candidate is `v0.5.0`, described by
[`release/v0.5.0-candidate.json`](release/v0.5.0-candidate.json). It adds a
strict external role-model configuration contract and a sixth package file,
while retaining the accepted v0.4.1 operation-local permission and exact DACL
restoration corrections. The descriptor is a pending pre-review snapshot;
there is no v0.5.0 receipt, installation, runtime role-delivery claim, or public
release claim.

The immutable v0.4.0 receipt binds its accepted candidate, five review results,
and the failed v0.3-to-v0.4 update at that checkpoint:
[`release/v0.4.0-local-release-receipt.json`](release/v0.4.0-local-release-receipt.json).
The later sixth result, R6, found no source issue and Planner accepted the prior
correction, which was committed as
`df674c773de6f915627af541f0eb37221da9adef`. A first authorized repair preflight
then stopped because `icacls /restore` changed automatic-inheritance control
state. The v0.4.1 C4 correction replaced that path with exact control-aware
restore and readback and was independently accepted at
`59b4d91f46c2ac797c71c900e62dda87cf0cca60`. A later ACL-only repair restored
default-reader access to the exact managed v0.4.0 copy and closed
`WC-INSTALL-POSTFLIGHT-F01` for that repair. The installed package remains
managed v0.4.0; v0.4.1 was not installed. Stable v0.5.0 loaded-copy behavior,
role-delivery adherence, cross-provider execution, cross-Harness behavior,
public release, and broad efficacy remain `UNKNOWN` or separately authorized.

## Role-model configuration

The package default is
[`skills/work-charter/assets/role-models.default.yaml`](skills/work-charter/assets/role-models.default.yaml):

| Role | Provider | Model | Reasoning effort |
|---|---|---|---|
| Orchestrator | OpenAI | `gpt-6-astra` | `xhigh` |
| Planner | OpenAI | `gpt-6-astra` | `xhigh` |
| Executor | OpenAI | `gpt-5.6-sol` | `high` |
| Reviewer | OpenAI | `gpt-6-astra` | `high` |

To customize later role deliveries, copy that file to
`~/.config/work-charter/role-models.yaml` and edit it, or have an approved
delivery contract name another exact file. No user file means the package
default applies. A user file may contain only changed roles, but each supplied
role replaces its whole default object and must repeat `provider` and `model`;
omitting `parameters` means no parameters for that role. Other absent roles
retain their package defaults. A missing or unreadable explicitly selected file
is an error rather than a fallback.

An already frozen delivery combination has priority over later file contents.
Before a newly authorized role is created, its dispatcher shows the resolved
role/provider/model/parameters and source and verifies support through the
intended native route. Codex OpenAI delivery maps `model` to native `model` and
`reasoning_effort` to `thinking`. Unsupported or ambiguous schema, fields,
provider, model, or parameters stop delivery; configuration never supplies role
authority, credentials, endpoints, or commands. Existing roles do not change
when the file changes. Install, update, rollback, and uninstall never create,
modify, or delete the external user file.

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
required selection, activation, authority, recovery, independent-review,
role-model resolution, and Standard O/P/E/R boundaries while preserving fixed
historical release identities. It does not execute a model, create a role,
read a live user configuration, re-read the installed copy, perform an
installation, prove publication, or establish broad efficacy.

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
recovery path. The v0.4.1 Windows correction first removes inheritance from
each random per-operation transaction directory and grants access only to Owner
Rights, SYSTEM, and Administrators. A new install inherits the destination
parent's existing DACL. Before update, rollback, or uninstall mutation, the tool
saves the complete existing DACL tree inside the private transaction and
restores it path by path to a private replica. Records whose snapshot already
contains AI use a one-record `icacls /restore`; records without AI use
`SetFileSecurityW` with DACL and, when required, protected-DACL information so
the setter does not propagate a directory policy to children. Shallow-to-deep
application is followed by the same bounded `/save` readback. The comparison
ignores record enumeration order and newline serialization, but requires the
same managed path set and exact DACL SDDL for each path, including P, AI, AR,
and ACE order/content. Unsupported control states or any mismatch fail before a
target move. The saved policy is then applied to the promoted or recovered
target and read back under the same rule before success is reported; backup and
tombstone trees inherit the private transaction DACL. A later mismatch enters
existing recovery, and the original snapshot remains in the protected
transaction when recovery is incomplete. Other platforms retain their prior
platform-default permission behavior.

Historical five-file receipts and candidate descriptors and the current six-
file descriptor are recognized only as exact allow-listed package shapes. A
legacy five-file candidate may omit the redundant package digest because its
actual tree must still match an independent trusted tree; the current six-file
shape requires the digest, and any supplied invalid or mismatched digest fails
closed. For a Windows update or rollback whose path set changes, the tool first
proves the original recovery
snapshot on a private replica, transforms only that replica to the target path
shape, resets only newly introduced paths to parent inheritance, verifies that
every common descriptor is unchanged and every new path is auto-inherited and
unprotected, and proves an exact readback of the projected snapshot. The
original snapshot remains the recovery authority. Unknown or self-declared
path sets, unsafe receipt keys, missing or extra paths, and tree mismatches fail
closed.

The install example is deliberately bound to an immutable v0.3.0 checkout,
whose package tree is already in the bundled trust map. Do not substitute this
working checkout into that historical command. The v0.4.0 package was reviewed,
accepted, externally trust-bound, and written through
the explicit route recorded in its local-release receipt, but the promoted
directory retained the transaction ACL and failed default-reader access. The
committed v0.4.0 correction still failed its first later actual-policy
preflight because `/restore` changed AI. The accepted v0.4.1 C4 source replaces
that restore path and also tightens permission-question routing. Its later
ACL-only application restored the exact v0.4.0 installed copy's default-reader
access; it did not install the v0.4.1 package. Neither v0.4 package tree is
added to the tool's historical built-in map, so later status or mutation must
continue to receive the independently retained trust identity.

The repair for that exact failed v0.4.0 copy remained ACL-only, not a generic
update that discards arbitrary policy. Its first authorized attempt stopped
before target mutation; the later bounded attempt used accepted C4 source,
reverified trusted content/receipt and rollback inputs, changed only the target
DACL, and passed default-identity status, direct-read, hash, and ACL postflight.
That result does not authorize another repair, package update, or installation.

The tool refuses destinations that are unreceipted, have a malformed or
mismatched receipt, use the wrong package tree, are locally modified or aliased,
or otherwise drift from the receipt. The receipt is an integrity and routing
record, not cryptographic ownership proof: a same-privilege local actor capable
of forging the complete receipt is outside this mechanism's protection.
For v0.3.0, the separately authorized persistent same-version lifecycle,
publication, tag, GitHub Release, and stable installed-copy evidence are
verified as recorded above. For v0.4.0, the original promotion failure and the
later exact ACL-only access repair remain separate evidence; the repaired copy
is managed and default-readable, but it is still v0.4.0. Other cross-version
transitions and stable loaded behavior still require separate evidence.

### Future update and rollback trust

The bundled trust map authorizes the v0.3.0 package tree only. A later immutable release must publish its human-reviewed package-tree identity independently of the candidate checkout. Supply that external trust anchor with `--trusted-target-package-tree <git-tree-sha1>` when updating or rolling back to a version not bundled in this tool. If the currently installed version is also absent from the bundled map, supply its independently retained identity with `--trusted-current-package-tree <git-tree-sha1>` for update, rollback, status, and uninstall. Never copy either trust value from the source tree being installed; future-version public release and cross-version lifecycle evidence remain `UNKNOWN` until separately established.
