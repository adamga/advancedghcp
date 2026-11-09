"""Compose full frames (scene + chrome + transitions) and preview/contact-sheet tools."""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

import scenes_a as A
import scenes_b as B
from gfx import ACCENT_CYCLE, FPS, H, W, chrome, clamp, curtain, ease_in_out, font, draw_text
from storyboards import CHAPTER_TAGS, VIDEOS
from timing import build_timings, load_manifest

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"

KINDS = {
    "title": A.TitleScene, "art": A.ArtScene, "statement": A.StatementScene, "team": A.TeamScene,
    "cards": A.CardsScene, "pairs": A.PairsScene, "steps": A.StepsScene, "checklist": A.ChecklistScene,
    "stamps": A.StampsScene, "board": B.BoardScene, "lanes": B.LanesScene, "score": B.ScoreScene,
    "timeline": B.TimelineScene, "terminal": B.TerminalScene, "table": B.TableScene,
}
OPEN_SECONDS = 0.42
CLOSE_SECONDS = 0.38


class Composer:
    def __init__(self, key, strict=True, manifest=True, only=None):
        self.key = key
        self.video = VIDEOS[key]
        if only:
            keep = [s for s in self.video["scenes"] if s["id"] in only]
            if not keep:
                raise KeyError(f"no scenes match {sorted(only)}")
            self.video = {**self.video, "scenes": keep}
        man = load_manifest(BUILD / key / "narration.json") if manifest else None
        self.manifest = man
        self.timings, self.starts, self.total = build_timings(self.video, man, strict=strict)
        self.specs = self.video["scenes"]
        self.count = len(self.specs)
        self.marks = [s / self.total for s in self.starts[1:]]
        self.tag = CHAPTER_TAGS[key]
        self._cache = {}

    def ids(self):
        return [s["id"] for s in self.specs]

    def index_of(self, scene_id):
        return self.ids().index(scene_id)

    def scene(self, index):
        if index not in self._cache:
            self._cache = {index: KINDS[self.specs[index]["kind"]](self.specs[index], self.timings[index], index, self.count)}
        return self._cache[index]

    def sound_events(self):
        """(global_time, kind) for every cue plus scene transitions."""
        events = []
        for index, spec in enumerate(self.specs):
            scene_obj = KINDS[spec["kind"]](spec, self.timings[index], index, self.count)
            start = self.starts[index]
            for time, kind in self.timings[index].events:
                events.append((start + time, kind))
            if index < self.count - 1:
                events.append((start + scene_obj.duration - CLOSE_SECONDS, "whoosh"))
        return sorted(events)

    def frame(self, index, t):
        scene = self.scene(index)
        img = scene.render(t)
        progress = (self.starts[index] + t) / self.total
        chrome(img, t, self.specs[index]["chapter"], index + 1, self.count, self.tag, scene.accent, progress, self.marks)
        d = scene.duration
        if t < OPEN_SECONDS and index > 0:
            curtain(img, 1 - ease_in_out(t / OPEN_SECONDS), ACCENT_CYCLE[index % 6], True)
        if t > d - CLOSE_SECONDS and index < self.count - 1:
            curtain(img, ease_in_out((t - (d - CLOSE_SECONDS)) / CLOSE_SECONDS), ACCENT_CYCLE[(index + 1) % 6], False)
        if index == 0 and t < 0.5:
            img = Image.blend(Image.new("RGB", img.size, (4, 6, 14)), img.convert("RGB"), ease_in_out(t / 0.5))
        if index == self.count - 1 and t > d - 0.7:
            img = Image.blend(img.convert("RGB"), Image.new("RGB", img.size, (4, 6, 14)), ease_in_out((t - (d - 0.7)) / 0.7))
        return img.convert("RGB")


def contact_sheet(composer, ids, out_path, fraction=0.88, cols=2, cell=(640, 360)):
    rows = -(-len(ids) // cols)
    sheet = Image.new("RGB", (cols * cell[0], rows * cell[1]), (0, 0, 0))
    for n, scene_id in enumerate(ids):
        index = composer.index_of(scene_id)
        t = composer.timings[index].duration * fraction
        frame = composer.frame(index, t).resize(cell, Image.LANCZOS)
        label = ImageDraw.Draw(frame)
        label.rectangle([0, cell[1] - 20, 64, cell[1]], fill=(0, 0, 0))
        label.text((6, cell[1] - 18), scene_id, fill=(255, 255, 255))
        sheet.paste(frame, ((n % cols) * cell[0], (n // cols) * cell[1]))
    sheet.save(out_path)
    return out_path


def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preview")
    p.add_argument("video")
    p.add_argument("scene")
    p.add_argument("--t", type=float, default=None, help="scene-local seconds (default 88%% of the scene)")
    s = sub.add_parser("sheet")
    s.add_argument("video")
    s.add_argument("ids", nargs="*")
    s.add_argument("--fraction", type=float, default=0.88)
    s.add_argument("--cols", type=int, default=2)
    s.add_argument("--name", default="sheet")
    args = parser.parse_args(argv)
    composer = Composer(args.video)
    out_dir = BUILD / "preview"
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.cmd == "preview":
        index = composer.index_of(args.scene)
        t = args.t if args.t is not None else composer.timings[index].duration * 0.88
        path = out_dir / f"{args.video}-{args.scene}-{t:.1f}.png"
        composer.frame(index, t).save(path)
        print(path)
    else:
        ids = args.ids or composer.ids()
        path = out_dir / f"{args.video}-{args.name}.png"
        contact_sheet(composer, ids, path, args.fraction, args.cols)
        print(path)


if __name__ == "__main__":
    main()
