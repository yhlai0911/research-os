"""Make a faster, pitch-preserving variant from the existing approved v4 recording.

uv run --with numpy python scripts/pace_audio.py
No TTS request. Installation scenes retain their pauses and use only 1.15x.
"""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import wave
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parents[1]
OUT=HERE/'paced'

def read(path):
    with wave.open(str(path),'rb') as f:
        assert f.getframerate()==44100 and f.getnchannels()==1 and f.getsampwidth()==2
        return f.getparams(),np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy()

def write(path,params,data):
    with wave.open(str(path),'wb') as f:f.setparams(params);f.writeframes(data.astype('<i2').tobytes())

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    original=json.loads((HERE/'alignment.json').read_text())
    assert original['status']=='aligned-reviewed-with-asr-crosscheck'
    master=HERE/'assets/voice/full-narration-original.wav'
    if not master.exists():
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(HERE/'assets/voice/full-narration-original.mp3'),'-ac','1','-ar','44100','-c:a','pcm_s16le',str(master)],check=True)
    assert sha(master)==original['master_wav_sha256']
    detected=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(master),'-af','silencedetect=noise=-42dB:d=0.45','-f','null','-'],check=True,capture_output=True,text=True).stderr
    intervals=[];start=None
    for line in detected.splitlines():
        a=re.search(r'silence_start: ([0-9.]+)',line)
        b=re.search(r'silence_end: ([0-9.]+)',line)
        if a:start=float(a[1])
        if b and start is not None:intervals.append((start,float(b[1])));start=None
    (OUT/'assets/voice').mkdir(parents=True,exist_ok=True)
    (OUT/'evidence').mkdir(exist_ok=True)
    scratch=OUT/'output';scratch.mkdir(exist_ok=True)
    scenes=[];records=[]
    for scene in original['scenes']:
        params,data=read(HERE/scene['audio']);rate=params.framerate
        protected=scene['id'] in ['09','10','11'];speed=1.15 if protected else 1.18
        origin=scene['start_sample_in_master']/rate;end=scene['end_sample_in_master']/rate
        removed=[]
        if not protected:
            for a,b in intervals:
                # Only shorten the center of strict quiet intervals within a paragraph.
                # Keep 180 ms at each edge; never cut a paragraph boundary or a word.
                if a>=origin+.15 and b<=end-.15 and b-a>.45:
                    lo=round((a-origin+.18)*rate);hi=round((b-origin-.18)*rate)
                    if hi>lo:removed.append((lo,hi))
        parts=[];cursor=0
        for a,b in removed:parts.append(data[cursor:a]);cursor=b
        parts.append(data[cursor:]);condensed=np.concatenate(parts)
        temp=scratch/f'quiet-trimmed-{scene["id"]}.wav';write(temp,params,condensed)
        target=OUT/f'assets/voice/scene-{scene["id"]}.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(temp),'-af',f'atempo={speed}','-c:a','pcm_s16le',str(target)],check=True)
        _,paced=read(target);duration=len(paced)/rate
        assert abs(duration-len(condensed)/rate/speed)<.08
        effective=len(condensed)/len(paced)
        def mapped(time):
            sample=round(time*rate)
            cut=sum(max(0,min(sample,b)-a) for a,b in removed if sample>a)
            return min(duration,max(0,(sample-cut)/rate/effective))
        caps=[]
        for cap in scene['captions']:
            a,b=mapped(cap['start']),mapped(cap['end'])
            assert b>a
            caps.append(dict(cap,start=round(a,3),end=round(b,3),alignment='reviewed source word times mapped through exact quiet cuts and measured atempo length'))
        result=dict(scene,audio=str(target.relative_to(HERE)),sha256=sha(target),duration=duration,
                    duration_samples=len(paced),captions=caps,source_pcm_sha256=scene['sha256'])
        scenes.append(result)
        records.append({'scene':scene['id'],'atempo':speed,'pitch_preserved':True,'protected_installation_pauses':protected,
                        'original_seconds':len(data)/rate,'removed_quiet_seconds':sum(b-a for a,b in removed)/rate,
                        'output_seconds':duration,'measured_effective_atempo':effective,
                        'removed_sample_ranges':removed,'output_sha256':sha(target)})
    result=dict(original,scenes=scenes,tempo_derivative=True,source_alignment_sha256=sha(HERE/'alignment.json'),
                timing_note='Source ASR reviewed; subtitle times transformed by exact sample cuts and measured pitch-preserving tempo output. No new TTS.')
    (OUT/'alignment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    report={'model':'same existing Eleven v4 recording; no new generation','pitch_preserving_filter':'FFmpeg atempo',
            'extra_credits':0,'original_seconds':original['master_duration_samples']/44100,
            'strict_quiet_threshold_db':-42,'minimum_quiet_seconds':.45,'retained_quiet_seconds_before_tempo':.36,
            'new_voice_seconds':sum(s['duration'] for s in scenes),
            'removed_quiet_seconds':sum(s['removed_quiet_seconds'] for s in records),'scenes':records}
    (OUT/'evidence/tempo-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='scenes'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
