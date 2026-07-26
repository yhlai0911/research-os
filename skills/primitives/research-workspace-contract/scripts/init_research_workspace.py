#!/usr/bin/env python3
"""Initialize and verify the additive Research OS workspace contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


DIRECTORIES = (
    "decisions",
    "evidence",
    "maps",
    "briefs",
    "plans",
    "workpackages",
    "papers",
    "proposals",
    "handoffs",
    "reviews",
    "pilots",
    "templates",
)

FILES = {
    "config.yaml": "config.yaml",
    "CONTEXT.md": "CONTEXT.md",
    "evidence/claims.yaml": "claims.yaml",
    "templates/decision-record.md": "decision-record.md",
    "templates/research-brief.md": "research-brief.md",
    "templates/research-plan.md": "research-plan.md",
    "templates/workpackage.md": "workpackage.md",
    "templates/handoff.md": "handoff.md",
    "templates/review.md": "review.md",
    "templates/map.md": "map.md",
    "templates/proposal.md": "proposal.md",
}

REQUIRED_CANONICAL_KEYS = (
    "context",
    "decisions",
    "claims",
    "maps",
    "briefs",
    "plans",
    "workpackages",
    "papers",
    "proposals",
    "handoffs",
    "reviews",
    "pilots",
    "templates",
)
ARTIFACT_INDEX_HEADER = (
    "| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |"
)
REQUIRED_CLAIM_STATUSES = (
    "unverified",
    "verified",
    "contested",
    "superseded",
    "blocked",
)
TEMPLATE_MARKERS = {
    "decision-record.md": ("# RDR-NNNN:", "## Decision", "## Revisit when"),
    "research-brief.md": (
        "# Research Brief:",
        "## Data and identification",
        "## Falsifiers and kill criteria",
        "## Acceptance",
    ),
    "research-plan.md": (
        "# Academic Research Plan:",
        "## Work plan and milestones",
        "## Acceptance",
    ),
    "workpackage.md": (
        "# WP-NN:",
        "## Context envelope",
        "## Acceptance criteria",
        "## Receipt",
    ),
    "handoff.md": ("# Research Handoff", "## Context envelope", "## Acceptance"),
    "review.md": ("# Research Review", "## Verdict", "## Readback"),
    "map.md": ("# Research Map:", "## Frontier", "## Fog", "## Out of scope"),
    "proposal.md": ("# Proposal:", "## Work plan and methods", "## Submission boundary"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args()


def canonical_values(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    in_canonical = False
    for line in text.splitlines():
        if line == "canonical:":
            in_canonical = True
            continue
        if in_canonical and line and not line.startswith(" "):
            break
        if not in_canonical:
            continue
        match = re.match(r"^  ([a-z_]+):\s*(.+?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip("\"'")
    return values


def validate_contract_content(
    research_dir: Path, assets_dir: Path, check_paths: bool = False
) -> list[dict[str, str]]:
    """Check stable contract markers without requiring a project dependency."""
    conflicts: list[dict[str, str]] = []
    config_path = research_dir / "config.yaml"
    if config_path.is_file():
        config_text = config_path.read_text(encoding="utf-8")
        if "canonical:" not in config_text:
            conflicts.append(
                {"path": str(config_path), "reason": "missing-canonical-mapping"}
            )
        for key in REQUIRED_CANONICAL_KEYS:
            if not re.search(rf"(?m)^  {re.escape(key)}:\s*\S+", config_text):
                conflicts.append(
                    {
                        "path": str(config_path),
                        "reason": f"missing-canonical-key:{key}",
                    }
                )
        actual_values = canonical_values(config_text)
        expected_values = canonical_values(
            (assets_dir / "config.yaml").read_text(encoding="utf-8")
        )
        if actual_values and actual_values != expected_values:
            conflicts.append(
                {
                    "path": str(config_path),
                    "reason": "nonbaseline-adapter-requires-direct-verification",
                }
            )
        if check_paths:
            root = research_dir.parent
            file_keys = {"context", "claims"}
            for key, configured in actual_values.items():
                resolved = Path(configured)
                if not resolved.is_absolute():
                    resolved = root / resolved
                expected_type = "file" if key in file_keys else "directory"
                if resolved.exists() and (
                    (expected_type == "file" and not resolved.is_file())
                    or (expected_type == "directory" and not resolved.is_dir())
                ):
                    conflicts.append(
                        {
                            "path": str(resolved),
                            "reason": f"canonical-{key}-expected-{expected_type}",
                        }
                    )

    context_path = research_dir / "CONTEXT.md"
    if context_path.is_file():
        context_text = context_path.read_text(encoding="utf-8")
        if context_text.count("## Artifact index") != 1:
            conflicts.append(
                {
                    "path": str(context_path),
                    "reason": "artifact-index-count-not-one",
                }
            )
        if ARTIFACT_INDEX_HEADER not in context_text:
            conflicts.append(
                {"path": str(context_path), "reason": "artifact-index-header-invalid"}
            )

    claims_path = research_dir / "evidence" / "claims.yaml"
    if claims_path.is_file():
        claims_text = claims_path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^schema_version:\s*\d+\s*$", claims_text):
            conflicts.append(
                {"path": str(claims_path), "reason": "claims-schema-version-invalid"}
            )
        if not re.search(r"(?m)^statuses:\s*$", claims_text):
            conflicts.append(
                {"path": str(claims_path), "reason": "claims-statuses-missing"}
            )
        for status in REQUIRED_CLAIM_STATUSES:
            if not re.search(
                rf'(?m)^\s*-\s*["\']?{re.escape(status)}["\']?\s*$',
                claims_text,
            ):
                conflicts.append(
                    {
                        "path": str(claims_path),
                        "reason": f"claims-status-missing:{status}",
                    }
                )
        if not re.search(r"(?m)^claims:\s*(\[\])?\s*$", claims_text):
            conflicts.append(
                {"path": str(claims_path), "reason": "claims-registry-missing"}
            )

    for template_name in FILES:
        if not template_name.startswith("templates/"):
            continue
        template_path = research_dir / template_name
        if template_path.is_file():
            template_text = template_path.read_text(encoding="utf-8")
            if not template_text.strip():
                conflicts.append(
                    {"path": str(template_path), "reason": "template-empty"}
                )
                continue
            for marker in TEMPLATE_MARKERS[Path(template_name).name]:
                if marker not in template_text:
                    conflicts.append(
                        {
                            "path": str(template_path),
                            "reason": f"template-marker-missing:{marker}",
                        }
                    )
    return conflicts


def receipt(root: Path, dry_run: bool, check: bool) -> tuple[dict[str, object], int]:
    research_dir = root.resolve() / ".research"
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    result: dict[str, object] = {
        "root": str(root.resolve()),
        "mode": "check" if check else "dry-run" if dry_run else "apply",
        "created": [],
        "unchanged": [],
        "conflicts": [],
        "missing": [],
        "hashes": {},
    }

    if not root.exists() or not root.is_dir():
        result["conflicts"].append({"path": str(root), "reason": "root-not-directory"})
        return result, 2

    preflight_conflicts = validate_contract_content(
        research_dir, assets_dir, check_paths=check
    )
    result["conflicts"].extend(preflight_conflicts)
    if preflight_conflicts and not check:
        return result, 2

    for relative in DIRECTORIES:
        target = research_dir / relative
        if target.exists() and not target.is_dir():
            result["conflicts"].append(
                {"path": str(target), "reason": "expected-directory"}
            )
        elif check and not target.is_dir():
            result["missing"].append(str(target))
        elif target.is_dir():
            result["unchanged"].append(str(target))
        elif not dry_run:
            target.mkdir(parents=True, exist_ok=True)
            result["created"].append(str(target))
        else:
            result["created"].append(str(target))

    for relative, asset_name in FILES.items():
        source = assets_dir / asset_name
        target = research_dir / relative
        if target.exists() and not target.is_file():
            result["conflicts"].append(
                {"path": str(target), "reason": "expected-file"}
            )
            continue
        if check:
            if not target.is_file():
                result["missing"].append(str(target))
            else:
                result["unchanged"].append(str(target))
                result["hashes"][str(target)] = digest(target)
            continue
        if target.is_file():
            result["unchanged"].append(str(target))
            result["hashes"][str(target)] = digest(target)
            continue
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            result["hashes"][str(target)] = digest(target)
        result["created"].append(str(target))

    if check:
        postflight_conflicts = validate_contract_content(
            research_dir, assets_dir, check_paths=True
        )
        for conflict in postflight_conflicts:
            if conflict not in result["conflicts"]:
                result["conflicts"].append(conflict)

    failed = bool(result["conflicts"] or result["missing"])
    return result, 2 if failed else 0


def main() -> int:
    args = parse_args()
    result, status = receipt(args.root, args.dry_run, args.check)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
