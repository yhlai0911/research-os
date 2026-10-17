#!/usr/bin/env python3
"""Recompute index.html timings from the current narration durations.

    uv run python scripts/retime.py [--dry-run]

The composition follows one strict pattern, verified against the v1 file:

    section#scene-NN   start = running total of previous scene durations
                       duration = take duration + 2.0s tail
    caption#caption-NN start = scene start + 0.8s lead
    audio#audio-NN     duration = take duration exactly
    root               duration = last scene start + last scene duration

Durations come from audio_meta.json, which regen_voice.py keeps current, so
this never re-probes the wav files and the two scripts cannot disagree.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
INDEX = HERE / "index.html"
AUDIO_META = HERE / "audio_meta.json"

TAIL = 2.0   # silence held after each take
LEAD = 0.8   # delay before caption and audio start inside a scene

# Captions must match what is on screen in that scene, not just the narration.
# Scene 2 argues against rigid pipelines, scene 6 is ONE BRIEF / MANY OUTPUTS,
# and scene 7 is the worked example -- an earlier pass mismatched all three.
CAPTIONS = {
    1: "AI 可以立刻寫三十頁；Research OS 先確認研究是否站得住。",
    2: "六個步驟各有過關條件，過不了就停，不把錯誤傳到下一步。",
    3: "交代主題、目的地、受眾、目前狀態與限制，然後從第一步開始。",
    4: "可查事實由 Agent 查；研究者決定目的、取捨與承諾。",
    5: "先查文獻與資料，再預先講定什麼結果會推翻自己的設計。",
    6: "Research Brief 是單一研究契約，再轉譯成計畫、企劃或論文。",
    7: "刪掉不能區分的分支，只留下可以被資料拒絕的那個問題。",
    8: "Conditional、blocked 或 kill，都是比虛構完成更可靠的答案。",
}


def replace_attr(text: str, anchor: str, attr: str, value: str) -> str:
    """Set attr on the single element whose id matches anchor."""
    pattern = re.compile(rf'(id="{anchor}"[^>]*?{attr}=")[^"]*(")')
    new_text, count = pattern.subn(rf"\g<1>{value}\g<2>", text)
    if count != 1:
        sys.exit(f"expected exactly one {attr} on #{anchor}, found {count}")
    return new_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    meta = json.loads(AUDIO_META.read_text(encoding="utf-8"))
    takes = {entry["id"]: float(entry["duration_s"]) for entry in meta["voices"]}
    text = INDEX.read_text(encoding="utf-8")

    cursor, rows = 0.0, []
    for index in range(1, 9):
        scene = f"scene-{index:02d}"
        take = takes[scene]
        scene_duration = round(take + TAIL, 3)
        scene_start = round(cursor, 3)
        inner_start = round(scene_start + LEAD, 3)

        text = replace_attr(text, scene, "data-start", f"{scene_start:g}")
        text = replace_attr(text, scene, "data-duration", f"{scene_duration:g}")
        for anchor in (f"caption-{index:02d}", f"audio-{index:02d}"):
            text = replace_attr(text, anchor, "data-start", f"{inner_start:g}")
            text = replace_attr(text, anchor, "data-duration", f"{take:g}")

        caption = re.compile(
            rf'(<div id="caption-{index:02d}"[^>]*>)[^<]*(</div>)'
        )
        text, count = caption.subn(rf"\g<1>{CAPTIONS[index]}\g<2>", text)
        if count != 1:
            sys.exit(f"expected one caption body for caption-{index:02d}")

        rows.append((scene, take, scene_start, scene_duration))
        cursor += scene_duration

    total = round(cursor, 3)
    text = replace_attr(text, "main", "data-duration", f"{total:g}")

    print(f"{'scene':<10}{'take':>9}{'start':>9}{'duration':>10}")
    for scene, take, start, duration in rows:
        print(f"{scene:<10}{take:9.3f}{start:9.3f}{duration:10.3f}")
    print(f"{'root':<10}{'':>9}{'':>9}{total:10.3f}")

    if args.dry_run:
        print("\ndry run: index.html unchanged")
        return 0

    INDEX.write_text(text, encoding="utf-8")
    print("\nindex.html updated. Run `npm run check`, then render.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
