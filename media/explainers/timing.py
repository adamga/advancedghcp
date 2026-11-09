"""Turn narration cue phrases into scene-local times.

Each scene is LEAD seconds of silence, then the narration chunks (each placed at
its manifest offset), then TAIL seconds. A cue phrase is located inside the chunk
that says it, and its time is interpolated by how much speech comes before it.
"""

import json
import math
import re

FPS = 24
LEAD = 0.55
TAIL = 0.80
CUE_EARLY = 0.12
WORDS_PER_SECOND = 2.75


def spoken_weight(text):
    """Rough proxy for speaking time: characters plus pauses at punctuation."""
    return len(text) + 5.0 * len(re.findall(r"[.?!]", text)) + 2.5 * len(re.findall(r"[,;:]", text))


def _fold(text):
    return re.sub(r"\s+", " ", text.replace("\u2019", "'")).lower()


class CueNotFound(KeyError):
    pass


class Timing:
    def __init__(self, scene, manifest_scene=None, strict=False):
        self.strict = strict
        self.scene_id = scene["id"]
        if manifest_scene:
            self.chunks = [
                {"text": c["text"], "seconds": float(c["seconds"]), "offset": float(c["offset"])}
                for c in manifest_scene["chunks"]
            ]
            self.narration = float(manifest_scene["seconds"])
        else:
            words = len(scene["narration"].split())
            self.narration = words / WORDS_PER_SECOND
            self.chunks = [{"text": scene["narration"], "seconds": self.narration, "offset": 0.0}]
        self.frames = max(1, math.ceil((LEAD + self.narration + TAIL) * FPS))
        self.duration = self.frames / FPS
        self.events = []

    def locate(self, phrase):
        """Scene-local seconds at which `phrase` starts being spoken."""
        needle = _fold(phrase)
        for chunk in self.chunks:
            hay = _fold(chunk["text"])
            pos = hay.find(needle)
            if pos >= 0:
                total = spoken_weight(hay) or 1.0
                fraction = spoken_weight(hay[:pos]) / total
                return LEAD + chunk["offset"] + fraction * chunk["seconds"] - CUE_EARLY
        joined = " ".join(_fold(c["text"]) for c in self.chunks)
        pos = joined.find(needle)
        if pos >= 0:
            consumed = 0
            for chunk in self.chunks:
                text = _fold(chunk["text"])
                if pos < consumed + len(text) + 1:
                    local = max(0, pos - consumed)
                    fraction = spoken_weight(text[:local]) / (spoken_weight(text) or 1.0)
                    return LEAD + chunk["offset"] + fraction * chunk["seconds"] - CUE_EARLY
                consumed += len(text) + 1
        raise CueNotFound(f"{self.scene_id}: cue phrase not in narration: {phrase!r}")

    def cue(self, phrase, kind="pop"):
        """Resolve a cue and register a sound event for it."""
        if phrase is None:
            return None
        try:
            time = max(0.35, self.locate(phrase))
        except CueNotFound:
            if self.strict:
                raise
            time = LEAD + self.narration * 0.5
        if kind:
            self.events.append((time, kind))
        return time

    def mark(self, time, kind):
        self.events.append((time, kind))

    def chunk_starts(self):
        return [LEAD + c["offset"] for c in self.chunks]


def load_manifest(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def build_timings(video, manifest=None, strict=False):
    """Timing per scene plus global start times and chapter fractions."""
    by_id = {s["id"]: s for s in manifest["scenes"]} if manifest else {}
    timings, starts, clock = [], [], 0.0
    for scene in video["scenes"]:
        timing = Timing(scene, by_id.get(scene["id"]), strict=strict)
        timings.append(timing)
        starts.append(clock)
        clock += timing.duration
    return timings, starts, clock
