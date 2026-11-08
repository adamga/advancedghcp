"""Produce a real narrated MP4, audio, synchronized captions and chapters."""

import argparse
import hashlib
import json
import math
import re
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw


def stamp(seconds, separator=","):
    milliseconds = round(seconds * 1000)
    hours, rem = divmod(milliseconds, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02}{separator}{ms:03}"


def run(ffmpeg, arguments):
    result = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", *arguments],
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("deliverables"))
    args = parser.parse_args()
    root = args.out.resolve()
    data = json.loads((root / "workshop-manifest.json").read_text(encoding="utf-8"))
    narrator = data.get("narrator", {"provider": "local Microsoft Zira", "voice": "Zira"})
    narration_path = root / "narration-manifest.json"
    narration = json.loads(narration_path.read_text(encoding="utf-8")) if narration_path.exists() else None
    if narration and (not narration["complete"] or len(narration["slides"]) != data["slides"]):
        raise ValueError("Foundry narration is incomplete; refusing to build a partial video.")
    if narration:
        from generate_foundry_narration import normalize
        if narration["narrator"] != narrator:
            raise ValueError("Voice provenance differs between narration and content manifests.")
        for index, (slide, recorded) in enumerate(zip(data["slides_data"], narration["slides"]), 1):
            if recorded["slide"] != index or normalize(slide["narration"]) != normalize(
                    " ".join(chunk["text"] for chunk in recorded["chunks"])):
                raise ValueError(f"Narration source or ordering mismatch on slide {index}.")
            if any(normalize(chunk["text"]) != normalize(chunk["transcript"]) for chunk in recorded["chunks"]):
                raise ValueError(f"Non-verbatim narration on slide {index}.")
    voice_label = f"{narrator['provider']} / {narrator.get('deployment', 'speech synthesis')} / {narrator['voice']}"
    audio_filter = ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"] if narrator["provider"] == "Microsoft Foundry" else []
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    segments = root / "segments"
    segments.mkdir(exist_ok=True)
    chapters, subtitles, transcript, timeline = [], [], [], []
    start, cue_id = 0.0, 1
    pcm = root / "explainer-narration.wav"
    output_audio = wave.open(str(pcm), "wb")
    params = None
    metadata = [";FFMETADATA1", "title=Advanced GitHub Copilot - Complete explainer",
                f"comment=Original narrated instruction. Synthesized voice: {voice_label}. Sources verified 7 Nov 2026."]
    try:
        for index, slide in enumerate(data["slides_data"], 1):
            audio = root / "audio" / f"slide-{index:02}.wav"
            image = root / "slides" / f"slide-{index:02}.png"
            if not audio.is_file() or not image.is_file():
                raise FileNotFoundError(f"Missing rendered image or narration for slide {index}")
            with wave.open(str(audio), "rb") as wav:
                current = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate())
                if params is None:
                    params = current
                    output_audio.setnchannels(current[0])
                    output_audio.setsampwidth(current[1])
                    output_audio.setframerate(current[2])
                if current != params:
                    raise ValueError("Narration audio formats must match.")
                frames = wav.readframes(wav.getnframes())
                duration = wav.getnframes() / wav.getframerate()
            if narration and abs(duration - narration["slides"][index - 1]["duration_seconds"]) > 0.001:
                raise ValueError(f"Measured and recorded audio durations differ on slide {index}.")
            if duration < 20:
                raise ValueError(f"Narration too short for complete explanation on slide {index}")
            full_duration = math.ceil((duration + 1) * 2) / 2
            output_audio.writeframes(frames)
            silence_frames = round((full_duration - duration) * params[2])
            output_audio.writeframes(b"\0" * silence_frames * params[0] * params[1])

            segment = segments / f"slide-{index:02}.mp4"
            cache = segment.with_suffix(".sha256")
            input_hash = hashlib.sha256(image.read_bytes() + str(full_duration).encode("ascii")).hexdigest()
            if not segment.is_file() or not cache.is_file() or cache.read_text().strip() != input_hash:
                run(ffmpeg, ["-loop", "1", "-framerate", "2", "-i", str(image), "-t", str(full_duration),
                             "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-crf", "24",
                             "-pix_fmt", "yuv420p", "-r", "2", "-an", str(segment)])
                cache.write_text(input_hash, encoding="ascii")
            title = slide["title"].replace("\n", " ")
            chapters.append(f"{stamp(start, '.').split('.')[0]}  {index:02}  {title}")
            transcript.append(f"\n## Slide {index}: {title}\n\nStart: {stamp(start, '.')}\n\n{slide['narration']}\n")
            timeline.append({"slide": index, "title": title, "start_seconds": start,
                             "speech_seconds": duration, "duration_seconds": full_duration})
            # Phrase timing uses exact per-slide audio duration and proportional
            # word counts, not forced-aligned word timestamps.
            anchors = narration["slides"][index - 1]["chunks"] if narration else [
                {"text": slide["narration"], "offset_seconds": 0, "duration_seconds": duration}
            ]
            for anchor in anchors:
                sentences = re.split(r"(?<=[.!?])\s+", anchor["text"].replace("\n", " "))
                phrases = []
                for sentence in sentences:
                    words = sentence.split()
                    for offset in range(0, len(words), 16):
                        phrases.append(" ".join(words[offset:offset + 16]))
                total_words = sum(len(p.split()) for p in phrases)
                elapsed = anchor["offset_seconds"]
                for phrase in phrases:
                    length = anchor["duration_seconds"] * len(phrase.split()) / total_words
                    subtitles.append(f"{cue_id}\n{stamp(start + elapsed)} --> {stamp(start + elapsed + length)}\n{phrase}\n")
                    cue_id += 1
                    elapsed += length
            escaped = title.replace("\\", "\\\\").replace("=", "\\=").replace(";", "\\;").replace("#", "\\#")
            metadata += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={round(start * 1000)}",
                         f"END={round((start + full_duration) * 1000)}", f"title={escaped}"]
            start += full_duration
            print(f"Encoded {index}/{data['slides']}: {full_duration:.1f}s", flush=True)
    finally:
        output_audio.close()

    concat = segments / "concat.txt"
    concat.write_text("".join(f"file '{(segments / f'slide-{i:02}.mp4').as_posix()}'\n"
                              for i in range(1, data["slides"] + 1)), encoding="utf-8")
    metadata_file = root / "chapters.ffmeta"
    metadata_file.write_text("\n".join(metadata) + "\n", encoding="utf-8")
    srt = root / "advanced-github-copilot-explainer.srt"
    srt.write_text("\n".join(subtitles), encoding="utf-8")
    vtt = root / "advanced-github-copilot-explainer.vtt"
    vtt.write_text("WEBVTT\n\n" + re.sub(r"(\d{2}:\d{2}:\d{2}),(\d{3})", r"\1.\2", "\n".join(subtitles)), encoding="utf-8")
    (root / "explainer-transcript.md").write_text(
        "# Complete explainer transcript\n\n"
        f"Original instruction covering all deck topics. Synthesized narration: {voice_label}.\n"
        "This is not a recording of a live product session. Captions are phrase-level estimates anchored "
        "to measured audio chunk durations where available; they are not word-level forced alignment.\n"
        + "\n".join(transcript), encoding="utf-8")
    (root / "video-chapters.txt").write_text("\n".join(chapters) + "\n", encoding="utf-8")
    (root / "video-timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    destination = root / "advanced-github-copilot-explainer.mp4"
    run(ffmpeg, ["-f", "concat", "-safe", "0", "-i", str(concat), "-i", str(pcm),
                 "-i", str(srt), "-i", str(metadata_file), "-map", "0:v:0", "-map", "1:a:0",
                 "-map", "2:s:0", "-map_metadata", "3", "-map_chapters", "3",
                 "-c:v", "copy", *audio_filter, "-c:a", "aac", "-b:a", "64k", "-ar", "48000",
                 "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
                 "-metadata:s:s:0", "title=English captions", "-movflags", "+faststart", str(destination)])
    run(ffmpeg, ["-i", str(pcm), *audio_filter, "-c:a", "aac", "-b:a", "64k",
                 "-map_metadata", "-1", str(root / "explainer-audio.m4a")])

    thumbs = Image.new("RGB", (1280, math.ceil(data["slides"] / 4) * 200), "#101218")
    draw = ImageDraw.Draw(thumbs)
    for index in range(1, data["slides"] + 1):
        with Image.open(root / "slides" / f"slide-{index:02}.png") as image:
            image.thumbnail((310, 175))
            x, y = ((index - 1) % 4) * 320, ((index - 1) // 4) * 200
            thumbs.paste(image, (x, y))
            draw.text((x + 5, y + 179), f"{index:02}  {data['slides_data'][index - 1]['section']}", fill="white")
    thumbs.save(root / "slide-contact-sheet.jpg", quality=90)
    print(json.dumps({"video": str(destination), "duration_seconds": start,
                      "duration_minutes": round(start / 60, 2),
                      "size_mb": round(destination.stat().st_size / 1_000_000, 2),
                      "slides": data["slides"], "caption_cues": cue_id - 1}), flush=True)


if __name__ == "__main__":
    main()
