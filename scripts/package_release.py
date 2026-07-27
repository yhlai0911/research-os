#!/usr/bin/env python3
"""Build and verify a deterministic Research OS ZIP and release receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent

# Names that must never enter a release even if something tracks them by
# mistake. This is a second line of defence: git ls-files already excludes
# ignored files, but a credential leaking into a distributed archive is not
# recoverable, so the check is cheap insurance rather than redundant.
SECRET_PATTERNS = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*_rsa",
    "*_ed25519",
    "*.p12",
    "*.pfx",
    "credentials.json",
    "service-account*.json",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_files() -> list[Path]:
    """Package exactly what is under version control.

    Walking the filesystem and subtracting a hardcoded exclusion list is not
    safe: it shipped .env, *.wav.bak and renders/ into a build. `git ls-files`
    honours .gitignore by construction, and it is the only inventory that is
    actually consistent with the source_commit recorded in the receipt.
    """
    listed = git_output("ls-files", "-z").split("\0")
    result = []
    for name in listed:
        if not name:
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        if path.name == ".DS_Store" or path.suffix == ".pyc":
            continue
        result.append(path)
    return sorted(result, key=lambda item: item.relative_to(ROOT).as_posix())


def reject_secrets(files: list[Path]) -> None:
    offenders = sorted(
        path.relative_to(ROOT).as_posix()
        for path in files
        if any(path.match(pattern) for pattern in SECRET_PATTERNS)
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
        digest.update(path.read_bytes())
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
    ).strip()


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
        if set(bundle.namelist()) != expected_members:
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

    catalog = yaml.safe_load((ROOT / "skills" / "catalog.yaml").read_text())
    version = catalog["version"]
    prefix = f"research-os-{version}"
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{prefix}.zip"
    archive_temp = output_dir / f".{prefix}.{os.getpid()}.tmp"
    files = source_files()
    reject_secrets(files)
    relative_paths = [path.relative_to(ROOT).as_posix() for path in files]
    manifest_lines = []

    try:
        with zipfile.ZipFile(
            archive_temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as bundle:
            for path, relative in zip(files, relative_paths, strict=True):
                data = path.read_bytes()
                manifest_lines.append(f"{sha256(data)}  {relative}")
                info = zipfile.ZipInfo(
                    f"{prefix}/{relative}", (1980, 1, 1, 0, 0, 0)
                )
                mode = 0o755 if path.stat().st_mode & 0o111 else 0o644
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
        os.replace(archive_temp, archive)
    finally:
        if archive_temp.exists():
            archive_temp.unlink()

    archive_hash = sha256(archive.read_bytes())
    sidecar = archive.with_suffix(".zip.sha256")
    sidecar_temp = sidecar.with_name(f".{sidecar.name}.{os.getpid()}.tmp")
    sidecar_temp.write_text(f"{archive_hash}  {archive.name}\n", encoding="utf-8")
    os.replace(sidecar_temp, sidecar)

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
        "source_commit": git_output("rev-parse", "HEAD"),
        "source_dirty": dirty,
        "source_tree_sha256": source_tree_hash(files),
        "version": version,
    }
    if dirty:
        receipt["dirty_status_sha256"] = sha256(dirty_porcelain.encode())
    receipt_path = output_dir / "release-receipt.json"
    receipt_temp = output_dir / f".release-receipt.{os.getpid()}.tmp"
    receipt_temp.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(receipt_temp, receipt_path)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
