#!/usr/bin/env python3
"""Build and verify a deterministic Research OS ZIP and release receipt."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent

# Git's tracked inventory includes ignored files. Reject credential-like names
# before filtering artifacts, including credentials force-added under dist/.
# This is a filename guard, not a substitute for a repository secret scanner.
SECRET_PATTERNS = (
    ".env",
    ".env.*",
    ".netrc",
    ".npmrc",
    ".pypirc",
    "*.pem",
    "*.key",
    "*_rsa",
    "*_dsa",
    "*_ecdsa",
    "*_ed25519",
    "*.p12",
    "*.pfx",
    "credentials*.json",
    "service-account*.json",
    "service_account*.json",
)
SECRET_DIRECTORIES = {".aws", ".azure", ".gnupg", ".kube", ".ssh"}
ARTIFACT_DIRECTORIES = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".scratch", "dist", "build", "renders", "node_modules",
}
ARTIFACT_PATTERNS = (
    ".ds_store", "*.pyc", "*.pyo", "*.bak", "*.tmp", "*~", ".coverage",
    ".coverage.*", "release-receipt.json", "research-os-*.zip",
    "research-os-*.zip.sha256",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write_text(path: Path, content: str) -> None:
    """Do not follow a pre-existing symlink at a predictable temporary name."""
    descriptor, name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def source_files() -> list[Path]:
    """Select tracked regular sources, never ignored or generated artifacts.

    Apply repository .gitignore rules explicitly even to tracked paths. Do not
    use --exclude-standard: user/global Git excludes must not change a release.
    Symlinks, submodules, conflicts and missing sources fail closed rather than
    silently changing the source inventory or following files outside ROOT.
    """
    tracked = []
    for entry in git_output("ls-files", "--stage", "-z").split("\0"):
        if not entry:
            continue
        metadata, name = entry.split("\t", 1)
        mode, _object_id, stage = metadata.split()
        validate_relative_path(name)
        if mode not in {"100644", "100755"} or stage != "0":
            raise RuntimeError(
                f"refusing non-regular or unmerged tracked source: {name}"
            )
        tracked.append(ROOT / name)
    reject_secrets(tracked)
    ignored = set(
        git_output(
            "ls-files", "--cached", "--ignored",
            "--exclude-per-directory=.gitignore", "-z",
        ).split("\0")
    )
    result = []
    for path in tracked:
        name = path.relative_to(ROOT).as_posix()
        parts = tuple(part.casefold() for part in path.relative_to(ROOT).parts)
        if name in ignored or any(part in ARTIFACT_DIRECTORIES for part in parts[:-1]):
            continue
        if any(fnmatch.fnmatchcase(parts[-1], pattern) for pattern in ARTIFACT_PATTERNS):
            continue
        validate_source_file(path)
        result.append(path)
    if not result:
        raise RuntimeError("refusing to package an empty source inventory")
    return sorted(result, key=lambda item: item.relative_to(ROOT).as_posix())


def validate_relative_path(name: str) -> None:
    """Keep ZIP names portable and the line-oriented manifest unambiguous."""
    if (
        not name
        or name.startswith("/")
        or "\\" in name
        or ":" in name
        or any(part in {"", ".", ".."} for part in name.split("/"))
        or any(ord(char) < 32 or ord(char) == 127 for char in name)
        or name == "MANIFEST.sha256"
    ):
        raise RuntimeError(f"refusing unsafe or reserved source path: {name!r}")


def validate_source_file(path: Path) -> None:
    """Use lstat so neither a file nor any parent can be a symlink."""
    relative = path.relative_to(ROOT)
    current = ROOT
    for index, part in enumerate(relative.parts):
        current /= part
        try:
            mode = current.lstat().st_mode
        except OSError as exc:
            raise RuntimeError(f"missing or unreadable tracked source: {relative}") from exc
        expected_type = stat.S_ISREG if index == len(relative.parts) - 1 else stat.S_ISDIR
        if not expected_type(mode):
            raise RuntimeError(f"refusing symlink or non-regular source: {relative}")


def read_source_file(path: Path) -> tuple[bytes, int]:
    """Read without following symlinks, including parent-directory replacements.

    Release builds require descriptor-relative, no-follow filesystem access.
    Fail closed on platforms without it instead of silently weakening safety.
    """
    relative = path.relative_to(ROOT)
    validate_relative_path(relative.as_posix())
    if os.open not in os.supports_dir_fd or not all(
        hasattr(os, flag) for flag in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK")
    ):
        raise RuntimeError(
            "safe release reads require descriptor-relative O_NOFOLLOW support"
        )
    directory_fd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in relative.parts[:-1]:
            next_fd = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd
            )
            os.close(directory_fd)
            directory_fd = next_fd
        file_fd = os.open(
            relative.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory_fd
        )
        with os.fdopen(file_fd, "rb") as handle:
            file_stat = os.fstat(handle.fileno())
            if not stat.S_ISREG(file_stat.st_mode):
                raise RuntimeError(f"refusing non-regular source: {relative}")
            return handle.read(), file_stat.st_mode
    except OSError as exc:
        raise RuntimeError(f"cannot safely read tracked source: {relative}") from exc
    finally:
        os.close(directory_fd)


def reject_secrets(files: list[Path]) -> None:
    offenders = sorted(
        path.relative_to(ROOT).as_posix()
        for path in files
        if any(
            fnmatch.fnmatchcase(part.casefold(), pattern)
            for part in path.relative_to(ROOT).parts
            for pattern in SECRET_PATTERNS
        )
        or any(
            part.casefold() in SECRET_DIRECTORIES
            for part in path.relative_to(ROOT).parts
        )
    )
    if offenders:
        raise RuntimeError(
            "refusing to package files that look like credentials: "
            + ", ".join(offenders)
        )


def source_tree_hash(files: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(read_source_file(path)[0])
        digest.update(b"\0")
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--allow-dirty", action="store_true")
    return parser.parse_args()


def git_output(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True
    ).rstrip("\n")


def run_release_gates() -> None:
    commands = (
        [sys.executable, str(ROOT / "scripts" / "sync_catalog.py"), "--check"],
        [sys.executable, str(ROOT / "scripts" / "validate_repository.py")],
        [sys.executable, "-m", "pytest", "-q"],
    )
    for command in commands:
        subprocess.run(command, cwd=ROOT, check=True)


def verify_archive(
    archive: Path, prefix: str, expected_paths: list[str]
) -> dict[str, object]:
    with zipfile.ZipFile(archive) as bundle:
        bad_member = bundle.testzip()
        if bad_member:
            raise RuntimeError(f"archive CRC failure: {bad_member}")
        manifest_name = f"{prefix}/MANIFEST.sha256"
        manifest_text = bundle.read(manifest_name).decode("utf-8")
        parsed: dict[str, str] = {}
        for line in manifest_text.splitlines():
            digest, relative = line.split("  ", 1)
            if relative in parsed:
                raise RuntimeError(f"duplicate manifest entry: {relative}")
            parsed[relative] = digest
        if sorted(parsed) != sorted(expected_paths):
            raise RuntimeError("archive manifest paths differ from source inventory")
        for relative, expected_digest in parsed.items():
            actual_digest = sha256(bundle.read(f"{prefix}/{relative}"))
            if actual_digest != expected_digest:
                raise RuntimeError(f"archive hash mismatch: {relative}")
        expected_members = {f"{prefix}/{path}" for path in expected_paths}
        expected_members.add(manifest_name)
        if (
            len(bundle.namelist()) != len(expected_members)
            or set(bundle.namelist()) != expected_members
        ):
            raise RuntimeError("archive member inventory differs from manifest")
    return {
        "archive_readback": "verified",
        "manifest_entries": len(expected_paths),
    }


def main() -> int:
    args = parse_args()
    run_release_gates()

    dirty_porcelain = git_output("status", "--porcelain")
    dirty = bool(dirty_porcelain)
    if dirty and not args.allow_dirty:
        print("Refusing to package a dirty source tree.", file=sys.stderr)
        return 2

    source_commit = git_output("rev-parse", "HEAD")
    tracked_status = git_output("status", "--porcelain", "--untracked-files=no")
    files = source_files()
    catalog_path = ROOT / "skills" / "catalog.yaml"
    if catalog_path not in files:
        raise RuntimeError("release inventory must contain skills/catalog.yaml")
    catalog = yaml.safe_load(read_source_file(catalog_path)[0])
    version = catalog["version"]
    if not isinstance(version, str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]*", version
    ):
        raise RuntimeError("catalog version is not a safe release filename")
    prefix = f"research-os-{version}"
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{prefix}.zip"
    archive_fd, archive_name = tempfile.mkstemp(
        dir=output_dir, prefix=f".{prefix}.", suffix=".tmp"
    )
    archive_temp = Path(archive_name)
    relative_paths = [path.relative_to(ROOT).as_posix() for path in files]
    manifest_lines = []
    tree_digest = hashlib.sha256()

    try:
        with (
            os.fdopen(archive_fd, "w+b") as archive_handle,
            zipfile.ZipFile(
                archive_handle, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
            ) as bundle,
        ):
            for path, relative in zip(files, relative_paths, strict=True):
                data, source_mode = read_source_file(path)
                manifest_lines.append(f"{sha256(data)}  {relative}")
                tree_digest.update(relative.encode() + b"\0" + data + b"\0")
                info = zipfile.ZipInfo(
                    f"{prefix}/{relative}", (1980, 1, 1, 0, 0, 0)
                )
                mode = 0o755 if source_mode & 0o111 else 0o644
                info.external_attr = mode << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(info, data)
            manifest = ("\n".join(manifest_lines) + "\n").encode()
            info = zipfile.ZipInfo(
                f"{prefix}/MANIFEST.sha256", (1980, 1, 1, 0, 0, 0)
            )
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, manifest)

        verification = verify_archive(archive_temp, prefix, relative_paths)
        if (
            git_output("rev-parse", "HEAD") != source_commit
            or git_output("status", "--porcelain", "--untracked-files=no") != tracked_status
            or source_tree_hash(files) != tree_digest.hexdigest()
        ):
            raise RuntimeError("source tree changed while building the release")
        os.replace(archive_temp, archive)
    finally:
        if archive_temp.exists():
            archive_temp.unlink()

    archive_hash = sha256(archive.read_bytes())
    sidecar = archive.with_suffix(".zip.sha256")
    atomic_write_text(sidecar, f"{archive_hash}  {archive.name}\n")

    receipt = {
        "archive": str(archive),
        "archive_sha256": archive_hash,
        "archive_readback": verification["archive_readback"],
        "catalog_version": version,
        "file_count": len(files),
        "gates": [
            "sync_catalog --check",
            "validate_repository",
            "pytest",
            "archive manifest readback",
        ],
        "manifest_entries": verification["manifest_entries"],
        "source_commit": source_commit,
        "source_dirty": dirty,
        "source_tree_sha256": tree_digest.hexdigest(),
        "version": version,
    }
    if dirty:
        receipt["dirty_status_sha256"] = sha256(dirty_porcelain.encode())
    receipt_path = output_dir / "release-receipt.json"
    atomic_write_text(receipt_path, json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
