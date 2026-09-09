#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import uuid
import zipfile
from pathlib import Path, PurePosixPath, PureWindowsPath


RECEIPT_NAME = ".work-charter-install.json"
RECEIPT_SCHEMA = "work-charter-install-receipt/v1"
LEGACY_PACKAGE_FILES = frozenset({
    "SKILL.md",
    "agents/openai.yaml",
    "assets/work-charter.md",
    "references/coordination-and-recovery.md",
    "references/standard-ope.md",
})
EXPECTED_FILES = LEGACY_PACKAGE_FILES | {"assets/role-models.default.yaml"}
ALLOWED_PACKAGE_FILE_SETS = frozenset({LEGACY_PACKAGE_FILES, EXPECTED_FILES})
TRUSTED_PACKAGE_TREES = {
    "0.3.0": "0ac3cbb0f1fa8fa51d8f832c8127eabc9863ec9e",
}
SELF_TEST_SOURCE_VERSION = "0.6.3"


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


def windows_security(path=None, descriptor=None):
    """Read native owner/DACL and decode only ordinary allow/deny ACEs."""
    import ctypes
    from ctypes import wintypes

    adv = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    adv.ConvertSidToStringSidW.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.LPWSTR)]
    adv.ConvertSidToStringSidW.restype = wintypes.BOOL
    adv.ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(wintypes.DWORD),
    ]
    adv.ConvertStringSecurityDescriptorToSecurityDescriptorW.restype = wintypes.BOOL
    adv.GetNamedSecurityInfoW.argtypes = [
        wintypes.LPWSTR, ctypes.c_int, wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p,
        ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p),
    ]
    adv.GetNamedSecurityInfoW.restype = wintypes.DWORD
    adv.ConvertSecurityDescriptorToStringSecurityDescriptorW.argtypes = [
        ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
        ctypes.POINTER(wintypes.LPWSTR), ctypes.POINTER(wintypes.DWORD),
    ]
    adv.ConvertSecurityDescriptorToStringSecurityDescriptorW.restype = wintypes.BOOL
    adv.GetSecurityDescriptorDacl.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(wintypes.BOOL),
        ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.BOOL),
    ]
    adv.GetSecurityDescriptorDacl.restype = wintypes.BOOL
    adv.GetAce.argtypes = [ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p)]
    adv.GetAce.restype = wintypes.BOOL

    def sid_text(pointer):
        text = wintypes.LPWSTR()
        if not adv.ConvertSidToStringSidW(pointer, ctypes.byref(text)):
            raise LifecycleError("Windows owner or trustee SID conversion failed")
        try:
            return text.value
        finally:
            kernel.LocalFree(ctypes.cast(text, ctypes.c_void_p))

    security = ctypes.c_void_p()
    owner = ctypes.c_void_p()
    if path is not None:
        assert_no_link_like_components(path, "security object")
        status = adv.GetNamedSecurityInfoW(
            str(path), 1, 5, ctypes.byref(owner), None, None, None,
            ctypes.byref(security),
        )
        if status:
            raise LifecycleError(f"Windows owner/DACL read failed with error {status}")
    elif not adv.ConvertStringSecurityDescriptorToSecurityDescriptorW(
        descriptor, 1, ctypes.byref(security), None,
    ):
        raise LifecycleError("Windows DACL admission conversion failed")
    try:
        text = wintypes.LPWSTR()
        if not adv.ConvertSecurityDescriptorToStringSecurityDescriptorW(
            security, 1, 4, ctypes.byref(text), None,
        ):
            raise LifecycleError("Windows DACL serialization failed")
        try:
            dacl_text = text.value
        finally:
            kernel.LocalFree(ctypes.cast(text, ctypes.c_void_p))
        present, defaulted = wintypes.BOOL(), wintypes.BOOL()
        dacl = ctypes.c_void_p()
        if not adv.GetSecurityDescriptorDacl(
            security, ctypes.byref(present), ctypes.byref(dacl), ctypes.byref(defaulted),
        ) or not present.value or not dacl.value:
            raise LifecycleError("Windows absent or NULL DACL is unsupported")
        # ACL header: revision/reserved, size, ACE count, reserved.
        count = ctypes.c_ushort.from_address(dacl.value + 4).value
        aces = []
        for index in range(count):
            ace = ctypes.c_void_p()
            if not adv.GetAce(dacl, index, ctypes.byref(ace)):
                raise LifecycleError("Windows DACL ACE read failed")
            kind = ctypes.c_ubyte.from_address(ace.value).value
            flags = ctypes.c_ubyte.from_address(ace.value + 1).value
            if kind not in {0, 1} or flags & ~0x1f:
                raise LifecycleError("Windows complex ACE type or flags are unsupported")
            aces.append({
                "type": kind, "flags": flags,
                "mask": ctypes.c_uint32.from_address(ace.value + 4).value,
                "sid": sid_text(ace.value + 8),
            })
        return {"owner": sid_text(owner) if owner.value else None,
                "dacl": dacl_text, "aces": aces}
    finally:
        kernel.LocalFree(security)


def windows_process_sid():
    import ctypes
    from ctypes import wintypes

    adv = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    adv.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
    adv.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                       wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    adv.ConvertSidToStringSidW.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.LPWSTR)]
    token = wintypes.HANDLE()
    if not adv.OpenProcessToken(kernel.GetCurrentProcess(), 8, ctypes.byref(token)):
        raise LifecycleError("Windows process identity read failed")
    try:
        size = wintypes.DWORD()
        adv.GetTokenInformation(token, 1, None, 0, ctypes.byref(size))
        if not size.value:
            raise LifecycleError("Windows process SID size unavailable")
        buffer = ctypes.create_string_buffer(size.value)
        if not adv.GetTokenInformation(token, 1, buffer, size, ctypes.byref(size)):
            raise LifecycleError("Windows process SID read failed")
        pointer = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_void_p))[0]
        text = wintypes.LPWSTR()
        if not adv.ConvertSidToStringSidW(pointer, ctypes.byref(text)):
            raise LifecycleError("Windows process SID conversion failed")
        try:
            return text.value
        finally:
            kernel.LocalFree(ctypes.cast(text, ctypes.c_void_p))
    finally:
        kernel.CloseHandle(token)


def assert_windows_trusted_writers(path, security=None):
    security = security or windows_security(path)
    trusted = {"S-1-5-18", "S-1-5-32-544", windows_process_sid()}
    if security["owner"] not in trusted:
        raise LifecycleError("Windows object owner is outside the trusted writer set")
    # Reject any untrusted allow capable of mutation, including inherit-only
    # grants. Do not try to prove that a deny ACE cancels such a grant.
    writing = 0x000d0156 | 0x40000000 | 0x10000000
    for ace in security["aces"]:
        trusted_sid = ace["sid"] in trusted | {"S-1-3-4", "S-1-3-0"}
        if ace["type"] == 0 and ace["mask"] & writing and not trusted_sid:
            raise LifecycleError("Windows DACL permits an untrusted writer")
    return security


def windows_private_descriptor(directory):
    flags = "OICI" if directory else ""
    return "D:P" + "".join(f"(A;{flags};FA;;;{sid})" for sid in ("OW", "SY", "BA"))


def assert_windows_private_object(path):
    security = assert_windows_trusted_writers(path)
    expected = windows_security(descriptor=windows_private_descriptor(Path(path).is_dir()))
    def ordered(aces):
        return sorted((ace["type"], ace["flags"], ace["mask"], ace["sid"]) for ace in aces)
    if ("P" not in windows_dacl_control_flags(security["dacl"])
            or ordered(security["aces"]) != ordered(expected["aces"])):
        raise LifecycleError("Windows transaction object is not individually private")


def create_private_directory(path):
    path = Path(path)
    if os.name == "nt":
        path.mkdir(mode=0o700)
        set_windows_dacl(path, windows_private_descriptor(True))
        assert_windows_private_object(path)
    else:
        path.mkdir()


def create_private_file(path):
    path = Path(path)
    with path.open("xb"):
        pass
    if os.name == "nt":
        set_windows_dacl(path, windows_private_descriptor(False))
        assert_windows_private_object(path)


def write_private_bytes(path, data):
    create_private_file(path)
    Path(path).write_bytes(data)


def assert_private_tree(path):
    if os.name == "nt":
        for target in [Path(path), *Path(path).rglob("*")]:
            assert_windows_private_object(target)


def privatize_tree(path):
    if os.name == "nt":
        for target in [Path(path), *sorted(Path(path).rglob("*"))]:
            assert_no_link_like_components(target, "private handoff")
            if target.is_file() and target.stat().st_nlink != 1:
                raise LifecycleError("Windows private handoff refuses a hard-linked file")
            set_windows_dacl(target, windows_private_descriptor(target.is_dir()))
        assert_private_tree(path)


def create_transaction_directory(transaction_root):
    if os.name == "nt":
        assert_windows_trusted_writers(transaction_root)
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
        if os.name == "nt":
            assert_windows_private_object(transaction)
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


def package_directories(files):
    return {
        Path(relative).parent.as_posix()
        for relative in files
        if Path(relative).parent.as_posix() != "."
    }


def validate_package_file_set(values, label):
    if not isinstance(values, (list, tuple, set, frozenset)):
        raise LifecycleError(f"{label} must be a path list")
    if any(not isinstance(value, str) for value in values):
        raise LifecycleError(f"{label} contains a non-string path")
    if len(values) != len(set(values)):
        raise LifecycleError(f"{label} contains duplicate paths")
    files = frozenset(values)
    for value in files:
        relative = PurePosixPath(value)
        if (
            not value
            or "\\" in value
            or ":" in value
            or relative.is_absolute()
            or relative.as_posix() != value
            or any(part in {"", ".", ".."} for part in relative.parts)
        ):
            raise LifecycleError(f"{label} contains an unsafe path")
    if files not in ALLOWED_PACKAGE_FILE_SETS:
        raise LifecycleError(f"{label} is not an allowed package path set")
    return files


def candidate_file_set(metadata):
    package = metadata.get("package", {})
    if package.get("path") != "skills/work-charter":
        raise LifecycleError("candidate package path mismatch")
    declared = package.get("files")
    if declared is None:
        files = LEGACY_PACKAGE_FILES
    else:
        files = validate_package_file_set(declared, "candidate package files")
    if package.get("file_count") != len(files):
        raise LifecycleError("candidate package file count mismatch")
    return files


def receipt_file_set(files):
    if not isinstance(files, dict):
        raise LifecycleError("receipt files must be an object")
    result = validate_package_file_set(list(files), "receipt file set")
    if any(
        not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
        for digest in files.values()
    ):
        raise LifecycleError("receipt contains an invalid file digest")
    return result


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
    candidate_file_set(value)
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


def candidate_package_digest(files):
    records = [[relative, files[relative]] for relative in sorted(files)]
    encoded = json.dumps(records, ensure_ascii=True, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def package_files(source, metadata, expected_tree):
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
    expected_files = candidate_file_set(metadata)
    if actual != expected_files:
        raise LifecycleError(f"package path set mismatch: {sorted(actual)}")
    tree = git_tree_hash(package)
    if tree != expected_tree:
        raise LifecycleError(f"package tree mismatch: expected {expected_tree}, got {tree}")
    files = {relative: sha256(package / relative) for relative in sorted(actual)}
    package_record = metadata.get("package", {})
    actual_digest = candidate_package_digest(files)
    if "sha256" not in package_record:
        if expected_files != LEGACY_PACKAGE_FILES:
            raise LifecycleError("candidate package digest is required for the current package shape")
    elif (
        not isinstance(package_record.get("sha256"), str)
        or len(package_record["sha256"]) != 64
        or any(character not in "0123456789abcdef" for character in package_record["sha256"])
    ):
        raise LifecycleError("candidate package digest is invalid")
    elif package_record["sha256"] != actual_digest:
        raise LifecycleError("candidate package digest mismatch")
    return package, files, tree


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
    try:
        expected_files = receipt_file_set(expected)
    except LifecycleError as error:
        return {"state": "DRIFTED", "reason": str(error)}
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
    if actual != expected_files:
        return {"state": "DRIFTED", "reason": "managed file set mismatch"}
    actual_directories = {
        path.relative_to(destination).as_posix()
        for path in entries
        if path.is_dir()
    }
    if actual_directories != package_directories(expected_files):
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
    create_private_directory(stage)
    try:
        for relative in sorted(package_directories(files), key=lambda value: (len(PurePosixPath(value).parts), value)):
            create_private_directory(stage / relative)
        for relative in sorted(files):
            target = stage / relative
            create_private_file(target)
            shutil.copyfile(package / relative, target)
        create_private_file(stage / RECEIPT_NAME)
        write_receipt(stage, metadata, files, destination)
        if any(sha256(stage / relative) != digest for relative, digest in files.items()):
            raise LifecycleError("staged package failed file verification")
        assert_private_tree(stage)
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
    create_private_file(snapshot)
    run_windows_acl(
        path,
        ["/save", str(snapshot), "/T", "/Q"],
        "DACL snapshot",
    )
    try:
        if not snapshot.is_file() or snapshot.stat().st_size == 0:
            raise LifecycleError("Windows DACL snapshot is missing or empty")
        assert_windows_private_object(snapshot)
        return sha256(snapshot)
    except OSError as error:
        raise LifecycleError("Windows DACL snapshot is unreadable") from error


def windows_dacl_snapshot_records(snapshot):
    return {
        key: descriptor
        for key, (_relative, descriptor) in windows_dacl_snapshot_entries(snapshot).items()
    }


def windows_dacl_snapshot_entries(snapshot):
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
        records[key] = (relative, descriptor)
    return records


def assert_windows_dacl_snapshot_match(expected_snapshot, observed_snapshot):
    expected = windows_dacl_snapshot_records(expected_snapshot)
    observed = windows_dacl_snapshot_records(observed_snapshot)
    if expected.keys() != observed.keys():
        raise LifecycleError("Windows restored DACL path set mismatch")
    for path in expected:
        if expected[path] == observed[path]:
            continue
        expected_flags = sorted(windows_dacl_control_flags(expected[path]))
        observed_flags = sorted(windows_dacl_control_flags(observed[path]))
        if expected_flags != observed_flags:
            raise LifecycleError(
                "Windows restored DACL descriptor mismatch "
                f"at {path}: control flags {expected_flags!r} != {observed_flags!r}"
            )
        raise LifecycleError(f"Windows restored DACL descriptor mismatch at {path}")


def windows_dacl_control_flags(descriptor):
    control_text = descriptor[2 : descriptor.find("(")]
    if "(" not in descriptor:
        control_text = descriptor[2:]
    flags = []
    while control_text:
        for flag in ("NO_ACCESS_CONTROL", "AR", "AI", "P"):
            if control_text.startswith(flag):
                flags.append(flag)
                control_text = control_text[len(flag) :]
                break
        else:
            raise LifecycleError("Windows DACL snapshot contains invalid control flags")
    return frozenset(flags)


def set_windows_dacl(path, descriptor):
    if os.name != "nt":
        raise LifecycleError("Windows DACL restore is unavailable on this platform")
    import ctypes
    from ctypes import wintypes

    convert = ctypes.WinDLL(
        "advapi32", use_last_error=True
    ).ConvertStringSecurityDescriptorToSecurityDescriptorW
    convert.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(wintypes.DWORD),
    ]
    convert.restype = wintypes.BOOL
    set_file_security = ctypes.WinDLL("advapi32", use_last_error=True).SetFileSecurityW
    set_file_security.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p]
    set_file_security.restype = wintypes.BOOL
    local_free = ctypes.WinDLL("kernel32", use_last_error=True).LocalFree
    local_free.argtypes = [ctypes.c_void_p]
    local_free.restype = ctypes.c_void_p

    security_descriptor = ctypes.c_void_p()
    if not convert(descriptor, 1, ctypes.byref(security_descriptor), None):
        error = ctypes.get_last_error()
        raise LifecycleError(
            f"Windows DACL descriptor conversion failed with error {error}"
        )
    try:
        flags = windows_dacl_control_flags(descriptor)
        security_information = 0x00000004
        if "P" in flags:
            security_information |= 0x80000000
        if not set_file_security(str(path), security_information, security_descriptor):
            error = ctypes.get_last_error()
            raise LifecycleError(
                f"Windows DACL native restore failed with error {error}"
            )
    finally:
        local_free(security_descriptor)


def restore_windows_dacl_with_ai(path, descriptor, snapshot):
    record = Path(snapshot).with_name(f".wcr-{uuid.uuid4().hex}.acl")
    try:
        write_private_bytes(record,
            f"{Path(path).name}\r\n{descriptor}\r\n\r\n".encode("utf-16-le")
        )
        run_windows_acl(
            Path(path).parent,
            ["/restore", str(record), "/Q"],
            "DACL automatic-inheritance restore",
        )
    finally:
        remove_permission_snapshot(record)


def restore_windows_dacl_records(path, snapshot):
    assert_no_link_like_components(path, "DACL restore")
    path = resolved(path)
    entries = windows_dacl_snapshot_entries(snapshot)
    root_key = path.name.casefold()
    if root_key not in entries:
        raise LifecycleError("Windows DACL snapshot does not contain the managed root")
    ordered = sorted(
        entries.values(), key=lambda entry: (len(entry[0].parts), str(entry[0]))
    )
    targets = []
    for relative, descriptor in ordered:
        if relative.parts[0].casefold() != root_key:
            raise LifecycleError("Windows DACL snapshot path escapes the managed root")
        declared_target = path.parent.joinpath(*relative.parts)
        assert_no_link_like_components(declared_target, "DACL restore")
        target = resolved(declared_target)
        if target != path and path not in target.parents:
            raise LifecycleError("Windows DACL snapshot path escapes the managed root")
        if not target.exists() or is_link_like(target):
            raise LifecycleError("Windows DACL restore target is missing or link-like")
        if target.is_file() and target.stat().st_nlink != 1:
            raise LifecycleError("Windows DACL restore refuses a hard-linked file")
        targets.append((target, descriptor))
    for target, descriptor in targets:
        if "AI" in windows_dacl_control_flags(descriptor):
            restore_windows_dacl_with_ai(target, descriptor, snapshot)
        else:
            set_windows_dacl(target, descriptor)


def restore_permission_snapshot(
    path,
    snapshot,
    expected_digest,
    descriptor_writer=restore_windows_dacl_records,
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
    descriptor_writer(path, snapshot)
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
    permission_context=None,
):
    if os.name != "nt":
        return "PLATFORM_DEFAULT"
    context = permission_context or capture_permission_context(path, snapshot, expected_digest)
    probe_parent = Path(transaction) / "p"
    probe = probe_parent / "context" / Path(path).name
    if probe_parent.exists():
        raise LifecycleError("Windows DACL restore preflight path is unavailable")
    try:
        create_permission_model(probe_parent, path, context)
        result = permission_restorer(probe, snapshot, expected_digest)
        if result != "PRESERVED_FROM_SNAPSHOT":
            raise LifecycleError("Windows DACL restore preflight returned an invalid result")
        privatize_tree(probe)
        if permission_restorer(probe, snapshot, expected_digest) != "PRESERVED_FROM_SNAPSHOT":
            raise LifecycleError("Windows private handoff roundtrip failed")
        assert_context_owners(probe, context)
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


def package_path_shape(root):
    root = Path(root)
    entries = {}
    for path in root.rglob("*"):
        if is_link_like(path):
            raise LifecycleError("permission projection contains a link-like path")
        relative = path.relative_to(root).as_posix()
        if path.is_dir():
            entries[relative] = "directory"
        elif path.is_file():
            entries[relative] = "file"
        else:
            raise LifecycleError("permission projection contains an unsupported path")
    return entries


def object_identity(path):
    metadata = Path(path).stat()
    return [metadata.st_dev, metadata.st_ino]


def capture_parent_context(path):
    parent = Path(path).parent
    security = assert_windows_trusted_writers(parent)
    return {"path": str(parent), "identity": object_identity(parent), "security": security}


def assert_parent_context(context):
    if os.name != "nt" or context is None:
        return
    parent = Path(context["path"])
    assert_no_link_like_components(parent, "destination parent")
    if object_identity(parent) != context["identity"] or windows_security(parent) != context["security"]:
        raise LifecycleError("Windows destination parent identity or permission drift")


def capture_permission_context(path, snapshot, expected_digest):
    path = Path(path)
    if sha256(snapshot) != expected_digest:
        raise LifecycleError("Windows DACL context snapshot identity mismatch")
    parent = capture_parent_context(path)
    shape = package_path_shape(path)
    files = {name for name, kind in shape.items() if kind == "file"}
    package = validate_package_file_set(files - {RECEIPT_NAME}, "DACL context package")
    if files != package | {RECEIPT_NAME} or {
        name for name, kind in shape.items() if kind == "directory"
    } != package_directories(package):
        raise LifecycleError("Windows DACL context shape is not managed")
    entries = windows_dacl_snapshot_records(snapshot)
    objects = {}
    for relative in ["", *sorted(shape)]:
        target = path / relative
        security = assert_windows_trusted_writers(target)
        if target.is_file() and target.stat().st_nlink != 1:
            raise LifecycleError("Windows DACL context refuses a hard-linked file")
        key = windows_snapshot_key(path.name, relative)
        if entries.get(key) != security["dacl"]:
            raise LifecycleError("Windows DACL context differs from original snapshot")
        objects[relative] = {
            "identity": object_identity(target), "security": security,
            "sha256": sha256(target) if target.is_file() else None,
        }
    if len(entries) != len(objects):
        raise LifecycleError("Windows DACL context snapshot path set mismatch")
    owner = objects[""]["security"]["owner"]
    if any(value["security"]["owner"] != owner for value in objects.values()):
        raise LifecycleError("Windows managed tree has differing owners")
    assert_parent_context(parent)
    return {"parent": parent, "path": str(path), "shape": shape,
            "objects": objects, "owner": owner, "snapshot_sha256": expected_digest}


def assert_context_owners(path, context):
    for target in [Path(path), *Path(path).rglob("*")]:
        if windows_security(target)["owner"] != context["owner"]:
            raise LifecycleError("Windows handoff would change an object owner")


def assert_permission_context(path, context, original_permissions=True, same_objects=True):
    if context is None:
        return
    assert_parent_context(context["parent"])
    if package_path_shape(path) != context["shape"]:
        raise LifecycleError("Windows managed path shape drift")
    for relative, expected in context["objects"].items():
        target = Path(path) / relative
        assert_no_link_like_components(target, "managed handoff")
        if same_objects and object_identity(target) != expected["identity"]:
            raise LifecycleError("Windows managed object identity drift")
        security = windows_security(target)
        if security["owner"] != expected["security"]["owner"]:
            raise LifecycleError("Windows managed owner drift")
        if original_permissions and security != expected["security"]:
            raise LifecycleError("Windows managed permission drift")
        if expected["sha256"] is not None and (
            target.stat().st_nlink != 1 or sha256(target) != expected["sha256"]
        ):
            raise LifecycleError("Windows managed file identity or content drift")


def create_permission_model(container, path, context):
    # Only empty managed-shaped objects enter the readable ACL model. Original
    # bytes, receipts and snapshots stay outside it in individually private files.
    create_private_directory(container)
    model_parent = Path(container) / "context"
    create_private_directory(model_parent)
    original = context["parent"]["security"]["dacl"]
    aces = []
    for ace in re.findall(r"\(([^()]*)\)", original):
        fields = ace.split(";")
        if len(fields) != 6 or fields[0] not in {"A", "D"}:
            raise LifecycleError("Windows inheritance context ACE is unsupported")
        fields[1] = fields[1].replace("ID", "")
        aces.append("(" + ";".join(fields) + ")")
    set_windows_dacl(model_parent, "D:P" + "".join(aces))
    assert_windows_trusted_writers(model_parent)
    probe = model_parent / Path(path).name
    probe.mkdir()
    for relative in sorted(context["shape"], key=lambda name: (len(PurePosixPath(name).parts), name)):
        target = probe / relative
        if context["shape"][relative] == "directory":
            target.mkdir()
        else:
            with target.open("xb"):
                pass
    assert_context_owners(probe, context)
    return probe


def reset_windows_path_inheritance(path):
    run_windows_acl(path, ["/reset", "/Q"], "new-path inheritance projection")


def windows_snapshot_key(root_name, relative=None):
    parts = [root_name]
    if relative:
        parts.extend(PurePosixPath(relative).parts)
    return "\\".join(part.casefold() for part in parts)


def assert_projected_permission_snapshot(
    original_snapshot,
    projected_snapshot,
    root_name,
    desired_shape,
    added_paths,
):
    original = windows_dacl_snapshot_records(original_snapshot)
    projected = windows_dacl_snapshot_records(projected_snapshot)
    expected_keys = {windows_snapshot_key(root_name)} | {
        windows_snapshot_key(root_name, relative) for relative in desired_shape
    }
    if projected.keys() != expected_keys:
        raise LifecycleError("Windows projected DACL path set mismatch")
    for key in original.keys() & projected.keys():
        if original[key] != projected[key]:
            raise LifecycleError(
                f"Windows permission projection changed an existing descriptor at {key}"
            )
    for relative in added_paths:
        descriptor = projected[windows_snapshot_key(root_name, relative)]
        flags = windows_dacl_control_flags(descriptor)
        if "P" in flags or "AI" not in flags:
            raise LifecycleError(
                f"Windows permission projection did not produce inherited ACLs at {relative}"
            )


def project_permission_snapshot(
    path,
    stage,
    transaction,
    original_snapshot,
    original_digest,
    permission_context=None,
):
    if os.name != "nt":
        return None, None
    context = permission_context or capture_permission_context(path, original_snapshot, original_digest)
    probe_parent = Path(transaction) / "pp"
    probe = probe_parent / "context" / Path(path).name
    projected_snapshot = Path(transaction) / "projected-dacl.acl"
    if probe_parent.exists() or projected_snapshot.exists():
        raise LifecycleError("Windows DACL projection path is unavailable")
    try:
        create_permission_model(probe_parent, path, context)
        restored = restore_permission_snapshot(
            probe,
            original_snapshot,
            original_digest,
        )
        if restored != "PRESERVED_FROM_SNAPSHOT":
            raise LifecycleError("Windows DACL projection restore returned an invalid result")

        current_shape = package_path_shape(probe)
        desired_shape = package_path_shape(stage)
        for relative in current_shape.keys() & desired_shape.keys():
            if current_shape[relative] != desired_shape[relative]:
                raise LifecycleError("package path type changed across permission projection")

        removed_paths = current_shape.keys() - desired_shape.keys()
        for relative in sorted(
            removed_paths,
            key=lambda value: (len(PurePosixPath(value).parts), value),
            reverse=True,
        ):
            target = probe.joinpath(*PurePosixPath(relative).parts)
            if current_shape[relative] == "directory":
                target.rmdir()
            else:
                target.unlink()

        added_paths = desired_shape.keys() - current_shape.keys()
        added_directories = [
            relative for relative in added_paths if desired_shape[relative] == "directory"
        ]
        for relative in sorted(
            added_directories,
            key=lambda value: (len(PurePosixPath(value).parts), value),
        ):
            probe.joinpath(*PurePosixPath(relative).parts).mkdir()
        added_files = [
            relative for relative in added_paths if desired_shape[relative] == "file"
        ]
        for relative in sorted(added_files):
            parts = PurePosixPath(relative).parts
            with probe.joinpath(*parts).open("xb"):
                pass
        for relative in sorted(
            added_paths,
            key=lambda value: (len(PurePosixPath(value).parts), value),
        ):
            reset_windows_path_inheritance(probe.joinpath(*PurePosixPath(relative).parts))

        projected_digest = capture_permission_snapshot(probe, projected_snapshot)
        if not projected_digest:
            raise LifecycleError("Windows projected DACL snapshot was not created")
        assert_projected_permission_snapshot(
            original_snapshot,
            projected_snapshot,
            Path(path).name,
            desired_shape,
            added_paths,
        )
        verified = restore_permission_snapshot(
            probe,
            projected_snapshot,
            projected_digest,
        )
        if verified != "PRESERVED_FROM_SNAPSHOT":
            raise LifecycleError("Windows projected DACL preflight returned an invalid result")
        privatize_tree(probe)
        restore_permission_snapshot(probe, projected_snapshot, projected_digest)
        assert_context_owners(probe, context)
    except Exception as error:
        remove_permission_snapshot(projected_snapshot)
        try:
            shutil.rmtree(probe_parent)
        except OSError:
            pass
        raise LifecycleError(
            "Windows DACL path-set projection failed before destination mutation"
        ) from error
    try:
        shutil.rmtree(probe_parent)
    except OSError as error:
        remove_permission_snapshot(projected_snapshot)
        raise LifecycleError("Windows DACL projection cleanup failed") from error
    return projected_snapshot, projected_digest


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
    package, files, tree = package_files(source, metadata, trusted_target_tree)
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
    target_permission_snapshot = permission_snapshot
    target_permission_snapshot_digest = None
    projected_permission_snapshot = transaction / "projected-dacl.acl"
    moved_old = False
    installed_new = False
    private_handoff_started = False
    permission_context = None
    context_file = transaction / "permission-context.json"
    parent_context = None
    try:
        parent_context = capture_parent_context(destination) if os.name == "nt" else None
        if action in {"update", "rollback"}:
            permission_snapshot_digest = permission_snapshotter(
                destination,
                permission_snapshot,
            )
            if os.name == "nt" and not permission_snapshot_digest:
                raise LifecycleError("Windows DACL snapshot was not created")
            if os.name == "nt":
                permission_context = capture_permission_context(
                    destination, permission_snapshot, permission_snapshot_digest,
                )
                parent_context = permission_context["parent"]
                write_private_bytes(context_file, json.dumps(permission_context).encode("utf-8"))
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
            target_permission_snapshot_digest = permission_snapshot_digest
            if os.name == "nt":
                receipt = read_receipt(destination)
                current_files = receipt_file_set(receipt.get("files"))
                if current_files != frozenset(files):
                    (
                        target_permission_snapshot,
                        target_permission_snapshot_digest,
                    ) = project_permission_snapshot(
                        destination,
                        stage,
                        transaction,
                        permission_snapshot,
                        permission_snapshot_digest,
                        permission_context,
                    )
                assert_context_owners(stage, permission_context)
                assert_permission_context(destination, permission_context)
                private_handoff_started = True
                privatize_tree(destination)
                assert_permission_context(destination, permission_context, original_permissions=False)
            assert_parent_context(parent_context)
            path_replacer(destination, backup)
            moved_old = True
            assert_private_tree(backup)
        elif destination.exists():
            raise LifecycleError("install destination appeared after preflight")
        assert_parent_context(parent_context)
        assert_private_tree(stage)
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
            assert_parent_context(parent_context)
            assert_context_owners(destination, permission_context)
            permission_result = permission_restorer(
                destination,
                target_permission_snapshot,
                target_permission_snapshot_digest,
            )
            if permission_result != "PRESERVED_FROM_SNAPSHOT":
                raise LifecycleError("destination DACL restore returned an invalid result")
            plan["destination_permissions"] = (
                "PROJECTED_FROM_PREVIOUS_DESTINATION"
                if target_permission_snapshot != permission_snapshot
                else "PRESERVED_FROM_PREVIOUS_DESTINATION"
            )
        if current_state(destination, tree).get("state") != "MANAGED":
            raise LifecycleError("installed destination failed receipt verification")
        assert_parent_context(parent_context)
    except Exception as operation_error:
        recovery_errors = []
        if installed_new and destination.exists():
            try:
                assert_parent_context(parent_context)
                assert_no_link_like_components(destination, "failed destination cleanup")
                shutil.rmtree(destination)
            except (OSError, LifecycleError) as error:
                recovery_errors.append(f"new destination cleanup failed: {error}")
        if moved_old:
            if destination.exists():
                recovery_errors.append("old destination restore blocked because destination still exists")
            elif not backup.exists():
                recovery_errors.append("old destination backup is missing")
            else:
                try:
                    assert_parent_context(parent_context)
                    assert_permission_context(backup, permission_context, original_permissions=False)
                    assert_private_tree(backup)
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
                    assert_permission_context(destination, permission_context)
                except Exception as error:
                    recovery_errors.append(f"old destination restore failed: {error}")
        elif private_handoff_started:
            try:
                assert_permission_context(destination, permission_context, original_permissions=False)
                if permission_restorer(destination, permission_snapshot, permission_snapshot_digest) != "PRESERVED_FROM_SNAPSHOT":
                    raise LifecycleError("partial private handoff restore returned an invalid result")
                assert_permission_context(destination, permission_context)
            except Exception as error:
                recovery_errors.append(f"partial private handoff restore failed: {error}")
        if stage.exists():
            try:
                assert_no_link_like_components(stage, "failed stage cleanup")
                shutil.rmtree(stage)
            except (OSError, LifecycleError) as error:
                recovery_errors.append(f"stage cleanup failed: {error}")
        if recovery_errors:
            raise LifecycleError(
                f"{action} failed; automatic recovery is incomplete; transaction preserved at "
                f"{transaction}: {'; '.join(recovery_errors)}"
            ) from operation_error
        remove_permission_snapshot(permission_snapshot)
        remove_permission_snapshot(projected_permission_snapshot)
        remove_permission_snapshot(context_file)
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
            assert_no_link_like_components(backup, "backup cleanup")
            assert_private_tree(backup)
            backup_remover(backup)
        except (OSError, LifecycleError) as error:
            plan["backup_path"] = str(backup)
            plan["cleanup_error"] = str(error)
            plan["package_sha256"] = package_digest(files)
            plan["result"] = "MANAGED_WITH_BACKUP"
            plan["transaction_path"] = str(transaction)
            return plan
    remove_permission_snapshot(permission_snapshot)
    remove_permission_snapshot(projected_permission_snapshot)
    remove_permission_snapshot(context_file)
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


def recovery_archive_members(archive):
    members = archive.infolist()
    names = [member.filename for member in members]
    if len(names) != len(set(names)):
        raise LifecycleError("uninstall recovery archive has duplicate paths")
    files = {member.filename for member in members if not member.is_dir()}
    package = validate_package_file_set(files - {RECEIPT_NAME}, "recovery archive package")
    directories = package_directories(package)
    if files != package | {RECEIPT_NAME} or any(
        member.filename not in files | {name + "/" for name in directories}
        for member in members
    ):
        raise LifecycleError("uninstall recovery archive path set mismatch")
    return files, directories


def verify_recovery_archive(archive_path, destination):
    with zipfile.ZipFile(archive_path) as archive:
        files, _directories = recovery_archive_members(archive)
        if any(archive.read(name) != (Path(destination) / name).read_bytes() for name in files):
            raise LifecycleError("uninstall recovery archive content mismatch")


def unpack_private_archive(archive_path, destination):
    with zipfile.ZipFile(archive_path) as archive:
        files, directories = recovery_archive_members(archive)
        create_private_directory(destination)
        for name in sorted(directories):
            create_private_directory(Path(destination) / name)
        for name in sorted(files):
            write_private_bytes(Path(destination) / name, archive.read(name))
    assert_private_tree(destination)


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
    context_file = transaction / "permission-context.json"
    permission_context = None
    try:
        permission_snapshot_digest = permission_snapshotter(
            destination,
            permission_snapshot,
        )
        if os.name == "nt" and not permission_snapshot_digest:
            raise LifecycleError("Windows DACL snapshot was not created")
        if os.name == "nt":
            permission_context = capture_permission_context(destination, permission_snapshot, permission_snapshot_digest)
            write_private_bytes(context_file, json.dumps(permission_context).encode("utf-8"))
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
        remove_permission_snapshot(context_file)
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
        create_private_file(recovery_base.with_suffix(".zip"))
        recovery_archive = Path(
            shutil.make_archive(str(recovery_base), "zip", root_dir=destination)
        )
        if os.name == "nt":
            assert_windows_private_object(recovery_archive)
        archive_digest = sha256(recovery_archive)
        verify_recovery_archive(recovery_archive, destination)
    except Exception:
        remove_permission_snapshot(permission_snapshot)
        remove_permission_snapshot(context_file)
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
    private_handoff_started = False
    try:
        assert_permission_context(destination, permission_context)
        private_handoff_started = True
        privatize_tree(destination)
        assert_permission_context(destination, permission_context, original_permissions=False)
        path_replacer(destination, tombstone)
    except Exception as operation_error:
        if private_handoff_started and permission_context is not None:
            try:
                assert_permission_context(destination, permission_context, original_permissions=False)
                if permission_restorer(destination, permission_snapshot, permission_snapshot_digest) != "PRESERVED_FROM_SNAPSHOT":
                    raise LifecycleError("partial uninstall handoff restore returned an invalid result")
                assert_permission_context(destination, permission_context)
            except Exception as restore_error:
                raise LifecycleError(
                    f"uninstall private handoff failed; recovery retained at {transaction}; "
                    f"automatic restore failed: {restore_error}"
                ) from operation_error
        recovery_archive.unlink(missing_ok=True)
        remove_permission_snapshot(permission_snapshot)
        remove_permission_snapshot(context_file)
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
        assert_private_tree(tombstone)
        tombstone_remover(tombstone)
    except Exception as error:
        try:
            if sha256(recovery_archive) != archive_digest:
                raise LifecycleError("uninstall recovery archive identity mismatch")
            recovery_stage = transaction / "recovery-stage"
            unpack_private_archive(recovery_archive, recovery_stage)
            assert_permission_context(recovery_stage, permission_context, original_permissions=False, same_objects=False)
            assert_private_tree(recovery_stage)
            if destination.exists():
                raise LifecycleError("uninstall recovery destination appeared")
            path_replacer(recovery_stage, destination)
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
            assert_permission_context(destination, permission_context, same_objects=False)
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
    remove_permission_snapshot(context_file)
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


def create_test_source(
    root,
    version,
    marker,
    files=LEGACY_PACKAGE_FILES,
    declare_files=False,
    include_package_sha256=True,
):
    source = root / f"source-{version}"
    package = source / "skills" / "work-charter"
    for relative in sorted(files):
        path = package / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{relative} {marker}\n", encoding="utf-8", newline="\n")
    file_hashes = {
        relative: sha256(package / relative) for relative in sorted(files)
    }
    package_record = {
        "file_count": len(files),
        "path": "skills/work-charter",
        "tree": git_tree_hash(package),
    }
    if include_package_sha256:
        package_record["sha256"] = candidate_package_digest(file_hashes)
    if declare_files:
        package_record["files"] = sorted(files)
    descriptor = {
        "package": package_record,
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


def self_test_inherited_permissions(root, legacy_source, other_legacy_source, current_source):
    if os.name != "nt":
        return "NOT_APPLICABLE"
    fixture = root / "fully-inherited"
    create_private_directory(fixture)
    policy = fixture / "policy"
    create_private_directory(policy)
    set_windows_dacl(policy, windows_private_descriptor(True) + "(A;OICI;0x1200a9;;;WD)")
    discovery = policy / "skills"
    discovery.mkdir()
    reset_windows_path_inheritance(discovery)
    destination = discovery / "work-charter"
    transactions = fixture / "transactions"
    create_private_directory(transactions)
    vault = fixture / "vault"
    create_private_directory(vault)
    transitions = [
        (legacy_source, "0.4.2"), (other_legacy_source, "0.4.3"),
        (current_source, SELF_TEST_SOURCE_VERSION), (legacy_source, "0.4.2"),
    ]
    current_tree = None
    model_observations = []
    move_observations = []

    def inspect_model(path, transaction, snapshot, digest):
        def restore_empty(probe, raw, identity):
            assert all(target.stat().st_size == 0 for target in probe.rglob("*") if target.is_file())
            assert_windows_private_object(raw)
            assert_private_tree(transaction / "stage") if (transaction / "stage").exists() else None
            model_observations.append(str(probe.relative_to(transaction)))
            return restore_permission_snapshot(probe, raw, identity)
        return preflight_permission_restore(path, transaction, snapshot, digest, restore_empty)

    def move_private(source_path, target_path):
        assert_private_tree(source_path)
        move_observations.append((Path(source_path).name, Path(target_path).name))
        os.replace(source_path, target_path)
        assert_private_tree(target_path)

    for index, (source, version) in enumerate(transitions):
        expected_tree = candidate_metadata(source, version)["package"]["tree"]
        before = None
        if current_tree:
            before_path = vault / f"before-{index}.acl"
            capture_permission_snapshot(destination, before_path)
            before = windows_dacl_snapshot_records(before_path)
            assert all("AI" in windows_dacl_control_flags(value)
                       and "P" not in windows_dacl_control_flags(value) for value in before.values())
        result = synchronize(
            "update" if current_tree else "install", source, destination, version, True,
            trusted_current_tree=current_tree, trusted_target_tree=expected_tree,
            transaction_root=transactions, path_replacer=move_private,
            permission_restore_preflight=inspect_model,
        )
        assert result["result"] == "MANAGED"
        current_tree = expected_tree
        after_path = vault / f"after-{index}.acl"
        capture_permission_snapshot(destination, after_path)
        after = windows_dacl_snapshot_records(after_path)
        assert all("AI" in windows_dacl_control_flags(value)
                   and "P" not in windows_dacl_control_flags(value) for value in after.values())
        if before:
            assert all(before[key] == after[key] for key in before.keys() & after.keys())
        assert not any(transactions.iterdir())
    assert len(model_observations) == 6 and len(move_observations) == 7

    snapshot = vault / "fault-baseline.acl"
    digest = capture_permission_snapshot(destination, snapshot)
    context = capture_permission_context(destination, snapshot, digest)
    original_setter = globals()["set_windows_dacl"]
    actual_writes = []

    def fail_partial_private(path, descriptor):
        path = Path(path)
        if path == destination or destination in path.parents:
            actual_writes.append(path)
            if len(actual_writes) == 2:
                raise OSError("simulated partial private DACL failure")
        return original_setter(path, descriptor)

    globals()["set_windows_dacl"] = fail_partial_private
    prior_moves = len(move_observations)
    try:
        try:
            synchronize(
                "update", other_legacy_source, destination, "0.4.3", True,
                trusted_current_tree=current_tree,
                trusted_target_tree=candidate_metadata(other_legacy_source, "0.4.3")["package"]["tree"],
                transaction_root=transactions, path_replacer=move_private,
            )
        except OSError as error:
            assert "partial private DACL failure" in str(error)
        else:
            raise AssertionError("partial private DACL failure was not surfaced")
    finally:
        globals()["set_windows_dacl"] = original_setter
    assert len(move_observations) == prior_moves and len(actual_writes) >= 2
    assert_permission_context(destination, context)
    assert not any(transactions.iterdir())

    # The same partial-ACL boundary also exists before an uninstall move.
    actual_writes.clear()
    globals()["set_windows_dacl"] = fail_partial_private
    try:
        try:
            uninstall(destination, True, trusted_tree=current_tree, transaction_root=transactions,
                      path_replacer=move_private)
        except OSError as error:
            assert "partial private DACL failure" in str(error)
        else:
            raise AssertionError("partial uninstall private DACL failure was not surfaced")
    finally:
        globals()["set_windows_dacl"] = original_setter
    assert len(move_observations) == prior_moves and len(actual_writes) >= 2
    assert_permission_context(destination, context)
    assert not any(transactions.iterdir())

    # Parent drift and unsupported writer policy fail before any target ACL or move.
    bad = windows_security(descriptor="D:P(A;OICI;FW;;;WD)")
    bad["owner"] = context["owner"]
    try:
        assert_windows_trusted_writers(destination, bad)
    except LifecycleError as error:
        assert "untrusted writer" in str(error)
    else:
        raise AssertionError("untrusted writer admission succeeded")
    bad_owner = dict(context["objects"][""]["security"], owner="S-1-1-0")
    try:
        assert_windows_trusted_writers(destination, bad_owner)
    except LifecycleError as error:
        assert "owner" in str(error)
    else:
        raise AssertionError("untrusted owner admission succeeded")
    try:
        windows_security(descriptor="D:NO_ACCESS_CONTROL")
    except LifecycleError as error:
        assert "NULL DACL" in str(error)
    else:
        raise AssertionError("NULL DACL admission succeeded")
    try:
        object_guid = "-".join("1" * width for width in (8, 4, 4, 4, 12))
        windows_security(descriptor=f"D:(OA;;FA;{object_guid};;WD)")
    except LifecycleError as error:
        assert "complex ACE" in str(error)
    else:
        raise AssertionError("complex DACL admission succeeded")
    drifted = dict(context["parent"], identity=[-1, -1])
    try:
        assert_parent_context(drifted)
    except LifecycleError as error:
        assert "drift" in str(error)
    else:
        raise AssertionError("parent identity drift was not refused")

    def count_actual_writes(path, descriptor):
        path = Path(path)
        if path == destination or destination in path.parents:
            actual_writes.append(path)
        return original_setter(path, descriptor)

    def refused_update():
        synchronize(
            "update", other_legacy_source, destination, "0.4.3", True,
            trusted_current_tree=current_tree,
            trusted_target_tree=candidate_metadata(other_legacy_source, "0.4.3")["package"]["tree"],
            transaction_root=transactions, path_replacer=move_private,
        )

    unsafe_parent = context["parent"]["security"]["dacl"] + "(A;OICI;FW;;;WD)"
    original_setter(discovery, unsafe_parent)
    actual_writes.clear()
    globals()["set_windows_dacl"] = count_actual_writes
    try:
        try:
            refused_update()
        except LifecycleError as error:
            assert "untrusted writer" in str(error)
        else:
            raise AssertionError("unsafe parent update was not refused")
    finally:
        globals()["set_windows_dacl"] = original_setter
        restore_windows_dacl_with_ai(discovery, context["parent"]["security"]["dacl"], snapshot)
    assert actual_writes == [] and len(move_observations) == prior_moves
    assert_permission_context(destination, context)
    assert not any(transactions.iterdir())

    alias = fixture / "hardlink-alias"
    alias.hardlink_to(destination / "SKILL.md")
    globals()["set_windows_dacl"] = count_actual_writes
    try:
        try:
            refused_update()
        except LifecycleError as error:
            assert "hard-linked" in str(error)
        else:
            raise AssertionError("hard-linked managed file was not refused")
    finally:
        globals()["set_windows_dacl"] = original_setter
        alias.unlink()
    assert actual_writes == [] and len(move_observations) == prior_moves
    assert_permission_context(destination, context)
    assert not any(transactions.iterdir())

    def partial_delete(path):
        assert_private_tree(path)
        assert_windows_private_object(path.parent / "uninstall-recovery.zip")
        (path / "SKILL.md").unlink()
        raise OSError("simulated inherited uninstall deletion failure")

    try:
        uninstall(destination, True, trusted_tree=current_tree, transaction_root=transactions,
                  tombstone_remover=partial_delete, path_replacer=move_private,
                  permission_restore_preflight=inspect_model)
    except LifecycleError as error:
        assert "managed destination was restored" in str(error)
    else:
        raise AssertionError("partial inherited uninstall failure was not surfaced")
    assert_permission_context(destination, context, same_objects=False)
    retained = list(transactions.iterdir())
    assert len(retained) == 1
    assert_private_tree(retained[0])
    shutil.rmtree(retained[0])
    uninstall(destination, True, trusted_tree=current_tree, transaction_root=transactions,
              path_replacer=move_private, permission_restore_preflight=inspect_model)
    assert not destination.exists() and not any(transactions.iterdir())
    return "PASS"


def self_test(source=None):
    candidate_tree = None
    if source is not None:
        metadata = candidate_metadata(source, SELF_TEST_SOURCE_VERSION)
        _package, _files, candidate_tree = package_files(
            source,
            metadata,
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
                expected = {
                    "PRESERVED_FROM_PREVIOUS_DESTINATION",
                    "PROJECTED_FROM_PREVIOUS_DESTINATION",
                }
            if isinstance(expected, set):
                assert result["destination_permissions"] in expected
            else:
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
        source_b = create_test_source(root, "0.4.2", "b")
        source_c = create_test_source(root, "0.4.3", "c")
        source_bad = create_test_source(root, "0.4.9", "bad")
        source_forged = create_test_source(root / "forged-source-root", "0.3.0", "forged")
        historical_v030 = candidate_metadata(source_a, "0.3.0")
        assert set(historical_v030["package"]) == {"file_count", "path", "tree"}
        source_legacy_without_digest = create_test_source(
            root / "legacy-without-digest-root",
            "0.4.4",
            "legacy-without-digest",
            include_package_sha256=False,
        )
        legacy_without_digest_metadata = candidate_metadata(
            source_legacy_without_digest,
            "0.4.4",
        )
        assert set(legacy_without_digest_metadata["package"]) == set(
            historical_v030["package"]
        )
        source_current_without_digest = create_test_source(
            root / "current-without-digest-root",
            "0.4.5",
            "current-without-digest",
            files=EXPECTED_FILES,
            declare_files=True,
            include_package_sha256=False,
        )
        current_without_digest_metadata = candidate_metadata(
            source_current_without_digest,
            "0.4.5",
        )
        try:
            package_files(
                source_current_without_digest,
                current_without_digest_metadata,
                current_without_digest_metadata["package"]["tree"],
            )
        except LifecycleError as error:
            assert "digest is required" in str(error)
        else:
            raise AssertionError("current package shape without a digest was not refused")
        source_invalid_digest = create_test_source(
            root / "invalid-digest-root",
            "0.4.6",
            "invalid-digest",
        )
        invalid_digest_metadata = candidate_metadata(source_invalid_digest, "0.4.6")
        invalid_digest_metadata["package"]["sha256"] = None
        try:
            package_files(
                source_invalid_digest,
                invalid_digest_metadata,
                invalid_digest_metadata["package"]["tree"],
            )
        except LifecycleError as error:
            assert "digest is invalid" in str(error)
        else:
            raise AssertionError("explicit invalid package digest was not refused")
        source_wrong_digest = create_test_source(
            root / "wrong-digest-root",
            "0.4.7",
            "wrong-digest",
        )
        wrong_digest_metadata = candidate_metadata(source_wrong_digest, "0.4.7")
        wrong_digest_metadata["package"]["sha256"] = "0" * 64
        try:
            package_files(
                source_wrong_digest,
                wrong_digest_metadata,
                wrong_digest_metadata["package"]["tree"],
            )
        except LifecycleError as error:
            assert "digest mismatch" in str(error)
        else:
            raise AssertionError("explicit wrong package digest was not refused")
        source_extra = create_test_source(
            root / "extra-source-root",
            "0.4.8",
            "extra",
            files=EXPECTED_FILES | {"assets/unexpected.txt"},
            declare_files=True,
        )
        try:
            candidate_metadata(source_extra, "0.4.8")
        except LifecycleError as error:
            assert "allowed package path set" in str(error)
        else:
            raise AssertionError("candidate-declared extra package file was not refused")
        source_missing = create_test_source(
            root / "missing-source-root",
            "0.4.10",
            "missing",
            files=EXPECTED_FILES,
            declare_files=True,
        )
        missing_metadata = candidate_metadata(source_missing, "0.4.10")
        (source_missing / "skills" / "work-charter" / "assets" / "role-models.default.yaml").unlink()
        try:
            package_files(
                source_missing,
                missing_metadata,
                missing_metadata["package"]["tree"],
            )
        except LifecycleError as error:
            assert "package path set mismatch" in str(error)
        else:
            raise AssertionError("candidate-declared missing package file was not refused")
        tree_a = candidate_metadata(source_a, SELF_TEST_SOURCE_VERSION)["package"]["tree"]
        tree_b = candidate_metadata(source_b, "0.4.2")["package"]["tree"]
        tree_c = candidate_metadata(source_c, "0.4.3")["package"]["tree"]
        tree_legacy_without_digest = legacy_without_digest_metadata["package"]["tree"]
        tree_bad = candidate_metadata(source_bad, "0.4.9")["package"]["tree"]
        tree_forged = candidate_metadata(source_forged, "0.3.0")["package"]["tree"]
        assert SELF_TEST_SOURCE_VERSION not in TRUSTED_PACKAGE_TREES
        assert "0.4.2" not in TRUSTED_PACKAGE_TREES
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

        legacy_without_digest_destination = (
            root / "legacy-without-digest" / "work-charter"
        )
        legacy_without_digest_dry_run = synchronize(
            "install",
            source_legacy_without_digest,
            legacy_without_digest_destination,
            "0.4.4",
            False,
            trusted_target_tree=tree_legacy_without_digest,
        )
        assert legacy_without_digest_dry_run["effect"] == "DRY_RUN"
        legacy_without_digest_result = synchronize(
            "install",
            source_legacy_without_digest,
            legacy_without_digest_destination,
            "0.4.4",
            True,
            trusted_target_tree=tree_legacy_without_digest,
            transaction_root=new_transaction_root("legacy-without-digest-install"),
        )
        assert_permission_handoff(legacy_without_digest_result)
        assert (
            current_state(
                legacy_without_digest_destination,
                tree_legacy_without_digest,
            )["version"]
            == "0.4.4"
        )
        uninstall(
            legacy_without_digest_destination,
            True,
            trusted_tree=tree_legacy_without_digest,
            transaction_root=new_transaction_root("legacy-without-digest-uninstall"),
        )
        assert current_state(legacy_without_digest_destination)["state"] == "ABSENT"

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
                "0.4.2",
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
        user_config = root / "user-config" / "role-models.yaml"
        user_config.parent.mkdir()
        user_config_bytes = (
            b"schema_version: 1\nroles:\n  executor:\n"
            b"    provider: example\n    model: custom\n"
        )
        user_config.write_bytes(user_config_bytes)
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
        assert user_config.read_bytes() == user_config_bytes
        receipt_path = destination / RECEIPT_NAME
        valid_receipt = receipt_path.read_text(encoding="utf-8")
        receipt_path.write_text('{"destination": null}\n', encoding="utf-8", newline="\n")
        assert current_state(destination, tree_a)["state"] == "DRIFTED"
        receipt_path.write_text(valid_receipt, encoding="utf-8", newline="\n")
        unsafe_receipt = json.loads(valid_receipt)
        unsafe_receipt["files"]["../outside"] = "0" * 64
        receipt_path.write_text(
            json.dumps(unsafe_receipt, sort_keys=True),
            encoding="utf-8",
            newline="\n",
        )
        unsafe_state = current_state(destination, tree_a)
        assert unsafe_state["state"] == "DRIFTED"
        assert "unsafe path" in unsafe_state["reason"]
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
            baseline_descriptors = tuple(baseline_records.values())
            assert any("P" in windows_dacl_control_flags(value) for value in baseline_descriptors)
            no_ai_records = []
            for relative, value in baseline_records.items():
                if "AI" in windows_dacl_control_flags(value):
                    value = value.replace("AI", "", 1)
                no_ai_records.append((relative, value))
            no_ai_snapshot = root / "dacl-without-ai.acl"
            write_dacl_records(no_ai_snapshot, no_ai_records)
            no_ai_digest = sha256(no_ai_snapshot)
            assert (
                restore_permission_snapshot(destination, no_ai_snapshot, no_ai_digest)
                == "PRESERVED_FROM_SNAPSHOT"
            )
            no_ai_readback = root / "dacl-without-ai-readback.acl"
            capture_permission_snapshot(destination, no_ai_readback)
            assert_windows_dacl_snapshot_match(no_ai_snapshot, no_ai_readback)
            assert (
                restore_permission_snapshot(
                    destination, baseline_snapshot, sha256(baseline_snapshot)
                )
                == "PRESERVED_FROM_SNAPSHOT"
            )
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
            for control_flag in ("P", "AI", "AR"):
                control_records = list(baseline_records.items())
                control_descriptor = control_records[0][1]
                control_flags = windows_dacl_control_flags(control_descriptor)
                if control_flag in control_flags:
                    changed_control = control_descriptor.replace(control_flag, "", 1)
                else:
                    changed_control = "D:" + control_flag + control_descriptor[2:]
                control_records[0] = (control_records[0][0], changed_control)
                changed_control_snapshot = root / f"dacl-changed-{control_flag}.acl"
                write_dacl_records(changed_control_snapshot, control_records)
                try:
                    assert_windows_dacl_snapshot_match(
                        baseline_snapshot, changed_control_snapshot
                    )
                except LifecycleError as error:
                    assert "descriptor mismatch" in str(error)
                else:
                    raise AssertionError(
                        f"changed DACL {control_flag} flag was not refused"
                    )
            escaped_snapshot = root / "dacl-escaped-path.acl"
            escaped_records = list(baseline_records.items())
            escaped_records[-1] = (
                "sibling\\outside",
                escaped_records[-1][1],
            )
            write_dacl_records(escaped_snapshot, escaped_records)
            try:
                restore_windows_dacl_records(destination, escaped_snapshot)
            except LifecycleError as error:
                assert "escapes the managed root" in str(error)
            else:
                raise AssertionError("escaped DACL snapshot path was not refused")
        update_moves = []

        def record_update_move(source_path, target_path):
            update_moves.append((Path(source_path), Path(target_path)))
            os.replace(source_path, target_path)

        update_transaction_root = new_transaction_root("update")
        update_result = synchronize(
            "update",
            source_b,
            destination,
            "0.4.2",
            True,
            trusted_current_tree=tree_a,
            trusted_target_tree=tree_b,
            transaction_root=update_transaction_root,
            path_replacer=record_update_move,
        )
        assert_permission_handoff(update_result)
        assert current_state(destination, tree_b)["version"] == "0.4.2"
        assert len(update_moves) == 2
        assert update_moves[0][0] == destination
        assert update_transaction_root in update_moves[0][1].parents
        assert update_transaction_root in update_moves[1][0].parents
        assert update_moves[1][1] == destination
        if os.name == "nt":
            after_update = root / "dacl-after-update.acl"
            saved_dacl(destination, after_update.name)
            after_update_records = windows_dacl_snapshot_records(after_update)
            original_records = windows_dacl_snapshot_records(
                root / "dacl-before-update.acl"
            )
            for key in original_records.keys() & after_update_records.keys():
                assert original_records[key] == after_update_records[key]
            assert windows_snapshot_key(destination.name, "assets/role-models.default.yaml") not in after_update_records

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
            after_rollback = root / "dacl-after-rollback.acl"
            original_dacl = saved_dacl(destination, after_rollback.name)
            after_rollback_records = windows_dacl_snapshot_records(after_rollback)
            original_records = windows_dacl_snapshot_records(
                root / "dacl-before-update.acl"
            )
            for key in original_records.keys() & after_rollback_records.keys():
                assert original_records[key] == after_rollback_records[key]
            added_descriptor = after_rollback_records[
                windows_snapshot_key(destination.name, "assets/role-models.default.yaml")
            ]
            added_flags = windows_dacl_control_flags(added_descriptor)
            assert "AI" in added_flags and "P" not in added_flags
            baseline_snapshot = after_rollback
            baseline_digest = sha256(baseline_snapshot)
        assert user_config.read_bytes() == user_config_bytes

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
                "0.4.2",
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
                "0.4.2",
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
                "0.4.2",
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
            def noop_dacl_restore(_path, _snapshot):
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
                    descriptor_writer=noop_dacl_restore,
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
                    descriptor_writer=noop_dacl_restore,
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
                    "0.4.2",
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

                    def restore_and_corrupt(path, snapshot):
                        restore_windows_dacl_records(path, snapshot)
                        run_windows_acl(
                            target,
                            ["/grant:r", "*S-1-1-0:(OI)(CI)(R)", "/Q"],
                            "self-test post-restore DACL mismatch",
                        )

                    return restore_permission_snapshot(
                        target,
                        snapshot,
                        digest,
                        descriptor_writer=restore_and_corrupt,
                    )
                return restore_permission_snapshot(target, snapshot, digest)

            try:
                synchronize(
                    "update",
                    source_b,
                    destination,
                    "0.4.2",
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

                def restore_and_corrupt(path, snapshot):
                    restore_windows_dacl_records(path, snapshot)
                    run_windows_acl(
                        target,
                        ["/grant:r", "*S-1-1-0:(OI)(CI)(R)", "/Q"],
                        "self-test persistent post-restore DACL mismatch",
                    )

                return restore_permission_snapshot(
                    target,
                    snapshot,
                    digest,
                    descriptor_writer=restore_and_corrupt,
                )

            try:
                synchronize(
                    "update",
                    source_b,
                    destination,
                    "0.4.2",
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
                "0.4.2",
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
                "0.4.2",
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
                "0.4.2",
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
                "0.4.2",
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
                    "0.4.2",
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
                    "0.4.2",
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
                "0.4.2",
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
                "0.4.2",
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
            "0.4.3",
            True,
            backup_remover=fail_backup_cleanup,
            trusted_current_tree=tree_a,
            trusted_target_tree=tree_c,
            transaction_root=cleanup_transaction_root,
        )
        assert cleanup_result["result"] == "MANAGED_WITH_BACKUP"
        assert current_state(destination, tree_c)["version"] == "0.4.3"
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
        assert user_config.read_bytes() == user_config_bytes
        inherited_permissions = self_test_inherited_permissions(root, source_b, source_c, source_a)
    return {
        "result": "PASS",
        "scope": (
            "disposable legacy-apply-compatibility/external-transaction "
            "install/update/rollback/failure-recovery/"
            "legacy-five-file/current-six-file-transition/external-user-config-invariance/"
            "legacy-candidate-digest-omission/strict-declared-digest-validation/"
            "Windows-DACL-control-aware-path-restore-and-semantic-readback/"
            "private-backup-tombstone/path-volume-guards/drift/receipt-integrity/"
            "unreceipted/wrong-tree/uninstall"
        ),
        "persistent_effect": False,
        "source_package_tree": candidate_tree,
        "destination_permission_handoff": (
            "PRESERVED_OR_INHERITED_BY_ACTION" if os.name == "nt" else "PLATFORM_DEFAULT"
        ),
        "permission_handoff_failure_recovery": "PASS",
        "legacy_candidate_digest_omission_compatibility": "PASS",
        "strict_declared_candidate_digest_validation": "PASS",
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
        "windows_dacl_ai_control_preservation": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "windows_dacl_no_ai_control_preservation": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "windows_dacl_control_flag_drift_refusal": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "windows_dacl_snapshot_path_escape_refusal": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "windows_restrictive_dacl_preservation": (
            "PASS" if os.name == "nt" else "NOT_APPLICABLE"
        ),
        "windows_fully_inherited_shape_transitions": inherited_permissions,
        "windows_empty_model_private_material": inherited_permissions,
        "windows_private_before_move_and_partial_handoff_restore": inherited_permissions,
        "windows_inherited_uninstall_private_archive_recovery": inherited_permissions,
        "windows_owner_writer_parent_context_admission": inherited_permissions,
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
