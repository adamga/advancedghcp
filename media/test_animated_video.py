import json
import tempfile
import unittest
from pathlib import Path

from PIL import ImageChops

from animated_content import CHAPTERS
from animated_renderer import Chapter
from audio_processing import mastering_filter
from generate_foundry_narration import INSTRUCTIONS, TranscriptMismatchError, generate_chunk, wav_info
from test_foundry_narration import speech_fixture
from video_source import effective_chapters
from workshop_content import SLIDES


class AnimatedVideoTests(unittest.TestCase):
    def test_all_workshop_chapters_have_short_visual_beats(self):
        self.assertEqual(len(CHAPTERS), 42)
        self.assertEqual(sum(len(c["beats"]) for c in CHAPTERS), 126)
        words = sum(len(b["text"].split()) for c in CHAPTERS for b in c["beats"])
        self.assertGreater(words, 4500)
        self.assertLess(words, 7000)
        self.assertGreaterEqual(len({b["scene"] for c in CHAPTERS for b in c["beats"]}), 10)

    def test_critical_caveats_and_exact_rules_are_not_lost(self):
        required = {
            5: ["do not automatically get independent worktrees", "not a locked room"],
            10: ["does not switch", "skills field", "handoffs"],
            12: ["do not receive repository instructions by default"],
            14: ["does not grant tools or credentials"],
            23: ["cannot produce exactly eighty", "seventy-five", "eighty-five", "zero points"],
            26: ["not a filesystem lock", "own tests"],
            29: ["codeowners", "timeouts fall through", "post-tool"],
            30: ["do not automatically appear", "not every part"],
            32: ["skip local git hooks", "closed"],
            40: ["stopping does not undo", "destructive reset"],
        }
        for number, phrases in required.items():
            text = " ".join(b["text"] for b in CHAPTERS[number - 1]["beats"]).casefold()
            for phrase in phrases:
                self.assertIn(phrase, text, (number, phrase))

    def test_loader_rejects_incomplete_story(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "storyboard.json"
            path.write_text(json.dumps({"fps": 24, "chapters": CHAPTERS[:2]}))
            with self.assertRaisesRegex(ValueError, "every chapter"):
                effective_chapters({"slides": 42, "slides_data": SLIDES}, folder, path)

    def test_every_chapter_moves_inside_the_illustration_not_only_progress(self):
        for chapter in CHAPTERS:
            chunks = [{"text": beat["text"], "offset_seconds": index * 20.2, "duration_seconds": 20}
                      for index, beat in enumerate(chapter["beats"])]
            obj = Chapter(chapter, {"chunks": chunks}, 61)
            first = obj.frame(0.3).crop((40, 177, 1240, 572))
            late = [obj.frame(t).crop((40, 177, 1240, 572)) for t in (0.95, 5.5, 12)]
            self.assertTrue(any(ImageChops.difference(first, image).getbbox() for image in late), chapter["slide"])
            for time in (21, 45, 58):
                self.assertEqual(obj.frame(time).size, (1280, 720))

    def test_quieter_mastering_has_peak_reserve_and_no_upward_volume(self):
        measured = {"input_i": "-25", "input_tp": "-8", "input_lra": "4",
                    "input_thresh": "-35", "target_offset": "0"}
        graph = mastering_filter(measured, 1.2)
        self.assertIn("highpass=f=80", graph)
        self.assertIn("I=-22:TP=-6", graph)
        self.assertIn("volume=-1.200dB", graph)

    def test_an_off_script_answer_is_retried_as_quoted_material(self):
        audio = speech_fixture()

        class Client:
            endpoint, deployment, voice = "https://example.services.ai.azure.com/openai/v1", "gpt-audio-1.5", "coral"
            instructions, target_wpm = INSTRUCTIONS, None

            def speak(self, passage, quotation=False):
                if not quotation:
                    raise TranscriptMismatchError("Answered the instruction instead of reading it.")
                return audio, {"transcript": passage, "audio": wav_info(audio), "usage": {}}

        with tempfile.TemporaryDirectory() as folder:
            record = generate_chunk(Client(), Path(folder), 1, 1, "Read this sentence.")
            self.assertTrue(record["quoted_retry"])
            self.assertEqual(record["transcript"], "Read this sentence.")


if __name__ == "__main__":
    unittest.main()
