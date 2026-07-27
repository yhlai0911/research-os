#!/usr/bin/env python3
"""Regenerate narration takes with ElevenLabs and report the timeline impact.

    # one take
    uv run python scripts/regen_voice.py --scene scene-03

    # every take (required when the voice ID changes)
    uv run python scripts/regen_voice.py --all

    # see what would happen without spending credits or touching files
    uv run python scripts/regen_voice.py --all --dry-run

Reads ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID from <repo-root>/.env.

Two things this handles that are easy to get wrong by hand:

* The existing takes are pcm_s16le / 44100 Hz / mono. `pcm_44100` needs an
  ElevenLabs Pro subscription, so this requests `mp3_44100_128` instead and
  decodes locally: same native sample rate, so nothing is resampled. Do not
  drop to a 22 kHz or 24 kHz format, which would have to be upsampled.
* Every regenerated take shifts the scenes after it. The script reports the
  cumulative offset per scene so index.html can be corrected deliberately,
  and it never edits index.html itself.

Narration text lives in NARRATION below, which is the v2 script. Keep it in
sync with SCRIPT.md.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parent.parent
VOICE_DIR = HERE / "assets" / "voice"
AUDIO_META = HERE / "audio_meta.json"
MODEL_ID = "eleven_multilingual_v2"
# 44.1 kHz to match the existing takes; pcm_44100 is Pro-tier only.
OUTPUT_FORMAT = "mp3_44100_128"

# v2 narration. scene-03 is the line that named the old skill out loud; the
# rest were rewritten so the video actually describes the six-step mainline.
NARRATION = {
    "scene-01": "只有一句模糊題目，AI 當然可以立刻寫出三十頁。但那通常只是把還不知道的地方，用流暢的文字蓋住。Research OS 的目的正好相反：先讓研究站得住，再開始寫。",
    "scene-02": "它不是論文代寫器，也不是一條你只能一路走到底的大流程。固定流程最大的問題，是早期的錯誤會被一路傳到最後。這裡的六個步驟各自有明確的過關條件：逼問想法、鎖定設計、預先找碴、拆成任務、逐一執行、最後審查。過不了就停在那一步，並且告訴你卡在哪裡，不會把問題帶下去。",
    "scene-03": "使用時，不要只丟一個名詞。告訴它主題、最後要變成什麼、受眾是誰、目前手上有什麼，以及不能碰的限制。然後從主線第一步開始。它會先把這些變成一份可以回讀的任務紀錄，而不是假裝答案已經存在。你也可以交給自動模式，讓它自己判斷該走哪一步。",
    "scene-04": "第一步只做一件事：一次問一個真正需要你決定的問題。能查證的事實由 Agent 自己去查；只有目的、範圍、取捨與承諾，才交還給研究者。每個問題都會附上建議，也會說清楚採用這個建議要付出什麼代價。所有分支都收斂之後，它才會讓你進到下一步。",
    "scene-05": "設計鎖定之後，先不要急著拆任務。系統會查最接近的文獻，區分真正的貢獻和只是換個名字；檢查資料是不是真的拿得到；再逼你講清楚，什麼樣的結果會推翻自己的設計。這一步就像先寫一個一定會失敗的測試：標準必須事先講定，看到結果才回頭調整，不算數。必要時先做一個小型 pilot，用最低的成本確認可行性。",
    "scene-06": "所有通過驗證的狀態，最後會收斂成一份 Research Brief。它是單一的研究契約，不綁定特定受眾，也不會把還沒做的事寫成已經完成。之後才依照你的目的，轉成學術研究計畫、補助或專案企劃案、論文藍圖，或者在真的有實證結果的時候，形成論文草稿。任何時候都可以查看自己走到第幾步、手上有什麼、還缺什麼。",
    "scene-07": "舉一個實際的例子。原始構想想把波方程、熱方程、拉普拉斯，甚至 Maxwell–Boltzmann 全都放進金融預測。經過限制與審查之後，不能區分的分支被逐一刪掉，問題收斂成一句話：有限速度的阻尼傳播，能不能和普通的擴散，由資料真正區分開來。留下的不是最多的想法，而是唯一那個可以被拒絕的問題。",
    "scene-08": "如果文獻邊界還沒掃完、資料還沒確認、實證還沒執行，系統就不應該捏造結果。conditional、blocked，甚至直接 kill 掉一個題目，都是有效的答案，而且比一份看起來完整、卻根本無法執行的計畫更有價值。現在，輸入你的主題，說明目的與限制，讓 Research OS 從第一個真正重要的問題開始。",
}


def load_env() -> tuple[str, str]:
    env_path = ROOT / ".env"
    if not env_path.is_file():
        sys.exit(f"missing {env_path}")
    values: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        values[name.strip()] = value.strip()
    try:
        return values["ELEVENLABS_API_KEY"], values["ELEVENLABS_VOICE_ID"]
    except KeyError as exc:
        sys.exit(f"{env_path} is missing {exc.args[0]}")


def duration_of(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def synthesize(key: str, voice: str, text: str, destination: Path) -> None:
    request = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
        f"?output_format={OUTPUT_FORMAT}",
        data=json.dumps({"text": text, "model_id": MODEL_ID}).encode("utf-8"),
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            encoded = response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:400]
        sys.exit(f"ElevenLabs HTTP {exc.code}: {body}")

    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "raw.mp3"
        raw.write_bytes(encoded)
        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(raw),
             "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le",
             "-y", str(destination)],
            check=True,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    scenes = sorted(NARRATION) if args.all else args.scene
    if not scenes:
        sys.exit("pass --scene <id> (repeatable) or --all")

    key, voice = load_env()
    meta = json.loads(AUDIO_META.read_text(encoding="utf-8"))
    if voice != meta.get("voice_id") and not args.all:
        sys.exit(
            f"voice_id changed ({meta.get('voice_id')} -> {voice}); regenerate "
            "every take with --all or the takes will not match each other"
        )

    results, cumulative = [], 0.0
    for scene in scenes:
        target = VOICE_DIR / f"{scene}.wav"
        if scene not in NARRATION or not target.is_file():
            sys.exit(f"unknown scene: {scene}")
        old = duration_of(target)

        if args.dry_run:
            results.append((scene, old, None, None))
            continue

        # Create the backup once only. Re-running must not overwrite the
        # original take with an already-regenerated one.
        backup = target.with_suffix(".wav.bak")
        if not backup.exists():
            shutil.copy2(target, backup)
        synthesize(key, voice, NARRATION[scene], target)
        new = duration_of(target)
        cumulative += new - old
        results.append((scene, old, new, cumulative))

        for entry in meta["voices"]:
            if entry["id"] == scene:
                entry["duration_s"] = round(new, 3)

    if args.dry_run:
        print(f"would regenerate {len(results)} take(s) with voice {voice}")
        for scene, old, _, _ in results:
            print(f"  {scene}: currently {old:.3f}s")
        return 0

    meta["voice_id"] = voice
    AUDIO_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")

    print(f"{'scene':<10} {'old':>8} {'new':>8} {'delta':>8} {'shift after':>12}")
    for scene, old, new, run in results:
        print(f"{scene:<10} {old:8.3f} {new:8.3f} {new - old:+8.3f} {run:+12.3f}")
    print(
        "\naudio_meta.json updated. Backups are alongside each take as *.wav.bak."
        "\nindex.html was NOT touched: shift each scene's data-start by the "
        "cumulative column, then run `npm run check` and re-render."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
