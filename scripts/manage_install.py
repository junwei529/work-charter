#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import shutil
import stat
import tempfile
import uuid
from pathlib import Path


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


def assert_safe_destination(destination, source=None):
    unresolved = Path(destination).expanduser().absolute()
    if any(is_link_like(path) for path in (unresolved, *unresolved.parents)):
        raise LifecycleError("destination or ancestor is a symbolic link, junction, or reparse point")
    destination = unresolved.resolve(strict=False)
    if destination == Path(destination.anchor) or destination == Path.home().resolve():
        raise LifecycleError("destination must not be a filesystem root or home directory")
    if source is not None:
        source = resolved(source)
        if destination == source or source in destination.parents or destination in source.parents:
            raise LifecycleError("destination and source repository must not contain each other")
    return destination


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


def stage_source(package, files, destination, metadata):
    stage = destination.parent / f".{destination.name}.stage-{uuid.uuid4().hex}"
    stage.mkdir(parents=False)
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


def synchronize(
    action,
    source,
    destination,
    expected_version,
    apply,
    backup_remover=shutil.rmtree,
    trusted_current_tree=None,
    trusted_target_tree=None,
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
    if not apply:
        return plan
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage, metadata, files = stage_source(package, files, destination, metadata)
    backup = destination.parent / f".{destination.name}.backup-{uuid.uuid4().hex}"
    moved_old = False
    try:
        if destination.exists():
            os.replace(destination, backup)
            moved_old = True
        os.replace(stage, destination)
        if current_state(destination, tree).get("state") != "MANAGED":
            raise LifecycleError("installed destination failed receipt verification")
    except Exception:
        if destination.exists():
            shutil.rmtree(destination, ignore_errors=True)
        if moved_old and backup.exists():
            os.replace(backup, destination)
        if stage.exists():
            shutil.rmtree(stage, ignore_errors=True)
        raise
    if moved_old:
        try:
            backup_remover(backup)
        except OSError as error:
            plan["backup_path"] = str(backup)
            plan["cleanup_error"] = str(error)
            plan["package_sha256"] = package_digest(files)
            plan["result"] = "MANAGED_WITH_BACKUP"
            return plan
    plan["package_sha256"] = package_digest(files)
    plan["result"] = "MANAGED"
    return plan


def uninstall(
    destination,
    apply,
    trusted_tree=None,
    tombstone_remover=shutil.rmtree,
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
        return result
    tombstone = destination.parent / f".{destination.name}.remove-{uuid.uuid4().hex}"
    recovery_base = destination.parent / f".{destination.name}.uninstall-recovery-{uuid.uuid4().hex}"
    recovery_archive = Path(
        shutil.make_archive(str(recovery_base), "zip", root_dir=destination)
    )
    try:
        os.replace(destination, tombstone)
    except Exception:
        recovery_archive.unlink(missing_ok=True)
        raise
    try:
        tombstone_remover(tombstone)
    except Exception as error:
        try:
            destination.mkdir()
            shutil.unpack_archive(recovery_archive, destination, "zip")
            if current_state(destination, trusted_tree).get("state") != "MANAGED":
                raise LifecycleError("restored destination failed receipt verification")
        except Exception as restore_error:
            raise LifecycleError(
                "uninstall cleanup failed; recovery archive preserved at "
                f"{recovery_archive}; automatic restore failed: {restore_error}"
            ) from error
        raise LifecycleError(
            "uninstall cleanup failed; managed destination was restored; "
            f"recovery archive preserved at {recovery_archive}; partial tombstone at {tombstone}"
        ) from error
    try:
        recovery_archive.unlink()
    except OSError as error:
        result["result"] = "ABSENT"
        result["recovery_archive"] = str(recovery_archive)
        result["warning"] = f"uninstall completed; recovery archive cleanup failed: {error}"
        return result
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
        metadata = candidate_metadata(source, "0.3.0")
        _package, _files, candidate_tree = package_files(
            source,
            metadata["package"]["tree"],
        )
    with tempfile.TemporaryDirectory(prefix="work-charter-lifecycle-") as temporary:
        root = Path(temporary)
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
        source_b = create_test_source(root, "0.3.1", "b")
        source_c = create_test_source(root, "0.3.2", "c")
        source_bad = create_test_source(root, "0.3.9", "bad")
        source_forged = create_test_source(root / "forged-source-root", "0.3.0", "forged")
        tree_a = candidate_metadata(source_a, "0.3.0")["package"]["tree"]
        tree_b = candidate_metadata(source_b, "0.3.1")["package"]["tree"]
        tree_c = candidate_metadata(source_c, "0.3.2")["package"]["tree"]
        tree_bad = candidate_metadata(source_bad, "0.3.9")["package"]["tree"]
        tree_forged = candidate_metadata(source_forged, "0.3.0")["package"]["tree"]
        assert TRUSTED_PACKAGE_TREES["0.3.0"] == tree_a
        assert "0.3.1" not in TRUSTED_PACKAGE_TREES
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
                "0.3.9",
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
            )
        except LifecycleError:
            pass
        else:
            raise AssertionError("forged source candidate was not refused")
        destination = root / "managed" / "work-charter"
        synchronize(
            "install",
            source_a,
            destination,
            "0.3.0",
            True,
            trusted_target_tree=tree_a,
        )
        assert current_state(destination, tree_a)["version"] == "0.3.0"
        assert current_state(destination, tree_b)["version"] == "0.3.0"
        receipt_path = destination / RECEIPT_NAME
        valid_receipt = receipt_path.read_text(encoding="utf-8")
        receipt_path.write_text('{"destination": null}\n', encoding="utf-8", newline="\n")
        assert current_state(destination, tree_a)["state"] == "DRIFTED"
        receipt_path.write_text(valid_receipt, encoding="utf-8", newline="\n")
        synchronize(
            "update",
            source_b,
            destination,
            "0.3.1",
            True,
            trusted_current_tree=tree_a,
            trusted_target_tree=tree_b,
        )
        assert current_state(destination, tree_b)["version"] == "0.3.1"
        synchronize(
            "rollback",
            source_a,
            destination,
            "0.3.0",
            True,
            trusted_current_tree=tree_b,
            trusted_target_tree=tree_a,
        )
        assert current_state(destination, tree_a)["version"] == "0.3.0"

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

        def fail_backup_cleanup(_path):
            raise OSError("simulated backup cleanup failure")

        cleanup_result = synchronize(
            "update",
            source_c,
            destination,
            "0.3.2",
            True,
            backup_remover=fail_backup_cleanup,
            trusted_current_tree=tree_a,
            trusted_target_tree=tree_c,
        )
        assert cleanup_result["result"] == "MANAGED_WITH_BACKUP"
        assert current_state(destination, tree_c)["version"] == "0.3.2"
        backup_path = Path(cleanup_result["backup_path"])
        assert backup_path.exists()
        shutil.rmtree(backup_path)

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

        try:
            uninstall(
                destination,
                True,
                trusted_tree=tree_c,
                tombstone_remover=fail_partial_uninstall,
            )
        except LifecycleError:
            pass
        else:
            raise AssertionError("partial uninstall cleanup failure was not surfaced")
        assert current_state(destination, tree_c)["state"] == "MANAGED"

        uninstall(destination, True, trusted_tree=tree_c)
        assert current_state(destination)["state"] == "ABSENT"
    return {
        "result": "PASS",
        "scope": "disposable tree-binding/install/update/rollback/drift/receipt-integrity/unreceipted/wrong-tree/cleanup-recovery/uninstall",
        "persistent_effect": False,
        "source_package_tree": candidate_tree,
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
        command.add_argument("--apply", action="store_true")
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--destination", required=True)
    status_parser.add_argument("--trusted-current-package-tree")
    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.add_argument("--destination", required=True)
    uninstall_parser.add_argument("--trusted-current-package-tree")
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
