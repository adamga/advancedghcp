"""Verify the finished explainer videos: decode, streams, loudness, motion, captions and chapters.

Usage (from the repository root):
    python .\\media\\explainers\\verify_explainers.py                # both videos in deliverables\\explainers
    python .\\media\\explainers\\verify_explainers.py --video attendee --file path\\to\\video.mp4
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import imageio_ffmpeg  # noqa: E402
from PIL import Image, ImageChops, ImageStat  # noqa: E402

from audio_processing import ENCODED_TP_LIMIT, profile  # noqa: E402
from renderer import Composer  # noqa: E402
from make_videos import DELIVERABLES, NAMES  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
LIMIT_MIB = 64
SAMPLE_FPS = 4
THUMB = (160, 90)


def ffmpeg_info(path):
    return subprocess.run([FFMPEG, "-hide_banner", "-i", str(path)], capture_output=True, text=True).stderr


def decoded_seconds(path, stream):
    """Fully decode one stream; returns (seconds, error_text)."""
    result = subprocess.run([FFMPEG, "-v", "error", "-stats", "-i", str(path), "-map", stream, "-f", "null", "-"],
                            capture_output=True, text=True)
    times = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", result.stderr)
    seconds = 0.0
    if times:
        h, m, s = times[-1]
        seconds = int(h) * 3600 + int(m) * 60 + float(s)
    errors = "\n".join(line for line in result.stderr.replace("\r", "\n").splitlines()
                       if line.strip() and "time=" not in line and "frame=" not in line)
    return seconds, errors


def motion_profile(path):
    """Mean absolute pixel change between consecutive samples (4 fps, tiny grayscale)."""
    proc = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-map", "0:v:0", "-vf", f"fps={SAMPLE_FPS},scale={THUMB[0]}:{THUMB[1]},format=gray",
         "-f", "rawvideo", "-"], capture_output=True)
    size = THUMB[0] * THUMB[1]
    data = proc.stdout
    frames = [Image.frombytes("L", THUMB, data[i:i + size]) for i in range(0, len(data) - size + 1, size)]
    return [ImageStat.Stat(ImageChops.difference(a, b)).mean[0] for a, b in zip(frames, frames[1:])]


def parse_srt(text):
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
        a = [int(x) for x in m.groups()]
        start = a[0] * 3600 + a[1] * 60 + a[2] + a[3] / 1000
        end = a[4] * 3600 + a[5] * 60 + a[6] + a[7] / 1000
        cues.append((start, end, lines[2:]))
    return cues


def verify(key, path, srt_path=None):
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    composer = Composer(key)
    expected = composer.total
    size_mib = Path(path).stat().st_size / (1024 * 1024)
    check("size under 64 MiB attachment limit", size_mib < LIMIT_MIB, f"{size_mib:.2f} MiB")

    info = ffmpeg_info(path)
    check("h264 1280x720 24fps", bool(re.search(r"Video: h264.*1280x720.*24 fps", info)))
    check("aac mono 48 kHz", bool(re.search(r"Audio: aac.*48000 Hz, mono", info)))
    check("soft captions stream", "Subtitle: mov_text" in info)
    chapters = re.findall(r"Chapter #0:\d+: start ([\d.]+), end ([\d.]+)", info)
    check("one chapter per scene", len(chapters) == composer.count, f"{len(chapters)} chapters / {composer.count} scenes")
    if chapters:
        check("chapters cover the whole video", abs(float(chapters[-1][1]) - expected) < 0.1 and float(chapters[0][0]) == 0.0)

    vsec, verr = decoded_seconds(path, "0:v:0")
    asec, aerr = decoded_seconds(path, "0:a:0")
    check("video decodes cleanly", not verr, verr[:200])
    check("audio decodes cleanly", not aerr, aerr[:200])
    check("video duration matches storyboard", abs(vsec - expected) < 0.15, f"{vsec:.2f}s vs {expected:.2f}s")
    check("audio duration matches storyboard", abs(asec - expected) < 0.15, f"{asec:.2f}s vs {expected:.2f}s")

    levels = profile(path)
    lufs, peak = float(levels["input_i"]), float(levels["input_tp"])
    check("integrated loudness -25..-21 LUFS (quiet, no distortion)", -25 <= lufs <= -21, f"{lufs} LUFS")
    check(f"true peak <= {ENCODED_TP_LIMIT} dBTP", peak <= ENCODED_TP_LIMIT, f"{peak} dBTP")

    diffs = motion_profile(path)
    per_scene = []
    for index, start in enumerate(composer.starts):
        end = start + composer.timings[index].duration
        window = diffs[int(start * SAMPLE_FPS): int(end * SAMPLE_FPS) - 1]
        mean = sum(window) / max(1, len(window))
        frozen = run = 0
        for value in window:
            run = run + 1 if value < 0.02 else 0
            frozen = max(frozen, run)
        per_scene.append({"scene": composer.specs[index]["id"], "mean_change": round(mean, 3), "longest_still_s": frozen / SAMPLE_FPS})
    still = [s for s in per_scene if s["mean_change"] < 0.08 or s["longest_still_s"] > 7]
    check("every scene keeps moving (no frozen stretches over 7 s)", not still, ", ".join(s["scene"] for s in still))

    srt_path = Path(srt_path) if srt_path else Path(path).with_suffix(".srt")
    if srt_path.exists():
        cues = parse_srt(srt_path.read_text(encoding="utf-8"))
        check("captions present", len(cues) >= composer.count * 2, f"{len(cues)} cues")
        check("captions in order, within the video",
              all(a[1] > a[0] and (n == 0 or a[0] >= cues[n - 1][0]) for n, a in enumerate(cues)) and cues[-1][1] <= expected + 0.05)
        spoken = sum(end - start for start, end, _ in cues)
        narrated = sum(t.narration for t in composer.timings)
        check("captions cover the narration", spoken >= narrated * 0.9, f"{spoken:.0f}s of {narrated:.0f}s")
        check("caption lines short enough", all(len(line) <= 46 and len(lines) <= 2 for _, _, lines in cues for line in lines))
    else:
        check("captions sidecar present", False, str(srt_path))

    return {
        "video": key, "file": Path(path).name, "size_mib": round(size_mib, 2), "duration_seconds": round(vsec, 2),
        "loudness_lufs": lufs, "true_peak_dbtp": peak, "scenes": composer.count, "checks": checks,
        "passed": all(c["ok"] for c in checks), "motion": per_scene,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", choices=["attendee", "trainer"], action="append")
    parser.add_argument("--file")
    parser.add_argument("--out", default=None, help="write the JSON report here")
    args = parser.parse_args(argv)
    keys = args.video or ["attendee", "trainer"]
    reports, ok = [], True
    for key in keys:
        path = Path(args.file) if args.file else DELIVERABLES / f"{NAMES[key]}.mp4"
        report = verify(key, path)
        reports.append(report)
        ok &= report["passed"]
        print(f"\n== {key}: {report['file']}  {report['size_mib']} MiB  {report['duration_seconds']}s  "
              f"{report['loudness_lufs']} LUFS  {report['true_peak_dbtp']} dBTP")
        for item in report["checks"]:
            print(f"  [{'PASS' if item['ok'] else 'FAIL'}] {item['check']}" + (f"  ({item['detail']})" if item["detail"] else ""))
    if args.out:
        Path(args.out).write_text(json.dumps(reports, indent=2), encoding="utf-8")
    print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
