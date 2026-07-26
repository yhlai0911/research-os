#!/usr/bin/env python3
"""Transactionally install catalogued Research OS skills without overwrite."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
CATALOG = yaml.safe_load((ROOT / "skills" / "catalog.yaml").read_text())
MARKER_NAME = ".research-os-install.json"


def tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode())
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def git_value(*args: str, fallback: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return fallback


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def marker_is_managed(marker: Path) -> bool:
    try:
        payload = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return payload.get("managed_by") == "research-os" and isinstance(
        payload.get("skills"), dict
    )


def main() -> int:
    args = parse_args()
    target = args.target.resolve()
    marker = target / MARKER_NAME
    receipt: dict[str, object] = {
        "managed_by": "research-os",
        "catalog_version": CATALOG["version"],
        "source_commit": git_value("rev-parse", "HEAD", fallback="uncommitted"),
        "source_dirty": bool(git_value("status", "--porcelain", fallback="unknown")),
        "target": str(target),
        "mode": args.mode,
        "planned": [],
        "created": [],
        "unchanged": [],
        "conflicts": [],
        "skills": {},
    }
    pending: list[tuple[Path, Path]] = []
    for skill in CATALOG["skills"]:
        source = ROOT / "skills" / skill["bucket"] / skill["name"]
        destination = target / skill["name"]
        source_hash = tree_hash(source)
        receipt["skills"][skill["name"]] = source_hash
        if destination.is_symlink():
            if destination.resolve() == source.resolve() and args.mode == "symlink":
                receipt["unchanged"].append(str(destination))
            else:
                receipt["conflicts"].append(str(destination))
            continue
        if destination.exists():
            if (
                args.mode == "copy"
                and destination.is_dir()
                and tree_hash(destination) == source_hash
            ):
                receipt["unchanged"].append(str(destination))
            else:
                receipt["conflicts"].append(str(destination))
            continue
        pending.append((source, destination))
        receipt["planned"].append(str(destination))

    if marker.exists() and not marker_is_managed(marker):
        receipt["conflicts"].append(str(marker))

    if receipt["conflicts"]:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    if args.dry_run:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if not pending and marker.is_file():
        receipt["marker"] = "preserved"
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".research-os-stage-", dir=target.parent))
    staged: list[tuple[Path, Path]] = []
    promoted: list[tuple[Path, Path]] = []
    try:
        for source, destination in pending:
            staged_path = stage / source.name
            if args.mode == "copy":
                shutil.copytree(source, staged_path)
                if tree_hash(staged_path) != tree_hash(source):
                    raise RuntimeError(f"staged tree hash mismatch: {source.name}")
            else:
                staged_path.symlink_to(source, target_is_directory=True)
                if staged_path.resolve() != source.resolve():
                    raise RuntimeError(f"staged symlink mismatch: {source.name}")
            staged.append((staged_path, destination))

        target.mkdir(parents=True, exist_ok=True)
        for staged_path, destination in staged:
            os.replace(staged_path, destination)
            promoted.append((destination, staged_path))
            receipt["created"].append(str(destination))

        final_marker = {
            **receipt,
            "installed_at": datetime.now(UTC).isoformat(),
            "planned": [],
        }
        marker_temp = target / f".{MARKER_NAME}.{os.getpid()}.tmp"
        marker_temp.write_text(
            json.dumps(final_marker, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        os.replace(marker_temp, marker)
        receipt["marker"] = str(marker)
    except Exception as exc:
        rollback_errors: list[str] = []
        for destination, staged_path in reversed(promoted):
            try:
                os.replace(destination, staged_path)
            except OSError as rollback_error:
                rollback_errors.append(f"{destination}: {rollback_error}")
        receipt["created"] = []
        receipt["failure"] = str(exc)
        receipt["rollback_errors"] = rollback_errors
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return 3
    finally:
        shutil.rmtree(stage, ignore_errors=True)

    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
