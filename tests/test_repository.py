from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.validate_repository import load_yaml_strict  # noqa: E402


CATALOG = yaml.safe_load((ROOT / "skills" / "catalog.yaml").read_text())


def run_script(
    name: str, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name), *args],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def test_catalog_is_synchronized() -> None:
    result = run_script("sync_catalog.py", "--check")
    assert result.returncode == 0, result.stderr


def test_tutorial_delivery_is_present_and_receipted() -> None:
    required_docs = (
        ROOT / "docs" / "USAGE_GUIDE.zh-TW.md",
        ROOT / "docs" / "PROMPT_COOKBOOK.zh-TW.md",
        ROOT / "docs" / "TROUBLESHOOTING.zh-TW.md",
        ROOT
        / "examples"
        / "financial-wave-diffusion"
        / "WALKTHROUGH.zh-TW.md",
    )
    for path in required_docs:
        assert path.is_file() and path.stat().st_size > 500

    tutorial = ROOT / "jobs" / "research-os-tutorial"
    video = tutorial / "output" / "research-os-tutorial-zh-TW.mp4"
    receipt = json.loads((tutorial / "render-receipt.json").read_text())
    assert video.is_file() and video.stat().st_size == receipt["output"]["size_bytes"]
    assert hashlib.sha256(video.read_bytes()).hexdigest() == receipt["output"]["sha256"]
    assert receipt["quality_gates"]["hyperframes_check_ok"] is True
    assert receipt["quality_gates"]["runtime_errors"] == 0
    assert receipt["quality_gates"]["layout_errors"] == 0
    assert receipt["quality_gates"]["contrast_warnings"] == 0

    ledger = json.loads((tutorial / "cost_ledger.json").read_text())
    attempts = ledger["paid_submission_attempts"]
    # 21 attempts / 8 successes built v1; the v2 narration rebuild added the rest,
    # including probes and one discarded take. The ledger records every paid
    # submission because the API never returns per-request credits.
    assert len(attempts) == 46
    assert sum(event["status"] == "success" for event in attempts) == 23
    assert ledger["totals"]["unreported_paid_submission_attempts"] == len(attempts)
    assert ledger["totals"]["successful_voice_clips"] == 23
    assert all(
        event["credits"] == "unreported" and event["usd"] == "unreported"
        for event in ledger["paid_submission_attempts"]
    )


def test_repository_validates() -> None:
    result = run_script("validate_repository.py")
    assert result.returncode == 0, result.stdout + result.stderr


def test_release_inventory_is_version_controlled_only() -> None:
    """A release must never carry ignored files, least of all credentials.

    An earlier build walked the filesystem and subtracted a hardcoded list,
    which packaged .env, *.wav.bak and renders/ into the archive.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "package_release", ROOT / "scripts" / "package_release.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    names = {
        path.relative_to(ROOT).as_posix() for path in module.source_files()
    }
    assert names, "release inventory is empty"
    assert not [n for n in names if n == ".env" or n.startswith(".env.")]
    assert not [n for n in names if n.endswith(".wav.bak")]
    assert not [n for n in names if "/renders/" in n]
    assert not [n for n in names if n.startswith(".venv/") or "/__pycache__/" in n]
    assert "skills/catalog.yaml" in names

    try:
        module.reject_secrets([ROOT / ".env", ROOT / "README.md"])
    except RuntimeError as exc:
        assert ".env" in str(exc)
    else:
        raise AssertionError("reject_secrets accepted a credential file")


def test_writeback_protocol_binding_fails_closed() -> None:
    """Prove the shared-contract rule catches a skill that drops the link.

    The rule replaced a literal-string check that had copied the same
    bookkeeping into 33 files. A pass-fail-pass cycle shows the replacement
    still enforces the binding rather than passing vacuously.
    """
    protocol = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "references"
        / "writeback-protocol.md"
    )
    assert protocol.is_file()
    protocol_text = protocol.read_text(encoding="utf-8")
    assert (
        "| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |"
        in protocol_text
    )

    target = ROOT / "skills" / "primitives" / "falsification-first" / "SKILL.md"
    original = target.read_text(encoding="utf-8")
    assert "references/writeback-protocol.md" in original

    assert run_script("validate_repository.py").returncode == 0

    # Exercise the validator with in-memory variants. Mutating the checkout
    # races concurrent installation/hash checks and can contaminate releases.
    from scripts.validate_repository import validate_workspace_contract

    errors: list[str] = []
    validate_workspace_contract("falsification-first", target, original, errors)
    assert not errors
    changed = original.replace(
        "[writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md)",
        "the workspace contract",
    )
    validate_workspace_contract("falsification-first", target, changed, errors)
    assert any("must link to references/writeback-protocol.md" in error for error in errors)
    restored_errors: list[str] = []
    validate_workspace_contract("falsification-first", target, original, restored_errors)
    assert not restored_errors
    assert target.read_text(encoding="utf-8") == original


def test_workspace_initializer_is_additive_and_idempotent(tmp_path: Path) -> None:
    script = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "scripts"
        / "init_research_workspace.py"
    )
    preview = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--dry-run"],
        check=True,
        capture_output=True,
        text=True,
    )
    preview_receipt = json.loads(preview.stdout)
    assert preview_receipt["created"]
    assert not (tmp_path / ".research").exists()

    first = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    first_receipt = json.loads(first.stdout)
    assert first_receipt["created"]
    context = tmp_path / ".research" / "CONTEXT.md"
    original = context.read_text()
    assert "## Artifact index" in original
    assert (
        "| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |"
        in original
    )
    config = yaml.safe_load((tmp_path / ".research" / "config.yaml").read_text())
    assert config["canonical"]["templates"] == ".research/templates"
    assert config["canonical"]["plans"] == ".research/plans"

    second = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    second_receipt = json.loads(second.stdout)
    assert second_receipt["unchanged"]
    assert context.read_text() == original

    check = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--check"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert not json.loads(check.stdout)["missing"]


def test_workspace_initializer_proves_contract_markers_pass_fail_pass(
    tmp_path: Path,
) -> None:
    script = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "scripts"
        / "init_research_workspace.py"
    )
    subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    config_path = tmp_path / ".research" / "config.yaml"
    original = config_path.read_text(encoding="utf-8")
    config_path.write_text(
        original.replace('  plans: ".research/plans"\n', ""),
        encoding="utf-8",
    )

    failed = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    failed_receipt = json.loads(failed.stdout)
    assert failed.returncode == 2
    assert {
        "path": str(config_path),
        "reason": "missing-canonical-key:plans",
    } in failed_receipt["conflicts"]

    config_path.write_text(original, encoding="utf-8")
    repaired_config = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--check"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert not json.loads(repaired_config.stdout)["conflicts"]

    claims_path = tmp_path / ".research" / "evidence" / "claims.yaml"
    original_claims = claims_path.read_text(encoding="utf-8")
    claims_path.write_text(
        original_claims.replace('  - "blocked"\n', ""),
        encoding="utf-8",
    )
    failed_claims = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert failed_claims.returncode == 2
    assert {
        "path": str(claims_path),
        "reason": "claims-status-missing:blocked",
    } in json.loads(failed_claims.stdout)["conflicts"]

    claims_path.write_text(original_claims, encoding="utf-8")
    repaired_claims = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--check"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert not json.loads(repaired_claims.stdout)["conflicts"]

    context_path = tmp_path / ".research" / "CONTEXT.md"
    context_path.write_text(
        context_path.read_text(encoding="utf-8") + "\nUser-maintained note.\n",
        encoding="utf-8",
    )
    mutable_context = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--check"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert not json.loads(mutable_context.stdout)["conflicts"]

    plan_template = tmp_path / ".research" / "templates" / "research-plan.md"
    original_plan = plan_template.read_text(encoding="utf-8")
    plan_template.write_text(
        original_plan.replace("## Acceptance", "## Missing gate"),
        encoding="utf-8",
    )
    failed_template = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert failed_template.returncode == 2
    assert {
        "path": str(plan_template),
        "reason": "template-marker-missing:## Acceptance",
    } in json.loads(failed_template.stdout)["conflicts"]
    plan_template.write_text(original_plan, encoding="utf-8")


def test_workspace_initializer_refuses_nonbaseline_adapter_without_writes(
    tmp_path: Path,
) -> None:
    script = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "scripts"
        / "init_research_workspace.py"
    )
    subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    config_path = tmp_path / ".research" / "config.yaml"
    config_path.write_text(
        config_path.read_text(encoding="utf-8").replace(
            '  plans: ".research/plans"',
            '  plans: "custom/research-plans"',
        ),
        encoding="utf-8",
    )
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    preview = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--dry-run"],
        check=False,
        capture_output=True,
        text=True,
    )
    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    assert preview.returncode == 2
    assert before == after
    assert {
        "path": str(config_path),
        "reason": "nonbaseline-adapter-requires-direct-verification",
    } in json.loads(preview.stdout)["conflicts"]
    assert not (tmp_path / "custom").exists()


def test_strict_yaml_loader_rejects_duplicate_keys(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.yaml"
    duplicate.write_text("name: first\nname: second\n", encoding="utf-8")
    try:
        load_yaml_strict(duplicate)
    except yaml.YAMLError as exc:
        assert "duplicate key" in str(exc)
    else:
        raise AssertionError("duplicate YAML key was silently accepted")


def test_comparison_packet_is_deterministic_markdown_aware_and_no_op(
    tmp_path: Path,
) -> None:
    script = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "scripts"
        / "build_comparison_packet.py"
    )
    base = tmp_path / "base.md"
    target = tmp_path / "target.md"
    packet_path = tmp_path / "delta.json"
    base.write_text(
        "# Study\n\n## Claim\n\nclaim-alpha is proposed.\n\n"
        "## Table\n\n| Item | Value |\n|---|---|\n| A | 1 |\n",
        encoding="utf-8",
    )
    target.write_text(
        "# Study\n\n## Claim\n\nclaim-alpha is verified.\n\n"
        "## Table\n\n| Item | Value |\n|---|---|\n| A | 2 |\n",
        encoding="utf-8",
    )
    changed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--base",
            str(base),
            "--target",
            str(target),
            "--output",
            str(packet_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    packet = json.loads(changed.stdout)
    assert packet == json.loads(packet_path.read_text(encoding="utf-8"))
    assert packet["status"] == "changed"
    assert "claim-alpha" in [item.lower() for item in packet["changed_claim_ids"]]
    assert any("## Claim" in item for item in packet["changed_sections"])
    assert any("## Table" in item for item in packet["changed_tables"])

    repeated = subprocess.run(
        [
            sys.executable,
            str(script),
            "--base",
            str(base),
            "--target",
            str(target),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(repeated.stdout) == packet

    no_op = subprocess.run(
        [
            sys.executable,
            str(script),
            "--base",
            str(base),
            "--target",
            str(base),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    no_op_packet = json.loads(no_op.stdout)
    assert no_op_packet["status"] == "no-op"
    assert no_op_packet["changed_sections"] == []
    assert no_op_packet["changed_claim_ids"] == []
    assert no_op_packet["changed_tables"] == []


def test_prompt_ports_keep_load_bearing_matt_mechanics() -> None:
    diagnosis = (
        ROOT / "skills" / "primitives" / "research-diagnosis" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for marker in (
        "exact-symptom red-capable",
        "reproduction count and rate",
        "fast enough",
        "agent-runnable",
        "Before changing the target",
        "zero-match cleanup",
    ):
        assert marker in diagnosis

    review = (
        ROOT / "skills" / "primitives" / "research-review" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "**full-target**" in review
    assert "**comparison**" in review
    assert "changed sections, changed claim IDs, changed tables" in review
    assert "same packet ID and hash" in review
    assert "register and report a read-back `no-op`" in review

    reconciliation = (
        ROOT / "skills" / "primitives" / "artifact-reconciliation" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for marker in (
        "fact conflict",
        "human-choice conflict",
        "schema conflict",
        "execution conflict",
        "concurrent-edit conflict",
        "exactly one current pointer",
    ):
        assert marker in reconciliation

    workspace = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "SKILL.md"
    ).read_text(encoding="utf-8")
    for marker in (
        "costly to reverse",
        "surprising or unsafe without its rationale",
        "genuine trade-off",
        "downstream artifacts unambiguous",
    ):
        assert marker in workspace

    triage = (
        ROOT / "skills" / "orchestrators" / "research-triage" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for marker in (
        "**discover**",
        "**resume**",
        "concept signature",
        "`checked_at`",
        "`already-established`",
        "`out-of-scope`",
    ):
        assert marker in triage

    pilot = (
        ROOT / "skills" / "primitives" / "pilot-study" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "**empirical tracer**" in pilot
    assert "**interaction prototype**" in pilot
    assert "quarantined under the pilot ID" in pilot


def test_brief_writer_and_plan_authority_are_unambiguous() -> None:
    synthesize = (
        ROOT
        / "skills"
        / "primitives"
        / "synthesize-research-brief"
        / "SKILL.md"
    ).read_text(encoding="utf-8")
    renderer = (
        ROOT
        / "skills"
        / "primitives"
        / "render-research-deliverable"
        / "SKILL.md"
    ).read_text(encoding="utf-8")
    plan = (
        ROOT / "skills" / "orchestrators" / "to-plan" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "only writer of the canonical Research Brief" in synthesize
    assert "blocked: canonical_writer_mismatch" in renderer
    assert "never initializes the workspace or synthesizes a missing brief" in plan


def test_workpackage_claim_is_atomic_and_sealed_receipt_is_idempotent(
    tmp_path: Path,
) -> None:
    script = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "scripts"
        / "atomic_claim.py"
    )
    workpackages = tmp_path / "workpackages"
    workpackages.mkdir()
    package = workpackages / "WP-01.md"
    package.write_text("# WP-01\n", encoding="utf-8")
    package_hash = hashlib.sha256(package.read_bytes()).hexdigest()
    claim_id = f"WP-01-v0.1-{package_hash[:12]}"
    base = [
        sys.executable,
        str(script),
        "claim",
        "--state-root",
        str(workpackages),
        "--claim-id",
        claim_id,
        "--source",
        str(package),
        "--expected-sha256",
        package_hash,
    ]

    first = subprocess.run(
        [*base, "--owner", "agent-a"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(first.stdout)["status"] == "claimed"

    competing = subprocess.run(
        [*base, "--owner", "agent-b"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert competing.returncode == 3
    assert json.loads(competing.stdout)["status"] == "already-claimed"

    receipt = tmp_path / "WP-01-receipt.json"
    receipt.write_text(
        json.dumps(
            {
                "claim_id": claim_id,
                "owner": "agent-a",
                "status": "complete",
                "source_sha256": package_hash,
                "domain_verdict": "continue",
                "outputs": [],
                "checks": ["fixture"],
                "readback": {"fixture": "verified"},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    seal = subprocess.run(
        [
            sys.executable,
            str(script),
            "seal",
            "--state-root",
            str(workpackages),
            "--claim-id",
            claim_id,
            "--owner",
            "agent-a",
            "--result",
            "complete",
            "--receipt",
            str(receipt),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    sealed = json.loads(seal.stdout)
    assert sealed["status"] == "complete"
    assert Path(sealed["receipt"]).is_file()

    repeated = subprocess.run(
        [*base, "--owner", "agent-b"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(repeated.stdout)["status"] == "already-sealed"

    package.write_text("# WP-01 changed\n", encoding="utf-8")
    changed_hash = hashlib.sha256(package.read_bytes()).hexdigest()
    conflict = subprocess.run(
        [
            sys.executable,
            str(script),
            "claim",
            "--state-root",
            str(workpackages),
            "--claim-id",
            claim_id,
            "--source",
            str(package),
            "--expected-sha256",
            changed_hash,
            "--owner",
            "agent-b",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert conflict.returncode == 2
    assert json.loads(conflict.stdout)["reason"] == "terminal-version-conflict"


def test_atomic_claim_rejects_changed_source_and_archives_owner_release(
    tmp_path: Path,
) -> None:
    script = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "scripts"
        / "atomic_claim.py"
    )
    state_root = tmp_path / "state"
    state_root.mkdir()
    source = tmp_path / "decision.md"
    source.write_text("# Decision\n", encoding="utf-8")
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    claim_id = f"MAP-01-D01-{source_hash[:12]}"
    claim_command = [
        sys.executable,
        str(script),
        "claim",
        "--state-root",
        str(state_root),
        "--claim-id",
        claim_id,
        "--source",
        str(source),
        "--expected-sha256",
        source_hash,
        "--owner",
        "agent-a",
    ]
    subprocess.run(claim_command, check=True, capture_output=True, text=True)

    receipt = tmp_path / "decision-receipt.json"
    receipt.write_text(
        json.dumps(
            {
                "claim_id": claim_id,
                "owner": "agent-a",
                "status": "complete",
                "source_sha256": source_hash,
                "domain_verdict": "continue",
                "outputs": [],
                "checks": [],
                "readback": {},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    source.write_text("# Mutated decision\n", encoding="utf-8")
    changed = subprocess.run(
        [
            sys.executable,
            str(script),
            "seal",
            "--state-root",
            str(state_root),
            "--claim-id",
            claim_id,
            "--owner",
            "agent-a",
            "--result",
            "complete",
            "--receipt",
            str(receipt),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert changed.returncode == 2
    assert json.loads(changed.stdout)["reason"] == "claimed-source-changed"

    released = subprocess.run(
        [
            sys.executable,
            str(script),
            "release",
            "--state-root",
            str(state_root),
            "--claim-id",
            claim_id,
            "--owner",
            "agent-a",
            "--reason",
            "source superseded",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    released_receipt = json.loads(released.stdout)
    assert released_receipt["status"] == "released"
    assert Path(released_receipt["release_receipt"]).is_file()
    assert not (state_root / ".claims" / f"{claim_id}.claim").exists()


def test_atomic_claim_seal_and_release_share_one_terminal_cas(
    tmp_path: Path,
) -> None:
    script = (
        ROOT
        / "skills"
        / "primitives"
        / "research-workspace-contract"
        / "scripts"
        / "atomic_claim.py"
    )
    state_root = tmp_path / "state"
    state_root.mkdir()
    source = tmp_path / "WP-03.md"
    source.write_text("# WP-03\n", encoding="utf-8")
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    claim_id = f"WP-03-v0.1-{source_hash[:12]}-a01"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "claim",
            "--state-root",
            str(state_root),
            "--claim-id",
            claim_id,
            "--source",
            str(source),
            "--expected-sha256",
            source_hash,
            "--owner",
            "agent-a",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    receipt = tmp_path / "WP-03-receipt.json"
    receipt.write_text(
        json.dumps(
            {
                "claim_id": claim_id,
                "owner": "agent-a",
                "status": "complete",
                "source_sha256": source_hash,
                "domain_verdict": "continue",
                "outputs": [],
                "checks": [],
                "readback": {},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    seal_command = [
        sys.executable,
        str(script),
        "seal",
        "--state-root",
        str(state_root),
        "--claim-id",
        claim_id,
        "--owner",
        "agent-a",
        "--result",
        "complete",
        "--receipt",
        str(receipt),
    ]
    release_command = [
        sys.executable,
        str(script),
        "release",
        "--state-root",
        str(state_root),
        "--claim-id",
        claim_id,
        "--owner",
        "agent-a",
        "--reason",
        "race probe",
    ]
    seal_process = subprocess.Popen(
        seal_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    release_process = subprocess.Popen(
        release_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    seal_stdout, seal_stderr = seal_process.communicate(timeout=10)
    release_stdout, release_stderr = release_process.communicate(timeout=10)
    assert sorted([seal_process.returncode, release_process.returncode]) == [0, 4], (
        seal_stdout,
        seal_stderr,
        release_stdout,
        release_stderr,
    )

    terminal_path = state_root / ".terminals" / f"{claim_id}.json"
    terminal = json.loads(terminal_path.read_text(encoding="utf-8"))
    sealed_path = state_root / ".receipts" / f"{claim_id}.json"
    release_path = state_root / ".claim-history" / claim_id / "release.json"
    assert terminal["terminal_state"] in {"sealed", "released"}
    assert sealed_path.exists() is (terminal["terminal_state"] == "sealed")
    assert release_path.exists() is (terminal["terminal_state"] == "released")
    assert not (state_root / ".claims" / f"{claim_id}.claim").exists()


def test_installer_flattens_without_overwrite(tmp_path: Path) -> None:
    result = run_script("install_skills.py", "--target", str(tmp_path))
    assert result.returncode == 0, result.stderr
    receipt = json.loads(result.stdout)
    assert len(receipt["skills"]) == len(CATALOG["skills"])
    assert (tmp_path / "research-help" / "SKILL.md").is_file()

    repeated = run_script("install_skills.py", "--target", str(tmp_path))
    assert repeated.returncode == 0, repeated.stderr
    assert not json.loads(repeated.stdout)["conflicts"]


def test_codex_install_defaults_to_codex_home_and_verifies_all_skills(
    tmp_path: Path,
) -> None:
    codex_home = tmp_path / "codex-home"
    env = {**os.environ, "CODEX_HOME": str(codex_home)}
    target = codex_home / "skills"

    preview = run_script("install_skills.py", "--dry-run", env=env)
    assert preview.returncode == 0, preview.stderr
    preview_receipt = json.loads(preview.stdout)
    assert preview_receipt["target"] == str(target)
    assert len(preview_receipt["planned"]) == len(CATALOG["skills"])
    assert not target.exists()

    installed = run_script("install_skills.py", env=env)
    assert installed.returncode == 0, installed.stderr
    assert len(json.loads(installed.stdout)["created"]) == len(CATALOG["skills"])

    verified = run_script("verify_install.py", env=env)
    assert verified.returncode == 0, verified.stdout + verified.stderr
    assert f"INSTALL OK: {len(CATALOG['skills'])} skills" in verified.stdout


def test_claude_code_install_generates_invocation_adapter_and_verifies(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    # Path.home() uses USERPROFILE on Windows; keep this test local there too.
    env = {**os.environ, "HOME": str(home), "USERPROFILE": str(home)}
    target = home / ".claude" / "skills"

    installed = run_script("install_skills.py", "--harness", "claude-code", env=env)
    assert installed.returncode == 0, installed.stderr
    receipt = json.loads(installed.stdout)
    assert receipt["harness"] == "claude-code"
    assert receipt["target"] == str(target)
    assert len(receipt["created"]) == len(CATALOG["skills"])
    assert len(receipt["source_skills"]) == len(CATALOG["skills"])
    assert receipt["source_skills"] != receipt["skills"]

    user_skill = target / "research-auto" / "SKILL.md"
    model_skill = target / "research-review" / "SKILL.md"
    assert "disable-model-invocation: true" in user_skill.read_text()
    assert "user-invocable: false" in model_skill.read_text()
    assert "disable-model-invocation" not in (
        ROOT / "skills" / "orchestrators" / "research-auto" / "SKILL.md"
    ).read_text()

    verified = run_script(
        "verify_install.py", "--harness", "claude-code", env=env
    )
    assert verified.returncode == 0, verified.stdout + verified.stderr
    assert f"INSTALL OK: {len(CATALOG['skills'])} skills" in verified.stdout


def test_claude_code_install_rejects_symlink_mode(tmp_path: Path) -> None:
    result = run_script(
        "install_skills.py",
        "--harness",
        "claude-code",
        "--mode",
        "symlink",
        "--target",
        str(tmp_path),
    )
    assert result.returncode == 2
    assert "requires copy mode" in result.stderr
    assert list(tmp_path.iterdir()) == []


def test_install_verifier_detects_partial_or_modified_skill(tmp_path: Path) -> None:
    installed = run_script("install_skills.py", "--target", str(tmp_path))
    assert installed.returncode == 0, installed.stderr

    metadata = tmp_path / "research-auto" / "agents" / "openai.yaml"
    metadata.unlink()
    verified = run_script("verify_install.py", "--target", str(tmp_path))

    assert verified.returncode == 2
    assert "INSTALL FAILED" in verified.stdout
    assert str(metadata) in verified.stdout


def test_installer_preflights_all_conflicts_before_writing(tmp_path: Path) -> None:
    conflict = tmp_path / "research-help"
    conflict.mkdir()
    (conflict / "SKILL.md").write_text("conflicting local skill\n", encoding="utf-8")

    result = run_script("install_skills.py", "--target", str(tmp_path))
    receipt = json.loads(result.stdout)

    assert result.returncode == 2
    assert str(conflict) in receipt["conflicts"]
    assert receipt["created"] == []
    assert not (tmp_path / "research-setup").exists()
    assert not (tmp_path / ".research-os-install.json").exists()


def test_installer_preflights_marker_and_preserves_user_owned_file(
    tmp_path: Path,
) -> None:
    marker = tmp_path / ".research-os-install.json"
    original = '{"owner":"user"}\n'
    marker.write_text(original, encoding="utf-8")

    result = run_script("install_skills.py", "--target", str(tmp_path))
    receipt = json.loads(result.stdout)

    assert result.returncode == 2
    assert str(marker) in receipt["conflicts"]
    assert marker.read_text(encoding="utf-8") == original
    assert not (tmp_path / "research-help").exists()


def test_installer_symlink_mode_is_idempotent_and_receipted(tmp_path: Path) -> None:
    first = run_script(
        "install_skills.py", "--target", str(tmp_path), "--mode", "symlink"
    )
    assert first.returncode == 0, first.stderr
    first_receipt = json.loads(first.stdout)
    assert (tmp_path / "research-help").is_symlink()
    marker = json.loads(
        (tmp_path / ".research-os-install.json").read_text(encoding="utf-8")
    )
    assert marker["managed_by"] == "research-os"
    assert marker["catalog_version"] == CATALOG["version"]
    assert marker["source_commit"]
    assert first_receipt["created"]

    repeated = run_script(
        "install_skills.py", "--target", str(tmp_path), "--mode", "symlink"
    )
    assert repeated.returncode == 0, repeated.stderr
    repeated_receipt = json.loads(repeated.stdout)
    assert repeated_receipt["marker"] == "preserved"
    assert not repeated_receipt["conflicts"]

    verified = run_script("verify_install.py", "--target", str(tmp_path))
    assert verified.returncode == 0, verified.stdout + verified.stderr
