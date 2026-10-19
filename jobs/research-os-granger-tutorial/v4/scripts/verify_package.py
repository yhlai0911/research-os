"""Check the public source allowlist, hashes, and all 40 scene timings offline."""

import hashlib
import json
import math
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify():
    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text())
    files = manifest["files"]
    require(manifest["scene_count"] == 40, "Unexpected scene count")
    for name, metadata in files.items():
        relative = pathlib.PurePosixPath(name)
        require(not relative.is_absolute() and ".." not in relative.parts,
                f"Unsafe manifest path: {name}")
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(), f"Missing regular file: {name}")
        require(path.resolve().is_relative_to(ROOT), f"Path escapes package: {name}")
        data = path.read_bytes()
        require(len(data) == metadata["bytes"], f"Size mismatch: {name}")
        require(hashlib.sha256(data).hexdigest() == metadata["sha256"],
                f"Hash mismatch: {name}")

    actual = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if set(relative.parts) & {"output", ".hyperframes", "__pycache__"}:
            continue
        require(not path.is_symlink(), f"Symlink is not public source: {relative}")
        if path.is_file() and relative.as_posix() != "PACKAGE_MANIFEST.json":
            actual.add(relative.as_posix())
    require(actual == set(files), "Public source allowlist differs from files on disk")
    require(not any(set(pathlib.PurePosixPath(n).parts) &
                    {"records", "snapshots", "research-run", "private", ".env"}
                    for n in files), "Private/raw source directory in allowlist")

    timeline = json.loads((ROOT / "timeline.json").read_text())
    selection = json.loads((ROOT / "voice/selection.json").read_text())
    html = (ROOT / "composition/index.html").read_text()
    match = re.search(r'<script[^>]*id="spec"[^>]*>(.*?)</script>', html, re.S)
    require(match is not None, "Missing embedded visual timeline")
    visual = json.loads(match.group(1))
    scenes, audio, images = timeline["scenes"], selection["scenes"], visual["scenes"]
    require(len(scenes) == len(audio) == len(images) == 40, "Scene arrays must all contain 40 entries")
    require(timeline["fps"] == 30 and timeline["frames"] == 14338,
            "Unexpected delivered frame count or rate")
    require(sum(s["frames"] for s in scenes) == timeline["frames"], "Frame sum mismatch")
    cursor = 0.0
    for i, (scene, voice, image) in enumerate(zip(scenes, audio, images, strict=True)):
        require(scene["scene"] == voice["scene"] == image["index"] == i,
                f"Scene identity mismatch: {i}")
        require(math.isclose(scene["start"], cursor, abs_tol=1e-6), f"Scene gap/overlap: {i}")
        require(math.isclose(scene["duration"] * 30, scene["frames"], abs_tol=1e-5),
                f"Scene frame duration mismatch: {i}")
        require(all(math.isclose(scene[k], image[k], abs_tol=1e-6)
                    for k in ("start", "duration")), f"Visual timing mismatch: {i}")
        require(voice["generation_source"] in {"full1859", "retake319"}, f"Unknown audio source: {i}")
        lo, hi = voice["generation_source_start_sample"], voice["generation_source_end_sample"]
        require(isinstance(lo, int) and isinstance(hi, int) and 0 <= lo < hi,
                f"Invalid sample interval: {i}")
        duration = (hi - lo) / selection["sample_rate"]
        require(math.isclose(scene["audio_start"], cursor + .25, abs_tol=1e-6),
                f"Audio lead-in mismatch: {i}")
        require(math.isclose(scene["audio_end"], scene["audio_start"] + duration, abs_tol=1e-6),
                f"Audio endpoint mismatch: {i}")
        require(scene["audio_end"] <= cursor + scene["duration"], f"Audio exceeds scene: {i}")
        cursor += scene["duration"]
    require(math.isclose(cursor, timeline["duration"], abs_tol=1e-6), "Total duration mismatch")
    require(math.isclose(cursor, visual["duration"], abs_tol=1e-6), "Visual total mismatch")
    print(f"PUBLIC PACKAGE OK: {len(files)} files, 40 scenes, 14338 frames; hashes and timing verified")


if __name__ == "__main__":
    verify()
