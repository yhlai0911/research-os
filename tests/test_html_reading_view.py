"""Executable export/response tests; browser acceptance is recorded separately."""
from __future__ import annotations
from copy import deepcopy
from decimal import Decimal
import base64
import functools
import hashlib
import http.server
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import threading

import pytest

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/primitives/render-research-deliverable'

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

renderer=load('reading_renderer',SKILL/'scripts/render_reading_view.py')
delivery=load('reading_delivery',SKILL/'scripts/build_reading_reply.py')

@pytest.fixture
def source():
    return {'title':'檢視已計算結果','summary':'比較同樣期間的誤差。','sources':[{'label':'已核對的研究結果','note':'測試資料；無母體推論。'}],
            'table':{'title':'比較表','columns':[{'key':'name','label':'方法','type':'text'},
                {'key':'value','label':'誤差','type':'number','unit':'百分點','decimals':3}],
                'rows':[{'name':'甲','value':Decimal('0.20624999999999993')},{'name':'乙','value':Decimal('0.677083333333334')}]},
            'chart':{'title':'同期間誤差','label_key':'name','value_key':'value'},
            'excerpt':{'title':'結果','text':'甲的誤差較小。','highlights':['較小']},
            'revision':{'before':'尚未比較。','after':'甲的誤差較小。'}}

def data_from(page):
    return json.loads(re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',page,re.S).group(1))

def test_numeric_precision_and_display_are_separate(source):
    p=renderer.prepare(source);cells=[r['cells']['value'] for r in p['rows']]
    assert cells[0]['raw']=='0.20624999999999993' and cells[0]['display']=='0.206'
    assert cells[1]['raw']=='0.677083333333334' and cells[1]['display']=='0.677'
    assert cells[0]['rank']<cells[1]['rank']
    source['table']['rows']=[{'name':'large','value':Decimal('9007199254740993')},{'name':'small','value':Decimal('9007199254740992')}]
    p=renderer.prepare(source)
    assert p['rows'][0]['cells']['value']['rank']>p['rows'][1]['cells']['value']['rank']

def test_display_rounding_does_not_sort_equal_rounded_observations_as_ties(source):
    source['table']['rows']=[{'name':'a','value':Decimal('1.00004')},{'name':'b','value':Decimal('1.00003')}]
    p=renderer.prepare(source);a,b=[r['cells']['value'] for r in p['rows']]
    assert a['display']==b['display']=='1.000' and a['rank']>b['rank']

def test_missing_and_empty_do_not_fabricate_observations(source):
    source['table']['rows']=[{'name':'missing','value':None},{'name':'absent'},{'name':'zero','value':0}]
    p=data_from(renderer.render(source));a,b,c=[r['cells']['value'] for r in p['rows']]
    assert a['missing'] and b['missing'] and a['raw'] is None
    assert c['numeric']==0 and not c['missing']
    source['table']['rows']=[]
    assert data_from(renderer.render(source))['rows']==[]

@pytest.mark.parametrize('number',[float('nan'),float('inf'),True,'not a number'])
def test_invalid_numbers_fail_before_output(source,number):
    source['table']['rows'][0]['value']=number
    with pytest.raises(ValueError):renderer.render(source)

def test_units_and_unique_columns_are_required(source):
    bad=deepcopy(source);bad['table']['columns'][1].pop('unit')
    with pytest.raises(ValueError,match='unit'):renderer.render(bad)
    bad=deepcopy(source);bad['table']['columns'].append(bad['table']['columns'][0])
    with pytest.raises(ValueError,match='unique'):renderer.render(bad)

def test_revision_uses_only_two_supplied_versions(source):
    p=renderer.prepare(source)['revision']
    assert ''.join(x['text'] for x in p['before'])==source['revision']['before']
    assert ''.join(x['text'] for x in p['after'])==source['revision']['after']
    source.pop('revision')
    assert renderer.prepare(source)['revision'] is None
    source['revision']={'before':'one version'}
    with pytest.raises(ValueError,match='both'):renderer.render(source)

def test_identical_revision_is_not_labelled_as_changed(source):
    source['revision']={'before':'未改動','after':'未改動'}
    assert renderer.prepare(source)['revision']['identical'] is True

@pytest.mark.parametrize('url',['javascript:alert(1)','data:text/html,evil','file:///private','https://user:secret@example.org'])
def test_unsafe_source_urls_are_not_rendered(source,url):
    source['sources'][0]['url']=url
    with pytest.raises(ValueError):renderer.render(source)

def test_untrusted_strings_cannot_break_out_of_json_or_markup(source):
    attack='</script><img src="https://example.org/track" onerror="alert(1)">'
    source['title']=attack;source['table']['rows'][0]['name']=attack
    source['excerpt']['text']=attack;source['excerpt']['highlights']=[attack]
    page=renderer.render(source)
    assert '<img' not in page and page.count('<script')==2
    assert data_from(page)['title']==attack
    assert data_from(page)['rows'][0]['cells']['name']['raw']==attack
    # Hashes independently checked against actual executable and CSS bytes.
    for expression,tag in [(r'<style>(.*?)</style>','style'),(r'<script id="reading-app">(.*?)</script>','script')]:
        body=re.search(expression,page,re.S).group(1)
        digest=base64.b64encode(hashlib.sha256(body.encode()).digest()).decode()
        assert f"{tag}-src 'sha256-{digest}'" in page
    assert "connect-src 'none'" in page and 'innerHTML' not in page

def test_cli_refuses_overwrite_and_invalid_data_leaves_no_artifact(tmp_path,source):
    src=tmp_path/'source.json';src.write_text(json.dumps(source,default=str),encoding='utf-8')
    output=tmp_path/'view.html';output.write_text('user artifact',encoding='utf-8')
    p=subprocess.run([sys.executable,str(SKILL/'scripts/render_reading_view.py'),'--input',str(src),'--output',str(output)],capture_output=True,text=True)
    assert p.returncode==2 and output.read_text()=='user artifact'
    source['table']['columns'][1].pop('unit');src.write_text(json.dumps(source,default=str),encoding='utf-8')
    absent=tmp_path/'absent.html'
    p=subprocess.run([sys.executable,str(SKILL/'scripts/render_reading_view.py'),'--input',str(src),'--output',str(absent)],capture_output=True,text=True)
    assert p.returncode==2 and not absent.exists()

def test_reply_missing_or_not_yet_generated_is_not_success(tmp_path):
    reply=tmp_path/'reply.md'
    p=subprocess.run([sys.executable,str(SKILL/'scripts/build_reading_reply.py'),'--artifact',str(tmp_path/'absent.html'),'--next-step','先產生閱讀頁','--output',str(reply)],capture_output=True,text=True)
    assert p.returncode==2 and not reply.exists()
    assert json.loads(p.stdout)['usable_link'] is False

def test_local_reply_reuses_actual_title_summary_and_marks_scope(tmp_path,source):
    artifact=tmp_path/'real view.html';artifact.write_text(renderer.render(source),encoding='utf-8')
    reply=delivery.build_reply(artifact,'先比較誤差。')
    assert source['summary'] in reply['markdown'] and source['title'] in reply['markdown']
    assert artifact.resolve().as_posix() in reply['markdown'] and '這份檔案的電腦' in reply['scope']
    assert '<a href=' in reply['response_html']

@pytest.fixture
def local_server(tmp_path):
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(tmp_path))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    yield f'http://127.0.0.1:{server.server_port}'
    server.shutdown();server.server_close();worker.join(timeout=2)

def test_loopback_reply_requires_exact_target_bytes(tmp_path,source,local_server):
    artifact=tmp_path/'real.html';artifact.write_text(renderer.render(source),encoding='utf-8')
    (tmp_path/'wrong.html').write_text('wrong document',encoding='utf-8')
    assert delivery.build_reply(artifact,'看表格',local_server+'/real.html')['target'].endswith('/real.html')
    for url in [local_server+'/wrong.html',local_server+'/missing.html','https://example.org/view.html']:
        with pytest.raises(ValueError):delivery.build_reply(artifact,'看表格',url)

def test_clean_install_includes_working_renderer_reply_and_template(tmp_path,source):
    target=tmp_path/'project/.agents/skills'
    p=subprocess.run([sys.executable,str(ROOT/'scripts/install_skills.py'),'--target',str(target)],capture_output=True,text=True,encoding='utf-8')
    assert p.returncode==0,p.stdout+p.stderr
    installed=target/'render-research-deliverable'
    src=tmp_path/'project/input.json';src.write_text(json.dumps(source,default=str),encoding='utf-8')
    output=tmp_path/'project/reading.html'
    p=subprocess.run([sys.executable,str(installed/'scripts/render_reading_view.py'),'--input',str(src),'--output',str(output)],capture_output=True,text=True,encoding='utf-8')
    assert p.returncode==0,p.stdout+p.stderr
    reply=tmp_path/'project/reply.md'
    p=subprocess.run([sys.executable,str(installed/'scripts/build_reading_reply.py'),'--artifact',str(output),'--next-step','讀取這份比較。','--output',str(reply)],capture_output=True,text=True,encoding='utf-8')
    assert p.returncode==0,p.stdout+p.stderr
    assert source['summary'] in reply.read_text(encoding='utf-8')
    p=subprocess.run([sys.executable,str(ROOT/'scripts/verify_install.py'),'--target',str(target)],capture_output=True,text=True,encoding='utf-8')
    assert p.returncode==0,p.stdout+p.stderr
