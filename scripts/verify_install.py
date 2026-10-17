#!/usr/bin/env python3
"""Verify a complete catalog-driven Research OS harness installation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from install_skills import (
    HARNESSES,
    PROFILES,
    default_skills_dir,
    expected_tree_hash,
    profile_settings,
    tree_hash,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a catalogued Research OS profile for an agent harness."
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
    return parser.parse_args()


def skill_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    loaded = yaml.safe_load(text[4:end])
    return loaded if isinstance(loaded, dict) else {}


def verify_install(target: Path, harness: str, profile: str = "core") -> list[str]:
    errors: list[str] = []
    target = target.expanduser().resolve()
    try:
        catalog, skills_root, marker_name = profile_settings(profile)
    except ValueError as exc:
        return [str(exc)]
    if profile != "core":
        errors.extend(
            f"core prerequisite: {error}" for error in verify_install(target, harness)
        )
    marker_path = target / marker_name
    marker: dict[str, object] = {}

    try:
        loaded = json.loads(marker_path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            errors.append(f"{marker_path}: receipt root must be an object")
        else:
            marker = loaded
    except FileNotFoundError:
        errors.append(f"{marker_path}: missing installation receipt")
    except json.JSONDecodeError as exc:
        errors.append(f"{marker_path}: invalid installation receipt: {exc}")
    except OSError as exc:
        errors.append(f"{marker_path}: cannot read installation receipt: {exc}")

    expected_names = {skill["name"] for skill in catalog["skills"]}
    recorded_skills = marker.get("skills")
    if marker and marker.get("managed_by") != "research-os":
        errors.append(f"{marker_path}: managed_by must be research-os")
    if marker and marker.get("catalog_version") != catalog["version"]:
        errors.append(
            f"{marker_path}: catalog version differs from {catalog['version']}"
        )
    if marker and marker.get("profile", "core") != profile:
        errors.append(f"{marker_path}: profile differs from {profile!r}")
    recorded_harness = marker.get("harness", "codex") if marker else harness
    if marker and recorded_harness != harness:
        errors.append(
            f"{marker_path}: harness is {recorded_harness!r}, expected {harness!r}"
        )
    if marker and not isinstance(recorded_skills, dict):
        errors.append(f"{marker_path}: skills hash map is missing")
        recorded_skills = {}
    elif isinstance(recorded_skills, dict):
        recorded_names = set(recorded_skills)
        if recorded_names != expected_names:
            errors.append(
                f"{marker_path}: receipt skill set differs; "
                f"missing={sorted(expected_names - recorded_names)}, "
                f"extra={sorted(recorded_names - expected_names)}"
            )
    else:
        recorded_skills = {}

    for skill in catalog["skills"]:
        name = skill["name"]
        source = skills_root / skill["bucket"] / name
        destination = target / name
        if not destination.is_dir():
            errors.append(f"{destination}: missing skill directory")
            continue
        if not (destination / "SKILL.md").is_file():
            errors.append(f"{destination / 'SKILL.md'}: missing")
            continue
        if harness == "codex" and not (
            destination / "agents" / "openai.yaml"
        ).is_file():
            errors.append(f"{destination / 'agents' / 'openai.yaml'}: missing")
        if harness == "claude-code":
            frontmatter = skill_frontmatter(destination / "SKILL.md")
            if skill["invocation"] == "user":
                if frontmatter.get("disable-model-invocation") is not True:
                    errors.append(
                        f"{destination / 'SKILL.md'}: "
                        "user skill must disable model invocation"
                    )
            elif frontmatter.get("user-invocable") is not False:
                errors.append(
                    f"{destination / 'SKILL.md'}: "
                    "model skill must be hidden from the user command menu"
                )

        expected_hash = expected_tree_hash(
            source, skill["invocation"], harness
        )
        installed_hash = tree_hash(destination)
        if installed_hash != expected_hash:
            errors.append(f"{destination}: installed content differs from source")
        if isinstance(recorded_skills, dict) and recorded_skills.get(name) != expected_hash:
            errors.append(f"{marker_path}: recorded hash differs for {name}")

    return errors


def main() -> int:
    args = parse_args()
    target = (args.target or default_skills_dir(args.harness)).expanduser().resolve()
    errors = verify_install(target, args.harness, args.profile)
    if errors:
        print(f"INSTALL FAILED: {len(errors)} errors")
        for message in errors:
            print(f"- {message}")
        return 2
    catalog, _skills_root, _marker_name = profile_settings(args.profile)
    profile_label = f" (profile: {args.profile})" if args.profile != "core" else ""
    print(
        f"INSTALL OK: {len(catalog['skills'])} skills "
        f"for {args.harness} at {target}{profile_label}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
