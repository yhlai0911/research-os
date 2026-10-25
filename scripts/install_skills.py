#!/usr/bin/env python3
"""Transactionally install Research OS skills for supported agent harnesses."""

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

try:
    from .skill_links import dependency_errors, rebase_markdown
except ImportError:
    from skill_links import dependency_errors, rebase_markdown


ROOT = Path(__file__).resolve().parent.parent
CATALOG = yaml.safe_load((ROOT / "skills" / "catalog.yaml").read_text())
MARKER_NAME = ".research-os-install.json"
HARNESSES = ("codex", "claude-code")
PROFILES = ("core", "finance-social-science")


def profile_settings(profile: str) -> tuple[dict[str, object], Path, str]:
    """Keep optional inventories and receipts separate from the core install."""
    if profile == "core":
        return CATALOG, ROOT / "skills", MARKER_NAME
    if profile not in PROFILES:
        raise ValueError(f"unsupported profile: {profile}")
    profile_root = ROOT / "profiles" / profile
    try:
        catalog = yaml.safe_load(
            (profile_root / "catalog.yaml").read_text(encoding="utf-8")
        )
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read profile {profile!r} catalog: {exc}") from exc
    if not isinstance(catalog, dict):
        raise ValueError(f"profile {profile!r} catalog must be a mapping")
    if catalog.get("requires_core") != CATALOG["version"]:
        raise ValueError(
            f"profile {profile!r} requires core {catalog.get('requires_core')!r}; "
            f"this checkout provides {CATALOG['version']!r}"
        )
    return catalog, profile_root / "skills", f".research-os-{profile}-install.json"


def default_skills_dir(harness: str) -> Path:
    """Resolve the personal skills directory for a supported agent harness."""
    if harness == "codex":
        codex_home = os.environ.get("CODEX_HOME")
        if codex_home:
            return Path(codex_home).expanduser() / "skills"
        return Path.home() / ".codex" / "skills"
    if harness == "claude-code":
        return Path.home() / ".claude" / "skills"
    raise ValueError(f"unsupported harness: {harness}")


def adapt_skill_markdown(text: str, invocation: str, harness: str) -> str:
    """Generate harness-specific invocation metadata without editing source skills."""
    if harness == "codex":
        return text
    if harness != "claude-code":
        raise ValueError(f"unsupported harness: {harness}")
    # Git for Windows may check out CRLF. Adapt semantic frontmatter while
    # preserving Codex's byte-identical path above and the source file itself.
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md is missing YAML frontmatter")
    frontmatter_end = text.find("\n---\n", 4)
    if frontmatter_end < 0:
        raise ValueError("SKILL.md has unterminated YAML frontmatter")
    field = (
        "disable-model-invocation: true"
        if invocation == "user"
        else "user-invocable: false"
    )
    return text[:frontmatter_end] + f"\n{field}" + text[frontmatter_end:]


def tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode())
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def packaged_roots() -> list[Path]:
    roots = [ROOT / 'skills' / skill['bucket'] / skill['name'] for skill in CATALOG['skills']]
    for profile in PROFILES:
        if profile == 'core':
            continue
        try:
            catalog, skills, _marker = profile_settings(profile)
        except ValueError:
            continue  # Unselected optional profiles cannot block core.
        roots.extend(skills / skill['bucket'] / skill['name'] for skill in catalog['skills'])
    return roots


def installed_payload(item: Path, source: Path, invocation: str, harness: str) -> bytes:
    payload = item.read_bytes()
    if item.suffix.lower() == '.md':
        text = payload.decode('utf-8')
        if item.relative_to(source).as_posix() == 'SKILL.md':
            text = adapt_skill_markdown(text, invocation, harness)
        text = rebase_markdown(text, item, packaged_roots())
        payload = text.encode('utf-8')
    return payload


def expected_tree_hash(path: Path, invocation: str, harness: str, mode: str = 'copy') -> str:
    if mode == 'symlink':
        return tree_hash(path)
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        relative = item.relative_to(path).as_posix()
        payload = installed_payload(item, path, invocation, harness)
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(payload)
        digest.update(b"\0")
    return digest.hexdigest()


def materialize_skill(
    source: Path, destination: Path, invocation: str, harness: str
) -> None:
    shutil.copytree(source, destination)
    for item in source.rglob('*.md'):
        (destination / item.relative_to(source)).write_bytes(
            installed_payload(item, source, invocation, harness)
        )


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
    parser = argparse.ArgumentParser(
        description="Install a catalogued Research OS profile into an agent harness."
    )
    parser.add_argument(
        "--target",
        type=Path,
        help=(
            "skills directory (default: Codex $CODEX_HOME/skills or ~/.codex/skills; "
            "Claude Code ~/.claude/skills)"
        ),
    )
    parser.add_argument("--harness", choices=HARNESSES, default="codex")
    parser.add_argument("--profile", choices=PROFILES, default="core")
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.harness == "claude-code" and args.mode == "symlink":
        parser.error("Claude Code installation requires copy mode for generated metadata")
    return args


def read_managed_marker(marker: Path) -> dict[str, object] | None:
    try:
        payload = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        not isinstance(payload, dict)
        or payload.get("managed_by") != "research-os"
        or not isinstance(payload.get("skills"), dict)
    ):
        return None
    return payload


def main() -> int:
    args = parse_args()
    target = (args.target or default_skills_dir(args.harness)).expanduser().resolve()
    try:
        catalog, skills_root, marker_name = profile_settings(args.profile)
    except ValueError as exc:
        print(json.dumps({"profile": args.profile, "failure": str(exc), "created": []}))
        return 2
    marker = target / marker_name
    receipt: dict[str, object] = {
        "managed_by": "research-os",
        "receipt_schema": 2,
        "content_adapter": "flat-markdown-links-v1",
        "harness": args.harness,
        "catalog_version": catalog["version"],
        "source_commit": git_value("rev-parse", "HEAD", fallback="uncommitted"),
        "source_dirty": bool(git_value("status", "--porcelain", fallback="unknown")),
        "target": str(target),
        "mode": args.mode,
        "planned": [],
        "created": [],
        "unchanged": [],
        "conflicts": [],
        "skills": {},
        "source_skills": {},
    }
    if args.profile != "core":
        # Import lazily because the verifier also uses the shared hash/adapter helpers.
        from verify_install import verify_install

        receipt["profile"] = args.profile
        prerequisite_errors = verify_install(target, args.harness)
        if prerequisite_errors:
            receipt["failure"] = (
                f"profile {args.profile!r} requires a verified core installation "
                f"for {args.harness!r} at {target}"
            )
            receipt["prerequisite_errors"] = prerequisite_errors
            print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
            return 2

    pending: list[tuple[Path, Path, str, str]] = []
    roots = packaged_roots()
    source_errors = []
    for skill in catalog['skills']:
        source_errors.extend(dependency_errors(skills_root / skill['bucket'] / skill['name'], roots))
    if source_errors:
        receipt['failure'] = 'source dependency validation failed'
        receipt['dependency_errors'] = source_errors
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return 2
    for skill in catalog["skills"]:
        source = skills_root / skill["bucket"] / skill["name"]
        destination = target / skill["name"]
        source_hash = tree_hash(source)
        installed_hash = expected_tree_hash(
            source, skill["invocation"], args.harness, args.mode
        )
        receipt["source_skills"][skill["name"]] = source_hash
        receipt["skills"][skill["name"]] = installed_hash
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
                and tree_hash(destination) == installed_hash
            ):
                receipt["unchanged"].append(str(destination))
            else:
                receipt["conflicts"].append(str(destination))
            continue
        pending.append(
            (source, destination, skill["invocation"], installed_hash)
        )
        receipt["planned"].append(str(destination))

    existing_marker = read_managed_marker(marker) if marker.exists() else None
    if marker.exists() and existing_marker is None:
        receipt["conflicts"].append(str(marker))
    elif existing_marker is not None:
        existing_harness = existing_marker.get("harness", "codex")
        if (
            existing_harness != args.harness
            or existing_marker.get("profile", "core") != args.profile
        ):
            receipt["conflicts"].append(str(marker))

    if receipt["conflicts"]:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    if args.dry_run:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    marker_is_current = (
        existing_marker is not None
        and existing_marker.get("catalog_version") == receipt["catalog_version"]
        and existing_marker.get("source_commit") == receipt["source_commit"]
        and existing_marker.get("harness", "codex") == args.harness
        and existing_marker.get("profile", "core") == args.profile
        and existing_marker.get("skills") == receipt["skills"]
    )
    if not pending and marker_is_current:
        receipt["marker"] = "preserved"
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".research-os-stage-", dir=target.parent))
    staged: list[tuple[Path, Path]] = []
    promoted: list[tuple[Path, Path]] = []
    try:
        for source, destination, invocation, installed_hash in pending:
            staged_path = stage / source.name
            if args.mode == "copy":
                materialize_skill(source, staged_path, invocation, args.harness)
                if tree_hash(staged_path) != installed_hash:
                    raise RuntimeError(f"staged tree hash mismatch: {source.name}")
            else:
                staged_path.symlink_to(source, target_is_directory=True)
                if staged_path.resolve() != source.resolve():
                    raise RuntimeError(f"staged symlink mismatch: {source.name}")
            staged.append((staged_path, destination))

        # Cross-skill links resolve across the entire staged view, including
        # a previously verified core when an optional profile is added.
        for staged_path, _destination in staged:
            allowed = [stage, target] + (roots if args.mode == 'symlink' else [])
            errors = dependency_errors(staged_path, allowed, fallback=(stage, target))
            if errors:
                raise RuntimeError('staged dependency validation failed: ' + '; '.join(errors))

        target.mkdir(parents=True, exist_ok=True)
        for staged_path, destination in staged:
            os.replace(staged_path, destination)
            promoted.append((destination, staged_path))
            receipt["created"].append(str(destination))

        for source, destination, _invocation, installed_hash in pending:
            if not destination.is_dir() or tree_hash(destination) != installed_hash:
                raise RuntimeError(f"installed tree hash mismatch: {source.name}")

        final_marker = {
            **receipt,
            "installed_at": datetime.now(UTC).isoformat(),
            "planned": [],
        }
        marker_temp = target / f".{marker_name}.{os.getpid()}.tmp"
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
