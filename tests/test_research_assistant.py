"""Distribution/fixture checks; these do not claim model behavior or triggering."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.install_skills import expected_tree_hash, materialize_skill, tree_hash  # noqa: E402
from scripts.prepare_assistant_eval import prepare  # noqa: E402
from scripts.sync_catalog import openai_yaml  # noqa: E402


def test_companion_discovery_preserves_explicit_workflows() -> None:
    catalog = yaml.safe_load((ROOT / "skills/catalog.yaml").read_text(encoding="utf-8"))
    skills = {skill["name"]: skill for skill in catalog["skills"]}
    assistant = skills["research-assistant"]
    assert assistant["bucket"] == "primitives"
    assert assistant["invocation"] == "model"
    # The companion's state resolution uses the same packaged contract as the
    # mainline, rather than a sidecar copy or an undeclared dependency.
    assert "research-workspace-contract" in catalog["composition"]["research-assistant"]
    assert yaml.safe_load(openai_yaml(assistant)).get("policy", {}).get(
        "allow_implicit_invocation", True
    ) is True
    for name in ("research-help", "research-auto", "to-paper", *(
        f"research-{i}-{suffix}" for i, suffix in enumerate(
            ("grill", "brief", "falsify", "tasks", "run", "review"), start=1
        )
    )):
        assert skills[name]["invocation"] == "user"
        assert yaml.safe_load(openai_yaml(skills[name]))["policy"][
            "allow_implicit_invocation"
        ] is False


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.parametrize("invocation", ["model", "user"])
def test_generated_adapter_accepts_windows_checkout_without_changing_source(
    tmp_path: Path, newline: str, invocation: str,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    original = newline.join([
        "---", "name: sample", "description: Test research assistance.",
        "---", "", "# Sample", "", "Keep the researcher's scope.", "",
    ]).encode("utf-8")
    (source / "SKILL.md").write_bytes(original)
    codex = tmp_path / "codex"
    claude = tmp_path / "claude"
    materialize_skill(source, codex, invocation, "codex")
    materialize_skill(source, claude, invocation, "claude-code")
    assert tree_hash(codex) == expected_tree_hash(source, invocation, "codex")
    assert tree_hash(claude) == expected_tree_hash(source, invocation, "claude-code")
    assert (source / "SKILL.md").read_bytes() == original
    assert (codex / "SKILL.md").read_bytes() == original
    text = (claude / "SKILL.md").read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---", 2)[1])
    expected = "user-invocable" if invocation == "model" else "disable-model-invocation"
    assert metadata[expected] is (invocation == "user")
    assert text.split("---", 2)[2] == original.decode().replace("\r\n", "\n").split("---", 2)[2]


def test_evaluation_preparation_is_local_exclusive_and_uses_adapter_paths(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "case"
    result = prepare("natural-data", workspace)
    assert result["model_executed"] == "false"
    config = yaml.safe_load((workspace / ".research/config.yaml").read_text(encoding="utf-8"))
    assert config["canonical"]["context"] == "state/context.md"
    assert "DECOY" in (workspace / ".research/CONTEXT.md").read_text()
    assert "DECOY" not in (workspace / config["canonical"]["context"]).read_text()
    assert (workspace / ".agents/skills/research-assistant/SKILL.md").is_file()
    assert (workspace / ".agents/skills/research-help/agents/openai.yaml").is_file()
    snapshot = {p.relative_to(workspace): p.read_bytes() for p in workspace.rglob("*") if p.is_file()}
    with pytest.raises(FileExistsError):
        prepare("natural-data", workspace)
    assert snapshot == {p.relative_to(workspace): p.read_bytes() for p in workspace.rglob("*") if p.is_file()}


def test_unknown_case_never_creates_output(tmp_path: Path) -> None:
    target = tmp_path / "absent"
    with pytest.raises(ValueError, match="unknown case"):
        prepare("unknown", target)
    assert not target.exists()
