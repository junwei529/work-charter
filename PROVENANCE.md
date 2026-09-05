# Provenance And Transformation Boundary

## Source identity

This standalone repository was materialized from named Git tree entries at
exact source commit `80910a8b2375a11be897e9660c4b00a06d00dd13`. The source commit tree is recorded in
[`provenance/source-map.json`](provenance/source-map.json).

The migration baseline files were read directly from the Git object database as
`80910a8b2375a11be897e9660c4b00a06d00dd13:<source-path>`; no clone, archive, installed copy, cache, discovery
mapping, or source working-tree byte was used.

The current `v0.4.0` update changes selected package, evaluation,
documentation, release-metadata, and checker files. Each changed destination is
classified as `repository-native` and bound to its current target SHA-256 in
the manifest. Unchanged destinations retain their prior exact-blob or
normalized-rewrite provenance. This preserves historical origin without making
a false byte-identity claim for new work.

## Transformation classes

- `exact-git-blob`: unchanged selected cases, fixtures, license, ignore rules,
  and applicable focused scripts are byte-identical to their named source blob.
- `standalone-normalized-text-rewrite`: repository instructions, product docs,
  evaluation index, checker, and this provenance summary were rewritten as
  UTF-8 without BOM with LF newlines. The manifest records every source path,
  source blob, source normalized-text SHA-256, and target SHA-256.
- `repository-native`: independently authored release metadata and lifecycle or
  qualification tooling added after the migration baseline. These files have
  no predecessor source blob; the manifest records their destination and exact
  target SHA-256.

The historical `v0.3.0` package behavior and evidence remain bound to their
recorded identities. The current `v0.4.0` candidate intentionally changes
package behavior; its independent review, Planner acceptance, installation,
and release remain pending. Historical monorepo operational detail and
cross-product release state remain omitted because full historical continuity
is not an acceptance requirement and would create a false standalone
dependency.

## Publication boundary

Tracked content contains no private task, host, checkout, account, destination,
or retained-quarantine locator. Immutable public commit
`b655c1aa42acc8c68b70e87c4c228445c5182d8b`, annotated tag `v0.3.0`, and the
public GitHub Release are independently verified. The post-release evidence
subject records bounded same-version install, update, rollback, uninstall, and
restoration effects plus fresh installed-copy behavior witnesses. The corrected
installed-state evidence preserves predecessor bytes outside every Skill
discovery root and binds one catalog-visible managed `work-charter`; its private
recovery locator remains controller-side. It makes no cross-version,
cross-Harness, untested-context, or broad-efficacy claim. Planner acceptance
`B2-WC-PUBLIC-EVIDENCE-F-01` verifies exact evidence subject F
`4ba904808fe86e270ebd405db1866d41d1cc032e` with tree
`03307594f66dfb92e262b73546fc4ec0ddb6d720`.

Those publication and installed-copy claims apply only to v0.3.0. The
`v0.4.0` descriptor is a local SOURCE candidate identity, not a receipt,
installation record, public ref, tag, or Release claim.

The repository-native lifecycle controller now confines every transient stage,
backup, tombstone, and recovery archive to a validated external task-scoped
transaction directory. Mutating operations fail closed before destination
changes when that directory is missing, aliased, link-like, inside or above a
declared Skill discovery root, or on a different filesystem volume. Existing
apply calls without an explicit root remain compatible through a visibly
reported, uniquely created automatic root subject to the same guards; planned
product operations still use an explicit operator-selected root. This controller
correction does not change the five-file installable package or any historical
v0.3.0 object.
