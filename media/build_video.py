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
    parser.add_argument("--preview-chapters", type=int)
    args = parser.parse_args()
    root = args.out.resolve()
    data = json.loads((root / "workshop-manifest.json").read_text(encoding="utf-8"))
    from video_source import effective_chapters
    source = effective_chapters(data, root)
    animated = data.get("video", {}).get("style") == "animated"
    count = args.preview_chapters or data["slides"]
    if not 1 <= count <= data["slides"]:
        raise ValueError("Preview chapter count is invalid.")
    source = source[:count]
    video_bitrate = 240
    narrator = data.get("narrator", {"provider": "local Microsoft Zira", "voice": "Zira"})
    narration_path = root / "narration-manifest.json"
    narration = json.loads(narration_path.read_text(encoding="utf-8")) if narration_path.exists() else None
    if narration and ((not narration["complete"] and not args.preview_chapters) or len(narration["slides"]) < count):
        raise ValueError("Foundry narration is incomplete; refusing to build a partial video.")
    if animated and not narration:
        raise ValueError("Animated scenes require their measured narration clips.")
    if args.preview_chapters and narration:
        narrator = narration["narrator"]
    if animated and not args.preview_chapters and narration:
        expected_seconds = sum(item["duration_seconds"] + 0.55 for item in narration["slides"])
        video_bitrate = min(240, int((95 * 1024 * 1024 * 8 / expected_seconds - 96000) * 0.94 / 1000))
        if video_bitrate < 160:
            raise ValueError("Narration is too long for the readable-animation delivery budget.")
    if narration:
        from generate_foundry_narration import normalize
        if narration["narrator"] != narrator:
            raise ValueError("Voice provenance differs between narration and content manifests.")
        for index, (slide, recorded) in enumerate(zip(source, narration["slides"]), 1):
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
        for index, slide in enumerate(source, 1):
            audio = root / "audio" / f"slide-{index:02}.wav"
            image = root / "slides" / f"slide-{index:02}.png"
            if not audio.is_file() or (not animated and not image.is_file()):
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
            fps = 24 if animated else 2
            full_duration = math.ceil((duration + (0.5 if animated else 1)) * fps) / fps
            output_audio.writeframes(frames)
            silence_frames = round((full_duration - duration) * params[2])
            output_audio.writeframes(b"\0" * silence_frames * params[0] * params[1])

            segment = segments / f"slide-{index:02}.mp4"
            if animated:
                from animated_renderer import render
                render(segment, slide, narration["slides"][index - 1], full_duration, video_bitrate)
            else:
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
            if animated:
                from animated_renderer import phrase_cues
                for cue in phrase_cues(anchors):
                    subtitles.append(f"{cue_id}\n{stamp(start + cue['start'])} --> {stamp(start + cue['end'])}\n{cue['text']}\n")
                    cue_id += 1
            for anchor in ([] if animated else anchors):
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
            print(f"Encoded {index}/{count}: {full_duration:.1f}s", flush=True)
    finally:
        output_audio.close()

    concat = segments / "concat.txt"
    concat.write_text("".join(f"file '{(segments / f'slide-{i:02}.mp4').as_posix()}'\n"
                              for i in range(1, count + 1)), encoding="utf-8")
    metadata_file = root / "chapters.ffmeta"
    metadata_file.write_text("\n".join(metadata) + "\n", encoding="utf-8")
    stem = "animated-explainer-preview" if args.preview_chapters else "advanced-github-copilot-explainer"
    srt = root / f"{stem}.srt"
    srt.write_text("\n".join(subtitles), encoding="utf-8")
    vtt = root / f"{stem}.vtt"
    vtt.write_text("WEBVTT\n\n" + re.sub(r"(\d{2}:\d{2}:\d{2}),(\d{3})", r"\1.\2", "\n".join(subtitles)), encoding="utf-8")
    (root / ("preview-transcript.md" if args.preview_chapters else "explainer-transcript.md")).write_text(
        "# Complete explainer transcript\n\n"
        f"Beginner-friendly narration covering the workshop topics. Synthesized narration: {voice_label}.\n"
        "This is not a recording of a live product session. Captions are phrase-level estimates anchored "
        "to measured audio chunk durations where available; they are not word-level forced alignment.\n"
        + "\n".join(transcript), encoding="utf-8")
    (root / ("preview-chapters.txt" if args.preview_chapters else "video-chapters.txt")).write_text("\n".join(chapters) + "\n", encoding="utf-8")
    (root / ("preview-timeline.json" if args.preview_chapters else "video-timeline.json")).write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    destination = root / f"{stem}.mp4"
    audio_destination = root / ("preview-audio.m4a" if args.preview_chapters else "explainer-audio.m4a")
    measured = None
    if animated:
        from audio_processing import profile, mastering_filter, ENCODED_TP_LIMIT
        measured = profile(pcm, highpass=True)
    attenuation = 0
    for attempt in range(3):
        if animated:
            audio_filter = ["-af", mastering_filter(measured, attenuation)]
        bitrate = "96k" if animated else "64k"
        run(ffmpeg, ["-f", "concat", "-safe", "0", "-i", str(concat), "-i", str(pcm),
                     "-i", str(srt), "-i", str(metadata_file), "-map", "0:v:0", "-map", "1:a:0",
                     "-map", "2:s:0", "-map_metadata", "3", "-map_chapters", "3",
                     "-c:v", "copy", *audio_filter, "-c:a", "aac", "-b:a", bitrate, "-ar", "48000", "-ac", "1",
                     "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
                     "-metadata:s:s:0", "title=English captions", "-disposition:s:0", "0",
                     "-movflags", "+faststart", str(destination)])
        run(ffmpeg, ["-i", str(pcm), *audio_filter, "-c:a", "aac", "-b:a", bitrate, "-ar", "48000", "-ac", "1",
                     "-map_metadata", "-1", str(audio_destination)])
        if not animated:
            break
        video_levels, audio_levels = profile(destination), profile(audio_destination)
        peak = max(float(video_levels["input_tp"]), float(audio_levels["input_tp"]))
        if peak <= ENCODED_TP_LIMIT:
            break
        if attempt == 2:
            raise ValueError("Encoded audio exceeds the safe peak ceiling.")
        attenuation += peak - ENCODED_TP_LIMIT + 0.5
    if animated:
        if not -25 <= float(video_levels["input_i"]) <= -21:
            raise ValueError("Encoded loudness is outside the quieter delivery range.")
        (root / ("preview-audio-verification.json" if args.preview_chapters else "audio-verification.json")).write_text(json.dumps({
            "result": "pass", "target_lufs": -22, "encoded_peak_limit_db": -4, "highpass_hz": 80,
            "source": measured, "video": video_levels, "audio_only": audio_levels,
            "additional_attenuation_db": attenuation, "preview": bool(args.preview_chapters),
        }, indent=2), encoding="utf-8")
    if destination.stat().st_size >= 95 * 1024 * 1024:
        raise ValueError("Video exceeds the repository delivery size budget.")

    thumbs = Image.new("RGB", (1280, math.ceil(count / 4) * 200), "#101218")
    draw = ImageDraw.Draw(thumbs)
    for index in range(1, count + 1):
        if animated:
            from animated_renderer import Chapter
            image = Chapter(source[index - 1], narration["slides"][index - 1], timeline[index - 1]["duration_seconds"]).frame(6)
        else:
            image = Image.open(root / "slides" / f"slide-{index:02}.png")
        image.thumbnail((310, 175))
        x, y = ((index - 1) % 4) * 320, ((index - 1) // 4) * 200
        thumbs.paste(image, (x, y))
        draw.text((x + 5, y + 179), f"{index:02}  {source[index - 1]['section']}", fill="white")
        image.close()
    thumbs.save(root / ("animation-contact-sheet.jpg" if animated else "slide-contact-sheet.jpg"), quality=90)
    if animated and not args.preview_chapters:
        (root / "animation-manifest.json").write_text(json.dumps({
            "fps": 24, "chapters": source, "burned_captions": True,
            "no_music_or_sound_effects": True, "preview": False,
        }, indent=2), encoding="utf-8")
        from video_source import write_script
        write_script(root, source)
    print(json.dumps({"video": str(destination), "duration_seconds": start,
                      "duration_minutes": round(start / 60, 2),
                      "size_mb": round(destination.stat().st_size / 1_000_000, 2),
                      "slides": count, "caption_cues": cue_id - 1, "preview": bool(args.preview_chapters),
                      "animated": animated}), flush=True)


if __name__ == "__main__":
    main()
