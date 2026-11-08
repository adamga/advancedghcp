"""Verify the actual deck/video outputs, including a complete AV decode."""

import argparse
import array
import hashlib
import json
import re
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageChops, ImageStat
from pptx import Presentation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("deliverables"))
    args = parser.parse_args()
    root = args.out.resolve()
    manifest = json.loads((root / "workshop-manifest.json").read_text(encoding="utf-8"))
    timeline = json.loads((root / "video-timeline.json").read_text(encoding="utf-8"))
    prs = Presentation(root / "advanced-github-copilot-workshop.pptx")
    assert len(prs.slides) == len(timeline) == manifest["slides"] == 42
    assert abs(prs.slide_width / prs.slide_height - 16 / 9) < 0.001
    assert sum(minutes for _, minutes in manifest["agenda"]) == 180
    assert sum(minutes for _, minutes in manifest["agenda"][:3]) == 60
    assert [minutes for _, minutes in manifest["agenda"][3:]] == [30, 35, 40, 15]
    for slide, data in zip(prs.slides, manifest["slides_data"]):
        assert data["narration"] in slide.notes_slide.notes_text_frame.text
        for source in data["sources"]:
            assert source in slide.notes_slide.notes_text_frame.text
    audio_checks = []
    for entry in timeline:
        path = root / "audio" / f"slide-{entry['slide']:02}.wav"
        with wave.open(str(path), "rb") as wav:
            assert wav.getsampwidth() == 2
            samples = array.array("h", wav.readframes(wav.getnframes()))
            rms = (sum(sample * sample for sample in samples) / len(samples)) ** 0.5
            assert rms > 100, f"Silent narration: {path}"
            duration = wav.getnframes() / wav.getframerate()
            assert abs(duration - entry["speech_seconds"]) < 0.001
            audio_checks.append({"slide": entry["slide"], "rms": round(rms, 1), "seconds": duration})

    total = sum(entry["duration_seconds"] for entry in timeline)
    subtitles = (root / "advanced-github-copilot-explainer.srt").read_text(encoding="utf-8")
    cues = len(re.findall(r"^\d+$", subtitles, re.MULTILINE))
    assert cues > 700
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    video = root / "advanced-github-copilot-explainer.mp4"
    probe = subprocess.run([ffmpeg, "-hide_banner", "-i", str(video)], capture_output=True, text=True)
    # FFmpeg inspection exits 1 because no output was requested.
    info = probe.stderr
    assert "Video: h264" in info and "1280x720" in info
    assert "Audio: aac" in info and "Subtitle: mov_text" in info
    assert len(re.findall(r"Chapter #0:", info)) == 42
    match = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    assert match, info
    actual = int(match[1]) * 3600 + int(match[2]) * 60 + float(match[3])
    assert abs(actual - total) < 0.15, (actual, total)
    decode = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(video),
                             "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"],
                            capture_output=True, text=True)
    assert decode.returncode == 0 and not decode.stderr, decode.stderr
    qa = root / "qa"
    qa.mkdir(exist_ok=True)
    image_checks = []
    for index in (1, 7, 14, 20, 23, 26, 35, 42):
        entry = timeline[index - 1]
        frame = qa / f"video-frame-{index:02}.png"
        extraction = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                                     "-ss", str(entry["start_seconds"] + 1), "-i", str(video),
                                     "-frames:v", "1", str(frame)], capture_output=True, text=True)
        assert extraction.returncode == 0, extraction.stderr
        with Image.open(frame) as actual_image, Image.open(root / "slides" / f"slide-{index:02}.png") as expected:
            assert actual_image.size == expected.size == (1280, 720)
            difference = sum(ImageStat.Stat(ImageChops.difference(actual_image.convert("RGB"), expected.convert("RGB"))).mean) / 3
            assert difference < 5, (index, difference)
            image_checks.append({"slide": index, "mean_pixel_difference": round(difference, 3)})
    assert (root / "advanced-github-copilot-workshop.pdf").read_bytes().startswith(b"%PDF-")
    outputs = [
        "advanced-github-copilot-workshop.pptx", "advanced-github-copilot-workshop.pdf",
        "advanced-github-copilot-explainer.mp4", "advanced-github-copilot-explainer.srt",
        "advanced-github-copilot-explainer.vtt", "explainer-audio.m4a",
        "explainer-transcript.md", "source-ledger.md", "video-chapters.txt",
    ]
    report = {
        "result": "pass", "slides": 42, "live_minutes": 180,
        "presentation_demo_minutes": 60, "lab_minutes": [30, 35, 40, 15],
        "video_seconds": actual, "video_minutes": round(actual / 60, 2),
        "complete_av_decode": "pass", "embedded_chapters": 42,
        "caption_cues": cues, "narration_checks": audio_checks,
        "sampled_video_frame_comparisons": image_checks,
        "artifacts": {name: {"bytes": (root / name).stat().st_size,
                             "sha256": hashlib.sha256((root / name).read_bytes()).hexdigest()} for name in outputs},
        "limits": "Synthesized local voice; phrase-level captions; no live Copilot UI recording.",
    }
    (root / "media-verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key not in ("artifacts", "narration_checks")}, indent=2))


if __name__ == "__main__":
    main()
