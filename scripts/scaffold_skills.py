#!/usr/bin/env python3
"""Scaffold every catalogued skill through Codex's official skill initializer."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path("skills/catalog.yaml"))
    parser.add_argument("--skills-root", type=Path, default=Path("skills"))
    parser.add_argument(
        "--initializer",
        type=Path,
        default=Path(
            os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))
        )
        / "skills"
        / ".system"
        / "skill-creator"
        / "scripts"
        / "init_skill.py",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.initializer.is_file():
        print(
            "Official skill initializer not found. Set CODEX_HOME or pass "
            "--initializer /absolute/path/to/init_skill.py.",
            file=sys.stderr,
        )
        return 2
    catalog = yaml.safe_load(args.catalog.read_text(encoding="utf-8"))
    for skill in catalog["skills"]:
        destination = args.skills_root / skill["bucket"]
        skill_dir = destination / skill["name"]
        if skill_dir.exists():
            print(f"SKIP {skill_dir}")
            continue
        command = [
            sys.executable,
            str(args.initializer),
            skill["name"],
            "--path",
            str(destination),
            "--interface",
            f"display_name={skill['display_name']}",
            "--interface",
            f"short_description={skill['short_description']}",
            "--interface",
            f"default_prompt={skill['default_prompt']}",
        ]
        subprocess.run(command, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
