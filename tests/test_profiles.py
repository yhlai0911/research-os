from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.validate_repository import validate_links  # noqa: E402


PROFILE = "finance-social-science"
PROFILE_SKILL = "research-finance-social-science"
CORE_MARKER = ".research-os-install.json"
PROFILE_MARKER = f".research-os-{PROFILE}-install.json"


def run_script(name: str, target: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name), "--target", str(target), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def install_core(target: Path, *args: str) -> None:
    result = run_script("install_skills.py", target, *args)
    assert result.returncode == 0, result.stdout + result.stderr


def test_optional_profile_does_not_expand_default_core(tmp_path: Path) -> None:
    core = yaml.safe_load((ROOT / "skills" / "catalog.yaml").read_text())
    profile = yaml.safe_load(
        (ROOT / "profiles" / PROFILE / "catalog.yaml").read_text()
    )
    assert len(core["skills"]) == 42
    assert profile["version"] == "0.1.0"
    assert profile["requires_core"] == core["version"]
    assert profile["skills"] == [
        {"name": PROFILE_SKILL, "bucket": "orchestrators", "invocation": "user"}
    ]

    install_core(tmp_path)
    marker = json.loads((tmp_path / CORE_MARKER).read_text())
    assert set(marker["skills"]) == {skill["name"] for skill in core["skills"]}
    assert not (tmp_path / PROFILE_SKILL).exists()
    assert not (tmp_path / PROFILE_MARKER).exists()

    explicit_core = run_script("install_skills.py", tmp_path, "--profile", "core")
    assert explicit_core.returncode == 0, explicit_core.stdout + explicit_core.stderr
    assert json.loads(explicit_core.stdout)["marker"] == "preserved"


def test_profile_metadata_and_document_links_match_catalog() -> None:
    profile_root = ROOT / "profiles" / PROFILE
    catalog = yaml.safe_load((profile_root / "catalog.yaml").read_text())
    for skill in catalog["skills"]:
        source = profile_root / "skills" / skill["bucket"] / skill["name"]
        text = (source / "SKILL.md").read_text()
        assert text.startswith("---\n")
        frontmatter = yaml.safe_load(text.split("---\n", 2)[1])
        assert set(frontmatter) == {"name", "description"}
        assert frontmatter["name"] == skill["name"]
        assert isinstance(frontmatter["description"], str) and frontmatter["description"]
        agent = yaml.safe_load((source / "agents" / "openai.yaml").read_text())
        assert agent["policy"]["allow_implicit_invocation"] is (
            skill["invocation"] != "user"
        )
        assert f"${skill['name']}" in agent["interface"]["default_prompt"]

    errors: list[str] = []
    markdown_files = [
        ROOT / "README.md",
        ROOT / "README.en.md",
        ROOT / "docs" / "QUICKSTART.en.md",
        ROOT / "docs" / "LANGUAGE.md",
        *profile_root.rglob("*.md"),
    ]
    for path in markdown_files:
        validate_links(path, path.read_text(), errors)
    assert not errors, "\n".join(errors)


def test_public_install_guides_target_main() -> None:
    for relative in ("README.md", "README.en.md", "docs/QUICKSTART.en.md"):
        text = (ROOT / relative).read_text()
        assert "git clone --branch main https://github.com/yhlai0911/research-os.git" in text
        assert "feat/bilingual-domain-profiles" not in text
        assert "refactor/explicit-pipeline" not in text


@pytest.mark.parametrize("script", ["install_skills.py", "verify_install.py"])
def test_profile_rejects_incompatible_core_catalog_before_writes(
    tmp_path: Path, script: str
) -> None:
    checkout = tmp_path / "checkout"
    scripts = checkout / "scripts"
    scripts.mkdir(parents=True)
    for name in ("install_skills.py", "verify_install.py"):
        shutil.copyfile(ROOT / "scripts" / name, scripts / name)
    (checkout / "skills").mkdir()
    shutil.copyfile(ROOT / "skills" / "catalog.yaml", checkout / "skills" / "catalog.yaml")
    profile_root = checkout / "profiles" / PROFILE
    profile_root.mkdir(parents=True)
    catalog = yaml.safe_load((ROOT / "profiles" / PROFILE / "catalog.yaml").read_text())
    catalog["requires_core"] = "incompatible-version"
    (profile_root / "catalog.yaml").write_text(yaml.safe_dump(catalog))
    target = tmp_path / "target"
    result = subprocess.run(
        [
            sys.executable, str(scripts / script), "--target", str(target),
            "--profile", PROFILE,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, result.stdout + result.stderr
    assert "requires core 'incompatible-version'" in result.stdout
    assert not target.exists()


@pytest.mark.parametrize(
    ("harness", "mode"),
    [("codex", "copy"), ("codex", "symlink"), ("claude-code", "copy")],
)
def test_profile_coexists_with_core_and_preserves_both_receipts(
    tmp_path: Path, harness: str, mode: str
) -> None:
    install_args = ("--harness", harness, "--mode", mode)
    profile_args = (*install_args, "--profile", PROFILE)
    install_core(tmp_path, *install_args)
    core_before = (tmp_path / CORE_MARKER).read_bytes()
    source = (
        ROOT / "profiles" / PROFILE / "skills" / "orchestrators" / PROFILE_SKILL
    )
    source_markdown = (source / "SKILL.md").read_bytes()

    preview = run_script("install_skills.py", tmp_path, *profile_args, "--dry-run")
    assert preview.returncode == 0, preview.stdout + preview.stderr
    preview_receipt = json.loads(preview.stdout)
    assert preview_receipt["profile"] == PROFILE
    assert preview_receipt["planned"] == [str(tmp_path / PROFILE_SKILL)]
    assert preview_receipt["created"] == []
    assert not (tmp_path / PROFILE_SKILL).exists()
    assert not (tmp_path / PROFILE_MARKER).exists()
    assert (tmp_path / CORE_MARKER).read_bytes() == core_before

    installed = run_script("install_skills.py", tmp_path, *profile_args)
    assert installed.returncode == 0, installed.stdout + installed.stderr
    receipt = json.loads(installed.stdout)
    assert receipt["created"] == [str(tmp_path / PROFILE_SKILL)]
    assert set(receipt["skills"]) == {PROFILE_SKILL}
    assert receipt["marker"] == str(tmp_path / PROFILE_MARKER)
    assert (tmp_path / CORE_MARKER).read_bytes() == core_before
    assert (tmp_path / PROFILE_SKILL).is_symlink() is (mode == "symlink")

    installed_markdown = (tmp_path / PROFILE_SKILL / "SKILL.md").read_bytes()
    if harness == "claude-code":
        assert b"disable-model-invocation: true" in installed_markdown
        assert receipt["source_skills"] != receipt["skills"]
    else:
        assert installed_markdown == source_markdown
        assert receipt["source_skills"] == receipt["skills"]
        assert (tmp_path / PROFILE_SKILL / "agents" / "openai.yaml").is_file()
    assert (source / "SKILL.md").read_bytes() == source_markdown

    for profile in ("core", PROFILE):
        verified = run_script(
            "verify_install.py", tmp_path, "--harness", harness, "--profile", profile
        )
        assert verified.returncode == 0, verified.stdout + verified.stderr
        count = 42 if profile == "core" else 1
        assert f"INSTALL OK: {count} skills" in verified.stdout

    profile_before = (tmp_path / PROFILE_MARKER).read_bytes()
    repeated = run_script("install_skills.py", tmp_path, *profile_args)
    assert repeated.returncode == 0, repeated.stdout + repeated.stderr
    assert json.loads(repeated.stdout)["marker"] == "preserved"
    install_core(tmp_path, *install_args)
    assert (tmp_path / CORE_MARKER).read_bytes() == core_before
    assert (tmp_path / PROFILE_MARKER).read_bytes() == profile_before


@pytest.mark.parametrize("harness", ["codex", "claude-code"])
@pytest.mark.parametrize("dry_run", [False, True])
def test_profile_requires_core_even_for_dry_run(
    tmp_path: Path, harness: str, dry_run: bool
) -> None:
    target = tmp_path / "not-installed"
    args = ["--harness", harness, "--profile", PROFILE]
    if dry_run:
        args.append("--dry-run")
    result = run_script("install_skills.py", target, *args)
    assert result.returncode == 2, result.stdout + result.stderr
    receipt = json.loads(result.stdout)
    assert "requires a verified core installation" in receipt["failure"]
    assert any(
        "missing installation receipt" in error
        for error in receipt["prerequisite_errors"]
    )
    assert receipt["created"] == []
    assert not target.exists()


@pytest.mark.parametrize(
    "core_state", ["missing_receipt", "changed_skill", "wrong_harness", "invalid_receipt"]
)
def test_profile_requires_a_current_verified_core(
    tmp_path: Path, core_state: str
) -> None:
    install_core(tmp_path)
    marker = tmp_path / CORE_MARKER
    harness = "codex"
    if core_state == "missing_receipt":
        marker.unlink()
    elif core_state == "changed_skill":
        (tmp_path / "research-help" / "SKILL.md").write_text("user changes\n")
    elif core_state == "wrong_harness":
        harness = "claude-code"
    else:
        marker.write_text("[]\n")
    before = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}

    result = run_script(
        "install_skills.py", tmp_path, "--profile", PROFILE,
        "--harness", harness, "--dry-run",
    )
    assert result.returncode == 2, result.stdout + result.stderr
    receipt = json.loads(result.stdout)
    assert "requires a verified core installation" in receipt["failure"]
    assert receipt["prerequisite_errors"]
    after = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    assert after == before


@pytest.mark.parametrize("changed", ["core", "profile", "profile_receipt"])
def test_profile_verifier_detects_changed_core_or_profile(
    tmp_path: Path, changed: str
) -> None:
    install_core(tmp_path)
    installed = run_script("install_skills.py", tmp_path, "--profile", PROFILE)
    assert installed.returncode == 0, installed.stdout + installed.stderr

    if changed == "profile_receipt":
        marker = tmp_path / PROFILE_MARKER
        receipt = json.loads(marker.read_text())
        receipt["profile"] = "core"
        marker.write_text(json.dumps(receipt))
    else:
        name = "research-help" if changed == "core" else PROFILE_SKILL
        (tmp_path / name / "SKILL.md").write_text("user changes\n")
    verified = run_script("verify_install.py", tmp_path, "--profile", PROFILE)
    assert verified.returncode == 2, verified.stdout + verified.stderr
    if changed == "core":
        assert "core prerequisite:" in verified.stdout
    elif changed == "profile":
        assert f"{tmp_path / PROFILE_SKILL}: installed content differs" in verified.stdout
    else:
        assert f"profile differs from {PROFILE!r}" in verified.stdout
    if changed != "core":
        core_verified = run_script("verify_install.py", tmp_path)
        assert core_verified.returncode == 0, core_verified.stdout + core_verified.stderr


@pytest.mark.parametrize("conflict", ["skill", "receipt", "non_object_receipt"])
def test_profile_conflicts_preserve_user_files_and_core(
    tmp_path: Path, conflict: str
) -> None:
    install_core(tmp_path)
    if conflict == "skill":
        destination = tmp_path / PROFILE_SKILL
        destination.mkdir()
        (destination / "SKILL.md").write_text("user-owned skill\n")
    else:
        destination = tmp_path / PROFILE_MARKER
        destination.write_text(
            "[]\n" if conflict == "non_object_receipt" else '{"owner":"user"}\n'
        )
    before = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    installed = run_script("install_skills.py", tmp_path, "--profile", PROFILE)
    assert installed.returncode == 2, installed.stdout + installed.stderr
    receipt = json.loads(installed.stdout)
    assert str(destination) in receipt["conflicts"]
    assert receipt["created"] == []
    after = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    assert after == before


def test_profile_claude_adapter_also_requires_copy_mode(tmp_path: Path) -> None:
    result = run_script(
        "install_skills.py", tmp_path, "--profile", PROFILE,
        "--harness", "claude-code", "--mode", "symlink",
    )
    assert result.returncode == 2
    assert "requires copy mode" in result.stderr
    assert list(tmp_path.iterdir()) == []
