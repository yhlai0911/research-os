"""Build one timeline from the storyboard and measured NEW narration audio.

--visual-draft writes a clearly labelled, silent design preview to visual-draft/.
It never writes the production index, timing manifest, or delivery MP4.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import math
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
E = html.escape
FPS = 30
TAIL_FRAMES = 8

CSS = '''
*{box-sizing:border-box}html,body{width:100%;height:100%;margin:0;overflow:hidden;background:#0B1020;color:#F2F4E9}
@font-face{font-family:ResearchSans;src:url('assets/fonts/ResearchSans-Regular.otf')}@font-face{font-family:ResearchSans;src:url('assets/fonts/ResearchSans-Black.otf');font-weight:900}
@font-face{font-family:ResearchMono;src:url('assets/fonts/ResearchMono.ttf');font-weight:100 900}
body{font-family:ResearchSans,sans-serif}#root{position:relative;width:100%;height:100%;overflow:hidden}
.canvas{position:absolute;inset:0;background:#0B1020}.toprule{position:absolute;left:80px;right:80px;top:36px;height:2px;background:#374158}
.scene-header{position:absolute;left:80px;top:66px;right:80px}.kicker{font:24px ResearchMono,ResearchSans,monospace;letter-spacing:2px;color:#FFCE57;margin:0 0 16px}
h1{font-size:66px;line-height:1.25;font-weight:900;margin:0;letter-spacing:-1px}.scene-body{position:absolute;left:80px;top:252px;width:1760px;height:660px}
.footer{position:absolute;left:80px;right:80px;bottom:43px;display:flex;justify-content:space-between;font-size:23px;color:#98A2B8;gap:30px}
.footer span{display:block}.progress{position:absolute;left:80px;right:80px;bottom:25px;height:3px;background:#374158}.progress-fill{height:100%;width:100%;background:#FFCE57;transform-origin:left}
.panel{background:#151C30;border:2px solid #374158;border-radius:20px;padding:32px}.paper{background:#F2F4E9;color:#0B1020;border-radius:8px;padding:32px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:60px;height:100%}.stack{display:flex;flex-direction:column;gap:23px}.row{display:flex;align-items:center;gap:25px}
h2{font-size:40px;line-height:1.35;margin:0 0 22px;font-weight:900}h3{font-size:31px;margin:0 0 18px}p{font-size:31px;line-height:1.55;margin:0 0 16px}
.muted{color:#98A2B8}.amber{color:#FFCE57}.small{font-size:25px;line-height:1.5}.mono,code,pre{font-family:ResearchMono,ResearchSans,monospace;font-variant-ligatures:none}
code{font-size:28px;line-height:1.6;display:block;white-space:pre-wrap;overflow-wrap:anywhere}pre{font-size:27px;line-height:1.65;white-space:pre-wrap;margin:0;overflow-wrap:anywhere}
.big{font-size:120px;line-height:1.1;font-weight:900}.tag{display:inline-block;border:2px solid #FFCE57;color:#FFCE57;padding:8px 16px;font-size:25px;border-radius:8px;max-width:100%}
.phase{position:absolute;inset:0;opacity:0}.camera{position:absolute;inset:0;transform-origin:center}.terminal{height:100%;background:#11172A;border:2px solid #596479;border-radius:18px;overflow:hidden}
.terminal-title{background:#20283C;border-bottom:2px solid #596479;padding:18px 30px;font-size:25px;color:#F2F4E9}.terminal-content{padding:28px 40px}.terminal-line{margin-bottom:14px;font:27px/1.5 ResearchMono,ResearchSans,monospace;white-space:pre-wrap;overflow-wrap:anywhere}
.output{color:#B8D49C}.warning{color:#F3A69B}.note{font-size:27px;color:#FFCE57;margin:20px 0}.caption{position:absolute;left:160px;right:160px;bottom:80px;text-align:center;font-size:31px;line-height:1.45;background:#0B1020;padding:8px 20px}
svg{width:100%;height:100%;display:block;overflow:visible}svg text{font-family:ResearchSans,sans-serif;fill:#F2F4E9;font-size:31px}svg .sublabel{fill:#98A2B8;font-size:25px}svg .accent{fill:#FFCE57}svg .wire{fill:none;stroke:#FFCE57;stroke-width:4}svg .node{fill:#151C30;stroke:#596479;stroke-width:2}svg .minor{fill:#151C30;stroke:#596479;stroke-width:2}svg .trace{fill:none;stroke:#FFCE57;stroke-width:4;stroke-linecap:round}
.sentence{padding:18px 25px;border-bottom:2px solid #596479;font-size:29px;line-height:1.5}.field-label{display:inline-block;color:#FFCE57;width:120px;font-size:27px;vertical-align:top}.field-text{display:inline-block;max-width:1390px}.draft{position:absolute;right:70px;top:50px;font-size:24px;color:#F3A69B;background:#0B1020;padding:5px 10px}
.document-lines{display:flex;flex-direction:column;gap:16px}.document-lines i{display:block;height:11px;background:#C2C5B8;width:100%}.document-lines i:nth-child(3n){width:70%}
.overall-progress{position:absolute;left:80px;right:80px;top:36px;height:3px;background:#FFCE57;transform-origin:left;z-index:100}
.quote{font-size:43px;line-height:1.6;font-weight:900}.divider{border-top:2px solid #596479;margin:20px 0}.badge-row{display:flex;gap:24px;margin-top:25px}.badge-row .tag{font-size:28px}
'''

def node(x, y, w, h, label, sub='', cls='', dark=False):
    return (f'<g class="node-group {cls}"><rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="18"/>'
            f'<text x="{x+w/2}" y="{y+52}" text-anchor="middle">{E(label)}</text>'
            + (f'<text class="sublabel" x="{x+w/2}" y="{y+98}" text-anchor="middle">{E(sub)}</text>' if sub else '') + '</g>')

def wire(d):
    return f'<path class="trace" d="{d}"/>'

def svg(body, width=1760):
    return f'<svg viewBox="0 0 {width} 660" aria-label="研究流程示意">{body}</svg>'

def terminal(title, lines):
    return '<div class="terminal"><div class="terminal-title">'+E(title)+'</div><div class="terminal-content">'+''.join(
        f'<div class="terminal-line {kind}">{E(text)}</div>' for kind,text in lines)+'</div></div>'

def phase(content, start, end):
    return f'<div class="phase" data-enter="{start}" data-leave="{end}">{content}</div>'

def visual(scene, evidence):
    kind = scene['visual']
    def cue(prefix, fallback):
        for cap in scene.get('_captions', []):
            if cap['text'].startswith(prefix):
                return cap['start']/scene['_duration']
        return fallback
    if kind == 'comparison':
        pages=''.join(f'<i style="width:{94-i%3*14}%"></i>' for i in range(12))
        return ('<div class="cols"><div class="stack"><h2 data-pop>流暢的三十頁</h2><div class="paper" data-pop>'
                '<div class="document-lines">'+pages+'</div><p style="margin-top:22px">未知 → 仍然未知</p></div>'
                '<p class="muted" data-pop>字數增加，無法替代查證。</p></div>'
                '<div class="stack"><h2 class="amber" data-pop>可回查的研究</h2>'+svg(
                node(80,25,650,120,'問題','要判斷什麼？')+wire('M405 145 V205')+
                node(80,205,650,120,'資料與證據','真的拿得到、能支持嗎？')+wire('M405 325 V385')+
                node(80,385,650,120,'推論與限制','什麼結果會推翻它？'),850)+'</div></div>')
    if kind == 'workflow':
        labels=['逼問','鎖定','找碴','拆解','執行','審查']
        commands=['research-1-grill','research-2-brief','research-3-falsify','research-4-tasks','research-5-run','research-6-review']
        graph=''
        for i,(label,command) in enumerate(zip(labels,commands)):
            x=10+i*292
            if i<5: graph+=wire(f'M{x+238} 180 H{x+292}')
            graph+=node(x,105,238,145,f'{i+1:02d}  {label}',cls=f'step-{i}')
            graph+=f'<text x="{x+119}" y="310" text-anchor="middle" class="sublabel">{command}</text>'
        graph+=node(390,430,970,145,'手動交棒 / research-auto','每輪只處理目前最重要的下一步')
        return svg(graph)
    if kind == 'install':
        first=terminal('01 / 取得 main 與鎖定依賴',[
            ('','$ git clone --branch main https://github.com/yhlai0911/research-os.git'),
            ('','$ cd research-os'),('','$ uv sync --locked'),('output','錄製來源 source commit: '+scene['source_commit']),
            ('','示範將 --target 指向副本內的隔離 skills 目錄。')])
        second=terminal('02 / 全批預檢 → 無衝突才安裝',[
            ('','$ TARGET=.scratch/tutorial-demo/codex/skills'),
            ('','$ uv run python scripts/install_skills.py --target "$TARGET" --dry-run'),
            ('','$ uv run python scripts/install_skills.py --target "$TARGET"'),
            ('output','結果節錄自真實驗證；完整 stdout：evidence/install-transcript.json'),
            ('warning','若出現 conflicts：整批停止，先保留並處理原檔。')])
        verify=next(x['stdout'].strip().split(' at ')[0] for x in evidence if x['label']=='codex-core-verify')
        third=terminal('03 / 驗證與版本回讀',[
            ('','$ uv run python scripts/verify_install.py --target "$TARGET"'),
            ('output',verify),('','$ cat "$TARGET/.research-os-install.json"'),
            ('output','source_commit: '+scene['source_commit']),
            ('output','衝突測試：拒絕覆寫；自訂內容原樣保留。')])
        preflight=cue('接著執行',.28)
        verify_start=cue('最後執行驗證',.65)
        return phase(first,0,preflight)+phase(second,preflight,verify_start)+phase(third,verify_start,1)
    if kind == 'harness':
        commands=['uv run python scripts/install_skills.py --dry-run','uv run python scripts/install_skills.py','uv run python scripts/verify_install.py']
        actual=terminal('Claude Code：預檢、安裝、驗證，三個都加 --harness claude-code',
            [('', '$ '+x.replace(' --dry-run','')+' --harness claude-code'+(' --dry-run' if '--dry-run' in x else '')) for x in commands]+
            [('output','Codex 使用預設 harness；上段已展示完整 Codex 指令。'),('', '若使用自訂 --target，三個指令都指定相同路徑。')])
        codex='<div class="panel"><h2>Codex</h2><p class="small">切到真正的研究專案後：</p><div class="divider"></div><p class="amber" style="font-size:44px">$research-setup</p><p style="font-size:44px">$research-1-grill</p><p style="font-size:44px">$research-status</p></div>'
        claude='<div class="panel"><h2>Claude Code</h2><p class="small">切到真正的研究專案後：</p><div class="divider"></div><p class="amber" style="font-size:44px">/research-setup</p><p style="font-size:44px">/research-1-grill</p><p style="font-size:44px">/research-status</p><p class="small muted">頂層 skills 目錄新建時，重啟 session。</p></div>'
        setup=cue('先啟動 research setup' if scene.get('_paced') else '安裝完成後',.47)
        return phase(actual,0,setup)+phase('<div class="cols">'+codex+claude+'</div>',setup,1)
    if kind == 'prompt':
        fields=[('主題','生成式 AI 是否改善大學生的學習成效？'),('成果','校內研究計畫'),('受眾','校內審查委員'),('現有材料','只有題目，尚無文獻、資料或方法。'),('限制','免費資料、六個月完成、不能虛構結果。')]
        return '<div class="terminal"><div class="terminal-title">提示詞範例 / research-1-grill</div>'+''.join(
            f'<div class="sentence" data-pop><span class="field-label">{E(a)}</span><span class="field-text">{E(b)}</span></div>' for a,b in fields)+'<div class="note" style="padding-left:25px">限制會成為後續選擇與停止條件。</div></div>'
    if kind == 'decision':
        return svg(node(10,210,410,160,'這次要決定什麼？','操作示意：成果與範圍')+
            wire('M420 290 H550 V90 H680')+wire('M550 290 H680')+wire('M550 290 V490 H680')+
            node(680,20,520,140,'跨校因果評估','需要額外授權與資料',cls='discard')+
            node(680,220,520,140,'校內可行性研究','先驗證資料與測量',cls='keep')+
            node(680,420,520,140,'完整論文結果','實證尚未完成',cls='discard')+
            wire('M1200 290 H1300')+node(1300,210,440,160,'研究者決定','Agent 另查可驗證事實'))
    if kind == 'gates':
        graph=''
        for i,(a,b) in enumerate([('最接近的文獻','差異真的成立？'),('資料可得性','取用、授權、涵蓋？'),('預先反證','哪些結果推翻設計？'),('小型測試','最低成本確認可行？')]):
            x=10+i*440
            graph+=node(x,100,400,180,a,b,cls=f'gate-{i}')
            if i<3: graph+=wire(f'M{x+400} 190 H{x+440}')
        graph+=node(410,405,940,155,'通過 → tasks → run → receipt','缺資料或條件不足 → blocked，停止並說明原因')
        return svg(graph)
    if kind == 'brief':
        return '<div class="cols"><div class="paper" data-pop><h2>Research Brief</h2><p>問題 / evidence / method</p><p>限制 / 未決事項 / falsifiers</p><div class="divider"></div><p class="small mono">.research/briefs/</p><p class="small">以 config.yaml 解析實際路徑</p><p class="quote">一份研究契約</p></div><div>'+svg(
            node(15,10,790,130,'學術研究計畫','to-plan')+wire('M410 140 V190')+
            node(15,190,790,130,'補助 / 專案企劃','to-proposal')+wire('M410 320 V370')+
            node(15,370,790,180,'論文藍圖 / 草稿','to-paper；實證完成才寫結果主張'),850)+'</div></div>'
    if kind == 'profile':
        top='<div class="row" style="gap:50px;margin-bottom:30px"><div class="row" data-pop><span class="big amber">42</span><div><h2>通用核心</h2><p>跨學科，預設安裝</p></div></div><span class="big" data-pop>+</span><div class="row" data-pop><span class="big amber">1</span><div><h2>選用領域 skill</h2><p>金融與社會科學</p></div></div></div>'
        return top+'<div style="height:450px">'+terminal('同一 repository；先驗證核心，再預檢、安裝、驗證 profile',[
            ('','$ uv run python scripts/install_skills.py --profile finance-social-science --dry-run'),
            ('','$ uv run python scripts/install_skills.py --profile finance-social-science'),
            ('','$ uv run python scripts/verify_install.py --profile finance-social-science'),
            ('output','INSTALL OK: 1 skills   |   核心仍為 42'),
            ('','Claude 三指令加 --harness claude-code；自訂 --target 必須與核心相同。')])+'</div>'
    if kind == 'case':
        # Geometric mechanisms, never empirical data or fitted coefficients.
        graph=('<text x="15" y="45" class="sublabel">原始構想：物理模型全部放進金融預測</text>'+node(20,100,350,130,'波方程')+node(20,290,350,130,'熱方程')+node(20,480,350,130,'更多物理模型',cls='discard')+
               wire('M370 165 H500 V335 H660')+wire('M370 355 H660')+wire('M370 545 H500 V375 H660')+
               node(660,230,1060,170,'有限速度的阻尼傳播，能否和普通擴散區分？','先問資料能否辨識，而非宣稱模型已經驗證'))
        graph+='<path class="trace" d="M770 160 L825 160 L860 80 L895 160 L1050 160"/><text x="1190" y="135" class="sublabel">有限傳播：機制示意</text>'
        graph+='<path class="trace" d="M770 540 C850 540 850 460 925 460 S1000 540 1080 540"/><text x="1190" y="515" class="sublabel">普通擴散：機制示意</text>'
        return svg(graph)
    if kind == 'language':
        return '<div class="cols"><div class="panel"><h2 class="amber" data-pop>繁體中文討論</h2><p data-pop>請用繁體中文討論，</p><p data-pop>Research Brief 請用英文。</p><div class="divider"></div><code data-pop>$research-1-grill</code><code data-pop>.research/config.yaml</code><p class="small muted" data-pop>skill、命令、路徑不翻譯</p></div><div class="paper"><h2 data-pop>Research Brief</h2><p data-pop>Question · Evidence · Method</p><p data-pop>Limitations · Open decisions</p><div class="divider"></div><p class="quote" data-pop>Same evidence standards.</p><p class="small" data-pop>明確指定優先；否則跟隨使用者語言。</p></div></div>'
    if kind == 'status':
        return '<div class="cols"><div class="stack"><div class="badge-row" data-pop><span class="tag">conditional</span><span class="tag">blocked</span><span class="tag">stop</span></div><h2 style="font-size:56px;margin-top:35px" data-pop>不確定之處，留下來。</h2><p data-pop>目的與限制 → setup → 第一問</p><p class="amber" data-pop>完成一步，就回查研究狀態。</p></div><div class="panel"><h2>research-status</h2><p data-pop>目前：走到哪一步？</p><div class="divider"></div><p data-pop>證據：已完成與仍缺少什麼？</p><div class="divider"></div><p data-pop>下一步：哪個問題需要你決定？</p><div class="divider"></div><p class="small muted">狀態回查項目示意，非虛構完成報告。</p></div></div>'
    raise ValueError(kind)

JS = '''
(()=>{const id=__ID__,d=__DURATION__,scope=document.getElementById(id+'-stage');
const tl=gsap.timeline({paused:true});
__CLAUDE_HELPERS__
const phases=scope.querySelectorAll('.phase');
phases.forEach(p=>{let a=Number(p.dataset.enter)*d,b=Number(p.dataset.leave)*d;
tl.fromTo(p,{opacity:0},{opacity:1,duration:.12,ease:'none'},a);
if(b<d)tl.fromTo(p,{opacity:1},{opacity:0,duration:.12,ease:'none',immediateRender:false},b-.12);
const lines=p.querySelectorAll('.terminal-line');lines.forEach((el,i)=>tl.fromTo(el,{opacity:0,y:12},{opacity:1,y:0,duration:.35,ease:'power2.out'},a+.25+i*Math.min(.8,(b-a-1)/Math.max(lines.length,1))));});
const pops=scope.querySelectorAll('[data-pop]');pops.forEach((el,i)=>tl.fromTo(el,{opacity:0,y:22},{opacity:1,y:0,duration:.5,ease:i%2?'power3.out':'power2.out'},.25+i*Math.min(.38,d*.65/Math.max(pops.length,1))));
scope.querySelectorAll('.trace').forEach((p,i)=>{let len=p.getTotalLength();p.style.strokeDasharray=String(len);tl.fromTo(p,{strokeDashoffset:len},{strokeDashoffset:0,duration:Math.min(1.3,d*.08),ease:'power2.out'},.5+i*Math.min(1.2,d*.45/Math.max(scope.querySelectorAll('.trace').length,1)));});
scope.querySelectorAll('.node-group').forEach((el,i)=>tl.fromTo(el,{opacity:0},{opacity:1,duration:.5,ease:'power1.out'},.3+i*Math.min(.65,d*.35/Math.max(scope.querySelectorAll('.node-group').length,1))));
scope.querySelectorAll('.discard').forEach((el,i)=>tl.fromTo(el,{opacity:1,x:0},{opacity:.24,x:-35,duration:1,ease:'power2.inOut',immediateRender:false},d*(.48+i*.13)));
tl.fromTo('#'+id+'-progress',{scaleX:0},{scaleX:1,duration:d,ease:'none'},0);
__CUSTOM__
window.__timelines[id]=tl;})();
'''

def build(draft=False,paced=False):
    assert not (draft and paced)
    plan=json.loads((HERE/'scenes.json').read_text())
    narration=json.loads((HERE/plan['narration_source']).read_text())
    texts={s['id']:s['text'] for s in narration['scenes']}
    assert [s['id'] for s in plan['scenes']]==[s['id'] for s in narration['scenes']]
    evidence=json.loads((HERE/'evidence/install-transcript.json').read_text())
    out=HERE/'visual-draft' if draft else (HERE/'paced' if paced else HERE)
    tail_frames=4 if paced else TAIL_FRAMES
    if not draft:
        missing=[s['id'] for s in plan['scenes'] if not (HERE/f"assets/voice/scene-{s['id']}.wav").exists()]
        if missing: raise SystemExit('BLOCKED: new narration missing: '+', '.join(missing))
        if narration['status']!='approved-generated': raise SystemExit('BLOCKED: narration approval and generation receipt required')
        alignment=json.loads((HERE/('paced/alignment.json' if paced else 'alignment.json')).read_text())
        if alignment['status']!='aligned-reviewed-with-asr-crosscheck':
            raise SystemExit('BLOCKED: narration alignment needs content review')
        master_hash=hashlib.sha256((HERE/'assets/voice/full-narration-original.mp3').read_bytes()).hexdigest()
        if alignment['master_mp3_sha256']!=master_hash: raise SystemExit('BLOCKED: master audio changed')
        receipt=json.loads((HERE/'voice-source.json').read_text())
        if receipt['model_id']!=narration['model_id'] or receipt['sha256']!=master_hash:
            raise SystemExit('BLOCKED: voice model/source receipt mismatch')
        aligned={s['id']:s for s in alignment['scenes']}
    (out/'compositions').mkdir(parents=True,exist_ok=True)
    if draft or paced:
        (out/'assets').mkdir(exist_ok=True)
        shutil.copytree(HERE/'assets/fonts',out/'assets/fonts',dirs_exist_ok=True)
    shutil.copyfile(HERE/'node_modules/gsap/dist/gsap.min.js',out/'assets/gsap.min.js')
    if draft or paced: shutil.copyfile(HERE/'hyperframes.json',out/'hyperframes.json')
    helpers=(HERE/'scripts/claude-motion.js').read_text()
    slots=[];audio=[];captions=[];caption_data=[];manifest=[];start_frame=0
    for position, original in enumerate(plan['scenes']):
        s=dict(original,source_commit=plan['source_commit'])
        sid='s'+s['id'];path=HERE/f"assets/voice/scene-{s['id']}.wav" if draft else HERE/aligned[s['id']]['audio']
        if not draft:
            raw_hash=master_hash
            if hashlib.sha256(path.read_bytes()).hexdigest()!=aligned[s['id']]['sha256']:
                raise SystemExit(f'BLOCKED: audio changed after alignment {s["id"]}')
            if hashlib.sha256(texts[s['id']].encode()).hexdigest()!=aligned[s['id']]['target_text_sha256']:
                raise SystemExit(f'BLOCKED: narration changed after alignment {s["id"]}')
            probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=duration_ts,time_base','-of','json',str(path)],text=True))['streams'][0]
            exact_voice=Fraction(probe['duration_ts'])*Fraction(probe['time_base'])
            if exact_voice<=0: raise SystemExit(f'BLOCKED: zero-length audio {s["id"]}')
        else: exact_voice=Fraction(0)
        voice_duration=float(exact_voice)
        frame_count=18*FPS if draft else math.ceil(exact_voice*FPS)+tail_frames
        if not draft and frame_count<6*FPS: raise SystemExit(f'BLOCKED: audio too short for scene {s["id"]}')
        duration=frame_count/FPS;time=start_frame/FPS
        if not draft:
            s['_captions']=aligned[s['id']]['captions']
            s['_duration']=duration
            s['_paced']=paced
        content=visual(s,evidence)
        s.pop('_captions',None);s.pop('_duration',None);s.pop('_paced',None)
        # Peak and return poses focus the same evidence element, not replacement cards.
        custom=''
        if s['visual']=='install':
            custom="evidenceFocus(tl,scope,d*.68,Math.min(2.5,d*.12),1.08,0,0);"
        if s['visual']=='brief':
            custom="evidenceFocus(tl,scope,d*.50,Math.min(3,d*.15),1.08,0,0);"
        if s['visual'] in ['workflow','gates']:
            custom="flowFrontier(tl,scope.querySelectorAll('.node-group'),d*.25,d*.55);"
        if s['visual']=='comparison':
            custom="evidenceCompare(tl,scope.querySelector('.paper'),scope.querySelector('svg'),d*.48,1.0);"
        script=JS.replace('__ID__',json.dumps(sid)).replace('__DURATION__',str(duration)).replace('__CUSTOM__',custom).replace('__CLAUDE_HELPERS__',helpers)
        filename=f'compositions/{sid}.html'
        sub=(f'<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8"></head><body><template>'
             f'<style>#{sid}-root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}}</style>'
             f'<div id="{sid}-root" data-composition-id="{sid}" data-width="1920" data-height="1080" data-duration="{duration:.6f}">'
             f'<div class="canvas"></div><div class="toprule"></div><header class="scene-header"><p class="kicker">{E(s["kicker"])}</p><h1>{E(s["title"])}</h1></header>'
             f'<div class="scene-body"><div class="camera" id="{sid}-stage">{content}</div></div>'
             f'<div class="footer"><span>RESEARCH OS / {position+1:02d} OF 12</span><span>{"安裝指令＋實測結果節錄" if s["visual"] in ["install","profile"] else "教學操作與概念示意"} · 錄製來源 56159bb</span></div>'
             f'<div class="progress"><div id="{sid}-progress" class="progress-fill"></div></div>'
             +('<div class="draft">視覺草稿 · 尚未配新旁白</div>' if draft else '')+f'</div><script>{script}</script></template></body></html>')
        (out/filename).write_text(sub)
        (out/filename.replace('.html','.motion.json')).write_text(json.dumps({
            'duration':duration,'maxStaticSec':3,
            'assertions':[
                {'kind':'appearsBy','selector':f'#{sid}-stage','bySec':.2},
                {'kind':'staysInFrame','selector':f'#{sid}-progress'},
                {'kind':'keepsMoving','withinSelector':f'#{sid}-progress'}
            ]},indent=2))
        slots.append(f'<div id="host-{sid}" class="clip" data-composition-id="{sid}" data-composition-src="{filename}" data-start="{time:.6f}" data-duration="{duration:.6f}" data-track-index="1" data-width="1920" data-height="1080"></div>')
        if not draft:
            audio.append(f'<audio id="voice-{sid}" class="clip" src="assets/voice/scene-{s["id"]}.wav" data-start="{time:.6f}" data-duration="{voice_duration:.9f}" data-track-index="2" data-volume="1"></audio>')
            for cap in aligned[s['id']]['captions']:
                ci=len(captions)
                cap_start=time+cap['start'];cap_end=time+cap['end']
                captions.append(f'<div id="caption-{ci}" class="clip caption" data-start="{cap_start:.6f}" data-duration="{cap_end-cap_start:.6f}" data-track-index="3">{E(cap["text"])}</div>')
                caption_data.append(dict(cap,start=cap_start,end=cap_end,scene=s['id']))
        manifest.append(dict(s,start=round(time,6),duration=round(duration,6),start_frame=start_frame,frame_count=frame_count,voice_duration=voice_duration,text=texts[s['id']],audio=None if draft else str(path.relative_to(out)),audio_sha256=None if draft else hashlib.sha256(path.read_bytes()).hexdigest(),raw_audio_sha256=None if draft else raw_hash))
        start_frame+=frame_count
    time=start_frame/FPS
    index=f'''<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920,height=1080"><title>Research OS v3{' — 視覺草稿' if draft else ''}</title><script src="assets/gsap.min.js"></script><style>{CSS}</style></head><body><div id="root" data-composition-id="research-os-v3" data-width="1920" data-height="1080" data-duration="{time:.6f}"><div class="canvas"></div>{''.join(slots)}{''.join(audio)}{''.join(captions)}<div id="overall-progress" class="overall-progress"></div></div><script>const master=gsap.timeline({{paused:true}});master.fromTo('#overall-progress',{{scaleX:0}},{{scaleX:1,duration:{time:.6f},ease:'none'}},0);window.__timelines['research-os-v3']=master;</script></body></html>'''
    (out/'index.html').write_text(index)
    (out/'index.motion.json').write_text(json.dumps({
        'duration':time,'maxStaticSec':3,
        'assertions':[
            {'kind':'appearsBy','selector':'#s01-stage','bySec':.2},
            {'kind':'staysInFrame','selector':'#overall-progress'},
            {'kind':'keepsMoving','withinSelector':'#overall-progress'}
        ]},indent=2))
    (out/'timeline.json').write_text(json.dumps({'status':'visual-draft' if draft else 'measured-new-narration','duration':round(time,6),'total_frames':start_frame,'fps':FPS,'tail_frames':0 if draft else tail_frames,'tempo_variant':paced,'scenes':manifest},ensure_ascii=False,indent=2))
    if not draft:
        (out/'captions.json').write_text(json.dumps(caption_data,ensure_ascii=False,indent=2))
        def stamp(t):
            ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000)
            return f'{h:02d}:{m:02d}:{sec:02d},{ms:03d}'
        (out/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(caption_data))+'\n')
    story=['# Research OS v3 分鏡（由 scenes.json 與實際音訊生成）']
    script=['# 新版完整旁白（生成檢視，原始稿保留）']
    for s in manifest:
        story.append(f'\n## Frame {s["id"]}\nstatus: {"visual-draft" if draft else "animated"}\nsrc: compositions/s{s["id"]}.html\nstart: {s["start"]}\nduration: {s["duration"]}\nmotion: {", ".join(s["motion"])}\n\n{s["title"]}。{s["proof"]}')
        script.append(f'\n## {s["id"]} — {s["title"]}\n\n{s["text"]}')
    (out/'STORYBOARD.md').write_text('\n'.join(story))
    (out/'SCRIPT.md').write_text('\n'.join(script))
    print(f'{"VISUAL DRAFT ONLY" if draft else "MEASURED PRODUCTION"}: {len(manifest)} scenes, {time:.3f}s, {out}')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--visual-draft',action='store_true');parser.add_argument('--paced',action='store_true')
    args=parser.parse_args();build(args.visual_draft,args.paced)
