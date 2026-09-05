#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import uuid
from pathlib import Path, PureWindowsPath


RECEIPT_NAME = ".work-charter-install.json"
RECEIPT_SCHEMA = "work-charter-install-receipt/v1"
EXPECTED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "assets/work-charter.md",
    "references/coordination-and-recovery.md",
    "references/standard-ope.md",
}
EXPECTED_DIRECTORIES = {
    Path(relative).parent.as_posix()
    for relative in EXPECTED_FILES
    if Path(relative).parent.as_posix() != "."
}
TRUSTED_PACKAGE_TREES = {
    "0.3.0": "0ac3cbb0f1fa8fa51d8f832c8127eabc9863ec9e",
}
SELF_TEST_SOURCE_VERSION = "0.4.0"


class LifecycleError(RuntimeError):
    pass


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolved(path):
    return Path(path).expanduser().resolve(strict=False)


def is_link_like(path):
    if path.is_symlink():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def assert_no_link_like_components(path, label):
    path = Path(path)
    for component in (path, *path.parents):
        try:
            metadata = component.lstat()
        except FileNotFoundError:
            continue
        except OSError as error:
            raise LifecycleError(f"{label} path component is unreadable: {component}: {error}") from error
        if stat.S_ISLNK(metadata.st_mode) or bool(
            getattr(metadata, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        ):
            raise LifecycleError(
                f"{label} or ancestor is a symbolic link, junction, or reparse point"
            )


def canonical_path_text(path):
    return os.path.normcase(os.path.normpath(os.fspath(path)))


def assert_safe_destination(destination, source=None):
    unresolved = Path(destination).expanduser().absolute()
    assert_no_link_like_components(unresolved, "destination")
    destination = unresolved.resolve(strict=False)
    if canonical_path_text(unresolved) != canonical_path_text(destination):
        raise LifecycleError("destination must use its exact canonical path, not an alias")
    if destination == Path(destination.anchor) or destination == Path.home().resolve():
        raise LifecycleError("destination must not be a filesystem root or home directory")
    if source is not None:
        source = resolved(source)
        if destination == source or source in destination.parents or destination in source.parents:
            raise LifecycleError("destination and source repository must not contain each other")
    return destination


def paths_overlap(left, right):
    return left == right or left in right.parents or right in left.parents


def nearest_existing_path(path):
    candidate = Path(path)
    while True:
        try:
            candidate.lstat()
            return candidate
        except FileNotFoundError:
            parent = candidate.parent
            if parent == candidate:
                raise LifecycleError(f"no existing ancestor for path: {path}")
            candidate = parent
        except OSError as error:
            raise LifecycleError(f"path component is unreadable: {candidate}: {error}") from error


def volume_identity(path):
    existing = nearest_existing_path(path)
    try:
        metadata = existing.stat()
    except OSError as error:
        raise LifecycleError(f"cannot determine filesystem volume for {path}: {error}") from error
    canonical = existing.resolve(strict=True)
    return metadata.st_dev, canonical_path_text(Path(canonical.anchor))


def assert_safe_transaction_root(
    transaction_root,
    destination,
    source=None,
    discovery_roots=(),
    volume_identity_getter=None,
    require_existing=True,
):
    if transaction_root is None:
        raise LifecycleError("transaction root is required")
    declared = Path(transaction_root).expanduser()
    if not declared.is_absolute():
        raise LifecycleError("transaction root must be an absolute path")
    unresolved = declared.absolute()
    assert_no_link_like_components(unresolved, "transaction root")
    try:
        root = unresolved.resolve(strict=require_existing)
    except (FileNotFoundError, OSError) as error:
        raise LifecycleError(f"transaction root must be an existing directory: {error}") from error
    if require_existing and not root.is_dir():
        raise LifecycleError("transaction root must be an existing directory")
    if not require_existing and root.exists():
        raise LifecycleError("automatic transaction root must not already exist")
    if canonical_path_text(unresolved) != canonical_path_text(root):
        raise LifecycleError("transaction root must use its exact canonical path, not an alias")
    if root == Path(root.anchor) or root == Path.home().resolve():
        raise LifecycleError("transaction root must not be a filesystem root or home directory")

    protected = [("destination", destination), ("destination discovery root", destination.parent)]
    if source is not None:
        protected.extend(
            [
                ("source repository", source),
                ("source Skill discovery root", source / "skills"),
            ]
        )
    for index, discovery_root in enumerate(discovery_roots):
        declared_discovery_root = Path(discovery_root).expanduser()
        if not declared_discovery_root.is_absolute():
            raise LifecycleError(f"additional discovery root {index + 1} must be an absolute path")
        unresolved_discovery_root = declared_discovery_root.absolute()
        assert_no_link_like_components(
            unresolved_discovery_root,
            f"additional discovery root {index + 1}",
        )
        protected.append(
            (
                f"additional Skill discovery root {index + 1}",
                unresolved_discovery_root.resolve(strict=False),
            )
        )
    for label, protected_path in protected:
        protected_path = Path(protected_path).resolve(strict=False)
        if paths_overlap(root, protected_path):
            raise LifecycleError(f"transaction root must be outside {label}: {protected_path}")

    identify_volume = volume_identity_getter or volume_identity
    if identify_volume(root) != identify_volume(destination):
        raise LifecycleError("transaction root and destination must be on the same filesystem volume")
    return root


def create_automatic_transaction_root(
    destination,
    source=None,
    discovery_roots=(),
    volume_identity_getter=None,
):
    container = nearest_existing_path(destination.parent.parent).resolve(strict=True)
    if not container.is_dir():
        raise LifecycleError("automatic transaction root has no existing directory parent")
    candidate = container / f".wca-{uuid.uuid4().hex}"
    root = assert_safe_transaction_root(
        candidate,
        destination,
        source,
        discovery_roots,
        volume_identity_getter,
        require_existing=False,
    )
    try:
        root.mkdir(mode=0o700)
        return assert_safe_transaction_root(
            root,
            destination,
            source,
            discovery_roots,
            volume_identity_getter,
        )
    except Exception:
        try:
            root.rmdir()
        except OSError:
            pass
        raise


def windows_acl_tool():
    system_root = os.environ.get("SystemRoot")
    if not system_root:
        raise LifecycleError("cannot locate the Windows system directory for ACL handoff")
    system_root_path = Path(system_root)
    if not system_root_path.is_absolute():
        raise LifecycleError("Windows system directory for ACL handoff is not absolute")
    executable = system_root_path / "System32" / "icacls.exe"
    if not executable.is_file():
        raise LifecycleError("cannot locate the Windows ACL tool")
    return executable


def run_windows_acl(path, arguments, operation):
    try:
        completed = subprocess.run(
            [str(windows_acl_tool()), str(path), *arguments],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise LifecycleError(f"Windows ACL {operation} could not complete") from error
    if completed.returncode != 0:
        raise LifecycleError(
            f"Windows ACL {operation} failed with tool exit code {completed.returncode}"
        )


def harden_transaction_permissions(transaction):
    if os.name != "nt":
        return "PLATFORM_DEFAULT"
    run_windows_acl(transaction, ["/inheritance:r", "/Q"], "transaction isolation")
    run_windows_acl(
        transaction,
        [
            "/grant:r",
            "*S-1-3-4:(OI)(CI)(F)",
            "*S-1-5-18:(OI)(CI)(F)",
            "*S-1-5-32-544:(OI)(CI)(F)",
            "/Q",
        ],
        "transaction isolation",
    )
    return "PRIVATE_OWNER_SYSTEM_ADMINISTRATORS"


def create_transaction_directory(transaction_root):
    transaction = transaction_root / f".wct-{uuid.uuid4().hex}"
    transaction.mkdir(mode=0o700)
    try:
        permission_result = harden_transaction_permissions(transaction)
        if permission_result not in {
            "PRIVATE_OWNER_SYSTEM_ADMINISTRATORS",
            "PLATFORM_DEFAULT",
        }:
            raise LifecycleError("transaction permission isolation returned an invalid result")
        assert_no_link_like_components(transaction, "transaction directory")
        return transaction
    except Exception:
        try:
            transaction.rmdir()
        except OSError:
            pass
        raise


def remove_empty_transaction_directory(transaction):
    try:
        transaction.rmdir()
    except FileNotFoundError:
        pass
    except OSError:
        # A preserved recovery artifact or concurrent unexpected entry makes the
        # transaction path part of the caller-visible recovery surface.
        return False
    return True


def remove_completed_transaction(transaction, transaction_root, remove_root):
    if not remove_empty_transaction_directory(transaction):
        return False
    if remove_root and not remove_empty_transaction_directory(transaction_root):
        return False
    return True


def transaction_recovery_path(transaction, transaction_root):
    return transaction if transaction.exists() else transaction_root


def remove_permission_snapshot(snapshot):
    try:
        Path(snapshot).unlink(missing_ok=True)
    except OSError:
        return False
    return True


def candidate_metadata(source, expected_version):
    source = resolved(source)
    path = source / "release" / f"v{expected_version}-candidate.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise LifecycleError(f"candidate descriptor is unreadable: {error}") from error
    if not isinstance(value, dict) or not isinstance(value.get("package"), dict):
        raise LifecycleError("candidate descriptor must be an object with an object package")
    if (
        value.get("schema") != "work-charter-local-release-candidate/v1"
        or value.get("product") != "work-charter"
        or value.get("public_identity") != "junwei529/work-charter"
        or value.get("version") != expected_version
        or not isinstance(value.get("package", {}).get("tree"), str)
        or len(value["package"]["tree"]) != 40
        or any(character not in "0123456789abcdef" for character in value["package"]["tree"])
    ):
        raise LifecycleError("candidate descriptor identity mismatch")
    return value


def git_object_hash(kind, data):
    header = f"{kind} {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def git_tree_hash(directory, excluded_names=frozenset()):
    children = [child for child in directory.iterdir() if child.name not in excluded_names]
    children.sort(
        key=lambda child: (child.name + ("/" if child.is_dir() else "")).encode("utf-8")
    )
    entries = []
    for child in children:
        if is_link_like(child):
            raise LifecycleError(f"package contains a symbolic link, junction, or reparse point: {child.name}")
        if child.is_dir():
            mode = b"40000"
            digest = bytes.fromhex(git_tree_hash(child))
        elif child.is_file():
            mode = b"100644"
            digest = bytes.fromhex(git_object_hash("blob", child.read_bytes()))
        else:
            raise LifecycleError(f"package contains an unsupported path: {child.name}")
        entries.append(mode + b" " + child.name.encode("utf-8") + b"\0" + digest)
    return git_object_hash("tree", b"".join(entries))


def package_files(source, expected_tree):
    package = resolved(source) / "skills" / "work-charter"
    if not package.is_dir() or is_link_like(package):
        raise LifecycleError("package root is missing or link-like")
    actual = {
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file()
    }
    if any(is_link_like(path) for path in package.rglob("*")):
        raise LifecycleError("package contains a symbolic link, junction, or reparse point")
    if actual != EXPECTED_FILES:
        raise LifecycleError(f"package path set mismatch: {sorted(actual)}")
    tree = git_tree_hash(package)
    if tree != expected_tree:
        raise LifecycleError(f"package tree mismatch: expected {expected_tree}, got {tree}")
    return package, {relative: sha256(package / relative) for relative in sorted(actual)}, tree


def package_digest(files):
    encoded = json.dumps(files, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def read_receipt(destination):
    receipt_path = destination / RECEIPT_NAME
    if not receipt_path.is_file():
        return None
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise LifecycleError(f"managed receipt is unreadable: {error}") from error
    if not isinstance(receipt, dict) or not isinstance(receipt.get("destination"), str):
        raise LifecycleError("destination receipt shape mismatch")
    if (
        receipt.get("schema") != RECEIPT_SCHEMA
        or receipt.get("product") != "work-charter"
        or receipt.get("public_identity") != "junwei529/work-charter"
        or resolved(receipt.get("destination", "")) != destination
    ):
        raise LifecycleError("destination receipt is malformed, mismatched, or aliased")
    return receipt


def current_state(destination, trusted_tree=None):
    destination = resolved(destination)
    if not destination.exists():
        return {"state": "ABSENT"}
    if not destination.is_dir():
        return {"state": "FOREIGN_COPY", "reason": "destination is not a directory"}
    try:
        receipt = read_receipt(destination)
    except LifecycleError as error:
        return {"state": "DRIFTED", "reason": str(error)}
    if receipt is None:
        return {"state": "FOREIGN_COPY", "reason": "management receipt is absent"}
    expected = receipt.get("files")
    if not isinstance(expected, dict) or set(expected) != EXPECTED_FILES:
        return {"state": "DRIFTED", "reason": "receipt file set mismatch"}
    version = receipt.get("version")
    if not isinstance(version, str):
        return {"state": "DRIFTED", "reason": "receipt version is invalid"}
    trusted_tree = TRUSTED_PACKAGE_TREES.get(version) or trusted_tree
    if trusted_tree is None or receipt.get("package_tree") != trusted_tree:
        return {"state": "FOREIGN_COPY", "reason": "receipt is not bound to a trusted package tree"}
    entries = list(destination.rglob("*"))
    if any(is_link_like(path) for path in entries):
        return {
            "state": "DRIFTED",
            "reason": "managed package contains a symbolic link, junction, or reparse point",
        }
    actual = {
        path.relative_to(destination).as_posix()
        for path in entries
        if path.is_file() and path.relative_to(destination).as_posix() != RECEIPT_NAME
    }
    if actual != EXPECTED_FILES:
        return {"state": "DRIFTED", "reason": "managed file set mismatch"}
    actual_directories = {
        path.relative_to(destination).as_posix()
        for path in entries
        if path.is_dir()
    }
    if actual_directories != EXPECTED_DIRECTORIES:
        return {"state": "DRIFTED", "reason": "managed directory set mismatch"}
    actual_hashes = {}
    for relative, expected_hash in expected.items():
        actual_hash = sha256(destination / relative)
        actual_hashes[relative] = actual_hash
        if actual_hash != expected_hash:
            return {"state": "DRIFTED", "reason": f"managed file changed: {relative}"}
    if receipt.get("package_sha256") != package_digest(actual_hashes):
        return {"state": "DRIFTED", "reason": "managed package digest mismatch"}
    if git_tree_hash(destination, {RECEIPT_NAME}) != trusted_tree:
        return {"state": "DRIFTED", "reason": "managed package tree mismatch"}
    return {
        "state": "MANAGED",
        "version": version,
        "package_sha256": receipt.get("package_sha256"),
        "package_tree": receipt.get("package_tree"),
    }


def write_receipt(destination, metadata, files, receipt_destination=None):
    receipt_destination = resolved(receipt_destination or destination)
    receipt = {
        "destination": str(receipt_destination),
        "files": files,
        "package_sha256": package_digest(files),
        "package_tree": metadata["package"]["tree"],
        "product": "work-charter",
        "public_identity": "junwei529/work-charter",
        "schema": RECEIPT_SCHEMA,
        "version": metadata["version"],
    }
    text = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    (destination / RECEIPT_NAME).write_text(text, encoding="utf-8", newline="\n")


def stage_source(package, files, destination, metadata, transaction):
    stage = transaction / "stage"
    stage.mkdir()
    try:
        for relative in sorted(files):
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(package / relative, target)
        write_receipt(stage, metadata, files, destination)
        if any(sha256(stage / relative) != digest for relative, digest in files.items()):
            raise LifecycleError("staged package failed file verification")
        return stage, metadata, files
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def reconcile_inherited_permissions(path):
    if os.name != "nt":
        return "PLATFORM_DEFAULT"
    run_windows_acl(path, ["/reset", "/T", "/Q"], "parent-inheritance handoff")
    return "INHERITED_FROM_PARENT"


def capture_permission_snapshot(path, snapshot):
    if os.name != "nt":
        return None
    snapshot = Path(snapshot)
    if snapshot.exists():
        raise LifecycleError("permission snapshot path already exists")
    run_windows_acl(
        path,
        ["/save", str(snapshot), "/T", "/Q"],
        "DACL snapshot",
    )
    try:
        if not snapshot.is_file() or snapshot.stat().st_size == 0:
            raise LifecycleError("Windows DACL snapshot is missing or empty")
        return sha256(snapshot)
    except OSError as error:
        raise LifecycleError("Windows DACL snapshot is unreadable") from error


def windows_dacl_snapshot_records(snapshot):
    snapshot = Path(snapshot)
    try:
        raw = snapshot.read_bytes()
    except OSError as error:
        raise LifecycleError("Windows DACL snapshot is unreadable") from error
    try:
        if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
            text = raw.decode("utf-16")
        else:
            text = raw.decode("utf-16-le")
    except UnicodeError as error:
        raise LifecycleError("Windows DACL snapshot encoding is invalid") from error
    lines = text.splitlines()
    while lines and not lines[-1]:
        lines.pop()
    if not lines or len(lines) % 2:
        raise LifecycleError("Windows DACL snapshot record structure is invalid")
    records = {}
    for index in range(0, len(lines), 2):
        relative_text = lines[index].strip()
        descriptor = lines[index + 1].strip()
        relative = PureWindowsPath(relative_text)
        if (
            not relative_text
            or relative.is_absolute()
            or relative.drive
            or any(part in {"", ".", ".."} for part in relative.parts)
        ):
            raise LifecycleError("Windows DACL snapshot contains an unsafe path")
        if not descriptor.startswith("D:"):
            raise LifecycleError("Windows DACL snapshot contains an invalid descriptor")
        key = "\\".join(part.casefold() for part in relative.parts)
        if key in records:
            raise LifecycleError("Windows DACL snapshot contains duplicate paths")
        records[key] = descriptor
    return records


def assert_windows_dacl_snapshot_match(expected_snapshot, observed_snapshot):
    expected = windows_dacl_snapshot_records(expected_snapshot)
    observed = windows_dacl_snapshot_records(observed_snapshot)
    if expected.keys() != observed.keys():
        raise LifecycleError("Windows restored DACL path set mismatch")
    if any(expected[path] != observed[path] for path in expected):
        raise LifecycleError("Windows restored DACL descriptor mismatch")


def restore_permission_snapshot(
    path,
    snapshot,
    expected_digest,
    acl_runner=run_windows_acl,
    snapshotter=capture_permission_snapshot,
):
    if os.name != "nt":
        return "PLATFORM_DEFAULT"
    snapshot = Path(snapshot)
    try:
        if not snapshot.is_file() or sha256(snapshot) != expected_digest:
            raise LifecycleError("Windows DACL snapshot identity mismatch")
    except OSError as error:
        raise LifecycleError("Windows DACL snapshot is unreadable") from error
    windows_dacl_snapshot_records(snapshot)
    acl_runner(
        Path(path).parent,
        ["/restore", str(snapshot), "/Q"],
        "DACL restore",
    )
    observed_snapshot = snapshot.with_name(f".wcv-{uuid.uuid4().hex}.acl")
    try:
        observed_digest = snapshotter(path, observed_snapshot)
        if not observed_digest or sha256(observed_snapshot) != observed_digest:
            raise LifecycleError("Windows restored DACL readback identity mismatch")
        if sha256(snapshot) != expected_digest:
            raise LifecycleError("Windows DACL snapshot changed during restore")
        assert_windows_dacl_snapshot_match(snapshot, observed_snapshot)
    except OSError as error:
        raise LifecycleError("Windows restored DACL readback is unreadable") from error
    finally:
        remove_permission_snapshot(observed_snapshot)
    return "PRESERVED_FROM_SNAPSHOT"


def preflight_permission_restore(
    path,
    transaction,
    snapshot,
    expected_digest,
    permission_restorer=restore_permission_snapshot,
):
    if os.name != "nt":
        return "PLATFORM_DEFAULT"
    probe_parent = Path(transaction) / "p"
    probe = probe_parent / Path(path).name
    if probe_parent.exists():
        raise LifecycleError("Windows DACL restore preflight path is unavailable")
    try:
        probe_parent.mkdir()
        shutil.copytree(path, probe, copy_function=shutil.copyfile)
        result = permission_restorer(probe, snapshot, expected_digest)
        if result != "PRESERVED_FROM_SNAPSHOT":
            raise LifecycleError("Windows DACL restore preflight returned an invalid result")
    except Exception as error:
        try:
            shutil.rmtree(probe_parent)
        except OSError:
            pass
        raise LifecycleError(
            "Windows DACL restore preflight failed before destination mutation"
        ) from error
    try:
        shutil.rmtree(probe_parent)
    except OSError as error:
        raise LifecycleError("Windows DACL restore preflight cleanup failed") from error
    return "VERIFIED_BEFORE_MUTATION"


def synchronize(
    action,
    source,
    destination,
    expected_version,
    apply,
    backup_remover=shutil.rmtree,
    trusted_current_tree=None,
    trusted_target_tree=None,
    transaction_root=None,
    discovery_roots=(),
    path_replacer=os.replace,
    volume_identity_getter=None,
    permission_reconciler=reconcile_inherited_permissions,
    permission_snapshotter=capture_permission_snapshot,
    permission_restorer=restore_permission_snapshot,
    permission_restore_preflight=preflight_permission_restore,
):
    source = resolved(source)
    destination = assert_safe_destination(destination, source)
    state = current_state(destination, trusted_current_tree)
    if action == "install" and state["state"] != "ABSENT":
        raise LifecycleError(f"install requires an absent destination; observed {state['state']}")
    if action in {"update", "rollback"} and state["state"] != "MANAGED":
        raise LifecycleError(f"{action} requires an unchanged managed destination; observed {state['state']}")
    metadata = candidate_metadata(source, expected_version)
    trusted_target_tree = TRUSTED_PACKAGE_TREES.get(expected_version) or trusted_target_tree
    if trusted_target_tree is None or metadata["package"]["tree"] != trusted_target_tree:
        raise LifecycleError("source candidate is not bound to a trusted release tree")
    package, files, tree = package_files(source, trusted_target_tree)
    plan = {
        "action": action,
        "destination": str(destination),
        "effect": "APPLY" if apply else "DRY_RUN",
        "source_identity": metadata.get("public_identity"),
        "version": metadata.get("version"),
        "package_tree": tree,
    }
    validated_transaction_root = None
    remove_transaction_root = False
    if transaction_root is not None:
        validated_transaction_root = assert_safe_transaction_root(
            transaction_root,
            destination,
            source,
            discovery_roots,
            volume_identity_getter,
        )
        plan["transaction_root"] = str(validated_transaction_root)
        plan["transaction_root_mode"] = "EXPLICIT"
    if not apply:
        return plan
    if validated_transaction_root is None:
        validated_transaction_root = create_automatic_transaction_root(
            destination,
            source,
            discovery_roots,
            volume_identity_getter,
        )
        remove_transaction_root = True
        plan["transaction_root"] = str(validated_transaction_root)
        plan["transaction_root_mode"] = "AUTO_COMPATIBILITY"
        plan["compatibility_warning"] = (
            "automatic safe transaction root used for legacy apply call; "
            "planned product mutation must pass --transaction-root explicitly"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        transaction = create_transaction_directory(validated_transaction_root)
    except Exception:
        if remove_transaction_root:
            remove_empty_transaction_directory(validated_transaction_root)
        raise
    try:
        stage, metadata, files = stage_source(
            package,
            files,
            destination,
            metadata,
            transaction,
        )
    except Exception:
        if not remove_completed_transaction(
            transaction,
            validated_transaction_root,
            remove_transaction_root,
        ):
            raise LifecycleError(
                "staging failed; transaction cleanup failed; preserved at "
                f"{transaction_recovery_path(transaction, validated_transaction_root)}"
            )
        raise
    backup = transaction / "backup"
    permission_snapshot = transaction / "previous-dacl.acl"
    permission_snapshot_digest = None
    moved_old = False
    installed_new = False
    try:
        if action in {"update", "rollback"}:
            permission_snapshot_digest = permission_snapshotter(
                destination,
                permission_snapshot,
            )
            if os.name == "nt" and not permission_snapshot_digest:
                raise LifecycleError("Windows DACL snapshot was not created")
            preflight_result = permission_restore_preflight(
                destination,
                transaction,
                permission_snapshot,
                permission_snapshot_digest,
            )
            if preflight_result not in {
                "VERIFIED_BEFORE_MUTATION",
                "PLATFORM_DEFAULT",
            }:
                raise LifecycleError("DACL restore preflight returned an invalid result")
            path_replacer(destination, backup)
            moved_old = True
            backup_permission_result = permission_reconciler(backup)
            if backup_permission_result not in {
                "INHERITED_FROM_PARENT",
                "PLATFORM_DEFAULT",
            }:
                raise LifecycleError("backup permission handoff returned an invalid result")
        elif destination.exists():
            raise LifecycleError("install destination appeared after preflight")
        path_replacer(stage, destination)
        installed_new = True
        if permission_snapshot_digest is None:
            permission_result = permission_reconciler(destination)
            if permission_result not in {
                "INHERITED_FROM_PARENT",
                "PLATFORM_DEFAULT",
            }:
                raise LifecycleError("destination permission handoff returned an invalid result")
            plan["destination_permissions"] = (
                "INHERITED_FROM_DESTINATION_PARENT"
                if permission_result == "INHERITED_FROM_PARENT"
                else permission_result
            )
        else:
            permission_result = permission_restorer(
                destination,
                permission_snapshot,
                permission_snapshot_digest,
            )
            if permission_result != "PRESERVED_FROM_SNAPSHOT":
                raise LifecycleError("destination DACL restore returned an invalid result")
            plan["destination_permissions"] = "PRESERVED_FROM_PREVIOUS_DESTINATION"
        if current_state(destination, tree).get("state") != "MANAGED":
            raise LifecycleError("installed destination failed receipt verification")
    except Exception as operation_error:
        recovery_errors = []
        if installed_new and destination.exists():
            try:
                shutil.rmtree(destination)
            except OSError as error:
                recovery_errors.append(f"new destination cleanup failed: {error}")
        if moved_old:
            if destination.exists():
                recovery_errors.append("old destination restore blocked because destination still exists")
            elif not backup.exists():
                recovery_errors.append("old destination backup is missing")
            else:
                try:
                    path_replacer(backup, destination)
                    if permission_snapshot_digest is None:
                        restored_permission_result = permission_reconciler(destination)
                        if restored_permission_result not in {
                            "INHERITED_FROM_PARENT",
                            "PLATFORM_DEFAULT",
                        }:
                            raise LifecycleError(
                                "restored destination permission handoff returned an invalid result"
                            )
                    else:
                        restored_permission_result = permission_restorer(
                            destination,
                            permission_snapshot,
                            permission_snapshot_digest,
                        )
                        if restored_permission_result != "PRESERVED_FROM_SNAPSHOT":
                            raise LifecycleError(
                                "restored destination DACL restore returned an invalid result"
                            )
                    if current_state(destination, state.get("package_tree")).get("state") != "MANAGED":
                        raise LifecycleError("restored destination failed receipt verification")
                except Exception as error:
                    recovery_errors.append(f"old destination restore failed: {error}")
        if stage.exists():
            shutil.rmtree(stage, ignore_errors=True)
        if recovery_errors:
            raise LifecycleError(
                f"{action} failed; automatic recovery is incomplete; transaction preserved at "
                f"{transaction}: {'; '.join(recovery_errors)}"
            ) from operation_error
        remove_permission_snapshot(permission_snapshot)
        if not remove_completed_transaction(
            transaction,
            validated_transaction_root,
            remove_transaction_root,
        ):
            raise LifecycleError(
                f"{action} failed; transaction cleanup failed; preserved at "
                f"{transaction_recovery_path(transaction, validated_transaction_root)}"
            ) from operation_error
        raise
    if moved_old:
        try:
            backup_remover(backup)
        except OSError as error:
            plan["backup_path"] = str(backup)
            plan["cleanup_error"] = str(error)
            plan["package_sha256"] = package_digest(files)
            plan["result"] = "MANAGED_WITH_BACKUP"
            plan["transaction_path"] = str(transaction)
            return plan
    remove_permission_snapshot(permission_snapshot)
    if not remove_completed_transaction(
        transaction,
        validated_transaction_root,
        remove_transaction_root,
    ):
        plan["transaction_path"] = str(
            transaction_recovery_path(transaction, validated_transaction_root)
        )
        plan["warning"] = "managed destination is valid; transaction directory cleanup failed"
    plan["package_sha256"] = package_digest(files)
    plan["result"] = "MANAGED"
    return plan


def uninstall(
    destination,
    apply,
    trusted_tree=None,
    tombstone_remover=shutil.rmtree,
    transaction_root=None,
    discovery_roots=(),
    path_replacer=os.replace,
    volume_identity_getter=None,
    permission_reconciler=reconcile_inherited_permissions,
    permission_snapshotter=capture_permission_snapshot,
    permission_restorer=restore_permission_snapshot,
    permission_restore_preflight=preflight_permission_restore,
):
    destination = assert_safe_destination(destination)
    state = current_state(destination, trusted_tree)
    if state["state"] == "ABSENT":
        return {"action": "uninstall", "destination": str(destination), "result": "ALREADY_ABSENT"}
    if state["state"] != "MANAGED":
        raise LifecycleError(
            "uninstall refuses an unreceipted, malformed or mismatched-receipt, "
            "wrong-tree, modified, aliased, or drifted destination; "
            f"observed {state['state']}"
        )
    result = {
        "action": "uninstall",
        "destination": str(destination),
        "effect": "APPLY" if apply else "DRY_RUN",
    }
    if not apply:
        if transaction_root is not None:
            result["transaction_root"] = str(
                assert_safe_transaction_root(
                    transaction_root,
                    destination,
                    discovery_roots=discovery_roots,
                    volume_identity_getter=volume_identity_getter,
                )
            )
            result["transaction_root_mode"] = "EXPLICIT"
        return result
    remove_transaction_root = transaction_root is None
    if remove_transaction_root:
        validated_transaction_root = create_automatic_transaction_root(
            destination,
            discovery_roots=discovery_roots,
            volume_identity_getter=volume_identity_getter,
        )
        result["transaction_root_mode"] = "AUTO_COMPATIBILITY"
        result["compatibility_warning"] = (
            "automatic safe transaction root used for legacy apply call; "
            "planned product uninstall must pass --transaction-root explicitly"
        )
    else:
        validated_transaction_root = assert_safe_transaction_root(
            transaction_root,
            destination,
            discovery_roots=discovery_roots,
            volume_identity_getter=volume_identity_getter,
        )
        result["transaction_root_mode"] = "EXPLICIT"
    result["transaction_root"] = str(validated_transaction_root)
    try:
        transaction = create_transaction_directory(validated_transaction_root)
    except Exception:
        if remove_transaction_root:
            remove_empty_transaction_directory(validated_transaction_root)
        raise
    tombstone = transaction / "tombstone"
    recovery_base = transaction / "uninstall-recovery"
    permission_snapshot = transaction / "previous-dacl.acl"
    try:
        permission_snapshot_digest = permission_snapshotter(
            destination,
            permission_snapshot,
        )
        if os.name == "nt" and not permission_snapshot_digest:
            raise LifecycleError("Windows DACL snapshot was not created")
        preflight_result = permission_restore_preflight(
            destination,
            transaction,
            permission_snapshot,
            permission_snapshot_digest,
        )
        if preflight_result not in {
            "VERIFIED_BEFORE_MUTATION",
            "PLATFORM_DEFAULT",
        }:
            raise LifecycleError("DACL restore preflight returned an invalid result")
    except Exception:
        remove_permission_snapshot(permission_snapshot)
        if not remove_completed_transaction(
            transaction,
            validated_transaction_root,
            remove_transaction_root,
        ):
            raise LifecycleError(
                "DACL snapshot failed; transaction cleanup failed; preserved at "
                f"{transaction_recovery_path(transaction, validated_transaction_root)}"
            )
        raise
    try:
        recovery_archive = Path(
            shutil.make_archive(str(recovery_base), "zip", root_dir=destination)
        )
    except Exception:
        remove_permission_snapshot(permission_snapshot)
        if not remove_completed_transaction(
            transaction,
            validated_transaction_root,
            remove_transaction_root,
        ):
            raise LifecycleError(
                "recovery archive creation failed; transaction preserved at "
                f"{transaction_recovery_path(transaction, validated_transaction_root)}"
            )
        raise
    try:
        path_replacer(destination, tombstone)
    except Exception:
        recovery_archive.unlink(missing_ok=True)
        remove_permission_snapshot(permission_snapshot)
        if not remove_completed_transaction(
            transaction,
            validated_transaction_root,
            remove_transaction_root,
        ):
            raise LifecycleError(
                "uninstall move failed; transaction cleanup failed; preserved at "
                f"{transaction_recovery_path(transaction, validated_transaction_root)}"
            )
        raise
    try:
        tombstone_permission_result = permission_reconciler(tombstone)
        if tombstone_permission_result not in {
            "INHERITED_FROM_PARENT",
            "PLATFORM_DEFAULT",
        }:
            raise LifecycleError("tombstone permission handoff returned an invalid result")
        tombstone_remover(tombstone)
    except Exception as error:
        try:
            destination.mkdir()
            shutil.unpack_archive(recovery_archive, destination, "zip")
            if permission_snapshot_digest is None:
                restored_permission_result = permission_reconciler(destination)
                if restored_permission_result not in {
                    "INHERITED_FROM_PARENT",
                    "PLATFORM_DEFAULT",
                }:
                    raise LifecycleError(
                        "restored destination permission handoff returned an invalid result"
                    )
            else:
                restored_permission_result = permission_restorer(
                    destination,
                    permission_snapshot,
                    permission_snapshot_digest,
                )
                if restored_permission_result != "PRESERVED_FROM_SNAPSHOT":
                    raise LifecycleError(
                        "restored destination DACL restore returned an invalid result"
                    )
            if current_state(destination, trusted_tree).get("state") != "MANAGED":
                raise LifecycleError("restored destination failed receipt verification")
        except Exception as restore_error:
            raise LifecycleError(
                "uninstall cleanup failed; recovery archive preserved at "
                f"{recovery_archive}; transaction preserved at {transaction}; "
                f"automatic restore failed: {restore_error}"
            ) from error
        raise LifecycleError(
            "uninstall cleanup failed; managed destination was restored; "
            f"transaction preserved at {transaction}; recovery archive at {recovery_archive}; "
            f"partial tombstone at {tombstone}"
        ) from error
    try:
        recovery_archive.unlink()
    except OSError as error:
        result["result"] = "ABSENT"
        result["recovery_archive"] = str(recovery_archive)
        result["transaction_path"] = str(transaction)
        result["warning"] = f"uninstall completed; recovery archive cleanup failed: {error}"
        return result
    remove_permission_snapshot(permission_snapshot)
    if not remove_completed_transaction(
        transaction,
        validated_transaction_root,
        remove_transaction_root,
    ):
        result["transaction_path"] = str(
            transaction_recovery_path(transaction, validated_transaction_root)
        )
        result["warning"] = "uninstall completed; transaction directory cleanup failed"
    result["result"] = "ABSENT"
    return result


def create_test_source(root, version, marker):
    source = root / f"source-{version}"
    package = source / "skills" / "work-charter"
    for relative in sorted(EXPECTED_FILES):
        path = package / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{relative} {marker}\n", encoding="utf-8", newline="\n")
    descriptor = {
        "package": {"tree": git_tree_hash(package)},
        "product": "work-charter",
        "public_identity": "junwei529/work-charter",
        "schema": "work-charter-local-release-candidate/v1",
        "version": version,
    }
    candidate = source / "release" / f"v{version}-candidate.json"
    candidate.parent.mkdir(parents=True)
    candidate.write_text(
        json.dumps(descriptor, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return source


def self_test(source=None):
    candidate_tree = None
    if source is not None:
        metadata = candidate_metadata(source, SELF_TEST_SOURCE_VERSION)
        _package, _files, candidate_tree = package_files(
            source,
            metadata["package"]["tree"],
        )
    with tempfile.TemporaryDirectory(prefix="work-charter-lifecycle-") as temporary:
        root = Path(temporary).resolve(strict=True)
        transaction_parent = root / "external-transactions"
        transaction_parent.mkdir()

        def new_transaction_root(name):
            path = transaction_parent / name
            path.mkdir()
            return path

        def assert_permission_handoff(result):
            if os.name != "nt":
                expected = "PLATFORM_DEFAULT"
            elif result["action"] == "install":
                expected = "INHERITED_FROM_DESTINATION_PARENT"
            else:
                expected = "PRESERVED_FROM_PREVIOUS_DESTINATION"
            assert result["destination_permissions"] == expected

        def saved_dacl(path, name):
            if os.name != "nt":
                return None
            snapshot = root / name
            digest = capture_permission_snapshot(path, snapshot)
            assert digest == sha256(snapshot)
            return snapshot.read_bytes()

        def write_dacl_records(path, records, newline="\n"):
            lines = []
            for relative, descriptor in records:
                lines.extend((relative, descriptor))
            Path(path).write_bytes(
                (newline.join(lines) + newline * 2).encode("utf-16-le")
            )

        malformed_source = root / "malformed-source"
        malformed_candidate = malformed_source / "release" / "v0.3.0-candidate.json"
        malformed_candidate.parent.mkdir(parents=True)
        malformed_candidate.write_text("[]\n", encoding="utf-8", newline="\n")
        try:
            candidate_metadata(malformed_source, "0.3.0")
        except LifecycleError:
            pass
        else:
            raise AssertionError("non-object candidate descriptor was not refused")
        source_a = resolved(source) if source is not None else ROOT
        source_b = create_test_source(root, "0.4.1", "b")
        source_c = create_test_source(root, "0.4.2", "c")
        source_bad = create_test_source(root, "0.4.9", "bad")
        source_forged = create_test_source(root / "forged-source-root", "0.3.0", "forged")
        tree_a = candidate_metadata(source_a, SELF_TEST_SOURCE_VERSION)["package"]["tree"]
        tree_b = candidate_metadata(source_b, "0.4.1")["package"]["tree"]
        tree_c = candidate_metadata(source_c, "0.4.2")["package"]["tree"]
        tree_bad = candidate_metadata(source_bad, "0.4.9")["package"]["tree"]
        tree_forged = candidate_metadata(source_forged, "0.3.0")["package"]["tree"]
        assert SELF_TEST_SOURCE_VERSION not in TRUSTED_PACKAGE_TREES
        assert "0.4.1" not in TRUSTED_PACKAGE_TREES
        (source_bad / "skills" / "work-charter" / "SKILL.md").write_text(
            "tampered after descriptor\n",
            encoding="utf-8",
            newline="\n",
        )
        try:
            synchronize(
                "install",
                source_bad,
                root / "bad-install",
                "0.4.9",
                False,
                trusted_target_tree=tree_bad,
            )
        except LifecycleError:
            pass
        else:
            raise AssertionError("package tree mismatch was not refused")
        try:
            synchronize(
                "install",
                source_forged,
                root / "known-anchor-override",
                "0.3.0",
                True,
                trusted_target_tree=tree_forged,
                transaction_root=new_transaction_root("forged-source"),
            )
        except LifecycleError:
            pass
        else:
            raise AssertionError("forged source candidate was not refused")

        legacy_container = root / "legacy-calls"
        legacy_container.mkdir()
        legacy_destination = legacy_container / "skills" / "work-charter"

        def assert_automatic_compatibility(result):
            assert result["transaction_root_mode"] == "AUTO_COMPATIBILITY"
            assert "compatibility_warning" in result
            if result.get("action") != "uninstall":
                assert_permission_handoff(result)
            automatic_root = Path(result["transaction_root"])
            assert legacy_destination.parent not in automatic_root.parents
            assert not automatic_root.exists()

        assert_automatic_compatibility(
            synchronize(
                "install",
                source_a,
                legacy_destination,
                SELF_TEST_SOURCE_VERSION,
                True,
                trusted_target_tree=tree_a,
            )
        )
        assert_automatic_compatibility(
            synchronize(
                "update",
                source_b,
                legacy_destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
            )
        )
        assert_automatic_compatibility(
            synchronize(
                "rollback",
                source_a,
                legacy_destination,
                SELF_TEST_SOURCE_VERSION,
                True,
                trusted_current_tree=tree_b,
                trusted_target_tree=tree_a,
            )
        )
        assert_automatic_compatibility(
            uninstall(
                legacy_destination,
                True,
                trusted_tree=tree_a,
            )
        )
        assert current_state(legacy_destination)["state"] == "ABSENT"

        destination = root / "managed" / "work-charter"
        dry_run = synchronize(
            "install",
            source_a,
            destination,
            SELF_TEST_SOURCE_VERSION,
            False,
            trusted_target_tree=tree_a,
        )
        assert dry_run["effect"] == "DRY_RUN"
        assert "transaction_root" not in dry_run
        install_result = synchronize(
            "install",
            source_a,
            destination,
            SELF_TEST_SOURCE_VERSION,
            True,
            trusted_target_tree=tree_a,
            transaction_root=new_transaction_root("install"),
        )
        assert install_result["transaction_root"].endswith("install")
        assert_permission_handoff(install_result)
        assert current_state(destination, tree_a)["version"] == SELF_TEST_SOURCE_VERSION
        assert current_state(destination, tree_b)["state"] == "FOREIGN_COPY"
        receipt_path = destination / RECEIPT_NAME
        valid_receipt = receipt_path.read_text(encoding="utf-8")
        receipt_path.write_text('{"destination": null}\n', encoding="utf-8", newline="\n")
        assert current_state(destination, tree_a)["state"] == "DRIFTED"
        receipt_path.write_text(valid_receipt, encoding="utf-8", newline="\n")
        original_dacl = None
        if os.name == "nt":
            run_windows_acl(
                destination.parent,
                ["/grant:r", "*S-1-1-0:(OI)(CI)(RX)", "/Q"],
                "self-test broader parent policy",
            )
            harden_transaction_permissions(destination)
            restricted_file = destination / "agents" / "openai.yaml"
            run_windows_acl(
                restricted_file,
                ["/inheritance:r", "/Q"],
                "self-test restrictive file policy",
            )
            run_windows_acl(
                restricted_file,
                [
                    "/grant:r",
                    "*S-1-3-4:(R)",
                    "*S-1-5-18:(F)",
                    "*S-1-5-32-544:(F)",
                    "/Q",
                ],
                "self-test restrictive file policy",
            )
            original_dacl = saved_dacl(destination, "dacl-before-update.acl")
            baseline_snapshot = root / "dacl-before-update.acl"
            baseline_records = windows_dacl_snapshot_records(baseline_snapshot)
            reordered_snapshot = root / "dacl-reordered-lf.acl"
            write_dacl_records(
                reordered_snapshot,
                reversed(tuple(baseline_records.items())),
            )
            assert_windows_dacl_snapshot_match(baseline_snapshot, reordered_snapshot)
            missing_snapshot = root / "dacl-missing-record.acl"
            write_dacl_records(missing_snapshot, tuple(baseline_records.items())[1:])
            try:
                assert_windows_dacl_snapshot_match(baseline_snapshot, missing_snapshot)
            except LifecycleError as error:
                assert "path set mismatch" in str(error)
            else:
                raise AssertionError("missing DACL readback record was not refused")
            changed_records = list(baseline_records.items())
            descriptor = changed_records[0][1]
            first_ace_start = descriptor.index("(")
            first_ace_end = descriptor.index(")", first_ace_start) + 1
            second_ace_start = descriptor.index("(", first_ace_end)
            second_ace_end = descriptor.index(")", second_ace_start) + 1
            reordered_aces = (
                descriptor[:first_ace_start]
                + descriptor[second_ace_start:second_ace_end]
                + descriptor[first_ace_start:first_ace_end]
                + descriptor[second_ace_end:]
            )
            changed_records[0] = (
                changed_records[0][0],
                reordered_aces,
            )
            changed_snapshot = root / "dacl-changed-descriptor.acl"
            write_dacl_records(changed_snapshot, changed_records, newline="\r\n")
            try:
                assert_windows_dacl_snapshot_match(baseline_snapshot, changed_snapshot)
            except LifecycleError as error:
                assert "descriptor mismatch" in str(error)
            else:
                raise AssertionError("changed DACL descriptor was not refused")
        update_moves = []

        def record_update_move(source_path, target_path):
            update_moves.append((Path(source_path), Path(target_path)))
            os.replace(source_path, target_path)

        update_transaction_root = new_transaction_root("update")
        update_result = synchronize(
            "update",
            source_b,
            destination,
            "0.4.1",
            True,
            trusted_current_tree=tree_a,
            trusted_target_tree=tree_b,
            transaction_root=update_transaction_root,
            path_replacer=record_update_move,
        )
        assert_permission_handoff(update_result)
        assert current_state(destination, tree_b)["version"] == "0.4.1"
        assert len(update_moves) == 2
        assert update_moves[0][0] == destination
        assert update_transaction_root in update_moves[0][1].parents
        assert update_transaction_root in update_moves[1][0].parents
        assert update_moves[1][1] == destination
        if os.name == "nt":
            assert saved_dacl(destination, "dacl-after-update.acl") == original_dacl

        rollback_moves = []

        def record_rollback_move(source_path, target_path):
            rollback_moves.append((Path(source_path), Path(target_path)))
            os.replace(source_path, target_path)

        rollback_transaction_root = new_transaction_root("rollback")
        rollback_result = synchronize(
            "rollback",
            source_a,
            destination,
            SELF_TEST_SOURCE_VERSION,
            True,
            trusted_current_tree=tree_b,
            trusted_target_tree=tree_a,
            transaction_root=rollback_transaction_root,
            path_replacer=record_rollback_move,
        )
        assert_permission_handoff(rollback_result)
        assert current_state(destination, tree_a)["version"] == SELF_TEST_SOURCE_VERSION
        assert len(rollback_moves) == 2
        assert rollback_transaction_root in rollback_moves[0][1].parents
        assert rollback_transaction_root in rollback_moves[1][0].parents
        if os.name == "nt":
            assert saved_dacl(destination, "dacl-after-rollback.acl") == original_dacl

        permission_failure_root = new_transaction_root("permission-handoff-failure")
        permission_failure_calls = []

        def fail_permission_handoff(target, snapshot=None, digest=None):
            permission_failure_calls.append(Path(target))
            if os.name == "nt":
                result = restore_permission_snapshot(target, snapshot, digest)
                if len(permission_failure_calls) == 1:
                    raise OSError("simulated destination permission handoff failure")
                return result
            if len(permission_failure_calls) == 2:
                raise OSError("simulated destination permission handoff failure")
            return "PLATFORM_DEFAULT"

        try:
            synchronize(
                "update",
                source_b,
                destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
                transaction_root=permission_failure_root,
                permission_reconciler=(
                    reconcile_inherited_permissions
                    if os.name == "nt"
                    else fail_permission_handoff
                ),
                permission_restorer=(
                    fail_permission_handoff
                    if os.name == "nt"
                    else restore_permission_snapshot
                ),
            )
        except OSError as error:
            assert "permission handoff failure" in str(error)
        else:
            raise AssertionError("destination permission handoff failure was not surfaced")
        assert len(permission_failure_calls) == (2 if os.name == "nt" else 3)
        if os.name == "nt":
            assert permission_failure_calls == [destination, destination]
        else:
            assert permission_failure_calls[0].name == "backup"
            assert permission_failure_calls[0].parent.parent == permission_failure_root
            assert permission_failure_calls[1:] == [destination, destination]
        assert current_state(destination, tree_a)["state"] == "MANAGED"
        assert not any(permission_failure_root.iterdir())
        if os.name == "nt":
            assert saved_dacl(destination, "dacl-after-failed-update.acl") == original_dacl

        snapshot_failure_root = new_transaction_root("dacl-snapshot-failure")
        snapshot_failure_moves = []

        def fail_dacl_snapshot(_path, _snapshot):
            raise OSError("simulated pre-mutation DACL snapshot failure")

        def record_snapshot_failure_move(source_path, target_path):
            snapshot_failure_moves.append((Path(source_path), Path(target_path)))
            os.replace(source_path, target_path)

        try:
            synchronize(
                "update",
                source_b,
                destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
                transaction_root=snapshot_failure_root,
                path_replacer=record_snapshot_failure_move,
                permission_snapshotter=fail_dacl_snapshot,
            )
        except OSError as error:
            assert "pre-mutation DACL snapshot failure" in str(error)
        else:
            raise AssertionError("pre-mutation DACL snapshot failure was not surfaced")
        assert snapshot_failure_moves == []
        assert current_state(destination, tree_a)["state"] == "MANAGED"
        assert not any(snapshot_failure_root.iterdir())

        preflight_failure_root = new_transaction_root("dacl-restore-preflight-failure")
        preflight_failure_moves = []

        def fail_dacl_restore_preflight(_path, _transaction, _snapshot, _digest):
            raise OSError("simulated pre-mutation DACL restore preflight failure")

        def record_preflight_failure_move(source_path, target_path):
            preflight_failure_moves.append((Path(source_path), Path(target_path)))
            os.replace(source_path, target_path)

        try:
            synchronize(
                "update",
                source_b,
                destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
                transaction_root=preflight_failure_root,
                path_replacer=record_preflight_failure_move,
                permission_restore_preflight=fail_dacl_restore_preflight,
            )
        except OSError as error:
            assert "restore preflight failure" in str(error)
        else:
            raise AssertionError("pre-mutation DACL restore preflight failure was not surfaced")
        assert preflight_failure_moves == []
        assert current_state(destination, tree_a)["state"] == "MANAGED"
        assert not any(preflight_failure_root.iterdir())

        if os.name == "nt":
            baseline_snapshot = root / "dacl-before-update.acl"
            baseline_digest = sha256(baseline_snapshot)

            def noop_acl_restore(_path, _arguments, _label):
                return None

            def missing_dacl_readback(_path, observed_snapshot):
                records = tuple(windows_dacl_snapshot_records(baseline_snapshot).items())
                write_dacl_records(observed_snapshot, records[:-1])
                return sha256(observed_snapshot)

            try:
                restore_permission_snapshot(
                    destination,
                    baseline_snapshot,
                    baseline_digest,
                    acl_runner=noop_acl_restore,
                    snapshotter=missing_dacl_readback,
                )
            except LifecycleError as error:
                assert "path set mismatch" in str(error)
            else:
                raise AssertionError("missing restored DACL readback was not refused")

            readback_preflight_root = new_transaction_root(
                "dacl-readback-preflight-mismatch"
            )
            readback_preflight_moves = []

            def false_success_restorer(target, snapshot, digest):
                return restore_permission_snapshot(
                    target,
                    snapshot,
                    digest,
                    acl_runner=noop_acl_restore,
                )

            def verify_false_success_preflight(path, transaction, snapshot, digest):
                return preflight_permission_restore(
                    path,
                    transaction,
                    snapshot,
                    digest,
                    permission_restorer=false_success_restorer,
                )

            def record_readback_preflight_move(source_path, target_path):
                readback_preflight_moves.append((Path(source_path), Path(target_path)))
                os.replace(source_path, target_path)

            try:
                synchronize(
                    "update",
                    source_b,
                    destination,
                    "0.4.1",
                    True,
                    trusted_current_tree=tree_a,
                    trusted_target_tree=tree_b,
                    transaction_root=readback_preflight_root,
                    path_replacer=record_readback_preflight_move,
                    permission_restore_preflight=verify_false_success_preflight,
                )
            except LifecycleError as error:
                assert "restore preflight failed before destination mutation" in str(error)
            else:
                raise AssertionError("false-success DACL preflight was not refused")
            assert readback_preflight_moves == []
            assert current_state(destination, tree_a)["state"] == "MANAGED"
            assert not any(readback_preflight_root.iterdir())

            readback_recovery_root = new_transaction_root(
                "dacl-readback-mismatch-recovery"
            )
            readback_restore_calls = []

            def restore_then_corrupt_once(target, snapshot, digest):
                readback_restore_calls.append(Path(target))
                if len(readback_restore_calls) == 1:

                    def restore_and_corrupt(path, arguments, label):
                        run_windows_acl(path, arguments, label)
                        run_windows_acl(
                            target,
                            ["/grant:r", "*S-1-1-0:(OI)(CI)(R)", "/Q"],
                            "self-test post-restore DACL mismatch",
                        )

                    return restore_permission_snapshot(
                        target,
                        snapshot,
                        digest,
                        acl_runner=restore_and_corrupt,
                    )
                return restore_permission_snapshot(target, snapshot, digest)

            try:
                synchronize(
                    "update",
                    source_b,
                    destination,
                    "0.4.1",
                    True,
                    trusted_current_tree=tree_a,
                    trusted_target_tree=tree_b,
                    transaction_root=readback_recovery_root,
                    permission_restorer=restore_then_corrupt_once,
                )
            except LifecycleError as error:
                assert "DACL descriptor mismatch" in str(error)
            else:
                raise AssertionError("post-restore DACL mismatch was reported successful")
            assert readback_restore_calls == [destination, destination]
            assert current_state(destination, tree_a)["state"] == "MANAGED"
            assert not any(readback_recovery_root.iterdir())
            assert (
                saved_dacl(destination, "dacl-after-readback-recovery.acl")
                == original_dacl
            )

            retained_mismatch_root = new_transaction_root(
                "dacl-readback-mismatch-retention"
            )
            retained_restore_calls = []

            def restore_then_always_corrupt(target, snapshot, digest):
                retained_restore_calls.append(Path(target))

                def restore_and_corrupt(path, arguments, label):
                    run_windows_acl(path, arguments, label)
                    run_windows_acl(
                        target,
                        ["/grant:r", "*S-1-1-0:(OI)(CI)(R)", "/Q"],
                        "self-test persistent post-restore DACL mismatch",
                    )

                return restore_permission_snapshot(
                    target,
                    snapshot,
                    digest,
                    acl_runner=restore_and_corrupt,
                )

            try:
                synchronize(
                    "update",
                    source_b,
                    destination,
                    "0.4.1",
                    True,
                    trusted_current_tree=tree_a,
                    trusted_target_tree=tree_b,
                    transaction_root=retained_mismatch_root,
                    permission_restorer=restore_then_always_corrupt,
                )
            except LifecycleError as error:
                assert "automatic recovery is incomplete" in str(error)
                assert "DACL descriptor mismatch" in str(error)
            else:
                raise AssertionError("persistent DACL mismatch was reported successful")
            assert retained_restore_calls == [destination, destination]
            retained_transactions = tuple(retained_mismatch_root.iterdir())
            assert len(retained_transactions) == 1
            retained_transaction = retained_transactions[0]
            retained_snapshot = retained_transaction / "previous-dacl.acl"
            assert retained_snapshot.is_file()
            assert sha256(retained_snapshot) == baseline_digest
            restore_permission_snapshot(destination, retained_snapshot, baseline_digest)
            assert current_state(destination, tree_a)["state"] == "MANAGED"
            assert (
                saved_dacl(destination, "dacl-after-retained-recovery.acl")
                == original_dacl
            )
            shutil.rmtree(retained_transaction)
            assert not any(retained_mismatch_root.iterdir())

        changed = destination / "SKILL.md"
        original = changed.read_text(encoding="utf-8")
        changed.write_text(original + "drift\n", encoding="utf-8", newline="\n")
        assert current_state(destination, tree_a)["state"] == "DRIFTED"
        changed.write_text(original, encoding="utf-8", newline="\n")

        nested_receipt = destination / "references" / RECEIPT_NAME
        nested_receipt.write_text("foreign\n", encoding="utf-8", newline="\n")
        assert current_state(destination, tree_a)["state"] == "DRIFTED"
        nested_receipt.unlink()

        unexpected_directory = destination / "user-empty-directory"
        unexpected_directory.mkdir()
        assert current_state(destination, tree_a)["state"] == "DRIFTED"
        unexpected_directory.rmdir()

        missing_root = transaction_parent / "missing"
        try:
            synchronize(
                "update",
                source_b,
                destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
                transaction_root=missing_root,
            )
        except LifecycleError as error:
            assert "existing directory" in str(error)
        else:
            raise AssertionError("missing transaction root was not refused")
        assert current_state(destination, tree_a)["state"] == "MANAGED"

        inside_discovery_root = destination.parent / "transactions"
        inside_discovery_root.mkdir()
        try:
            synchronize(
                "update",
                source_b,
                destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
                transaction_root=inside_discovery_root,
            )
        except LifecycleError as error:
            assert "destination discovery root" in str(error)
        else:
            raise AssertionError("transaction root inside a Skill discovery root was not refused")
        assert current_state(destination, tree_a)["state"] == "MANAGED"
        inside_discovery_root.rmdir()

        additional_discovery_root = root / "additional-skill-root"
        additional_discovery_root.mkdir()
        declared_inside_root = additional_discovery_root / "transactions"
        declared_inside_root.mkdir()
        try:
            synchronize(
                "update",
                source_b,
                destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
                transaction_root=declared_inside_root,
                discovery_roots=(additional_discovery_root,),
            )
        except LifecycleError as error:
            assert "additional Skill discovery root" in str(error)
        else:
            raise AssertionError("transaction root inside a declared discovery root was not refused")
        assert current_state(destination, tree_a)["state"] == "MANAGED"
        declared_inside_root.rmdir()

        cross_volume_root = new_transaction_root("cross-volume")

        def simulated_volume_identity(path):
            if resolved(path) == cross_volume_root.resolve():
                return "simulated-other-volume"
            return "simulated-destination-volume"

        try:
            synchronize(
                "update",
                source_b,
                destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
                transaction_root=cross_volume_root,
                volume_identity_getter=simulated_volume_identity,
            )
        except LifecycleError as error:
            assert "same filesystem volume" in str(error)
        else:
            raise AssertionError("cross-volume transaction root was not refused")
        assert current_state(destination, tree_a)["state"] == "MANAGED"
        assert not any(cross_volume_root.iterdir())

        alias_check = "NOT_APPLICABLE"
        raw_temporary = Path(temporary)
        if canonical_path_text(raw_temporary) != canonical_path_text(root):
            alias_root = new_transaction_root("aliased-root")
            aliased_spelling = raw_temporary / "external-transactions" / alias_root.name
            try:
                synchronize(
                    "update",
                    source_b,
                    destination,
                    "0.4.1",
                    True,
                    trusted_current_tree=tree_a,
                    trusted_target_tree=tree_b,
                    transaction_root=aliased_spelling,
                )
            except LifecycleError as error:
                assert "exact canonical path" in str(error)
                alias_check = "PASS"
            else:
                raise AssertionError("aliased transaction root was not refused")
            assert current_state(destination, tree_a)["state"] == "MANAGED"

        link_check = "UNAVAILABLE"
        link_target = new_transaction_root("link-target")
        link_path = root / "transaction-root-link"
        link_created = False
        try:
            link_path.symlink_to(link_target, target_is_directory=True)
        except OSError:
            if os.name == "nt":
                completed = subprocess.run(
                    ["cmd.exe", "/d", "/c", "mklink", "/J", str(link_path), str(link_target)],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                link_created = completed.returncode == 0 and is_link_like(link_path)
        else:
            link_created = True
        if link_created:
            try:
                synchronize(
                    "update",
                    source_b,
                    destination,
                    "0.4.1",
                    True,
                    trusted_current_tree=tree_a,
                    trusted_target_tree=tree_b,
                    transaction_root=link_path,
                )
            except LifecycleError as error:
                assert "symbolic link, junction, or reparse point" in str(error)
                link_check = "PASS"
            else:
                raise AssertionError("link-like transaction root was not refused")
            finally:
                if link_path.is_symlink():
                    link_path.unlink(missing_ok=True)
                elif link_path.exists():
                    link_path.rmdir()
        assert current_state(destination, tree_a)["state"] == "MANAGED"

        backup_move_failure_root = new_transaction_root("backup-move-failure")

        def fail_backup_move(_source_path, _target_path):
            raise OSError("simulated old-destination backup move failure")

        try:
            synchronize(
                "update",
                source_b,
                destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
                transaction_root=backup_move_failure_root,
                path_replacer=fail_backup_move,
            )
        except OSError as error:
            assert "backup move failure" in str(error)
        else:
            raise AssertionError("old-destination backup move failure was not surfaced")
        assert current_state(destination, tree_a)["state"] == "MANAGED"
        assert not any(backup_move_failure_root.iterdir())

        later_failure_root = new_transaction_root("later-failure")
        replace_calls = 0

        def fail_new_destination_move(source_path, target_path):
            nonlocal replace_calls
            replace_calls += 1
            if replace_calls == 2:
                raise OSError("simulated staged-package move failure")
            os.replace(source_path, target_path)

        try:
            synchronize(
                "update",
                source_b,
                destination,
                "0.4.1",
                True,
                trusted_current_tree=tree_a,
                trusted_target_tree=tree_b,
                transaction_root=later_failure_root,
                path_replacer=fail_new_destination_move,
            )
        except OSError as error:
            assert "staged-package move failure" in str(error)
        else:
            raise AssertionError("staged-package move failure was not surfaced")
        assert replace_calls == 3
        assert current_state(destination, tree_a)["state"] == "MANAGED"
        assert not any(later_failure_root.iterdir())

        def fail_backup_cleanup(_path):
            raise OSError("simulated backup cleanup failure")

        cleanup_transaction_root = new_transaction_root("backup-cleanup-failure")
        cleanup_result = synchronize(
            "update",
            source_c,
            destination,
            "0.4.2",
            True,
            backup_remover=fail_backup_cleanup,
            trusted_current_tree=tree_a,
            trusted_target_tree=tree_c,
            transaction_root=cleanup_transaction_root,
        )
        assert cleanup_result["result"] == "MANAGED_WITH_BACKUP"
        assert current_state(destination, tree_c)["version"] == "0.4.2"
        backup_path = Path(cleanup_result["backup_path"])
        assert backup_path.exists()
        assert cleanup_transaction_root in backup_path.parents
        shutil.rmtree(Path(cleanup_result["transaction_path"]))

        unreceipted = root / "unreceipted" / "work-charter"
        unreceipted.mkdir(parents=True)
        (unreceipted / "SKILL.md").write_text("unreceipted\n", encoding="utf-8", newline="\n")
        assert current_state(unreceipted)["state"] == "FOREIGN_COPY"
        try:
            uninstall(unreceipted, True)
        except LifecycleError:
            pass
        else:
            raise AssertionError("unreceipted destination uninstall was not refused")
        assert unreceipted.exists()

        wrong_tree = root / "wrong-tree" / "work-charter"
        wrong_tree.mkdir(parents=True)
        wrong_tree_files = {}
        for relative in sorted(EXPECTED_FILES):
            path = wrong_tree / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("wrong tree\n", encoding="utf-8", newline="\n")
            wrong_tree_files[relative] = sha256(path)
        wrong_tree_receipt = {
            "destination": str(wrong_tree.resolve()),
            "files": wrong_tree_files,
            "package_sha256": package_digest(wrong_tree_files),
            "package_tree": TRUSTED_PACKAGE_TREES["0.3.0"],
            "product": "work-charter",
            "public_identity": "junwei529/work-charter",
            "schema": RECEIPT_SCHEMA,
            "version": "0.3.0",
        }
        (wrong_tree / RECEIPT_NAME).write_text(
            json.dumps(wrong_tree_receipt, sort_keys=True),
            encoding="utf-8",
        )
        assert current_state(wrong_tree)["state"] == "DRIFTED"
        try:
            uninstall(wrong_tree, True)
        except LifecycleError:
            pass
        else:
            raise AssertionError("wrong-tree receipt uninstall was not refused")
        assert wrong_tree.exists()

        def fail_partial_uninstall(path):
            (path / "SKILL.md").unlink()
            raise OSError("simulated partial uninstall cleanup failure")

        dacl_before_uninstall_recovery = saved_dacl(
            destination,
            "dacl-before-uninstall-recovery.acl",
        )
        uninstall_recovery_root = new_transaction_root("uninstall-recovery")
        try:
            uninstall(
                destination,
                True,
                trusted_tree=tree_c,
                tombstone_remover=fail_partial_uninstall,
                transaction_root=uninstall_recovery_root,
            )
        except LifecycleError as error:
            assert str(uninstall_recovery_root) in str(error)
        else:
            raise AssertionError("partial uninstall cleanup failure was not surfaced")
        assert current_state(destination, tree_c)["state"] == "MANAGED"
        if os.name == "nt":
            assert (
                saved_dacl(destination, "dacl-after-uninstall-recovery.acl")
                == dacl_before_uninstall_recovery
            )
        recovery_transactions = list(uninstall_recovery_root.iterdir())
        assert len(recovery_transactions) == 1
        retained_transaction = recovery_transactions[0]
        assert (retained_transaction / "uninstall-recovery.zip").is_file()
        assert (retained_transaction / "tombstone").is_dir()
        assert destination.parent not in retained_transaction.parents
        shutil.rmtree(retained_transaction)

        uninstall(
            destination,
            True,
            trusted_tree=tree_c,
            transaction_root=new_transaction_root("uninstall"),
        )
        assert current_state(destination)["state"] == "ABSENT"
    return {
        "result": "PASS",
        "scope": (
            "disposable legacy-apply-compatibility/external-transaction "
            "install/update/rollback/failure-recovery/"
            "Windows-DACL-snapshot-preservation-and-semantic-readback/"
            "private-backup-tombstone/path-volume-guards/drift/receipt-integrity/"
            "unreceipted/wrong-tree/uninstall"
        ),
        "persistent_effect": False,
        "source_package_tree": candidate_tree,
        "destination_permission_handoff": (
            "PRESERVED_OR_INHERITED_BY_ACTION" if os.name == "nt" else "PLATFORM_DEFAULT"
        ),
        "permission_handoff_failure_recovery": "PASS",
        "pre_mutation_dacl_snapshot_failure": "PASS",
        "pre_mutation_dacl_restore_preflight_failure": "PASS",
        "pre_mutation_dacl_readback_mismatch": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "post_restore_dacl_readback_mismatch_recovery": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "incomplete_recovery_snapshot_retention": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "missing_dacl_readback_record": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "windows_dacl_snapshot_normalization": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "windows_restrictive_dacl_preservation": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "transaction_alias_test": alias_check,
        "transaction_reparse_test": link_check,
    }


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)
    for action in ("install", "update", "rollback"):
        command = subparsers.add_parser(action)
        command.add_argument("--source", required=True)
        command.add_argument("--destination", required=True)
        command.add_argument("--expected-version", required=True)
        command.add_argument("--trusted-current-package-tree")
        command.add_argument("--trusted-target-package-tree")
        command.add_argument("--transaction-root")
        command.add_argument("--discovery-root", action="append", default=[])
        command.add_argument("--apply", action="store_true")
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--destination", required=True)
    status_parser.add_argument("--trusted-current-package-tree")
    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.add_argument("--destination", required=True)
    uninstall_parser.add_argument("--trusted-current-package-tree")
    uninstall_parser.add_argument("--transaction-root")
    uninstall_parser.add_argument("--discovery-root", action="append", default=[])
    uninstall_parser.add_argument("--apply", action="store_true")
    self_test_parser = subparsers.add_parser("self-test")
    self_test_parser.add_argument("--source", required=False)
    args = parser.parse_args()

    try:
        if args.action in {"install", "update", "rollback"}:
            result = synchronize(
                args.action,
                args.source,
                args.destination,
                args.expected_version,
                args.apply,
                trusted_current_tree=args.trusted_current_package_tree,
                trusted_target_tree=args.trusted_target_package_tree,
                transaction_root=args.transaction_root,
                discovery_roots=args.discovery_root,
            )
        elif args.action == "status":
            result = current_state(
                assert_safe_destination(args.destination),
                args.trusted_current_package_tree,
            )
            result["destination"] = str(resolved(args.destination))
        elif args.action == "uninstall":
            result = uninstall(
                args.destination,
                args.apply,
                trusted_tree=args.trusted_current_package_tree,
                transaction_root=args.transaction_root,
                discovery_roots=args.discovery_root,
            )
        else:
            result = self_test(args.source)
    except (LifecycleError, OSError, AssertionError) as error:
        print(json.dumps({"error": str(error), "result": "FAIL"}, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
