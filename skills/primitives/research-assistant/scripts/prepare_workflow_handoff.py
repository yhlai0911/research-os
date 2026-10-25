#!/usr/bin/env python3
"""Non-mutating preflight for a selected workflow, never a model/skill executor."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import yaml

SKILL = Path(__file__).resolve().parents[1]


def prepare(project: Path, workflow: str, *, local_writes: bool = False,
            skill_dir: Path = SKILL) -> dict[str, object]:
    routes = json.loads((skill_dir / "assets/workflow-routes.json").read_text(encoding="utf-8"))
    allowed = {row["name"]: row for row in routes["workflows"]}
    if workflow not in allowed:
        return {"action": "blocked", "reason": "workflow_not_delegable", "workflow": workflow,
                "executed": False, "native_invocation": False}
    root = project.resolve()
    base = {"workflow": workflow, "project": str(root), "executed": False,
            "native_invocation": False, "research_readiness_verified": False}
    # Source checkout and installed flat package are both supported; no home scan.
    meta = allowed[workflow]
    candidates = [skill_dir.parent / workflow / "SKILL.md",
                  skill_dir.parent.parent / meta["bucket"] / workflow / "SKILL.md"]
    target = next((p.resolve() for p in candidates if p.is_file()), None)
    if target is None:
        return {**base, "action": "blocked", "reason": "receiving_skill_missing"}
    base.update({"instructions": str(target),
                 "instruction_sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    if not root.is_dir():
        return {**base, "action": "blocked", "reason": "project_missing"}
    if not local_writes:
        return {**base, "action": "guidance_only", "reason": "local_write_authority_missing"}
    config = root / ".research/config.yaml"
    if not config.exists():
        if workflow == "research-setup":
            return {**base, "action": "delegate", "contract_ready": False,
                    "reason": "authorised_additive_setup_required"}
        return {**base, "action": "prerequisite", "reason": "workspace_not_initialized",
                "required_workflow": "research-setup"}
    try:
        data = yaml.safe_load(config.read_text(encoding="utf-8"))
        canonical = data["canonical"]
        bindings = {}
        for key in ("context", "claims", "decisions", "templates"):
            value = canonical[key]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"invalid canonical.{key}")
            p = Path(value)
            p = (p if p.is_absolute() else root / p).resolve()
            if not p.is_relative_to(root):
                return {**base, "action": "blocked", "reason": "additional_path_authority_required",
                        "canonical_key": key}
            expected_file = key in {"context", "claims"}
            if not (p.is_file() if expected_file else p.is_dir()):
                return {**base, "action": "blocked", "reason": "canonical_target_missing_or_wrong_type",
                        "canonical_key": key, "target": str(p)}
            bindings[key] = str(p)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        return {**base, "action": "blocked", "reason": "invalid_workspace_contract",
                "detail": str(exc)}
    return {**base, "action": "delegate", "contract_ready": True, "bindings": bindings,
            "next_obligation": "Read full receiving instructions/applicable references, inspect current artifacts and research gates, perform only that workflow, then return real output/readback."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--local-writes", action="store_true",
                        help="Only when the actual user delegation includes scoped local writes.")
    args = parser.parse_args()
    result = prepare(args.project, args.workflow, local_writes=args.local_writes)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["action"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
