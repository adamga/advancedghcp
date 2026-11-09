"""Pure-Python sound effects and a quiet looping music bed (no third-party audio packages)."""

import math
import random
import wave
from array import array

RATE = 48000
MIN_GAP = 0.30


def _tone(freq, seconds, decay, shape="sine", sweep_to=None, phase=0.0):
    count = int(seconds * RATE)
    out = []
    for i in range(count):
        t = i / RATE
        f = freq if sweep_to is None else freq + (sweep_to - freq) * min(1.0, t / seconds)
        phase += 2 * math.pi * f / RATE
        if shape == "sine":
            v = math.sin(phase)
        elif shape == "soft":
            v = math.sin(phase) + 0.28 * math.sin(2 * phase) + 0.1 * math.sin(3 * phase)
        else:
            v = math.sin(phase + 1.2 * math.sin(phase))
        attack = min(1.0, i / (0.004 * RATE))
        out.append(v * attack * math.exp(-t * decay))
    return out


def _mix_into(buf, samples, start, gain=1.0, wrap=False):
    n = len(buf)
    for i, value in enumerate(samples):
        j = start + i
        if j >= n:
            if not wrap:
                break
            j %= n
        buf[j] += value * gain


def make_pop():
    body = _tone(520, 0.16, 26, "soft", sweep_to=980)
    tick = _tone(1800, 0.03, 160)
    out = [0.0] * len(body)
    _mix_into(out, body, 0, 0.8)
    _mix_into(out, tick, 0, 0.25)
    return out


def make_ding():
    out = [0.0] * int(0.9 * RATE)
    for freq, gain, decay in ((1318.5, 0.55, 5.5), (1976.0, 0.3, 7.5), (2637.0, 0.14, 11)):
        _mix_into(out, _tone(freq, 0.9, decay), 0, gain)
    return out


def make_boom():
    rng = random.Random(7)
    out = _tone(120, 0.6, 7.5, "sine", sweep_to=42)
    noise, state = [], 0.0
    for i in range(int(0.18 * RATE)):
        state += 0.22 * (rng.uniform(-1, 1) - state)
        noise.append(state * math.exp(-i / RATE * 28))
    _mix_into(out, noise, 0, 0.5)
    return out


def make_whoosh():
    rng = random.Random(11)
    seconds = 0.5
    count = int(seconds * RATE)
    out, low, band = [], 0.0, 0.0
    for i in range(count):
        t = i / count
        cutoff = 0.03 + 0.5 * math.sin(math.pi * t) ** 1.5
        sample = rng.uniform(-1, 1)
        low += cutoff * (sample - low)
        band += cutoff * (low - band)
        env = math.sin(math.pi * t) ** 1.6
        out.append((low - band) * 3.2 * env)
    return out


SOUNDS = {"pop": make_pop, "ding": make_ding, "boom": make_boom, "whoosh": make_whoosh}
GAINS = {"pop": 0.55, "ding": 0.5, "boom": 0.75, "whoosh": 0.5}


def select_events(events):
    """Drop sounds that would pile up closer than MIN_GAP; transitions always win."""
    kept, last = [], -9.0
    for time, kind in sorted(events):
        if kind not in SOUNDS:
            continue
        if kind != "whoosh" and time - last < MIN_GAP:
            continue
        kept.append((time, kind))
        last = time
    return kept


def sfx_track(events, total_seconds):
    library = {name: make() for name, make in SOUNDS.items()}
    buf = [0.0] * int((total_seconds + 1.0) * RATE)
    kept = select_events(events)
    for time, kind in kept:
        _mix_into(buf, library[kind], int(max(0.0, time) * RATE), GAINS[kind])
    return buf, kept


MUSIC_BPM = 108
CHORDS = (
    ((48, 55, 64), (60, 64, 67, 72)),
    ((45, 57, 64), (57, 60, 64, 69)),
    ((53, 60, 65), (60, 65, 69, 72)),
    ((43, 55, 62), (59, 62, 67, 74)),
)


def _hz(note):
    return 440.0 * 2 ** ((note - 69) / 12)


def music_loop():
    """Eight bars (two passes of C-Am-F-G): marimba-style arpeggio, soft pad, bass and a gentle shaker."""
    beat = 60.0 / MUSIC_BPM
    bar = beat * 4
    bars = 8
    buf = [0.0] * int(bars * bar * RATE)
    rng = random.Random(3)
    pluck = {}

    def note_samples(note, length, decay):
        key = (note, length, decay)
        if key not in pluck:
            pluck[key] = _tone(_hz(note), length, decay, "soft")
        return pluck[key]

    for b in range(bars):
        chord = CHORDS[b % 4]
        bar_start = b * bar
        bass_root, tones = chord
        pad = _tone(_hz(tones[0] - 12), bar + 0.6, 0.9, "sine")
        _mix_into(buf, pad, int(bar_start * RATE), 0.22, wrap=True)
        for k, note in enumerate((bass_root[0], bass_root[0], bass_root[1] - 12, bass_root[0])):
            _mix_into(buf, note_samples(note - 12, 0.38, 7), int((bar_start + k * beat) * RATE), 0.55, wrap=True)
        order = (0, 1, 2, 3, 2, 1, 2, 3) if b < 4 else (3, 2, 1, 0, 1, 2, 3, 2)
        for step, idx in enumerate(order):
            when = bar_start + step * beat / 2
            lift = 12 if (b >= 4 and step % 4 == 3) else 0
            _mix_into(buf, note_samples(tones[idx] + lift, 0.45, 8), int(when * RATE), 0.42, wrap=True)
        for step in range(8):
            when = bar_start + step * beat / 2 + (beat / 4 if step % 2 else 0)
            length = int(0.05 * RATE)
            hat = [rng.uniform(-1, 1) * math.exp(-i / RATE * 90) * (0.12 if step % 2 else 0.2) for i in range(length)]
            _mix_into(buf, hat, int(when * RATE), 1.0, wrap=True)
    return buf


def music_track(total_seconds):
    loop = music_loop()
    peak = max(abs(v) for v in loop) or 1.0
    scaled = [v / peak * 0.5 for v in loop]
    needed = int((total_seconds + 1.0) * RATE)
    reps = -(-needed // len(scaled))
    track = (scaled * reps)[:needed]
    fade = int(2.5 * RATE)
    for i in range(fade):
        track[i] *= i / fade
        track[-1 - i] *= i / fade
    return track


def write_wav(path, samples, rate=RATE, peak=0.95):
    top = max((abs(v) for v in samples), default=0.0)
    scale = min(1.0, peak / top) if top else 1.0
    data = array("h", (int(max(-1.0, min(1.0, v * scale)) * 32767) for v in samples))
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(rate)
        out.writeframes(data.tobytes())
    return path


if __name__ == "__main__":
    import sys
    from pathlib import Path

    target = Path(sys.argv[1] if len(sys.argv) > 1 else "sfx-demo.wav")
    demo = [0.0] * (RATE * 5)
    for t, kind in ((0.2, "pop"), (0.9, "ding"), (1.8, "boom"), (2.8, "whoosh")):
        _mix_into(demo, make_pop() if kind == "pop" else SOUNDS[kind](), int(t * RATE), GAINS[kind])
    print(write_wav(target, demo))
