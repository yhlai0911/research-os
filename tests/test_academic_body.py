"""Observable contrasts: keep statistical substance, locate implementation leaks."""
from pathlib import Path
import importlib.util
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/primitives/research-writing/scripts/check_academic_body.py'
spec=importlib.util.spec_from_file_location('academic_body',SCRIPT);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def test_preserves_disciplinary_methods_and_null_evidence():
    text='# Methods\nMonthly log returns are estimated by OLS with HAC standard errors.\nVar(r)=Var(s)+Var(f)+2Cov(s,f). The paired block bootstrap uses 6-month blocks and 5,000 replications.\nThe defined mathematical symbol $r_t$ denotes the monthly return.\n## Results\nThe interaction p=.767 does not support different slopes.\n'
    assert module.check(text)==[]

def test_locates_implementation_without_rewriting_the_source(tmp_path):
    source=tmp_path/'paper.md';text='# Results\nWe call `fit()` on r_FX, write 05_results/results.json, then run pytest with seed=20261023.\n';source.write_text(text,encoding='utf-8')
    run=subprocess.run([sys.executable,str(SCRIPT),str(source)],capture_output=True,text=True)
    assert run.returncode==1 and source.read_text(encoding='utf-8')==text
    hits=module.check(text);assert all(x['line']==2 and x['section']=='Results' for x in hits)
    assert {'inline-code','code-identifier','source-file','filesystem-path','workflow','reproducibility-metadata'}<=set(x['category'] for x in hits)

def test_companion_and_reference_destinations_are_not_body():
    text='# Methods\nMonthly exchange rates use the final valid quote; no missing quotes are imputed.\n![Figure](../05_results/figures/figure.png)\n## References\nSource [data](https://example.org/data.csv).\n## 技術附錄\nPython reads a CSV with read_csv().\n'
    assert module.check(text)==[]

def test_narrow_research_object_exception_does_not_hide_other_leaks():
    text='# Methods\nWe study Python as a programming-language intervention. Results are in results.json.\n'
    hits=module.check(text,('Python',))
    assert all(x['match']!='Python' for x in hits)
    assert any(x['match']=='results.json' for x in hits)

def test_code_block_in_body_is_located():
    hits=module.check('# Methods\n```python\nprint(1)\n```\n')
    assert any(x['category']=='code-block' and x['line']==2 for x in hits)
