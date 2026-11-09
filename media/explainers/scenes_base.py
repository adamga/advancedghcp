"""Scene base class and shared layout helpers for the explainer renderer."""

import math
from functools import lru_cache

from PIL import Image, ImageDraw

from gfx import (ACCENT_CYCLE, Background, COLORS, H, W, clamp, draw_robot, ease_in_out, ease_out, font, glow_blob, mix,
                 pill, panel, paste, paste_center, pop, prog, put_text, rgb, rgba, text_width, wrap, draw_text)

SAFE_TOP = 84
SAFE_BOTTOM = 676
INTRO_MIN_FIRST_CUE = 2.4
INTRO_START = 0.3
INK = (10, 12, 22, 255)
WHITE = (240, 246, 252, 255)
SOFT = (200, 210, 226, 255)
MUTED = (139, 148, 158, 255)


@lru_cache(maxsize=256)
def _center_offset(kind, size):
    box = font(kind, size).getbbox("Ag")
    return (box[1] + box[3]) / 2


def centered_text(img, cx, cy, text, kind, size, fill, align="center", draw=None):
    """Draw single-line text whose visual middle sits at cy."""
    f = font(kind, size)
    return draw_text(img, (cx, cy - _center_offset(kind, size)), text, f, fill, align, draw=draw)


def text_block(img, x, y, lines, kind, size, fill, leading, align="left"):
    f = font(kind, size)
    d = ImageDraw.Draw(img, "RGBA")
    for index, line in enumerate(lines):
        draw_text(img, (x, y + index * leading), line, f, fill, align, draw=d)
    return y + len(lines) * leading


def fit_font(text, kind, size, max_w, minimum=16):
    """Largest font (<= size) that renders text on one line within max_w."""
    while size > minimum and text_width(text, font(kind, size)) > max_w:
        size -= 1
    return font(kind, size)


def appear(t, cue_time, duration=0.45):
    """0..1 ease-out fade/slide progress starting at cue_time."""
    return ease_out(prog(t, cue_time, duration))


def arrow(img, start, end, color, width=6, head=18, alpha=255, progress=1.0):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0 = start
    x1, y1 = end
    x1 = x0 + (x1 - x0) * progress
    y1 = y0 + (y1 - y0) * progress
    d.line([(x0, y0), (x1, y1)], fill=rgba(color, alpha), width=width)
    if progress >= 0.98:
        ang = math.atan2(y1 - y0, x1 - x0)
        for side in (-1, 1):
            a = ang + math.pi + side * 0.5
            d.line([(x1, y1), (x1 + math.cos(a) * head, y1 + math.sin(a) * head)], fill=rgba(color, alpha), width=width)


def glow_ring(img, rect, color, t, strength=1.0, radius=14, width=4):
    x0, y0, x1, y1 = rect
    pulse = 0.5 + 0.5 * math.sin(t * 6)
    grow = 3 + 5 * pulse
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([x0 - grow, y0 - grow, x1 + grow, y1 + grow], radius=radius + grow,
                        outline=rgba(color, int((150 + 100 * pulse) * strength)), width=width)


@lru_cache(maxsize=256)
def card_panel(w, h, color=None, radius=20, fill=(20, 24, 40, 238), glow=False):
    sprite, pad = panel(w, h, radius=radius, fill=fill, outline=rgba(color) if color else None, outline_w=3,
                        glow=color if glow else None, glow_r=12)
    return sprite, pad


def put_panel(img, x, y, w, h, color=None, alpha=1.0, scale=1.0, glow=False, radius=20, fill=(20, 24, 40, 238)):
    sprite, pad = card_panel(int(w), int(h), color, radius, fill, glow)
    if scale != 1.0:
        paste_center(img, sprite, x + w / 2, y + h / 2, scale, alpha)
    else:
        paste(img, sprite, x - pad, y - pad, alpha)


def build_card(w, h, color, painter, glow=True, fill=(20, 24, 40, 238), radius=20, outline_w=3):
    """Panel sprite (with glow padding) that `painter(sprite, pad)` decorates."""
    sprite, pad = panel(int(w), int(h), radius=radius, fill=fill, outline=rgba(color) if color else None,
                        outline_w=outline_w, glow=color if (glow and color) else None, glow_r=12)
    out = sprite.copy()
    painter(out, pad)
    return out


def flow_rows(widths, max_width, gap):
    """Greedy wrap of item widths into rows; returns lists of indices."""
    rows, current, used = [], [], 0
    for index, width in enumerate(widths):
        need = width + (gap if current else 0)
        if current and used + need > max_width:
            rows.append(current)
            current, used = [], 0
            need = width
        current.append(index)
        used += need
    if current:
        rows.append(current)
    return rows


class Scene:
    uses_art = False
    mode = "dim"
    # Kinds that already show content from the first frame turn the chapter intro card off.
    intro = True
    intro_width = 1040
    own_robot = False

    def __init__(self, spec, timing, index, count):
        self.spec = spec
        self.p = spec.get("params", {})
        self.tm = timing
        self.index = index
        self.count = count
        self.accent = ACCENT_CYCLE[index % len(ACCENT_CYCLE)]
        self.duration = timing.duration
        self.setup()
        self.intro_window = self._intro_window()
        art = spec.get("art")
        self.bg = Background(art, self.mode, tint=self.accent, seed=index * 7 + 3,
                             motion=self.p.get("motion", "in"), duration=self.duration)

    def setup(self):
        pass

    def cue(self, phrase, kind="pop"):
        return self.tm.cue(phrase, kind)

    def cues(self, items, key="cue", kind="pop", start=0.7, step=0.6):
        """Cue time per item; items without a cue are staggered so they still appear."""
        times = []
        for index, item in enumerate(items):
            when = self.tm.cue(item.get(key), kind) if item.get(key) else None
            times.append(when if when is not None else start + index * step)
        return times

    def heading(self, img, t, text, cy=102, size=38, color="white"):
        p = pop(t, 0.15, 0.5)
        if p <= 0:
            return
        put_text(img, text, W / 2, cy, "black", size, rgba(color), glow=self.accent, scale=min(p, 1.04))

    def shake(self, t):
        return 0.0

    def draw(self, img, t):
        raise NotImplementedError

    def _intro_window(self):
        """(start, end) of the chapter card, shown while nothing else has appeared yet."""
        if not self.intro:
            return None
        times = [when for when, kind in self.tm.events if kind != "whoosh"]
        if not times or min(times) < INTRO_MIN_FIRST_CUE:
            return None
        return INTRO_START, min(times) - 0.15

    def draw_intro(self, img, t):
        """Big bouncing chapter title with orbiting sparkles so the opening seconds are never empty."""
        if not self.intro_window:
            return
        start, end = self.intro_window
        enter = pop(t, start, 0.6)
        fade = 1 - ease_in_out(prog(t, end - 0.25, 0.4))
        if enter <= 0.01 or fade <= 0.01:
            return
        alpha = min(1.0, enter) * fade
        leaving = 1 - fade
        cx, cy = W / 2, 318
        title = self.spec["chapter"]
        hook = self.spec.get("hook")

        paste_center(img, glow_blob(340, self.accent, 130), cx, cy + 10, 1.0 + 0.06 * math.sin(t * 3.0), alpha)

        d = ImageDraw.Draw(img, "RGBA")
        for k in range(8):
            ang = t * (0.8 + 0.11 * k) + k * 0.8
            sx, sy = cx + math.cos(ang) * (300 + 38 * (k % 3)), cy + math.sin(ang) * (118 + 12 * (k % 2))
            s = 13 + 4 * (k % 3) + 4 * math.sin(t * 4 + k)
            color = rgba(ACCENT_CYCLE[(self.index + k) % len(ACCENT_CYCLE)], int(255 * alpha * (0.55 + 0.45 * math.sin(t * 5 + k))))
            d.polygon([(sx, sy - s), (sx + s * .3, sy - s * .3), (sx + s, sy), (sx + s * .3, sy + s * .3),
                       (sx, sy + s), (sx - s * .3, sy + s * .3), (sx - s, sy), (sx - s * .3, sy - s * .3)], fill=color)

        put_text(img, f"CHAPTER {self.index + 1} OF {self.count}", cx, cy - 98, "bold", 26, rgba(self.accent), alpha=alpha)
        size = 100
        while size > 44 and text_width(title, font("black", size)) > self.intro_width:
            size -= 2
        scale = min(enter, 1.06) * (1 + 0.14 * leaving)
        put_text(img, title, cx, cy, "black", size, WHITE, glow=self.accent, scale=scale, alpha=alpha,
                 angle=math.sin(t * 2.2) * 1.3)
        sweep = ease_out(prog(t, start + 0.35, 0.5))
        half = min(text_width(title, font("black", size)) / 2, self.intro_width / 2) * sweep
        d.rounded_rectangle([cx - half, cy + 62, cx + half, cy + 68], radius=3, fill=rgba(self.accent, int(255 * alpha)))
        if hook:
            hook_alpha = appear(t, start + 0.7, 0.5) * fade
            if hook_alpha > 0.01:
                hook_size = 40
                while hook_size > 24 and text_width(hook, font("bold", hook_size)) > 1000:
                    hook_size -= 1
                put_text(img, hook, cx, cy + 118, "bold", hook_size, rgba(SOFT), alpha=hook_alpha)
        if not self.own_robot:
            draw_robot(img, self.accent, cx, 556, 170, t, phase=self.index * 0.9, mood="happy", prop="clipboard",
                       scale=min(enter, 1.05) * (1 - 0.1 * leaving), alpha=alpha)

    def render(self, t):
        img = self.bg.frame(t, self.shake(t))
        self.draw(img, t)
        self.draw_intro(img, t)
        return img
