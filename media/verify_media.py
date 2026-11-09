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


def motion_ratio(a, b):
    difference = ImageChops.difference(a, b).convert("L")
    histogram = difference.point(lambda value: 255 if value > 10 else 0).histogram()
    return histogram[255] / (difference.width * difference.height)


def verify_animation(root, video, timeline, source, narration, ffmpeg):
    from animated_renderer import Chapter, FPS
    qa = root / "qa"
    qa.mkdir(exist_ok=True)
    requests = []
    for chapter in timeline:
        first_clip_seconds = narration["slides"][chapter["slide"] - 1]["chunks"][0]["duration_seconds"]
        for offset in (0.3, 0.95, 5.5, min(12, first_clip_seconds * 0.6)):
            frame_number = round((chapter["start_seconds"] + offset) * FPS)
            requests.append((chapter["slide"], frame_number, frame_number / FPS - chapter["start_seconds"]))
    expression = "+".join(f"eq(n,{number})" for _, number, _ in requests)
    extraction = subprocess.run(
        [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-threads", "2", "-i", str(video),
         "-vf", f"select='{expression}',scale=640:360", "-fps_mode", "vfr", str(qa / "motion-%03d.png")],
        capture_output=True, text=True,
    )
    assert extraction.returncode == 0, extraction.stderr
    results = []
    for index, chapter in enumerate(timeline):
        obj = Chapter(source[index], narration["slides"][index], chapter["duration_seconds"])
        actual, expected = [], []
        for probe in range(4):
            sequence = index * 4 + probe + 1
            path = qa / f"motion-{sequence:03}.png"
            with Image.open(path) as image:
                actual.append(image.convert("RGB").crop((20, 89, 620, 286)))
            time = requests[sequence - 1][2]
            expected.append(obj.frame(time).resize((640, 360), Image.Resampling.LANCZOS).crop((20, 89, 620, 286)))
        intended_motion = max(motion_ratio(expected[0], item) for item in expected[1:])
        encoded_motion = max(motion_ratio(actual[0], item) for item in actual[1:])
        assert intended_motion > 0.003 and encoded_motion > 0.003, (chapter["slide"], intended_motion, encoded_motion)
        error = sum(ImageStat.Stat(ImageChops.difference(actual[-1], expected[-1])).mean) / 3
        assert error < 12, (chapter["slide"], error)
        results.append({"chapter": chapter["slide"], "intended_motion_ratio": round(intended_motion, 4),
                        "encoded_motion_ratio": round(encoded_motion, 4), "mean_render_difference": round(error, 3)})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("deliverables"))
    parser.add_argument("--baseline-audio", type=Path)
    args = parser.parse_args()
    root = args.out.resolve()
    manifest = json.loads((root / "workshop-manifest.json").read_text(encoding="utf-8"))
    from video_source import effective_chapters
    source = effective_chapters(manifest, root)
    animated = manifest.get("video", {}).get("style") == "animated"
    narration_path = root / "narration-manifest.json"
    narration = json.loads(narration_path.read_text(encoding="utf-8")) if narration_path.exists() else None
    if narration:
        from generate_foundry_narration import normalize
        assert narration["complete"] and len(narration["slides"]) == 42
        for slide, record in zip(source, narration["slides"]):
            assert normalize(slide["narration"]) == normalize(" ".join(chunk["text"] for chunk in record["chunks"]))
            assert all(normalize(chunk["text"]) == normalize(chunk["transcript"]) for chunk in record["chunks"])
    timeline = json.loads((root / "video-timeline.json").read_text(encoding="utf-8"))
    prs = Presentation(root / "advanced-github-copilot-workshop.pptx")
    assert len(prs.slides) == len(timeline) == manifest["slides"] == 42
    assert abs(prs.slide_width / prs.slide_height - 16 / 9) < 0.001
    assert sum(minutes for _, minutes in manifest["agenda"]) == 180
    assert sum(minutes for _, minutes in manifest["agenda"][:3]) == 60
    assert [minutes for _, minutes in manifest["agenda"][3:]] == [30, 35, 40, 15]
    for slide, data in zip(prs.slides, manifest["slides_data"]):
        assert data["narration"] in slide.notes_slide.notes_text_frame.text
        for source_id in data["sources"]:
            assert source_id in slide.notes_slide.notes_text_frame.text
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
    if animated:
        from animated_renderer import phrase_cues
        assert cues == sum(len(phrase_cues(chapter["chunks"])) for chapter in narration["slides"])
        assert 145 <= narration["actual_wpm"] <= 180
    else:
        assert cues > 700
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    video = root / "advanced-github-copilot-explainer.mp4"
    probe = subprocess.run([ffmpeg, "-hide_banner", "-i", str(video)], capture_output=True, text=True)
    # FFmpeg inspection exits 1 because no output was requested.
    info = probe.stderr
    assert "Video: h264" in info and "1280x720" in info
    assert "Audio: aac" in info and "Subtitle: mov_text" in info
    if animated:
        assert "24 fps" in info
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
    if animated:
        image_checks = verify_animation(root, video, timeline, source, narration, ffmpeg)
    for index in (() if animated else (1, 7, 14, 20, 23, 26, 35, 42)):
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
    levels = None
    if animated:
        from audio_processing import profile
        levels = profile(video)
        assert -25 <= float(levels["input_i"]) <= -21
        assert float(levels["input_tp"]) <= -4
        if args.baseline_audio:
            baseline = profile(args.baseline_audio)
            levels["baseline_input_i"] = baseline["input_i"]
            levels["baseline_input_tp"] = baseline["input_tp"]
            levels["loudness_reduction_lu"] = float(baseline["input_i"]) - float(levels["input_i"])
            assert levels["loudness_reduction_lu"] >= 5
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
        "visual_style": "animated" if animated else "slides",
        "fps": 24 if animated else 2,
        "spoken_words": narration.get("spoken_words") if narration else None,
        "actual_wpm": narration.get("actual_wpm") if narration else None,
        "encoded_audio_levels": levels,
        "sampled_video_frame_comparisons": image_checks,
        "artifacts": {name: {"bytes": (root / name).stat().st_size,
                             "sha256": hashlib.sha256((root / name).read_bytes()).hexdigest()} for name in outputs},
        "narrator": manifest.get("narrator", {"provider": "local Microsoft Zira", "voice": "Zira"}),
        "verbatim_chunks_verified": narration["chunks"] if narration else None,
        "limits": "Synthesized voice; phrase-level captions; no live Copilot UI recording or independent ASR verification.",
    }
    (root / "media-verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key not in ("artifacts", "narration_checks")}, indent=2))


if __name__ == "__main__":
    main()
