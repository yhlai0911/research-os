"""Install into clean projects and read dependencies, beyond header/hash checks."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import install_skills as installer
from scripts.skill_links import dependency_errors,rebase_markdown

def run(script,*args):
    return subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],
                          capture_output=True,text=True,encoding='utf-8')

@pytest.mark.parametrize('harness',['codex','claude-code'])
def test_clean_flat_install_reads_every_local_markdown_dependency(tmp_path,harness):
    target=tmp_path/'project/.agents/skills'
    source=ROOT/'skills/orchestrators/research-1-grill/SKILL.md';before=source.read_bytes()
    result=run('install_skills.py','--target',target,'--harness',harness)
    assert result.returncode==0,result.stdout+result.stderr
    read_count=0
    # Independent oracle: resolve and actually open each installed link. This
    # catches failures even if the production validator shares an adapter bug.
    for folder in target.iterdir():
        if not folder.is_dir():continue
        assert (folder/'SKILL.md').is_file()
        for file in folder.rglob('*.md'):
            for raw in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',file.read_text(encoding='utf-8')):
                parts=urlsplit(raw.strip('<>'))
                if parts.scheme or parts.netloc or not parts.path:continue
                linked=(file.parent/unquote(parts.path)).resolve()
                assert linked.is_relative_to(target.resolve()),(file,raw)
                assert linked.is_file(),(file,raw)
                assert linked.read_bytes(),(file,raw)
                read_count+=1
    assert read_count>0
    assert source.read_bytes()==before
    assert run('verify_install.py','--target',target,'--harness',harness).returncode==0
    repeated=run('install_skills.py','--target',target,'--harness',harness)
    assert repeated.returncode==0,repeated.stdout+repeated.stderr
    assert json.loads(repeated.stdout)['marker']=='preserved'

def test_reference_style_fragment_and_encoded_path_are_rebased(tmp_path):
    a=tmp_path/'skills/orchestrators/a';b=tmp_path/'skills/primitives/b'
    a.mkdir(parents=True);(b/'references').mkdir(parents=True)
    guide=b/'references/a guide.md';guide.write_text('# Heading',encoding='utf-8')
    text='[guide]: ../../primitives/b/references/a%20guide.md#heading\n'
    rewritten=rebase_markdown(text,a/'SKILL.md',[a,b])
    assert rewritten=='[guide]: ../b/references/a%20guide.md#heading\n'
    flat=tmp_path/'installed';(flat/'a').mkdir(parents=True);(flat/'b/references').mkdir(parents=True)
    (flat/'a/SKILL.md').write_text(rewritten,encoding='utf-8')
    (flat/'b/references/a guide.md').write_bytes(guide.read_bytes())
    assert not dependency_errors(flat/'a',[flat])
    (flat/'b/references/a guide.md').unlink()
    assert 'missing/unreadable dependency' in dependency_errors(flat/'a',[flat])[0]

def test_bad_source_dependency_stops_before_creating_install(tmp_path,monkeypatch,capsys):
    source=tmp_path/'skills/primitives/a';source.mkdir(parents=True)
    (source/'SKILL.md').write_text('---\nname: a\ndescription: Test.\n---\n[Missing](references/absent.md)\n',encoding='utf-8')
    catalog={'version':'test','skills':[{'name':'a','bucket':'primitives','invocation':'model'}]}
    target=tmp_path/'output/.agents/skills'
    monkeypatch.setattr(installer,'packaged_roots',lambda:[source])
    monkeypatch.setattr(installer,'profile_settings',lambda _p:(catalog,tmp_path/'skills','.marker.json'))
    monkeypatch.setattr(installer,'parse_args',lambda:argparse.Namespace(target=target,harness='codex',profile='core',mode='copy',dry_run=False))
    assert installer.main()==2
    report=json.loads(capsys.readouterr().out)
    assert report['dependency_errors'] and 'absent.md' in report['dependency_errors'][0]
    assert not target.exists()

def test_missing_installed_shared_file_has_located_dependency_error(tmp_path):
    target=tmp_path/'project/.agents/skills'
    assert run('install_skills.py','--target',target).returncode==0
    (target/'research-workspace-contract/references/writeback-protocol.md').unlink()
    result=run('verify_install.py','--target',target)
    assert result.returncode==2
    assert 'research-1-grill' in result.stdout and 'missing/unreadable dependency' in result.stdout

def test_symlink_expected_hash_preserves_source_layout():
    source=ROOT/'skills/orchestrators/research-1-grill'
    assert installer.expected_tree_hash(source,'user','codex',mode='symlink')==installer.tree_hash(source)
    assert not dependency_errors(source,installer.packaged_roots())
