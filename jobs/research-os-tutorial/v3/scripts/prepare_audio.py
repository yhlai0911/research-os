"""Recover the reviewed PCM scene clips from the saved v4 MP3, without TTS."""
from __future__ import annotations
import hashlib
import json
import subprocess
import tempfile
import wave
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    alignment=json.loads((HERE/'alignment.json').read_text())
    source=HERE/'assets/voice/full-narration-original.mp3'
    assert digest(source)==alignment['master_mp3_sha256'],'Source MP3 hash mismatch'
    master=source.with_suffix('.wav')
    if not master.exists():
        subprocess.run(['ffmpeg','-v','error','-i',str(source),'-ac','1','-ar','44100','-c:a','pcm_s16le',str(master)],check=True)
    with wave.open(str(master),'rb') as reader:
        params=reader.getparams();pcm=reader.readframes(reader.getnframes())
        assert reader.getnframes()==alignment['master_duration_samples']
    width=params.nchannels*params.sampwidth
    for scene in alignment['scenes']:
        target=HERE/scene['audio']
        if target.exists():
            assert digest(target)==scene['sha256'],f'Preserved conflicting audio: {target.name}'
            continue
        with tempfile.TemporaryDirectory() as temp:
            clip=Path(temp)/target.name
            with wave.open(str(clip),'wb') as writer:
                writer.setparams(params)
                writer.writeframes(pcm[scene['start_sample_in_master']*width:scene['end_sample_in_master']*width])
            assert digest(clip)==scene['sha256'],'PCM decoder output differs from reviewed scene; inspect before rebuilding'
            target.write_bytes(clip.read_bytes())
    print('Prepared 12 reviewed PCM clips from the saved v4 master; no TTS called.')

if __name__=='__main__':main()
