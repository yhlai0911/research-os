"""Synthetic receipts test mechanical gates; none is a real TeX build receipt."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import zipfile
import pytest

SCRIPT=Path(__file__).resolve().parents[1]/'skills/primitives/research-writing/scripts/check_latex_delivery.py'
spec=importlib.util.spec_from_file_location('latex_delivery',SCRIPT)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
sha=lambda b:hashlib.sha256(b).hexdigest()

@pytest.fixture
def project(tmp_path):
    files={'main.tex':b'\\documentclass{article}\n\\begin{document}Synthetic unit fixture.\\end{document}\n',
           'references.bib':b'@misc{fixture,title={Synthetic test fixture}}\n',
           'BUILD.md':b'Synthetic metadata fixture; not an actual compilation.\n'}
    for name,data in files.items(): (tmp_path/name).write_bytes(data)
    inputs={n:sha(b) for n,b in files.items()}
    log=b'This is XeTeX (synthetic unit-test log)\nOutput written on main.pdf (1 page).\n'
    (tmp_path/'main.log').write_bytes(log)
    pdf=b'%PDF-1.4\nsynthetic signature fixture, not a real compiled document\n'
    (tmp_path/'main.pdf').write_bytes(pdf)
    with zipfile.ZipFile(tmp_path/'source.zip','w') as z:
        for name,data in files.items(): z.writestr(name,data)
    reviews={}
    for kind in ('academic','citations','visual'):
        data=f'Synthetic {kind} review for integrity checks only.'.encode()
        name=f'{kind}.md';(tmp_path/name).write_bytes(data)
        reviews[kind]={'path':name,'sha256':sha(data),'status':'complete','unresolved_material_findings':0}
        reviews[kind].update({'pdf_sha256':sha(pdf)} if kind=='visual' else {'input_hashes':inputs.copy()})
    receipt={'schema_version':1,'main':'main.tex','pdf':'main.pdf','inputs':inputs,
             'build':{'engine':'xelatex','command':['latexmk','-xelatex','main.tex'],'exit_code':0,
                      'logs':{'main.log':sha(log)},'pdf_sha256':sha(pdf)},
             'source_package':{'path':'source.zip','sha256':sha((tmp_path/'source.zip').read_bytes())},'reviews':reviews}
    return tmp_path,receipt

def codes(project): return {x['code'] for x in module.check(*project)}

def test_consistent_synthetic_receipt_passes_only_mechanical_checks(project):
    assert module.check(*project)==[]

@pytest.mark.parametrize('diagnostic',[
    "LaTeX Warning: Citation 'missing' undefined on input line 8.",
    "LaTeX Warning: Reference `eq:missing' undefined.",
    'There were undefined references.',
    'Missing character: There is no 中 in font cmr10!',
    'Package biblatex Warning: Please (re)run Biber on the file.',
    'Label(s) may have changed. Rerun to get cross-references right.',
    'LaTeX Warning: Label eq:model multiply defined.',
    "Warning--I didn't find a database entry for missing",
    'Package biblatex Warning: Please rerun LaTeX.',
])
def test_final_diagnostics_cannot_pass_even_with_success_exit(project,diagnostic):
    root,r=project;path=root/'main.log';path.write_text(path.read_text()+diagnostic,encoding='utf-8')
    r['build']['logs']['main.log']=sha(path.read_bytes())
    assert 'unresolved-diagnostic' in codes(project)

def test_changed_bibliography_invalidates_hash_and_review(project):
    root,r=project;(root/'references.bib').write_text('@misc{changed,title={Unreviewed}}',encoding='utf-8')
    assert 'hash-mismatch' in codes(project)
    r['inputs']['references.bib']=sha((root/'references.bib').read_bytes())
    assert {'stale-review','package-input-stale'}<=codes(project)

def test_word_conversion_is_not_a_latex_build(project):
    _,r=project;r['build'].update(engine='word',command=['soffice','--convert-to','pdf'])
    assert {'compiler','build-command'}<=codes(project)


def test_native_xetex_requires_explicit_xelatex_format_and_program(project):
    _,r=project
    r['build']['command']=[r'C:\TeX\xetex.exe',r'-fmt=C:\project\xelatex.fmt',
                           '-progname=xelatex','main.tex']
    assert module.check(*project)==[]
    r['build']['command'].remove('-progname=xelatex')
    assert 'build-command' in codes(project)
    r['build']['command']=['xetex','-fmt=plain.fmt','-progname=xelatex','main.tex']
    assert 'build-command' in codes(project)

def test_missing_or_failed_compile_is_not_completion(project):
    _,r=project;r['build']['exit_code']=1;r['build']['logs']={}
    assert {'compile-failed','invalid-or-incomplete-receipt'}<=codes(project)

def test_old_pdf_review_does_not_cover_new_pdf(project):
    _,r=project;r['reviews']['visual']['pdf_sha256']='0'*64
    assert 'stale-review' in codes(project)

def test_audit_completed_with_negative_findings_is_not_a_pass(project):
    _,r=project;r['reviews']['citations']['unresolved_material_findings']=1
    assert 'review-unresolved' in codes(project)

def test_source_package_must_include_pinned_inputs(project):
    root,r=project
    with zipfile.ZipFile(root/'source.zip','w') as z:z.writestr('main.tex',(root/'main.tex').read_bytes())
    r['source_package']['sha256']=sha((root/'source.zip').read_bytes())
    assert 'package-input-missing' in codes(project)

def test_receipt_cannot_probe_outside_project(project):
    _,r=project;r['main']='../outside.tex';r['inputs']={'../outside.tex':'0'*64}
    assert 'invalid-or-incomplete-receipt' in codes(project)

def test_cli_reports_missing_evidence_without_mutating_sources(project):
    root,r=project;del r['build']
    receipt=root/'receipt.json';receipt.write_text(json.dumps(r),encoding='utf-8')
    before={p.name:p.read_bytes() for p in root.iterdir() if p.is_file()}
    result=subprocess.run([sys.executable,str(SCRIPT),str(root),str(receipt)],capture_output=True,text=True)
    report=json.loads(result.stdout)
    assert result.returncode==1 and report['status']=='needs-review'
    assert any(x['code']=='invalid-or-incomplete-receipt' for x in report['findings'])
    assert before=={p.name:p.read_bytes() for p in root.iterdir() if p.is_file()}
