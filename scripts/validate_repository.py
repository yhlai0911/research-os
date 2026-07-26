#!/usr/bin/env python3
"""Validate Research OS structural and semantic repository invariants."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

import yaml
from yaml.constructor import ConstructorError


ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "skills" / "catalog.yaml"
MATT_PORT_MAP_PATH = ROOT / "docs" / "MATT_PORT_MAP.yaml"
MATT_INVENTORY_PATH = ROOT / "docs" / "upstream" / "MATT_SKILL_INVENTORY.txt"
MATT_SOURCE_COMMIT = "ed37663cc5fbef691ddfecd080dff42f7e7e350d"
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKILL_REFERENCE = re.compile(r"\$([a-z0-9-]+)")
ARTIFACT_INDEX_COLUMNS = (
    "Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes"
)
WORKSPACE_CONTRACT_EXEMPT = {"setup-research-os", "writing-research-skills"}
REQUIRED_CANONICAL_KEYS = {
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
}
WORKSPACE_TEMPLATE_NAMES = {
    "decision-record.md",
    "research-brief.md",
    "research-plan.md",
    "workpackage.md",
    "handoff.md",
    "review.md",
    "map.md",
    "proposal.md",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that fails instead of silently replacing duplicate keys."""


def construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping
)


def load_yaml_strict(path: Path) -> object:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def validate_links(path: Path, text: str, errors: list[str]) -> None:
    for target in MARKDOWN_LINK.findall(text):
        target = target.strip().strip("<>")
        if (
            not target
            or target.startswith(("#", "http://", "https://", "mailto:"))
            or "$" in target
        ):
            continue
        relative = target.split("#", 1)[0]
        if not relative:
            continue
        resolved = (path.parent / relative).resolve()
        if not resolved.exists():
            error(errors, path, f"dangling Markdown link: {target}")


def validate_workspace_contract(
    skill_name: str, path: Path, text: str, errors: list[str]
) -> None:
    """Prevent adapter-path drift and unregistered research artifacts."""
    first_workspace_path = text.find(".research/")
    if first_workspace_path < 0 or skill_name in WORKSPACE_CONTRACT_EXEMPT:
        return

    first_config_path = text.find(".research/config.yaml")
    if first_config_path != first_workspace_path:
        error(
            errors,
            path,
            "must mention .research/config.yaml before every other .research path",
        )
    if "Artifact index" not in text or ARTIFACT_INDEX_COLUMNS not in text:
        error(
            errors,
            path,
            "workspace skill must register outcomes in the canonical Artifact index",
        )


def validate_matt_port_map(skill_names: set[str], errors: list[str]) -> None:
    if not MATT_INVENTORY_PATH.is_file():
        error(errors, MATT_INVENTORY_PATH, "missing pinned upstream inventory")
        return
    inventory_lines = MATT_INVENTORY_PATH.read_text(encoding="utf-8").splitlines()
    if not inventory_lines or MATT_SOURCE_COMMIT not in inventory_lines[0]:
        error(errors, MATT_INVENTORY_PATH, "header does not name pinned source commit")
    inventory = [line for line in inventory_lines if line and not line.startswith("#")]
    if len(inventory) != 41 or len(inventory) != len(set(inventory)):
        error(errors, MATT_INVENTORY_PATH, "must contain 41 unique upstream skills")
    if inventory != sorted(inventory):
        error(errors, MATT_INVENTORY_PATH, "upstream inventory must be sorted")

    if not MATT_PORT_MAP_PATH.is_file():
        error(errors, MATT_PORT_MAP_PATH, "missing")
        return
    try:
        port_map = load_yaml_strict(MATT_PORT_MAP_PATH)
    except yaml.YAMLError as exc:
        error(errors, MATT_PORT_MAP_PATH, f"invalid YAML: {exc}")
        return
    if not isinstance(port_map, dict):
        error(errors, MATT_PORT_MAP_PATH, "root must be a mapping")
        return
    source = port_map.get("source", {})
    if source.get("commit") != MATT_SOURCE_COMMIT:
        error(errors, MATT_PORT_MAP_PATH, "source commit differs from pinned inventory")
    if source.get("skill_count") != 41:
        error(errors, MATT_PORT_MAP_PATH, "source.skill_count must equal 41")
    if source.get("tracked_files") != 167:
        error(errors, MATT_PORT_MAP_PATH, "source.tracked_files must equal 167")
    if source.get("inventory") != "upstream/MATT_SKILL_INVENTORY.txt":
        error(errors, MATT_PORT_MAP_PATH, "source.inventory path differs from contract")

    entries = port_map.get("entries", [])
    if not isinstance(entries, list):
        error(errors, MATT_PORT_MAP_PATH, "entries must be a list")
        return
    mapped_paths = [entry.get("upstream_path") for entry in entries if isinstance(entry, dict)]
    if len(entries) != 41 or len(mapped_paths) != len(set(mapped_paths)):
        error(errors, MATT_PORT_MAP_PATH, "must contain 41 unique disposition entries")
    if set(mapped_paths) != set(inventory):
        missing = sorted(set(inventory) - set(mapped_paths))
        extra = sorted(set(mapped_paths) - set(inventory))
        error(
            errors,
            MATT_PORT_MAP_PATH,
            f"entry paths differ from inventory; missing={missing}, extra={extra}",
        )
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            error(errors, MATT_PORT_MAP_PATH, f"entry {index} must be a mapping")
            continue
        disposition = entry.get("disposition")
        if disposition not in {"ported", "adapted", "excluded"}:
            error(
                errors,
                MATT_PORT_MAP_PATH,
                f"entry {index} has invalid disposition {disposition!r}",
            )
        targets = entry.get("research_os_skills")
        if not isinstance(targets, list):
            error(errors, MATT_PORT_MAP_PATH, f"entry {index} targets must be a list")
            targets = []
        unknown_targets = sorted(set(targets) - skill_names)
        if unknown_targets:
            error(
                errors,
                MATT_PORT_MAP_PATH,
                f"entry {index} has unknown skill targets {unknown_targets}",
            )
        if disposition == "excluded" and targets:
            error(errors, MATT_PORT_MAP_PATH, f"entry {index} excluded but has targets")
        if disposition != "excluded" and not targets:
            error(errors, MATT_PORT_MAP_PATH, f"entry {index} retained but has no target")
        for field in ("retained_mechanics", "rejected_mechanics"):
            values = entry.get(field)
            if not isinstance(values, list) or not values:
                error(
                    errors,
                    MATT_PORT_MAP_PATH,
                    f"entry {index} must name at least one {field}",
                )

    audit_by_group = {
        "engineering": ROOT / "docs" / "port-audit" / "engineering.md",
        "productivity": ROOT
        / "docs"
        / "port-audit"
        / "productivity-in-progress.md",
        "in-progress": ROOT
        / "docs"
        / "port-audit"
        / "productivity-in-progress.md",
        "deprecated": ROOT / "docs" / "port-audit" / "lifecycle-repository.md",
        "misc": ROOT / "docs" / "port-audit" / "lifecycle-repository.md",
        "personal": ROOT / "docs" / "port-audit" / "lifecycle-repository.md",
    }
    audit_text: dict[Path, str] = {}
    for path in inventory:
        parts = Path(path).parts
        group = parts[1]
        skill = parts[2]
        audit_path = audit_by_group[group]
        if not audit_path.is_file():
            error(errors, audit_path, f"missing prompt-level audit for {group}")
            continue
        text = audit_text.setdefault(
            audit_path, audit_path.read_text(encoding="utf-8")
        )
        if f"`{skill}`" not in text:
            error(
                errors,
                audit_path,
                f"prompt-level audit does not name upstream skill {skill}",
            )


def main() -> int:
    errors: list[str] = []
    try:
        catalog = load_yaml_strict(CATALOG_PATH)
    except yaml.YAMLError as exc:
        print("VALIDATION FAILED")
        print(f"- skills/catalog.yaml: invalid YAML: {exc}")
        return 1
    if not isinstance(catalog, dict):
        print("VALIDATION FAILED")
        print("- skills/catalog.yaml: root must be a mapping")
        return 1
    skills = catalog.get("skills", [])
    names = [skill.get("name") for skill in skills]
    if len(names) != len(set(names)):
        errors.append("skills/catalog.yaml: duplicate skill names")

    defaults = catalog.get("defaults", {})
    if defaults != {
        "lifecycle": "stable",
        "distribution": "core",
        "replaced_by": None,
    }:
        errors.append(
            "skills/catalog.yaml: defaults must define stable/core/no replacement"
        )

    expected_paths: set[Path] = set()
    discovered_references: dict[str, list[str]] = {}
    for skill in skills:
        skill_dir = ROOT / "skills" / skill["bucket"] / skill["name"]
        skill_md = skill_dir / "SKILL.md"
        expected_paths.add(skill_md.resolve())
        if not skill_md.is_file():
            error(errors, skill_md, "missing")
            continue
        text = skill_md.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            error(errors, skill_md, "invalid frontmatter")
            continue
        try:
            frontmatter = yaml.load(match.group(1), Loader=UniqueKeyLoader)
        except yaml.YAMLError as exc:
            error(errors, skill_md, f"invalid frontmatter YAML: {exc}")
            continue
        if set(frontmatter) != {"name", "description"}:
            error(errors, skill_md, "frontmatter must contain only name and description")
        if frontmatter.get("name") != skill["name"]:
            error(errors, skill_md, "frontmatter name differs from catalog")
        if frontmatter.get("description") != skill["description"]:
            error(errors, skill_md, "description differs from catalog")
        if skill_dir.name != skill["name"]:
            error(errors, skill_md, "directory name differs from skill name")
        if len(text.splitlines()) > 500:
            error(errors, skill_md, "SKILL.md exceeds 500 lines")
        if re.search(r"\bTODO\b|Structuring This Skill|\[TODO:", text):
            error(errors, skill_md, "initializer placeholder remains")
        references = sorted(set(SKILL_REFERENCE.findall(text)))
        if references:
            discovered_references[skill["name"]] = references
        if skill["invocation"] == "model" and "Use " not in skill["description"]:
            error(errors, skill_md, "model-invoked description lacks trigger phrasing")
        validate_workspace_contract(skill["name"], skill_md, text, errors)
        validate_links(skill_md, text, errors)

        openai_path = skill_dir / "agents" / "openai.yaml"
        if not openai_path.is_file():
            error(errors, openai_path, "missing")
            continue
        try:
            openai = load_yaml_strict(openai_path)
        except yaml.YAMLError as exc:
            error(errors, openai_path, f"invalid YAML: {exc}")
            continue
        interface = openai.get("interface", {})
        for field in ("display_name", "short_description", "default_prompt"):
            if interface.get(field) != skill[field]:
                error(errors, openai_path, f"{field} differs from catalog")
        if not 25 <= len(interface.get("short_description", "")) <= 64:
            error(errors, openai_path, "short_description must be 25-64 characters")
        if f"${skill['name']}" not in interface.get("default_prompt", ""):
            error(errors, openai_path, "default_prompt must mention the skill")
        policy = openai.get("policy", {})
        if skill["invocation"] == "user":
            if policy.get("allow_implicit_invocation") is not False:
                error(errors, openai_path, "user skill must disable implicit invocation")
        elif "policy" in openai:
            error(errors, openai_path, "model skill must omit user-only policy")

        for readme in skill_dir.rglob("README.md"):
            error(errors, readme, "skill-local README is forbidden")
        for resource_dir in ("references", "scripts", "assets"):
            candidate = skill_dir / resource_dir
            if candidate.is_dir() and not any(candidate.iterdir()):
                error(errors, candidate, "empty resource directory")
        for markdown in skill_dir.rglob("*.md"):
            validate_links(markdown, markdown.read_text(encoding="utf-8"), errors)

    discovered = {
        path.resolve()
        for path in (ROOT / "skills").rglob("SKILL.md")
        if ".venv" not in path.parts
    }
    for extra in sorted(discovered - expected_paths):
        error(errors, extra, "not catalogued")
    for missing in sorted(expected_paths - discovered):
        error(errors, missing, "catalogued but missing")

    composition = catalog.get("composition", {})
    if not isinstance(composition, dict):
        errors.append("skills/catalog.yaml: composition must be a mapping")
    else:
        normalized_composition: dict[str, list[str]] = {}
        for owner, targets in composition.items():
            if owner not in set(names):
                errors.append(
                    f"skills/catalog.yaml: composition has unknown owner {owner}"
                )
                continue
            if not isinstance(targets, list) or len(targets) != len(set(targets)):
                errors.append(
                    f"skills/catalog.yaml: composition for {owner} must be a unique list"
                )
                continue
            unknown = sorted(set(targets) - set(names))
            if unknown:
                errors.append(
                    f"skills/catalog.yaml: composition for {owner} has unknown targets {unknown}"
                )
            normalized_composition[owner] = sorted(targets)
        if normalized_composition != discovered_references:
            missing_or_changed = {
                key: discovered_references.get(key)
                for key in sorted(
                    set(normalized_composition) | set(discovered_references)
                )
                if normalized_composition.get(key) != discovered_references.get(key)
            }
            errors.append(
                "skills/catalog.yaml: composition differs from $skill references: "
                f"{missing_or_changed}"
            )

    validate_matt_port_map(set(names), errors)

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    if project["project"]["version"] != catalog["version"]:
        errors.append("version mismatch between pyproject.toml and skills/catalog.yaml")

    context_template = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "assets"
        / "CONTEXT.md"
    )
    context_text = context_template.read_text(encoding="utf-8")
    if "## Artifact index" not in context_text:
        error(errors, context_template, "missing canonical Artifact index")
    if f"| {ARTIFACT_INDEX_COLUMNS} |" not in context_text:
        error(errors, context_template, "Artifact index columns differ from contract")

    config_template = context_template.parent / "config.yaml"
    config = load_yaml_strict(config_template)
    canonical = config.get("canonical", {})
    missing_canonical = REQUIRED_CANONICAL_KEYS - set(canonical)
    if missing_canonical:
        error(
            errors,
            config_template,
            f"missing canonical keys: {sorted(missing_canonical)}",
        )

    example_root = ROOT / "examples" / "financial-wave-diffusion"
    example_config_path = example_root / ".research" / "config.yaml"
    example_config = load_yaml_strict(example_config_path)
    example_canonical = example_config.get("canonical", {})
    missing_example_keys = REQUIRED_CANONICAL_KEYS - set(example_canonical)
    if missing_example_keys:
        error(
            errors,
            example_config_path,
            f"missing canonical keys: {sorted(missing_example_keys)}",
        )
    for key in sorted(REQUIRED_CANONICAL_KEYS & set(example_canonical)):
        resolved = Path(example_canonical[key])
        if not resolved.is_absolute():
            resolved = example_root / resolved
        if not resolved.exists():
            error(errors, example_config_path, f"{key} path does not exist: {resolved}")
    for template_name in sorted(WORKSPACE_TEMPLATE_NAMES):
        source_template = context_template.parent / template_name
        example_template = example_root / ".research" / "templates" / template_name
        if (
            not example_template.is_file()
            or example_template.read_bytes() != source_template.read_bytes()
        ):
            error(
                errors,
                example_template,
                "worked-example template differs from setup source",
            )

    if errors:
        print("VALIDATION FAILED")
        for item in errors:
            print(f"- {item}")
        return 1
    print(f"VALIDATION OK: {len(skills)} skills, 0 errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
