"""Verify visible glyph coverage, offline assets, source identity and measured timing.

uv run --with fonttools python scripts/verify_assets.py [visual-draft]
"""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from fontTools.ttLib import TTFont

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[2]

class Text(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.text=[];self.remote=[]
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style']:self.skip+=1
        for name,value in attrs:
            if name in ['src','href'] and value and value.startswith(('http:','https:')):self.remote.append(value)
    def handle_endtag(self,tag):
        if tag in ['script','style']:self.skip=max(0,self.skip-1)
    def handle_data(self,data):
        if not self.skip:self.text.append(data)

def main():
    project=HERE/sys.argv[1] if len(sys.argv)>1 else HERE
    expected=json.loads((HERE/'scenes.json').read_text())['source_commit']
    actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    subprocess.run(['git','merge-base','--is-ancestor',expected,'HEAD'],cwd=ROOT,check=True)
    assert not subprocess.check_output(['git','diff',expected,'--name-only','--','skills','profiles'],cwd=ROOT,text=True).strip()
    glyphs=set();assets=[]
    for font in (HERE/'assets/fonts').glob('Research*'):
        obj=TTFont(font);glyphs.update(obj.getBestCmap());obj.close()
        assets.append({'path':str(font.relative_to(HERE)),'bytes':font.stat().st_size,'sha256':hashlib.sha256(font.read_bytes()).hexdigest()})
    visible=[];html_files=[project/'index.html',*sorted((project/'compositions').glob('*.html'))]
    for path in html_files:
        parser=Text();source=path.read_text();parser.feed(source)
        assert not parser.remote,(path,parser.remote)
        visible+=parser.text
    visible+=[s['text'] for s in json.loads((HERE/'narration-v3.json').read_text())['scenes']]
    missing=sorted({c for c in ''.join(visible) if not c.isspace() and ord(c) not in glyphs})
    assert not missing,'Missing font glyphs: '+''.join(missing)
    timeline=json.loads((project/'timeline.json').read_text())
    cursor=0
    for s in timeline['scenes']:
        assert s['start_frame']==cursor;cursor+=s['frame_count']
        assert abs(s['start']-s['start_frame']/30)<1e-6
        if timeline['status']!='visual-draft':
            path=project/s['audio'];assert hashlib.sha256(path.read_bytes()).hexdigest()==s['audio_sha256']
    assert cursor==timeline['total_frames']
    report={'ok':True,'source_commit':expected,'checkout_head':actual,'html_files':len(html_files),'visible_characters_checked':len(''.join(visible)),
            'missing_glyphs':missing,'remote_render_assets':[],'total_frames':cursor,'assets':assets,
            'status':timeline['status']}
    target=(HERE if timeline['status']=='visual-draft' else project)/'evidence'/('assets-visual-draft.json' if timeline['status']=='visual-draft' else 'assets-production.json')
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False)[:500])

if __name__=='__main__':main()
