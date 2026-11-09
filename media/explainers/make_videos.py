"""Render, mix, master and package the two Workshop 2 explainer videos.

Usage (run from the repository root):
    python .\\media\\explainers\\make_videos.py all attendee
    python .\\media\\explainers\\make_videos.py all trainer
    python .\\media\\explainers\\make_videos.py all attendee --only a01 a02 a03   # quick slice, build/ only
"""

import argparse
import hashlib
import json
import multiprocessing
import re
import shutil
import subprocess
import sys
import textwrap
import time
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import imageio_ffmpeg  # noqa: E402

import sfx  # noqa: E402
from audio_processing import ENCODED_TP_LIMIT, mastering_filter, profile  # noqa: E402
from gfx import FPS, H, W  # noqa: E402
from renderer import BUILD, Composer  # noqa: E402
from storyboards import VIDEOS  # noqa: E402
from timing import LEAD  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
REPO = HERE.parents[1]
DELIVERABLES = REPO / "deliverables" / "explainers"
NAMES = {"attendee": "workshop2-attendee-guide", "trainer": "workshop2-trainer-briefing"}
NARRATION_RATE = 24000
MAX_MIB = {"attendee": 40, "trainer": 60}
AUDIO_KBPS = 72
SOURCES = ("storyboards.py", "scenes_base.py", "scenes_a.py", "scenes_b.py", "gfx.py", "timing.py", "renderer.py")


def run(args, **kwargs):
    result = subprocess.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", *map(str, args)],
                            capture_output=True, text=True, **kwargs)
    if result.returncode:
        raise RuntimeError(f"ffmpeg failed: {result.stderr[-2500:]}")
    return result


def source_stamp(key):
    digest = hashlib.sha256()
    for name in SOURCES:
        digest.update((HERE / name).read_bytes())
    for art in sorted((HERE / "art").glob("*.jpg")):
        digest.update(art.read_bytes())
    digest.update((BUILD / key / "narration.json").read_bytes())
    return digest.hexdigest()


def work_dir(key, only):
    path = BUILD / key / ("slice" if only else "final")
    path.mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------------------- video

_COMPOSERS = {}


def render_scene(job):
    key, scene_id, out_path = job
    if key not in _COMPOSERS:
        _COMPOSERS[key] = Composer(key)
    composer = _COMPOSERS[key]
    index = composer.index_of(scene_id)
    frames = composer.timings[index].frames
    partial = Path(out_path).with_suffix(".part.mp4")
    log = Path(out_path).with_suffix(".log")
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "16", "-pix_fmt", "yuv420p", "-bf", "0", "-g", str(FPS * 2), "-threads", "2", str(partial)]
    started = time.time()
    with open(log, "wb") as err:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=err)
        try:
            for frame in range(frames):
                proc.stdin.write(composer.frame(index, frame / FPS).tobytes())
            proc.stdin.close()
        except BrokenPipeError:
            pass
        code = proc.wait()
    if code:
        raise RuntimeError(f"segment {scene_id} failed; see {log}")
    Path(partial).replace(out_path)
    return scene_id, frames, time.time() - started


def render_segments(key, only=None, workers=6, force=False):
    seg_dir = BUILD / key / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    stamp_file = seg_dir / ".stamp"
    stamp = source_stamp(key)
    if force or not stamp_file.exists() or stamp_file.read_text() != stamp:
        for old in seg_dir.glob("*.mp4"):
            old.unlink()
        stamp_file.write_text(stamp)
    composer = Composer(key, only=only)
    jobs = []
    for index, spec in enumerate(composer.specs):
        target = seg_dir / f"{spec['id']}.mp4"
        if not target.exists():
            jobs.append((composer.timings[index].frames, (key, spec["id"], str(target))))
    jobs.sort(key=lambda item: -item[0])
    total_frames = sum(frames for frames, _ in jobs)
    print(f"[{key}] rendering {len(jobs)} of {composer.count} scenes ({total_frames} frames) with {workers} workers")
    started, done_frames = time.time(), 0
    if jobs:
        with multiprocessing.Pool(workers) as pool:
            for n, (scene_id, frames, seconds) in enumerate(pool.imap_unordered(render_scene, [j for _, j in jobs]), 1):
                done_frames += frames
                print(f"  {scene_id}: {frames} frames in {seconds:.0f}s  ({n}/{len(jobs)}, {time.time() - started:.0f}s elapsed)", flush=True)
    return [seg_dir / f"{spec['id']}.mp4" for spec in composer.specs]


def concat_list(segments, path):
    path.write_text("".join(f"file '{seg.as_posix()}'\n" for seg in segments), encoding="utf-8")
    return path


def file_mib(path):
    return Path(path).stat().st_size / (1024 * 1024)


def encode_video(segments, duration, max_mib, out_dir):
    """Re-encode the lossless-ish segments to a size-budgeted H.264 stream."""
    listing = concat_list(segments, out_dir / "concat.txt")
    target = out_dir / "video.mp4"
    budget_bits = max_mib * 1024 * 1024 * 8 * 0.965
    cap = int(budget_bits / duration - AUDIO_KBPS * 1000 * 1.06)
    cap = max(250_000, min(cap, 2_400_000))
    base = ["-f", "concat", "-safe", "0", "-i", listing, "-an", "-c:v", "libx264", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-r", FPS, "-g", FPS * 3, "-tune", "animation"]
    run([*base, "-crf", "24", "-maxrate", f"{cap}", "-bufsize", f"{cap * 2}", target])
    video_mib = file_mib(target)
    limit = max_mib - duration * AUDIO_KBPS * 1000 / 8 * 1.05 / 1048576
    mode = "crf24+maxrate"
    if video_mib > limit:
        mode = "two-pass abr"
        passlog = out_dir / "x264pass"
        rate = int(cap * 0.94)
        common = ["-f", "concat", "-safe", "0", "-i", listing, "-c:v", "libx264", "-preset", "slow",
                  "-pix_fmt", "yuv420p", "-r", FPS, "-g", FPS * 3, "-tune", "animation", "-b:v", rate,
                  "-passlogfile", passlog]
        run([*common, "-pass", "1", "-an", "-f", "mp4", out_dir / "pass1.mp4"])
        run([*common, "-pass", "2", "-an", target])
    return {"mode": mode, "cap_bps": cap, "video_mib": round(file_mib(target), 2)}


# ---------------------------------------------------------------- audio


def narration_track(composer, work):
    """Place every narration chunk at its absolute time. Returns (path, max_overlap_seconds)."""
    base = BUILD / composer.key
    by_id = {s["id"]: s for s in composer.manifest["scenes"]}
    out = bytearray()
    worst = 0.0
    for index, spec in enumerate(composer.specs):
        for chunk in by_id[spec["id"]]["chunks"]:
            with wave.open(str(base / chunk["wav"]), "rb") as wav:
                assert wav.getframerate() == NARRATION_RATE and wav.getnchannels() == 1 and wav.getsampwidth() == 2
                pcm = wav.readframes(wav.getnframes())
            start = round((composer.starts[index] + LEAD + float(chunk["offset"])) * NARRATION_RATE)
            have = len(out) // 2
            if start > have:
                out.extend(b"\x00\x00" * (start - have))
            else:
                worst = max(worst, (have - start) / NARRATION_RATE)
            out.extend(pcm)
    total = round(composer.total * NARRATION_RATE)
    if len(out) // 2 < total:
        out.extend(b"\x00\x00" * (total - len(out) // 2))
    path = work / "narration.wav"
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(NARRATION_RATE)
        wav.writeframes(bytes(out))
    return path, worst


def build_audio(composer, work):
    narration, overlap = narration_track(composer, work)
    samples, kept = sfx.sfx_track(composer.sound_events(), composer.total)
    effects = sfx.write_wav(work / "sfx.wav", samples)
    music = sfx.write_wav(work / "music.wav", sfx.music_track(composer.total), peak=0.98)
    total = composer.total
    graph = (
        "[0:a]aresample=48000,highpass=f=70,asplit=2[nar][key];"
        "[2:a]volume=0.11,lowpass=f=5200[bed];"
        "[bed][key]sidechaincompress=threshold=0.012:ratio=7:attack=15:release=500:makeup=1[duck];"
        "[1:a]volume=0.5[fx];"
        "[nar][duck][fx]amix=inputs=3:normalize=0:duration=longest:dropout_transition=0,"
        f"afade=t=out:st={total - 0.8:.3f}:d=0.8[mix]"
    )
    mix = work / "mix.wav"
    run(["-i", narration, "-i", effects, "-i", music, "-filter_complex", graph, "-map", "[mix]",
         "-t", f"{total:.3f}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_f32le", mix])
    return mix, {"sfx_events": len(kept), "max_chunk_overlap_s": round(overlap, 3)}


# ---------------------------------------------------------------- captions and chapters


def split_caption(text, limit=84):
    parts = []
    for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
        pending = [sentence]
        while pending:
            piece = pending.pop(0)
            if len(piece) <= limit:
                parts.append(piece)
                continue
            middle = len(piece) // 2
            cuts = [m.end() for m in re.finditer(r"[,;:]\s+", piece)] or [m.end() for m in re.finditer(r"\s+", piece)]
            cut = min(cuts, key=lambda pos: abs(pos - middle))
            pending[0:0] = [piece[:cut].strip(), piece[cut:].strip()]
    return [p for p in parts if p]


def srt_time(seconds):
    ms = int(round(seconds * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def build_captions(composer):
    by_id = {s["id"]: s for s in composer.manifest["scenes"]}
    cues = []
    for index, spec in enumerate(composer.specs):
        for chunk in by_id[spec["id"]]["chunks"]:
            start = composer.starts[index] + LEAD + float(chunk["offset"])
            pieces = split_caption(chunk["text"])
            weight = sum(len(p) for p in pieces)
            clock = start
            for piece in pieces:
                span = float(chunk["seconds"]) * len(piece) / weight
                cues.append((clock, clock + span, piece))
                clock += span
    lines = []
    for n, (start, end, text) in enumerate(cues, 1):
        wrapped = "\n".join(textwrap.wrap(text, 44))
        lines.append(f"{n}\n{srt_time(start)} --> {srt_time(max(start + 0.4, end - 0.04))}\n{wrapped}\n")
    return "\n".join(lines), len(cues)


def build_chapters(composer, title):
    lines = [";FFMETADATA1", f"title={title}", "artist=Advanced GitHub Copilot Workshop"]
    for index, spec in enumerate(composer.specs):
        start = int(round(composer.starts[index] * 1000))
        end = int(round((composer.starts[index] + composer.timings[index].duration) * 1000))
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={start}", f"END={end}", f"title={spec['chapter']}"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- mux


def mux(video, mix, srt, meta, destination):
    measured = profile(mix, highpass=True)
    attenuation = 0.0
    for attempt in range(4):
        run(["-i", video, "-i", mix, "-i", srt, "-i", meta,
             "-map", "0:v:0", "-map", "1:a:0", "-map", "2:s:0", "-map_metadata", "3", "-map_chapters", "3",
             "-c:v", "copy", "-af", mastering_filter(measured, attenuation), "-c:a", "aac", "-b:a", f"{AUDIO_KBPS}k",
             "-ar", "48000", "-ac", "1", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
             "-metadata:s:s:0", "title=English captions", "-disposition:s:0", "0",
             "-movflags", "+faststart", destination])
        levels = profile(destination)
        peak = float(levels["input_tp"])
        if peak <= ENCODED_TP_LIMIT:
            break
        if attempt == 3:
            raise ValueError("Encoded audio exceeds the safe peak ceiling.")
        attenuation += peak - ENCODED_TP_LIMIT + 0.5
    if not -25 <= float(levels["input_i"]) <= -21:
        raise ValueError(f"Encoded loudness {levels['input_i']} LUFS is outside the quieter delivery range.")
    return {"source": measured, "encoded": levels, "additional_attenuation_db": round(attenuation, 3)}


def build_all(key, only=None, workers=6, force=False, max_mib=None):
    started = time.time()
    video = VIDEOS[key]
    segments = render_segments(key, only=only, workers=workers, force=force)
    composer = Composer(key, only=only)
    work = work_dir(key, only)
    duration = sum(t.frames for t in composer.timings) / FPS
    print(f"[{key}] audio mix ({composer.total:.1f}s)")
    mix, audio_info = build_audio(composer, work)
    srt_text, cue_count = build_captions(composer)
    srt = work / "captions.srt"
    srt.write_text(srt_text, encoding="utf-8")
    meta = work / "chapters.ffmeta"
    meta.write_text(build_chapters(composer, video["title"]), encoding="utf-8")
    budget = max_mib or MAX_MIB[key]
    print(f"[{key}] encoding video (budget {budget} MiB)")
    video_info = encode_video(segments, duration, budget, work)
    destination = work / f"{NAMES[key]}.mp4"
    print(f"[{key}] muxing and mastering audio")
    audio_levels = mux(work / "video.mp4", mix, srt, meta, destination)
    info = {
        "video": key, "scenes": composer.count, "duration_seconds": round(duration, 3), "captions": cue_count,
        "size_mib": round(file_mib(destination), 2), "budget_mib": budget, "video_encode": video_info,
        "audio": {**audio_info, **audio_levels}, "build_seconds": round(time.time() - started),
        "slice": sorted(only) if only else None,
    }
    (work / "build-info.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    print(json.dumps({k: info[k] for k in ("duration_seconds", "size_mib", "captions", "build_seconds")}))
    return destination, srt, info


def publish(key):
    work = work_dir(key, None)
    DELIVERABLES.mkdir(parents=True, exist_ok=True)
    name = NAMES[key]
    shutil.copyfile(work / f"{name}.mp4", DELIVERABLES / f"{name}.mp4")
    shutil.copyfile(work / "captions.srt", DELIVERABLES / f"{name}.srt")
    composer = Composer(key)
    composer.frame(0, 2.0).save(DELIVERABLES / f"{name}-poster.jpg", quality=90)
    print(f"[{key}] published to {DELIVERABLES}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["segments", "all", "publish"])
    parser.add_argument("video", choices=["attendee", "trainer"])
    parser.add_argument("--only", nargs="*", help="scene ids for a quick slice (never published)")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--max-mib", type=float, default=None)
    args = parser.parse_args(argv)
    only = set(args.only) if args.only else None
    if args.command == "segments":
        render_segments(args.video, only=only, workers=args.workers, force=args.force)
    elif args.command == "all":
        build_all(args.video, only=only, workers=args.workers, force=args.force, max_mib=args.max_mib)
    else:
        publish(args.video)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
