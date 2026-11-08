"""Procedural, scene-specific teaching animation with large on-screen captions."""

import hashlib
import json
import math
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 24
BG, PANEL, WHITE = "#0a0c10", "#171b25", "#f4f7fb"
CYAN, PURPLE, BLUE, GREEN, ORANGE = "#4de1f5", "#a371f7", "#388bfd", "#56d364", "#ff9855"
COLORS = [CYAN, PURPLE, BLUE, GREEN]
FONTS = {}
LAYOUT_CHECKS = []


def font(size, bold=False, mono=False):
    key = (size, bold, mono)
    if key not in FONTS:
        filename = "consola.ttf" if mono else ("arialbd.ttf" if bold else "arial.ttf")
        FONTS[key] = ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / filename), size)
    return FONTS[key]


def lines(text, size, width, bold=False, mono=False):
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    result = []
    for paragraph in text.split("\n"):
        current = ""
        for word in paragraph.split():
            candidate = (current + " " + word).strip()
            if current and draw.textlength(candidate, font=font(size, bold, mono)) > width:
                result.append(current)
                current = word
            else:
                current = candidate
        result.append(current)
    return result


def label(image, x, y, text, size=28, color=WHITE, bold=False, width=1100, mono=False, max_lines=3):
    wrapped = lines(text, size, width, bold, mono)
    if len(wrapped) > max_lines:
        raise ValueError(f"Text needs a simpler layout: {text}")
    if x < 0 or y < 0 or x + width > W or y + len(wrapped) * (size + 7) > H:
        raise ValueError(f"Text is outside the video frame: {text}")
    draw = ImageDraw.Draw(image)
    for index, line in enumerate(wrapped):
        draw.text((x, y + index * (size + 7)), line, font=font(size, bold, mono), fill=color)
    return len(wrapped) * (size + 7)


def rect(image, bounds, fill=PANEL, outline=None, radius=18, width=3):
    ImageDraw.Draw(image).rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)


def ease(value):
    value = max(0, min(1, value))
    return 1 - (1 - value) ** 3


def packet(image, a, b, time, delay=0, color=CYAN):
    position = ((max(0, time - delay) % 6) / 6)
    x, y = a[0] + (b[0] - a[0]) * position, a[1] + (b[1] - a[1]) * position
    ImageDraw.Draw(image).rounded_rectangle((x - 10, y - 7, x + 10, y + 7), 4, fill=color)


def arrow(image, a, b, color="#596577", width=4):
    draw = ImageDraw.Draw(image)
    draw.line((a, b), fill=color, width=width)
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    points = [b, (b[0] - 13 * math.cos(angle - 0.5), b[1] - 13 * math.sin(angle - 0.5)),
              (b[0] - 13 * math.cos(angle + 0.5), b[1] - 13 * math.sin(angle + 0.5))]
    draw.polygon(points, fill=color)


def avatar(image, x, y, name, color, time=0):
    draw = ImageDraw.Draw(image)
    y += 3 * math.sin(time * 1.2)
    draw.ellipse((x - 43, y - 43, x + 43, y + 43), fill=color)
    draw.ellipse((x - 17, y - 12, x - 8, y - 3), fill=BG)
    draw.ellipse((x + 8, y - 12, x + 17, y - 3), fill=BG)
    draw.arc((x - 20, y - 12, x + 20, y + 23), 15, 165, fill=BG, width=4)
    label(image, x - 105, y + 58, name, 23, color, True, 210, max_lines=2)


def node(image, x, y, name, color, active=False, width=215):
    rect(image, (x, y, x + width, y + 108), "#23243a", color if active else "#485063")
    label(image, x + 14, y + 25, name, 25, color if active else WHITE, True, width - 28, max_lines=2)


class Scene:
    def __init__(self, chapter, beat):
        self.chapter, self.beat = chapter, beat
        self.base = Image.new("RGB", (W, H), BG)
        rect(self.base, (0, 0, 10, H), PURPLE, radius=0)
        label(self.base, 40, 20, "COPILOT TEAMWORK / " + chapter["section"], 18, CYAN, True, 1060, max_lines=2)
        label(self.base, 1115, 22, f"{chapter['slide']:02} / 42", 18, "#aab3c0", width=125)
        label(self.base, 40, 64, beat["headline"], 45, WHITE, True, 1180, max_lines=2)
        rect(self.base, (40, 177, 1240, 572), PANEL)
        label(self.base, 45, 580, "Teaching illustration | Pause whenever you want to try it", 16, "#aab3c0", width=1150)
        LAYOUT_CHECKS.append({"chapter": chapter["slide"], "headline": beat["headline"], "scene": beat["scene"]})

    def frame(self, time, duration):
        image = self.base.copy()
        scene, labels = self.beat["scene"], self.beat["labels"]
        variant = self.beat.get("variant", "")
        phase = min(2, int(time / max(3, duration / 3)))
        if scene == "team":
            count = len(labels)
            points = [(170 + i * (940 / max(1, count - 1)), 330) for i in range(count)]
            for i in range(count - 1):
                arrow(image, (points[i][0] + 48, 330), (points[i + 1][0] - 48, 330))
                packet(image, (points[i][0] + 48, 330), (points[i + 1][0] - 48, 330), time, i, COLORS[i % 4])
            for i, (x, y) in enumerate(points):
                y += 80 * (1 - ease((time - i * 0.18) / 0.75))
                avatar(image, x, y, labels[i], COLORS[i % 4], time)
            label(image, 90, 507, "Small jobs. Clear boundaries. Useful reports.", 26, CYAN, width=1080)
        elif scene == "split":
            toward = ease(min(time, 5) / 5)
            ax, bx = 200 + toward * 270, 1080 - toward * 270
            avatar(image, ax, 305, labels[0], CYAN, time)
            avatar(image, bx, 305, labels[-1], PURPLE, time)
            rect(image, (540, 280, 740, 437), "#24283a", ORANGE if time > 4 else BLUE)
            label(image, 555, 302, labels[1] if len(labels) > 2 else "Shared file", 25, WHITE, True, 170, max_lines=3)
            if time > 4:
                rect(image, (382, 455, 898, 515), "#352820", ORANGE)
                label(image, 400, 469, "PAUSE: choose one write owner", 26, ORANGE, True, 485, max_lines=1)
            label(image, 91, 534, "Separate notes do not guarantee separate files.", 23, CYAN, width=1100)
        elif scene == "flow":
            if len(labels) == 4 and ("Worker A" in labels or "A + B" in labels[1]):
                node(image, 80, 308, labels[0], GREEN, phase == 0)
                node(image, 520, 222, labels[1], BLUE, phase == 1)
                node(image, 520, 411, labels[2] if "Worker B" in labels else "Worker B", CYAN, phase == 1)
                node(image, 975, 308, labels[-1], PURPLE, phase == 2)
                edges = [((295, 360), (520, 275)), ((295, 360), (520, 463)),
                         ((735, 275), (975, 360)), ((735, 463), (975, 360))]
                for edge, (a, b) in enumerate(edges):
                    arrow(image, a, b)
                    if (phase == 1 and edge < 2) or (phase == 2 and edge >= 2):
                        packet(image, a, b, time, color=CYAN)
            else:
                count = len(labels)
                gap = 930 / max(1, count - 1)
                for i, name in enumerate(labels):
                    x = 66 + i * gap
                    y = 318 + 65 * (1 - ease((time - i * 0.2) / 0.7))
                    node(image, x, y, name, COLORS[i % 4], i == int(time / 4) % count)
                    if i < count - 1:
                        arrow(image, (x + 217, 370), (x + gap, 370))
                        packet(image, (x + 217, 370), (x + gap, 370), time, i)
                label(image, 80, 496, "An arrow means a real dependency, not a wish.", 27, CYAN, width=1100)
        elif scene in ("brief", "recipe"):
            count = len(labels)
            for i, name in enumerate(labels):
                x = 83 + i * (1080 / count)
                y = 275 + 70 * (1 - ease((time - i * 0.25) / 0.7))
                rect(image, (x, y, x + 1020 / count, y + 190), "#24243b",
                     COLORS[i % 4] if i == int(time / 4) % count else "#596577")
                label(image, x + 14, y + 17, f"{i + 1:02}", 37, COLORS[i % 4], True, 120)
                label(image, x + 14, y + 78, name, 27, WHITE, True, 1020 / count - 28, max_lines=3)
            footer = ("Goal + context + write set + checks." if scene == "brief"
                      else "Load the recipe when relevant. Tools stay separately controlled.")
            label(image, 85, 517, footer, 24, CYAN, width=1100)
        elif scene == "review":
            count = len(labels)
            for i, name in enumerate(labels):
                y = 212 + i * (310 / max(1, count)) + 35 * (1 - ease((time - i * 0.18) / 0.8))
                rect(image, (90, y, 1180, y + 62), "#24283a", COLORS[i % 4])
                limited = "not run" in name.casefold()
                failed = "failed" in name.casefold()
                active = time > 1 + i * 1.0 and not limited
                ImageDraw.Draw(image).rectangle((115, y + 17, 140, y + 42),
                                               outline=ORANGE if failed else (GREEN if active else "#919aad"), width=3)
                if active and failed:
                    ImageDraw.Draw(image).line((119, y + 21, 136, y + 39), ORANGE, 4)
                    ImageDraw.Draw(image).line((119, y + 39, 136, y + 21), ORANGE, 4)
                elif active:
                    ImageDraw.Draw(image).line((119, y + 29, 126, y + 37, 140, y + 19), GREEN, 4)
                label(image, 162, y + 15, name, 27, WHITE, width=940, max_lines=1)
            label(image, 89, 529, "Passed / failed / not run are different outcomes.", 25, CYAN, width=1100)
        elif scene == "compare":
            for i, name in enumerate(labels[:2]):
                x = 85 + i * 610
                offset = 28 * (1 - ease((time - i * 0.22) / 0.8))
                node(image, x, 264 + offset, name, CYAN if i == 0 else PURPLE, phase % 2 == i, 500)
                label(image, x + 20, 398 + offset, "Check the selected runtime\nand actual behavior.", 27, WHITE, width=460, max_lines=2)
            label(image, 90, 526, labels[-1] if len(labels) > 2 else "Different controls solve different problems.", 29, GREEN, True, 1090, max_lines=1)
        elif scene == "code":
            code = self.beat["code"]
            rows = code.splitlines()
            rect(image, (74, 210, 1206, 537), "#101521", BLUE)
            active = int(time / 4) % max(1, len(rows))
            rect(image, (95, 230 + active * 46, 1185, 275 + active * 46), "#25334e", radius=7)
            for i, row in enumerate(rows):
                label(image, 110, 237 + i * 46, row, 27, CYAN, width=1050, mono=True, max_lines=1)
        elif scene == "interface":
            if variant == "modes":
                for i, row in enumerate((["Plan", "Interactive", "Autopilot"], ["Manual", "Assisted", "Approve all"])):
                    label(image, 83, 213 + i * 157, "Workflow mode" if i == 0 else "Tool permissions", 26, CYAN, True, 1100)
                    for j, name in enumerate(row):
                        node(image, 83 + j * 391, 257 + i * 157, name, COLORS[j], j == int(time / (4 + i)) % 3, 350)
            else:
                for x, width in ((70, 240), (330, 570), (920, 285)):
                    rect(image, (x, 210, x + width, 544), "#24283a", BLUE)
                label(image, 88, 226, labels[0], 25, CYAN, True, 205, max_lines=2)
                for i in range(3):
                    rect(image, (88, 323 + i * 62, 290, 372 + i * 62),
                         "#3c2f65" if i == int(time / 4) % 3 else "#161d2a", radius=8)
                    label(image, 99, 336 + i * 62, f"Task {i + 1}", 24, WHITE, width=175)
                label(image, 353, 229, labels[1], 29, PURPLE, True, 515, max_lines=2)
                label(image, 354, 330, "Goal\nAllowed files\nAcceptance checks", 28, WHITE, width=500, max_lines=3)
                label(image, 941, 230, labels[-1], 25, GREEN, True, 240, max_lines=3)
                label(image, 941, 386, "Files\nChanges\nChecks", 27, WHITE, width=235, max_lines=3)
        elif scene == "score":
            if variant == "boundary":
                for i, (value, caption, color) in enumerate((("75", "P2", BLUE), ("80", "threshold", ORANGE), ("85", "P1", GREEN))):
                    x = 96 + i * 395
                    offset = 30 * (1 - ease((time - i * 0.2) / 0.8))
                    rect(image, (x, 233 + offset, x + 345, 449 + offset), "#24243b",
                         WHITE if i == int(time / 4) % 3 else color)
                    label(image, x + 36, 250 + offset, value, 82, color, True, 270)
                    label(image, x + 36, 362 + offset, caption, 33, WHITE, True, 270)
                label(image, 97, 488, "80 is unreachable here: test nearest 75 and 85.", 28, CYAN, width=1100)
            else:
                score = [0, 60, 85, 95, 100][min(4, int(time / 2))]
                if variant == "closed":
                    score = 0
                label(image, 93, 222, str(score), 104, GREEN if score >= 80 else CYAN, True, 280)
                label(image, 379, 255, "P1" if score >= 80 else ("P2" if score >= 40 else "P3"), 61, PURPLE, True, 225)
                rect(image, (93, 362, 1180, 402), "#293148", radius=10)
                if score:
                    rect(image, (93, 362, 93 + 1087 * score / 100, 402), GREEN, radius=10)
                for i, name in enumerate(labels[:4]):
                    label(image, 95 + i * 272, 446, name, 26, COLORS[i], True, 245, max_lines=2)
                if variant == "closed":
                    label(image, 96, 529, "Closed override: zero / P3 / closed reason only.", 27, ORANGE, width=1100)
        elif scene == "filter":
            if variant == "all":
                for i, (number, caption) in enumerate((("8", "visible"), ("6", "active"), ("2", "active blocked"))):
                    x = 93 + i * 393
                    offset = 28 * (1 - ease((time - i * 0.2) / 0.8))
                    label(image, x, 227 + offset, number, 104, COLORS[i], True, 325)
                    label(image, x, 367 + offset, caption, 32, WHITE, True, 325)
                label(image, 95, 484, "Four categories. Two fictional issues in each.", 28, CYAN, width=1080)
            else:
                query = "PAYMENTS"[:min(8, int(time * 3))]
                rect(image, (79, 211, 1205, 265), "#101521", CYAN)
                label(image, 100, 221, "Search: " + query, 28, WHITE, width=1040)
                for i, (identity, status, color) in enumerate((("ISS-101", "active / P1", GREEN), ("ISS-105", "closed / P3", "#aab3c0"))):
                    x = 89 + i * 548
                    rect(image, (x, 297, x + 509, 455), "#24243b", color)
                    label(image, x + 20, 310, identity, 35, color, True, 467)
                    label(image, x + 20, 377, status, 30, WHITE, width=467)
                if variant == "export":
                    label(image, 92, 497, "Export: ISS-101 only. Closed issue stays out.", 29, GREEN, True, 1090)
                    packet(image, (270, 450), (500, 516), time, color=GREEN)
                else:
                    label(image, 92, 499, "2 visible | 1 active | 1 active blocked", 29, CYAN, True, 1090)
        elif scene == "branch":
            node(image, 78, 300, labels[0], GREEN, True, 244)
            node(image, 558, 218, labels[1], BLUE, phase == 1, 244)
            node(image, 558, 408, labels[2], CYAN, phase == 1, 244)
            for a, b in (((322, 353), (558, 271)), ((322, 353), (558, 461))):
                arrow(image, a, b)
                packet(image, a, b, time, color=BLUE)
            node(image, 943, 300, "Integrate + retest", PURPLE, phase == 2, 254)
            for a, b in (((802, 271), (943, 353)), ((802, 461), (943, 353))):
                arrow(image, a, b)
                packet(image, a, b, time, 2, PURPLE)
            label(image, 91, 529, "Working copies differ. Machine access is separate.", 25, CYAN, width=1090)
        elif scene == "board":
            for i, name in enumerate(("Ready", "Working", "Review", "Done")):
                x = 76 + i * 296
                label(image, x + 4, 218, name, 25, COLORS[i], True, 268, max_lines=2)
                rect(image, (x, 264, x + 273, 545), "#24283a", "#495365")
            for i, name in enumerate(labels[:4]):
                x = 86 + 888 * ease((time - i * 1.4) / 12)
                y = 270 + i * 67
                rect(image, (x, y, x + 253, y + 61), "#253854", COLORS[i])
                label(image, x + 10, y + 5, name, 21, WHITE, True, 232, max_lines=2)
        else:
            raise ValueError(f"Unsupported teaching scene: {scene}")
        return image


def phrase_cues(chunks, max_words=12):
    result = []
    for chunk in chunks:
        words = chunk["text"].split()
        pieces = [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
        offset = chunk["offset_seconds"]
        for text in pieces:
            duration = chunk["duration_seconds"] * len(text.split()) / len(words)
            result.append({"text": text, "start": offset, "end": offset + duration})
            offset += duration
    return result


class Chapter:
    def __init__(self, source, recorded, duration):
        if len(source["beats"]) != len(recorded["chunks"]):
            raise ValueError("Every visual beat needs exactly one narration clip.")
        self.source, self.recorded, self.duration = source, recorded, duration
        self.scenes = [Scene(source, beat) for beat in source["beats"]]
        self.cues = phrase_cues(recorded["chunks"])
        self.caption_cache = {}

    def frame(self, time):
        active = 0
        for index, chunk in enumerate(self.recorded["chunks"]):
            if chunk["offset_seconds"] <= time:
                active = index
        chunk = self.recorded["chunks"][active]
        local = max(0, time - chunk["offset_seconds"])
        image = self.scenes[active].frame(local, chunk["duration_seconds"])
        if active and local < 0.35:
            previous = self.recorded["chunks"][active - 1]
            earlier = self.scenes[active - 1].frame(previous["duration_seconds"], previous["duration_seconds"])
            image = Image.blend(earlier, image, local / 0.35)
        cue = next((cue for cue in self.cues if cue["start"] <= time < cue["end"]), None)
        if cue:
            text = cue["text"]
            if text not in self.caption_cache:
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                rect(layer, (42, 606, 1238, 704), "#080b12", radius=12)
                label(layer, 67, 617, text, 29, WHITE, width=1142, max_lines=2)
                self.caption_cache[text] = layer
            image.paste(self.caption_cache[text], (0, 0), self.caption_cache[text])
        progress = min(1, time / self.duration)
        ImageDraw.Draw(image).rectangle((0, 714, int(W * progress), 719), fill=CYAN)
        return image


def render(path, source, recorded, duration, bitrate_kbps):
    cache = path.with_suffix(".sha256")
    fingerprint = hashlib.sha256(json.dumps({
        "source": source, "recorded": recorded, "duration": duration, "fps": FPS, "bitrate": bitrate_kbps,
        "renderer": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }, sort_keys=True).encode()).hexdigest()
    if path.is_file() and cache.is_file() and cache.read_text() == fingerprint:
        return
    chapter = Chapter(source, recorded, duration)
    process = subprocess.Popen(
        [imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1280x720", "-r", str(FPS),
         "-i", "pipe:0", "-an", "-c:v", "libx264", "-preset", "veryfast",
         "-threads", "2",
         "-b:v", f"{bitrate_kbps}k", "-maxrate", f"{bitrate_kbps * 2}k",
         "-bufsize", f"{bitrate_kbps * 8}k", "-pix_fmt", "yuv420p", str(path)],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    try:
        for index in range(round(duration * FPS)):
            process.stdin.write(chapter.frame(index / FPS).tobytes())
        process.stdin.close()
        error = process.stderr.read().decode("utf-8", errors="replace")
        if process.wait() != 0:
            raise RuntimeError(error)
    except (BrokenPipeError, OSError):
        error = process.stderr.read().decode("utf-8", errors="replace")
        process.wait()
        raise RuntimeError(error) from None
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    cache.write_text(fingerprint, encoding="ascii")
