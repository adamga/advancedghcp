import io
import math
import tempfile
import unittest
import wave
from pathlib import Path

from generate_foundry_narration import NoRedirects, assemble, canonical_wav, chunks, normalize, wav_info


def speech_fixture(rate=24000, seconds=1):
    import array
    samples = array.array("h", (int(4000 * math.sin(i / 10)) for i in range(rate * seconds)))
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setparams((1, 2, rate, 0, "NONE", "not compressed"))
        wav.writeframes(samples.tobytes())
    return output.getvalue()


class NarrationTests(unittest.TestCase):
    def test_credential_requests_cannot_follow_redirects(self):
        self.assertIsNone(NoRedirects().redirect_request(None, None, 302, "", {}, "https://example.com"))

    def test_chunks_preserve_every_word_and_order(self):
        passage = "First sentence. " + " ".join(["word"] * 230) + ".\nFinal sentence."
        parts = chunks(passage)
        self.assertEqual(" ".join(parts), " ".join(passage.split()))
        self.assertTrue(all(len(part.split()) <= 110 for part in parts))

    def test_typography_and_spoken_number_equivalents(self):
        self.assertEqual(normalize("ISS one hundred and one is P one."),
                         normalize("ISS-101 is P1."))
        self.assertEqual(normalize("November seventh, twenty twenty-six"),
                         normalize("November seventh, 2026"))
        self.assertEqual(normalize("GitHub’s subagent."), normalize("Git Hub's sub-agent."))

    def test_omissions_and_negation_are_not_accepted(self):
        self.assertNotEqual(normalize("Do not edit the shared file."),
                            normalize("Do edit the shared file."))

    def test_wav_validation_rejects_silence(self):
        wav_info(speech_fixture())
        output = io.BytesIO()
        with wave.open(output, "wb") as wav:
            wav.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
            wav.writeframes(b"\0" * 48000)
        with self.assertRaisesRegex(ValueError, "silent"):
            wav_info(output.getvalue())

    def test_streaming_wav_size_sentinel_is_finalized_from_pcm(self):
        audio = bytearray(speech_fixture())
        audio[4:8] = b"\xff" * 4
        audio[40:44] = b"\xff" * 4
        result = canonical_wav(bytes(audio))
        self.assertAlmostEqual(wav_info(result)["seconds"], 1)
        self.assertEqual(result[44:], audio[44:])

    def test_truncated_finite_wav_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "truncated"):
            canonical_wav(speech_fixture()[:-100])

    def test_chunk_audio_assembly_and_timing(self):
        audio = speech_fixture()
        record = {"audio": wav_info(audio), "transcript": "Example."}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "audio").mkdir()
            (root / "narration-chunks").mkdir()
            for index in (1, 2):
                (root / "narration-chunks" / f"slide-01-chunk-{index:02}.wav").write_bytes(audio)
            result = assemble(root, 1, ["Example.", "Example."], [record, record])
            self.assertAlmostEqual(result["duration_seconds"], 2.2)
            self.assertAlmostEqual(result["chunks"][1]["offset_seconds"], 1.2)
            self.assertAlmostEqual(wav_info((root / "audio" / "slide-01.wav").read_bytes())["seconds"], 2.2)


if __name__ == "__main__":
    unittest.main()
