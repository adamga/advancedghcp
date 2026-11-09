"""Generate verbatim Foundry narration for the two workshop2 explainer videos.

Credentials are read only from AZURE_TENANT_ID, AZURE_CLIENT_ID and
AZURE_CLIENT_SECRET in the environment (see generate_foundry_narration.Foundry);
nothing secret is ever written to disk. Chunks are cached, so reruns are cheap.
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import generate_foundry_narration as gfn  # noqa: E402
from storyboards import VIDEOS  # noqa: E402

BUILD = HERE / "build"
CHUNK_WORDS = 40
GAP_SECONDS = 0.2


def scene_chunks(scene):
    return gfn.chunks(scene["narration"], CHUNK_WORDS)


def video_jobs(video):
    jobs = []
    for number, scene in enumerate(video["scenes"], 1):
        for index, text in enumerate(scene_chunks(scene), 1):
            jobs.append((number, index, text))
    return jobs


def chunk_directory(key):
    return BUILD / key / "chunks"


def speak_with_retry(client, root, number, index, text, attempts=3):
    for attempt in range(1, attempts + 1):
        try:
            return gfn.generate_chunk(client, root, number, index, text)
        except Exception as error:  # noqa: BLE001 - report and retry transient service errors
            if attempt == attempts or isinstance(error, gfn.TranscriptMismatchError):
                raise
            print(f"  retry {attempt} for scene {number:02} chunk {index:02}: {type(error).__name__}", flush=True)
            time.sleep(2 * attempt)


def generate(key, client, workers):
    video = VIDEOS[key]
    root = chunk_directory(key)
    root.mkdir(parents=True, exist_ok=True)
    jobs = video_jobs(video)
    records, failures = {}, []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(speak_with_retry, client, root, n, i, t): (n, i, t) for n, i, t in jobs}
        for future in as_completed(futures):
            n, i, t = futures[future]
            try:
                records[(n, i)] = future.result()
            except Exception as error:  # noqa: BLE001
                failures.append((n, i, f"{type(error).__name__}: {error}"))
    if failures:
        for n, i, message in sorted(failures):
            print(f"FAILED scene {n:02} chunk {i:02}: {message[:300]}", flush=True)
        raise SystemExit(f"{len(failures)} chunk(s) failed for {key}; fix the text or rerun to resume.")
    scenes = []
    for number, scene in enumerate(video["scenes"], 1):
        offset, items = 0.0, []
        passages = scene_chunks(scene)
        for index, text in enumerate(passages, 1):
            seconds = records[(number, index)]["audio"]["seconds"]
            items.append({"index": index, "text": text, "seconds": round(seconds, 4),
                          "offset": round(offset, 4),
                          "wav": f"chunks/slide-{number:02}-chunk-{index:02}.wav"})
            offset += seconds + (GAP_SECONDS if index < len(passages) else 0)
        scenes.append({"id": scene["id"], "number": number, "seconds": round(offset, 4), "chunks": items})
    manifest = {
        "video": key, "deployment": client.deployment, "voice": client.voice,
        "style": client.style if hasattr(client, "style") else None,
        "target_wpm": client.target_wpm, "gap_seconds": GAP_SECONDS, "scenes": scenes,
        "total_seconds": round(sum(s["seconds"] for s in scenes), 3),
    }
    (BUILD / key / "narration.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    words = sum(len(s["narration"].split()) for s in video["scenes"])
    print(f"{key}: {len(jobs)} chunks, {words} words, {manifest['total_seconds']:.1f}s of narration "
          f"({words / manifest['total_seconds'] * 60:.0f} wpm).", flush=True)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("videos", nargs="*", choices=sorted(VIDEOS))
    parser.add_argument("--endpoint", default=os.environ.get("AZURE_OPENAI_ENDPOINT"),
                        help="Foundry OpenAI v1 endpoint, https://<resource>.services.ai.azure.com/openai/v1 "
                             "(or set AZURE_OPENAI_ENDPOINT)")
    parser.add_argument("--deployment", default="gpt-audio-1.5")
    parser.add_argument("--voice", default="coral")
    parser.add_argument("--style", default="playful", choices=("calm", "playful"))
    parser.add_argument("--target-wpm", type=int, default=165)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--dry-run", action="store_true", help="validate chunking only; no service calls")
    args = parser.parse_args()
    args.videos = args.videos or sorted(VIDEOS)
    if args.dry_run:
        for key in args.videos:
            jobs = video_jobs(VIDEOS[key])
            print(f"{key}: {len(jobs)} chunks, largest {max(len(t.split()) for _, _, t in jobs)} words")
        return
    if not args.endpoint:
        parser.error("--endpoint (or AZURE_OPENAI_ENDPOINT) is required to generate narration")
    client = gfn.Foundry(args.endpoint, args.deployment, args.voice, style=args.style,
                         target_wpm=args.target_wpm)
    for key in args.videos:
        generate(key, client, args.workers)


if __name__ == "__main__":
    main()
