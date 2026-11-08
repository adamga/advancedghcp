"""Measured cadence and quieter, peak-safe audio mastering."""

import io
import json
import re
import subprocess
import wave

import imageio_ffmpeg

TARGET_LUFS = -22
PREENCODE_TP = -6
ENCODED_TP_LIMIT = -4


def adjust_cadence(audio, words, target_wpm):
    with wave.open(io.BytesIO(audio), "rb") as wav:
        seconds = wav.getnframes() / wav.getframerate()
    original_wpm = words / seconds * 60
    factor = min(1.18, max(0.90, target_wpm / original_wpm))
    result = subprocess.run(
        [imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error",
         "-i", "pipe:0", "-af", f"atempo={factor:.8f}", "-ar", "24000", "-ac", "1",
         "-c:a", "pcm_s16le", "-f", "wav", "pipe:1"],
        input=audio, capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout, {"factor": factor, "original_wpm": original_wpm, "requested_wpm": target_wpm}


def profile(path, highpass=False):
    prefix = "highpass=f=80," if highpass else ""
    result = subprocess.run(
        [imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-i", str(path),
         "-map", "0:a:0", "-af", prefix + "loudnorm=I=-22:TP=-4:LRA=9:print_format=json",
         "-f", "null", "-"], capture_output=True, text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:])
    matches = re.findall(r"\{[^{}]+\}", result.stderr)
    if not matches:
        raise ValueError("FFmpeg did not return a loudness measurement.")
    return json.loads(matches[-1])


def mastering_filter(measured, attenuation=0):
    values = ":".join((
        f"I={TARGET_LUFS}", f"TP={PREENCODE_TP}", "LRA=9",
        f"measured_I={measured['input_i']}", f"measured_TP={measured['input_tp']}",
        f"measured_LRA={measured['input_lra']}", f"measured_thresh={measured['input_thresh']}",
        f"offset={measured['target_offset']}", "linear=true",
    ))
    suffix = f",volume=-{attenuation:.3f}dB" if attenuation else ""
    return "highpass=f=80,loudnorm=" + values + suffix
