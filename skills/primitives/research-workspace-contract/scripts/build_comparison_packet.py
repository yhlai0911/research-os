#!/usr/bin/env python3
"""Build one deterministic Markdown-aware comparison packet for review axes."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path


HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
CLAIM_ID = re.compile(r"\b(?:claim|clm)[-_:/.][A-Za-z0-9_.:/-]+\b", re.I)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def section_map(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {"<preamble>#1": []}
    counts: Counter[str] = Counter()
    current = "<preamble>#1"
    for line in text.splitlines():
        match = HEADING.match(line)
        if match:
            label = f"{match.group(1)} {match.group(2).strip()}"
            counts[label] += 1
            current = f"{label}#{counts[label]}"
            sections[current] = [line]
        else:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def table_map(text: str) -> dict[str, str]:
    tables: dict[str, str] = {}
    current_section = "<preamble>#1"
    section_counts: Counter[str] = Counter()
    table_counts: Counter[str] = Counter()
    block: list[str] = []

    def flush() -> None:
        nonlocal block
        if block:
            table_counts[current_section] += 1
            key = f"{current_section}/table-{table_counts[current_section]}"
            tables[key] = "\n".join(block)
            block = []

    for line in text.splitlines() + [""]:
        match = HEADING.match(line)
        if match:
            flush()
            label = f"{match.group(1)} {match.group(2).strip()}"
            section_counts[label] += 1
            current_section = f"{label}#{section_counts[label]}"
        if line.lstrip().startswith("|"):
            block.append(line.rstrip())
        else:
            flush()
    return tables


def changed_keys(base: dict[str, str], target: dict[str, str]) -> list[str]:
    return sorted(
        key
        for key in set(base) | set(target)
        if base.get(key) != target.get(key)
    )


def build_packet(base_path: Path, target_path: Path) -> dict[str, object]:
    base_bytes = base_path.read_bytes()
    target_bytes = target_path.read_bytes()
    base_hash = digest(base_bytes)
    target_hash = digest(target_bytes)
    base_text = base_bytes.decode("utf-8")
    target_text = target_bytes.decode("utf-8")
    diff_lines = list(
        difflib.unified_diff(
            base_text.splitlines(),
            target_text.splitlines(),
            fromfile=base_path.name,
            tofile=target_path.name,
            lineterm="",
        )
    )
    changed_text = "\n".join(
        line[1:]
        for line in diff_lines
        if (line.startswith("+") or line.startswith("-"))
        and not line.startswith("+++")
        and not line.startswith("---")
    )
    packet_id = f"delta-{base_hash[:12]}-{target_hash[:12]}"
    status = "no-op" if base_hash == target_hash else "changed"
    return {
        "schema_version": 1,
        "packet_id": packet_id,
        "status": status,
        "base": {"path": str(base_path.resolve()), "sha256": base_hash},
        "target": {"path": str(target_path.resolve()), "sha256": target_hash},
        "changed_sections": changed_keys(
            section_map(base_text), section_map(target_text)
        ),
        "changed_claim_ids": sorted(set(CLAIM_ID.findall(changed_text))),
        "changed_tables": changed_keys(table_map(base_text), table_map(target_text)),
        "unified_diff": "\n".join(diff_lines),
    }


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    args = parse_args()
    if not args.base.is_file() or not args.target.is_file():
        raise SystemExit("base and target must both be readable files")
    packet = build_packet(args.base, args.target)
    rendered = json.dumps(packet, indent=2, sort_keys=True) + "\n"
    if args.output:
        atomic_write(args.output, rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
