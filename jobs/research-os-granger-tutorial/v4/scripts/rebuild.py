"""Rebuild the film locally from retained new generation audio and final visual source.

uv run --no-project python scripts/rebuild.py [--audio-only]
Requires ffmpeg, Node/npm and no ElevenLabs credentials or new paid calls.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import wave

root=pathlib.Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root/'scripts/verify_package.py')], check=True)
ffmpeg=shutil.which('ffmpeg');assert ffmpeg
timeline=json.loads((root/'timeline.json').read_text())
selection=json.loads((root/'voice/selection.json').read_text())
output=root/'output';output.mkdir(exist_ok=True)
audio_only='--audio-only' in sys.argv
target=output/('rebuilt-voice.wav' if audio_only else 'rebuilt.mp4');assert not target.exists()
with tempfile.TemporaryDirectory(prefix='research-os-v4-') as work:
    scratch=pathlib.Path(work);sources={};params=None
    for key,name in [('full1859','full-narration.mp3'),('retake319','retakes.mp3')]:
        wav=scratch/(key+'.wav')
        subprocess.run([ffmpeg,'-v','error','-i',str(root/'voice'/name),'-ac','1','-ar','44100','-c:a','pcm_s16le',str(wav)],check=True)
        with wave.open(str(wav),'rb') as f:
            p=f.getparams();sources[key]=f.readframes(f.getnframes())
        if params is None:params=p
        assert (p.nchannels,p.sampwidth,p.framerate)==(1,2,44100)
    parts=[];width=2;rate=44100
    for a,t in zip(selection['scenes'],timeline['scenes'],strict=True):
        lo=a['generation_source_start_sample'];hi=a['generation_source_end_sample'];pcm=sources[a['generation_source']][lo*width:hi*width]
        assert len(pcm)==(hi-lo)*width
        delay=round(.25*rate);length=round(t['duration']*rate);assert length>=delay+hi-lo
        parts += [bytes(delay*width),pcm,bytes((length-delay-hi+lo)*width)]
    raw=scratch/'raw.wav'
    with wave.open(str(raw),'wb') as f:f.setparams(params);f.writeframes(b''.join(parts))
    measure=subprocess.run([ffmpeg,'-hide_banner','-nostats','-i',str(raw),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
    d=json.JSONDecoder().raw_decode(measure[measure.rfind('{'):])[0]
    settings=f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={d['input_i']}:measured_LRA={d['input_lra']}:measured_TP={d['input_tp']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true"
    voice=scratch/'voice.wav'
    subprocess.run([ffmpeg,'-v','error','-i',str(raw),'-af',settings,'-ar','44100','-c:a','pcm_s16le',str(voice)],check=True)
    if audio_only:shutil.copy2(voice,target)
    else:
        npm=shutil.which('npx');assert npm
        visual=scratch/'visual.mp4'
        subprocess.run([npm,'--yes','hyperframes@0.8.167','render',str(root/'composition'),'--fps','30','--workers','1','--quality','delivery','--experimental-fast-capture=false','--output',str(visual)],check=True,cwd=root)
        subprocess.run([ffmpeg,'-v','error','-i',str(visual),'-i',str(voice),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','96k','-movflags','+faststart','-t',str(timeline['duration']),'-n',str(target)],check=True)
print(json.dumps({'output':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'new_TTS_calls':0}))
