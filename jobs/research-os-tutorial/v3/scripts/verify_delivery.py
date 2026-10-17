"""Decode the delivered MP4, verify measured placement, and extract review frames.

uv run --with numpy --with pillow python scripts/verify_delivery.py
This checks encoding and sample placement; it does not claim human listening QA.
"""
from __future__ import annotations
import hashlib
import sys
import json
import math
import subprocess
import wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parents[1]
if '--paced' in sys.argv:HERE=HERE/'paced'
VIDEO=HERE/('output/research-os-tutorial-v3-paced-zh-TW.mp4' if '--paced' in sys.argv else 'output/research-os-tutorial-v3-zh-TW.mp4')
EVIDENCE=HERE/'evidence'

def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True)

def pcm(path):
    with wave.open(str(path),'rb') as reader:
        assert reader.getframerate()==44100 and reader.getnchannels()==1 and reader.getsampwidth()==2
        return np.frombuffer(reader.readframes(reader.getnframes()),dtype='<i2').astype(np.float64)/32768

def main():
    timeline=json.loads((HERE/'timeline.json').read_text())
    info=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(VIDEO)]).stdout)
    video=next(s for s in info['streams'] if s['codec_type']=='video')
    audio=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert video['codec_name']=='h264' and audio['codec_name']=='aac'
    assert (video['width'],video['height'],video['r_frame_rate'])==(1920,1080,'30/1')
    assert int(video['nb_read_frames'])==timeline['total_frames']
    decode=run(['ffmpeg','-v','error','-i',str(VIDEO),'-f','null','-'])
    (EVIDENCE/'full-decode.log').write_text(decode.stderr)
    extracted=HERE/'output/decoded-delivery.wav'
    run(['ffmpeg','-v','error','-y','-i',str(VIDEO),'-vn','-ar','44100','-ac','1','-c:a','pcm_s16le',str(extracted)])
    encoded=pcm(extracted);rate=44100;sync=[];margin=round(.15*rate)
    for scene in timeline['scenes']:
        source=pcm(HERE/scene['audio'])
        # Pick a voiced two-second window, excluding paragraph boundaries.
        window=min(2*rate,len(source)//3)
        candidates=range(rate,max(rate+1,len(source)-window-rate),rate//2)
        offset=max(candidates,key=lambda x:np.dot(source[x:x+window],source[x:x+window]))
        ref=source[offset:offset+window]
        expected=scene['start_frame']*(rate//30)+offset
        begin=expected-margin;query=encoded[begin:expected+len(ref)+margin]
        nfft=1 << (len(query)+len(ref)-1).bit_length()
        convolution=np.fft.irfft(np.fft.rfft(query,nfft)*np.fft.rfft(ref[::-1],nfft),nfft)
        dots=convolution[len(ref)-1:len(query)]
        squares=np.concatenate(([0.],np.cumsum(query*query)))
        energy=squares[len(ref):]-squares[:-len(ref)]
        corr=dots/np.sqrt(np.maximum(energy*np.dot(ref,ref),1e-20))
        best=int(np.argmax(corr));lag=(best-margin)/rate;score=float(corr[best])
        assert abs(lag)<1/30,(scene['id'],lag)
        assert score>.97,(scene['id'],score)
        placement=scene['start_frame']*(rate//30)+best-margin
        full=encoded[placement:placement+len(source)]
        full_corr=float(np.dot(source,full)/np.sqrt(np.dot(source,source)*np.dot(full,full)))
        assert full_corr>.97,(scene['id'],'full clip',full_corr)
        seconds=[]
        for position in range(0,len(source),rate):
            a=source[position:position+rate];b=full[position:position+rate]
            if np.sqrt(np.mean(a*a))<.015:continue
            value=float(np.dot(a,b)/np.sqrt(np.dot(a,a)*np.dot(b,b)))
            assert value>.95,(scene['id'],'voiced second',position/rate,value)
            seconds.append(value)
        sync.append({'scene':scene['id'],'source_window_start':offset/rate,'lag_seconds':lag,
                     'correlation':score,'full_clip_correlation':full_corr,
                     'voiced_seconds_checked':len(seconds),'minimum_voiced_second_correlation':min(seconds)})
    caps=json.loads((HERE/'captions.json').read_text())
    assert all(0<=c['start']<c['end']<=timeline['duration'] for c in caps)
    assert all(a['end']<=b['start']+.00001 for a,b in zip(caps,caps[1:]))
    frames=EVIDENCE/'delivery-frames';frames.mkdir(exist_ok=True)
    samples=[('head',0.)]+[(f"scene-{s['id']}",s['start']+s['duration']/2) for s in timeline['scenes']]
    samples += [(f"cut-{s['id']}-{side}",s['start']+delta) for s in timeline['scenes'][1:] for side,delta in [('before',-1/30),('after',1/30)]]
    samples += [('tail',timeline['duration']-1/30)]
    for name,t in samples:
        run(['ffmpeg','-v','error','-y','-ss',f'{t:.6f}','-i',str(VIDEO),'-frames:v','1','-update','1',str(frames/f'{name}.png')])
    for group,chosen in [('scenes',samples[:13]),('cuts',samples[13:])]:
        columns=3;tw=640;th=385
        sheet=Image.new('RGB',(columns*tw,math.ceil(len(chosen)/columns)*th),'#1b2030')
        draw=ImageDraw.Draw(sheet)
        for i,(name,t) in enumerate(chosen):
            img=Image.open(frames/f'{name}.png');img.thumbnail((tw,360))
            x=i%columns*tw;y=i//columns*th
            sheet.paste(img,(x,y));draw.text((x+10,y+363),f'{name} / {t:.3f}s',fill='white')
        sheet.save(EVIDENCE/f'delivery-{group}-contact.jpg',quality=93)
    report={'ok':True,'file':str(VIDEO.relative_to(HERE)),'sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),
            'bytes':VIDEO.stat().st_size,'duration_seconds':float(info['format']['duration']),
            'video_frames':int(video['nb_read_frames']),'canvas':[1920,1080],'fps':30,
            'video_codec':video['codec_name'],'audio_codec':audio['codec_name'],
            'full_decode_exit_code':decode.returncode,'full_decode_errors':decode.stderr,
            'audio_peak_dbfs':20*math.log10(max(float(np.max(np.abs(encoded))),1e-12)),
            'audio_sync':sync,'max_abs_audio_lag_seconds':max(abs(s['lag_seconds']) for s in sync),
            'minimum_audio_correlation':min(s['correlation'] for s in sync),
            'subtitle_cues':len(caps),'subtitle_overlap':False,'sampled_frames':len(samples),
            'limitation':'ASR and waveform correlation are objective checks, not a claim of human auditory review.'}
    (HERE/'render-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
