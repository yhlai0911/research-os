"""Actual preflight behavior; separate from fresh-agent skill followthrough."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'skills/primitives/research-assistant'
spec=importlib.util.spec_from_file_location('handoff_preflight',SOURCE/'scripts/prepare_workflow_handoff.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


def snapshot(root):
    return {str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}


def test_blank_project_reports_setup_prerequisite_without_writing(tmp_path):
    before=snapshot(tmp_path)
    result=module.prepare(tmp_path,'research-1-grill',local_writes=True)
    assert result['action']=='prerequisite' and result['required_workflow']=='research-setup'
    assert not result['executed'] and not result['native_invocation']
    assert snapshot(tmp_path)==before
    assert module.prepare(tmp_path,'research-setup',local_writes=True)['action']=='delegate'
    assert module.prepare(tmp_path,'research-setup')['action']=='guidance_only'
    assert snapshot(tmp_path)==before


def test_repaired_real_contract_allows_transfer_not_research_completion(tmp_path):
    setup=ROOT/'skills/primitives/research-workspace-contract/scripts/init_research_workspace.py'
    result=subprocess.run([sys.executable,str(setup),'--root',str(tmp_path)],capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    before=snapshot(tmp_path)
    ready=module.prepare(tmp_path,'research-1-grill',local_writes=True)
    assert ready['action']=='delegate' and ready['contract_ready']
    assert not ready['research_readiness_verified'] and not ready['executed']
    assert Path(ready['instructions']).is_file()
    assert snapshot(tmp_path)==before


def test_invalid_contract_does_not_probe_defaults_or_claim_ready(tmp_path):
    (tmp_path/'.research').mkdir()
    (tmp_path/'.research/config.yaml').write_text('canonical: {context: [wrong]}',encoding='utf-8')
    before=snapshot(tmp_path)
    result=module.prepare(tmp_path,'research-1-grill',local_writes=True)
    assert result['action']=='blocked' and not result['research_readiness_verified']
    assert snapshot(tmp_path)==before


def test_installed_transfer_inventory_and_real_instruction_dependencies(tmp_path):
    target=tmp_path/'project/.agents/skills'
    install=subprocess.run([sys.executable,str(ROOT/'scripts/install_skills.py'),'--target',str(target)],capture_output=True,text=True)
    assert install.returncode==0,install.stdout+install.stderr
    skill=target/'research-assistant'
    generated=json.loads((skill/'assets/workflow-routes.json').read_text('utf-8'))
    catalog=yaml.safe_load((ROOT/'skills/catalog.yaml').read_text('utf-8'))
    assert [x['name'] for x in generated['workflows']]==catalog['assistant_delegation']
    for row in generated['workflows']:
        result=module.prepare(tmp_path/'project',row['name'],local_writes=True,skill_dir=skill)
        assert Path(result['instructions']).is_file()
        assert not result['native_invocation'] and not result['executed']
    assert module.prepare(tmp_path,'unlisted-skill',local_writes=True)['reason']=='workflow_not_delegable'
    # Individual native mainlines remain explicit selection, not broad implicit triggers.
    policy=yaml.safe_load((target/'research-1-grill/agents/openai.yaml').read_text('utf-8'))
    assert policy['policy']['allow_implicit_invocation'] is False
