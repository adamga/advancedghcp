"""Fast, offline tests for the Workshop 2 explainer videos (no network, no full render)."""

import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import make_videos as mv  # noqa: E402
import sfx  # noqa: E402
from gfx import H, W  # noqa: E402
from renderer import BUILD, KINDS, Composer  # noqa: E402
from storyboards import CHAPTER_TAGS, VIDEOS  # noqa: E402
from timing import CueNotFound, Timing, build_timings  # noqa: E402

KEYS = ("attendee", "trainer")


def scenes(key):
    return VIDEOS[key]["scenes"]


class StoryboardTests(unittest.TestCase):
    def test_scene_ids_are_unique_and_prefixed(self):
        for key, prefix in (("attendee", "a"), ("trainer", "t")):
            ids = [s["id"] for s in scenes(key)]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertTrue(all(i.startswith(prefix) for i in ids))

    def test_every_kind_has_a_renderer_and_art_exists(self):
        for key in KEYS:
            for scene in scenes(key):
                self.assertIn(scene["kind"], KINDS, scene["id"])
                self.assertTrue(scene["chapter"].strip())
                if scene.get("art"):
                    self.assertTrue((HERE / "art" / f"{scene['art']}.jpg").is_file(), scene["id"])

    def test_narration_is_tts_friendly(self):
        for key in KEYS:
            for scene in scenes(key):
                text = scene["narration"]
                self.assertFalse(re.search(r"\d{1,3},\d{3}|\d{4,}", text), f"{scene['id']}: spell out big numbers")
                self.assertNotRegex(text, r"[<>{}\[\]\\]|https?://", scene["id"])
                self.assertGreater(len(text.split()), 20, scene["id"])

    def test_trainer_is_the_longer_deeper_video(self):
        words = {k: sum(len(s["narration"].split()) for s in scenes(k)) for k in KEYS}
        self.assertGreater(words["trainer"], words["attendee"] * 1.6)
        for key in KEYS:
            self.assertIn(key, CHAPTER_TAGS)

    def test_required_topics_are_covered(self):
        topics = {
            "attendee": ("Harbor", "Sam", "lab", "stuck", "git clone", "agent", "skill", "subagent", "contract"),
            "trainer": ("Harbor", "setup", "troubleshoot", "preflight", "zip", "restore", "lease", "contract", "answer key"),
        }
        for key, words in topics.items():
            blob = " ".join(json.dumps(s, ensure_ascii=False) for s in scenes(key)).lower()
            for word in words:
                self.assertIn(word.lower(), blob, f"{key} video never mentions {word!r}")


class TimingAndCueTests(unittest.TestCase):
    def test_every_cue_phrase_is_in_its_narration_and_scenes_render(self):
        for key in KEYS:
            composer = Composer(key, strict=True, manifest=False)
            try:
                events = composer.sound_events()
            except CueNotFound as error:  # pragma: no cover - failure path
                self.fail(str(error))
            self.assertGreater(len(events), composer.count)
            for index in range(composer.count):
                for t in (0.6, composer.timings[index].duration * 0.5, composer.timings[index].duration - 0.1):
                    frame = composer.frame(index, t)
                    self.assertEqual(frame.size, (W, H))

    def test_scenes_animate(self):
        from PIL import ImageChops, ImageStat

        for key in KEYS:
            composer = Composer(key, strict=True, manifest=False)
            for index in range(composer.count):
                d = composer.timings[index].duration
                a, b = composer.frame(index, d * 0.55), composer.frame(index, d * 0.55 + 0.5)
                change = ImageStat.Stat(ImageChops.difference(a, b)).mean
                self.assertGreater(sum(change), 0.05, f"{composer.specs[index]['id']} looks frozen")

    def test_no_scene_opens_with_dead_air(self):
        from scenes_base import INTRO_MIN_FIRST_CUE

        for key in KEYS:
            composer = Composer(key, strict=True, manifest=False)
            for index in range(composer.count):
                scene = composer.scene(index)
                firsts = [e[0] for e in composer.timings[index].events if e[1] != "whoosh"]
                first = min(firsts) if firsts else None
                window = scene.intro_window
                name = composer.specs[index]["id"]
                if window is not None:
                    self.assertGreaterEqual(first, INTRO_MIN_FIRST_CUE, f"{name} has an intro it does not need")
                    self.assertLess(window[1], first, f"{name} intro overlaps its first cue")
                elif scene.intro and first is not None:
                    self.assertLess(first, INTRO_MIN_FIRST_CUE, f"{name} would show empty space for {first:.1f}s")

    def test_missing_cue_fails_loudly_when_strict(self):
        scene = {"id": "x", "narration": "one two three four five"}
        with self.assertRaises(CueNotFound):
            Timing(scene, strict=True).cue("not in the script")

    def test_timings_are_frame_aligned(self):
        timings, starts, total = build_timings(VIDEOS["attendee"])
        self.assertAlmostEqual(total, sum(t.duration for t in timings))
        for t in timings:
            self.assertAlmostEqual(t.duration * 24, round(t.duration * 24), places=6)


class SoundTests(unittest.TestCase):
    def test_effects_are_finite_and_bounded(self):
        for name, make in sfx.SOUNDS.items():
            samples = make()
            self.assertGreater(len(samples), 1000, name)
            self.assertTrue(all(abs(v) < 2.0 for v in samples), name)

    def test_event_selection_spaces_sounds_but_keeps_transitions(self):
        events = [(1.0, "pop"), (1.1, "pop"), (1.15, "whoosh"), (2.0, "boom"), (2.1, "ding"), (3.0, "unknown")]
        kept = sfx.select_events(events)
        self.assertIn((1.15, "whoosh"), kept)
        self.assertNotIn((1.1, "pop"), kept)
        self.assertNotIn((3.0, "unknown"), kept)
        times = [t for t, k in kept if k != "whoosh"]
        self.assertTrue(all(b - a >= sfx.MIN_GAP for a, b in zip(times, times[1:])))

    def test_music_loop_is_seamless_length_and_quiet_peak(self):
        loop = sfx.music_loop()
        beat = 60.0 / sfx.MUSIC_BPM
        self.assertAlmostEqual(len(loop) / sfx.RATE, 8 * 4 * beat, places=2)


class CaptionAndChapterTests(unittest.TestCase):
    def test_caption_splitter_keeps_text_and_limits_length(self):
        text = ("This is a long sentence, with several clauses, that keeps going and going until it is much too long "
                "for a single caption card. Short one.")
        parts = mv.split_caption(text)
        self.assertTrue(all(len(p) <= 84 for p in parts))
        self.assertEqual(re.sub(r"\s+", " ", " ".join(parts)), re.sub(r"\s+", " ", text))

    def test_srt_time_format(self):
        self.assertEqual(mv.srt_time(3723.456), "01:02:03,456")

    def test_chapters_and_captions_when_narration_is_cached(self):
        for key in KEYS:
            if not (BUILD / key / "narration.json").is_file():
                self.skipTest("narration not generated on this machine")
            composer = Composer(key)
            meta = mv.build_chapters(composer, VIDEOS[key]["title"])
            self.assertEqual(meta.count("[CHAPTER]"), composer.count)
            ends = [int(x) for x in re.findall(r"END=(\d+)", meta)]
            self.assertLessEqual(abs(ends[-1] - composer.total * 1000), 2)
            srt, count = mv.build_captions(composer)
            self.assertGreater(count, composer.count * 2)
            self.assertIn("-->", srt)

    def test_cached_narration_matches_storyboard_text(self):
        for key in KEYS:
            path = BUILD / key / "narration.json"
            if not path.is_file():
                self.skipTest("narration not generated on this machine")
            manifest = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual([s["id"] for s in manifest["scenes"]], [s["id"] for s in scenes(key)])
            for entry, scene in zip(manifest["scenes"], scenes(key)):
                spoken = re.sub(r"\W+", "", " ".join(c["text"] for c in entry["chunks"])).lower()
                written = re.sub(r"\W+", "", scene["narration"]).lower()
                self.assertEqual(spoken, written, f"{scene['id']} narration is stale - regenerate it")
                for chunk in entry["chunks"]:
                    self.assertTrue((BUILD / key / chunk["wav"]).is_file())


class SecretHygieneTests(unittest.TestCase):
    def test_no_azure_client_secret_in_sources_or_manifests(self):
        pattern = re.compile(r"[A-Za-z0-9_.~-]{3}\dQ~[A-Za-z0-9_.~-]{28,}")
        for path in list(HERE.glob("*.py")) + list(HERE.glob("*.json")) + list(BUILD.glob("*/narration.json")):
            self.assertIsNone(pattern.search(path.read_text(encoding="utf-8", errors="ignore")), str(path))


if __name__ == "__main__":
    unittest.main()
