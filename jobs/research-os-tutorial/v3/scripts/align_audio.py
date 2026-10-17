"""Align the approved script to LOCAL Whisper word times and cut lossless PCM scenes.

Run: uv run --with opencc-python-reimplemented python scripts/align_audio.py
No network inference, API credentials, or TTS regeneration.
"""
from __future__ import annotations
import difflib
import hashlib
import json
import re
import unicodedata
import wave
from pathlib import Path
from opencc import OpenCC

HERE=Path(__file__).resolve().parents[1]
CC=OpenCC('s2twp')

def normalize(text):
    return ''.join(c.lower() for c in CC.convert(unicodedata.normalize('NFKC',text)) if c.isalnum())

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    source=HERE/'assets/voice/full-narration-original.wav'
    transcript=HERE/'evidence/transcribe/full-narration-original.json'
    narration=json.loads((HERE/'narration-v3.json').read_text())
    asr=json.loads(transcript.read_text())
    chars=[];times=[]
    for segment in asr['segments']:
        for word in segment['words']:
            norm=normalize(word['word'])
            for i,c in enumerate(norm):
                chars.append(c)
                times.append((word['start']+(word['end']-word['start'])*i/max(1,len(norm)),
                              word['start']+(word['end']-word['start'])*(i+1)/max(1,len(norm))))
    asr_text=''.join(chars)
    target='';ranges=[]
    for scene in narration['scenes']:
        begin=len(target);target+=normalize(scene['text']);ranges.append((begin,len(target)))
    matcher=difflib.SequenceMatcher(None,target,asr_text,autojunk=False)
    mapping={}
    for a,b,size in matcher.get_matching_blocks():
        for j in range(size): mapping[a+j]=b+j
    def nearest(position,limit=18):
        if position in mapping:return mapping[position]
        choices=[j for j in mapping if abs(j-position)<=limit]
        if not choices:raise SystemExit(f'BLOCKED: no reliable alignment near target char {position}')
        j=min(choices,key=lambda x:abs(x-position));return mapping[j]
    boundaries=[0.]
    for (previous_begin,end),(begin,next_end) in zip(ranges,ranges[1:]):
        left_anchor=max(j for j in mapping if previous_begin<=j<end)
        right_anchor=min(j for j in mapping if begin<=j<next_end)
        left=times[mapping[left_anchor]][1];right=times[mapping[right_anchor]][0]
        if right<left-.05:raise SystemExit(f'BLOCKED: paragraph boundary time reversed: {end}, {left}, {right}')
        boundaries.append((left+right)/2)
    with wave.open(str(source),'rb') as reader:
        params=reader.getparams();rate=reader.getframerate();nframes=reader.getnframes()
        boundaries.append(nframes/rate)
        source_pcm=reader.readframes(nframes)
    byte_per_frame=params.nchannels*params.sampwidth
    boundary_frames=[max(0,min(nframes,round(t*rate))) for t in boundaries]
    scenes=[];offset=0
    for idx,(scene,(begin,end)) in enumerate(zip(narration['scenes'],ranges)):
        a,b=boundary_frames[idx:idx+2];origin=a/rate
        coverage=sum(i in mapping for i in range(begin,end))/max(1,end-begin)
        if coverage<.68:raise SystemExit(f'BLOCKED: low coverage {scene["id"]}: {coverage:.3f}')
        out=HERE/f'assets/voice/scene-{scene["id"]}.wav'
        with wave.open(str(out),'wb') as writer:
            writer.setparams(params);writer.writeframes(source_pcm[a*byte_per_frame:b*byte_per_frame])
        captions=[];cursor=begin
        units=re.findall(r'[^，。；！？、：]+[，。；！？、：]?|[，。；！？、：]',scene['text'])
        for unit in units:
            length=len(normalize(unit))
            if not length:continue
            first=nearest(cursor);last=nearest(cursor+length-1)
            start=max(0,times[first][0]-origin-.05);finish=min((b-a)/rate,times[last][1]-origin+.08)
            if captions and start<=captions[-1]['start']+.08:
                captions[-1]['text']+=unit;captions[-1]['end']=max(captions[-1]['end'],round(finish,3))
            else:
                captions.append({'text':unit,'start':round(start,3),'end':round(max(start+.12,finish),3),
                                 'alignment':'target text mapped to local Whisper word timestamps'})
            cursor+=length
        for cap,next_cap in zip(captions,captions[1:]):cap['end']=min(cap['end'],next_cap['start'])
        scenes.append({'id':scene['id'],'audio':str(out.relative_to(HERE)),
                       'start_sample_in_master':a,'end_sample_in_master':b,
                       'duration_samples':b-a,'sample_rate':rate,'duration':(b-a)/rate,
                       'sha256':digest(out),'target_text_sha256':hashlib.sha256(scene['text'].encode()).hexdigest(),
                       'matched_character_coverage':round(coverage,4),'captions':captions})
        offset+=end-begin
    opcodes=[{'operation':op,'target':target[a:b],'asr':asr_text[c:d]} for op,a,b,c,d in matcher.get_opcodes() if op!='equal']
    result={'status':'aligned-awaiting-content-review','method':'local Whisper turbo + traditional normalization + monotone character alignment',
            'master_mp3_sha256':digest(HERE/'assets/voice/full-narration-original.mp3'),
            'master_wav_sha256':digest(source),'master_duration_samples':nframes,'sample_rate':rate,
            'global_sequence_similarity':matcher.ratio(),'transcript_sha256':digest(transcript),
            'differences_for_review':opcodes,'scenes':scenes}
    (HERE/'alignment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    (HERE/'evidence/asr-vs-script.txt').write_text('\n'.join(f'{s["id"]}: {s["matched_character_coverage"]:.1%}' for s in scenes)+'\n\n'+json.dumps(opcodes,ensure_ascii=False,indent=2))
    print(f'Aligned {len(scenes)} scenes, similarity {matcher.ratio():.3f}; cut {nframes} exact PCM samples without re-encoding.')

if __name__=='__main__':main()
