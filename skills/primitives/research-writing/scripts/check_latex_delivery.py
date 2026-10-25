#!/usr/bin/env python3
"""Read-only consistency check, not a compiler or scholarly-quality certificate."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ENGINES = {'xelatex': r'XeTeX', 'lualatex': r'Lua(?:HB)?TeX',
           'pdflatex': r'pdfTeX', 'tectonic': r'(?:Tectonic|XeTeX)'}
FATAL = re.compile(
    r'undefined (?:citations?|references?)|(?:Citation|Reference)\s+[^\n]*undefined'
    r'|Missing character:|missing glyph|There were undefined'
    r'|Please\s+\(re\)run\s+(?:Biber|BibTeX|LaTeX)|Please rerun\s+(?:Biber|BibTeX|LaTeX)'
    r'|Label\(s\) may have changed|multiply[- ]defined labels|multiply defined'
    r'|(?:^|\n)!\s|Fatal error occurred|Emergency stop|I couldn.t open database file'
    r'|Cannot find.*\.bib|I didn.t find a database entry|ERROR\s*-', re.I)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def check(root: Path, receipt: dict) -> list[dict[str, str]]:
    root=root.resolve(); findings=[]
    def fail(code, detail): findings.append({'code':code,'detail':str(detail)})
    def local(name):
        p=Path(name)
        if p.is_absolute() or '..' in p.parts:
            raise ValueError(f'not a project-relative path: {name}')
        target=(root/p).resolve()
        if not target.is_relative_to(root):
            raise ValueError(f'path leaves project: {name}')
        return target
    def verify(name, digest):
        p=local(name)
        if not p.is_file(): fail('missing-file',name);return None
        data=p.read_bytes()
        if sha(data)!=digest: fail('hash-mismatch',name)
        return data
    try:
        if receipt['schema_version']!=1: fail('schema','expected version 1')
        inputs=receipt['inputs'];main=receipt['main'];pdf_name=receipt['pdf']
        if not isinstance(inputs,dict) or not inputs: raise ValueError('inputs must be a nonempty hash map')
        if main not in inputs or Path(main).suffix.lower()!='.tex': fail('main-source','main .tex must be pinned')
        if not any(Path(p).suffix.lower()=='.bib' for p in inputs): fail('bibliography','managed .bib input missing')
        source_bytes={name:verify(name,digest) for name,digest in inputs.items()}
        build=receipt['build'];engine=build['engine']
        if not isinstance(engine,str): raise ValueError('engine must be a string')
        engine=engine.lower()
        if engine not in ENGINES: fail('compiler','unrecognised LaTeX engine')
        if build['exit_code']!=0: fail('compile-failed','nonzero compiler exit')
        command=build['command']
        if not isinstance(command,list) or not command or not all(isinstance(x,str) for x in command):
            fail('build-command','record the actual command argument list')
        else:
            executable=Path(command[0].replace('\\','/')).stem.lower()
            # A native engine can load an explicit LaTeX format without a launcher.
            explicit_xelatex=(engine=='xelatex' and executable=='xetex'
                and '-progname=xelatex' in command
                and any(arg.startswith('-fmt=')
                    and Path(arg[5:].replace('\\','/')).name.lower()=='xelatex.fmt'
                    for arg in command[1:]))
            if executable not in {*ENGINES,'latexmk'} and not explicit_xelatex:
                fail('build-command','not a supported LaTeX build command')
        logs=build['logs']
        if not isinstance(logs,dict) or not logs: raise ValueError('real build logs required')
        texts=[]
        for name,digest in logs.items():
            data=verify(name,digest)
            if data is not None: texts.append(data.decode('utf-8',errors='replace'))
        text='\n'.join(texts)
        if engine in ENGINES and not re.search(ENGINES[engine],text,re.I): fail('compiler-log','matching compiler banner missing')
        if not re.search(r'(?:Output written on|Writing)[^\n]*'+re.escape(Path(pdf_name).name),text,re.I):
            fail('compiler-log','PDF output message missing')
        for match in FATAL.finditer(text): fail('unresolved-diagnostic',match.group().strip())
        pdf=verify(pdf_name,build['pdf_sha256'])
        if pdf is not None and not pdf.startswith(b'%PDF-'): fail('pdf','invalid PDF signature')
        package=receipt['source_package'];package_data=verify(package['path'],package['sha256'])
        if package_data is not None:
            with zipfile.ZipFile(local(package['path'])) as archive:
                for name,data in source_bytes.items():
                    arc_name=Path(name).as_posix()
                    if arc_name not in archive.namelist(): fail('package-input-missing',name)
                    elif data is not None and archive.read(arc_name)!=data: fail('package-input-stale',name)
        reviews=receipt['reviews']
        for kind in ('academic','citations','visual'):
            review=reviews[kind];verify(review['path'],review['sha256'])
            if review['status']!='complete' or review['unresolved_material_findings']!=0:
                fail('review-unresolved',kind)
            if kind=='visual':
                if review['pdf_sha256']!=build['pdf_sha256']: fail('stale-review',kind)
            elif review['input_hashes']!=inputs: fail('stale-review',kind)
    except (KeyError,TypeError,ValueError,OSError,zipfile.BadZipFile) as error:
        fail('invalid-or-incomplete-receipt',error)
    return findings

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=Path);parser.add_argument('receipt',type=Path)
    args=parser.parse_args()
    try: findings=check(args.project,json.loads(args.receipt.read_text(encoding='utf-8')))
    except (ValueError,OSError) as error: findings=[{'code':'receipt-read','detail':str(error)}]
    print(json.dumps({'status':'needs-review' if findings else 'mechanical-checks-pass','findings':findings,
        'limits':'Does not compile, establish authentic execution, assess scholarly depth, verify bibliography online, or certify readiness.'},ensure_ascii=False,indent=2))
    return 1 if findings else 0

if __name__=='__main__': raise SystemExit(main())
