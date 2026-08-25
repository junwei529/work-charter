# Work Charter Verification

## Accepted migration baseline

- Source commit: `80910a8b2375a11be897e9660c4b00a06d00dd13`
- Package path: `skills/work-charter/`
- Package files: 5
- Provenance manifest: [`../../../provenance/source-map.json`](../../../provenance/source-map.json)

## Repository check

```powershell
python -B scripts/check_repository.py --json
```

This verifies exact Git-blob identity for package/case/fixture/license inputs,
the adapted-file hashes and source mappings, expected package and evaluation
shape, UTF-8/BOM and Markdown-link boundaries, and publication safety.
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
The admitted publication-classifier input domain is the UTF-8 text of mapped
repository files plus every string value consumed from the v1 provenance
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

The repository checker covers the retained deterministic cases and fixtures.

## Evidence limits

The retained cases are deterministic contract fixtures; they do not create fresh product, efficacy, release, or installed-copy evidence. A local clean commit and native review prove only this
standalone migration checkpoint; they do not authorize or prove publication,
installation, a remote, tag, Release, or broad product efficacy.
