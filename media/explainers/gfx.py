"""Shared Pillow drawing toolkit for the explainer renderer.

Everything is procedural so there are no dependencies beyond Pillow: panels,
glow text, colour emoji sprites, animated robot sprites, backgrounds,
confetti and the scene-transition curtain. Expensive sprites are cached.
"""

import math
import os
import random
import re
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1280, 720, 24
ART_DIR = Path(__file__).resolve().parent / "art"
FONT_DIR = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
FONT_FILES = {
    "reg": "segoeui.ttf", "bold": "segoeuib.ttf", "black": "seguibl.ttf", "mono": "consola.ttf",
    "monob": "consolab.ttf", "emoji": "seguiemj.ttf", "display": "bahnschrift.ttf",
}

COLORS = {
    "cyan": (77, 225, 245), "purple": (163, 113, 247), "green": (86, 211, 100),
    "orange": (255, 152, 85), "pink": (255, 105, 180), "red": (255, 95, 95),
    "blue": (74, 144, 255), "yellow": (255, 214, 10), "muted": (139, 148, 158),
    "white": (240, 246, 252), "ink": (12, 14, 26), "panel": (23, 27, 42), "bg": (10, 12, 20),
}
ACCENT_CYCLE = ["cyan", "purple", "pink", "orange", "green", "blue"]


def rgb(color):
    return COLORS[color] if isinstance(color, str) else tuple(color[:3])


def rgba(color, alpha=255):
    r, g, b = rgb(color)
    return (r, g, b, alpha)


def mix(a, b, t):
    a, b = rgb(a), rgb(b)
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def shade(color, factor):
    """factor < 1 darkens toward black; factor > 1 lightens toward white."""
    if factor <= 1:
        return mix(color, (0, 0, 0), 1 - factor)
    return mix(color, (255, 255, 255), min(1.0, factor - 1))


# ---------------------------------------------------------------- easing

def clamp(x, low=0.0, high=1.0):
    return low if x < low else high if x > high else x


def prog(t, start, duration):
    return clamp((t - start) / duration) if duration > 0 else (1.0 if t >= start else 0.0)


def ease_out(p):
    return 1 - (1 - p) ** 3


def ease_in_out(p):
    return 3 * p * p - 2 * p * p * p


def back_out(p, overshoot=1.9):
    p -= 1
    return 1 + (overshoot + 1) * p ** 3 + overshoot * p ** 2


def pop(t, start, duration=0.5):
    """0 before start, then springs to 1 with a little overshoot."""
    if t < start:
        return 0.0
    return back_out(prog(t, start, duration))


# ----------------------------------------------------------------- fonts

@lru_cache(maxsize=None)
def font(kind, size):
    path = FONT_DIR / FONT_FILES[kind]
    if not path.is_file():
        path = FONT_DIR / FONT_FILES["bold" if kind in ("black", "display") else "reg"]
    return ImageFont.truetype(str(path), int(size))


SPECIAL_RE = re.compile("([\U0001F000-\U0001FAFF\u2300-\u23FF\u2600-\u26FF\u2705\u2753\u2B00-\u2BFF\u2713\u2717\u2714\u2716\ufe0f])")
ICONS = {"\u2713": "check", "\u2717": "cross"}


@lru_cache(maxsize=1024)
def emoji_sprite(char, px):
    char = char.replace("\ufe0f", "")
    f = ImageFont.truetype(str(FONT_DIR / FONT_FILES["emoji"]), int(px * 1.0))
    size = int(px * 2)
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((px * 0.4, px * 0.2), char, font=f, embedded_color=True)
    box = layer.getchannel("A").getbbox()
    if not box:
        return Image.new("RGBA", (int(px), int(px)), (0, 0, 0, 0))
    layer = layer.crop(box)
    scale = px / max(layer.size)
    return layer.resize((max(1, round(layer.width * scale)), max(1, round(layer.height * scale))), Image.LANCZOS)


@lru_cache(maxsize=64)
def icon_sprite(name, px, color):
    big = px * 4
    layer = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    fill = rgba(color)
    d.ellipse([big * 0.04, big * 0.04, big * 0.96, big * 0.96], fill=fill)
    ink = (10, 12, 20, 255)
    if name == "check":
        d.line([(big * 0.26, big * 0.53), (big * 0.44, big * 0.70), (big * 0.75, big * 0.33)],
               fill=ink, width=int(big * 0.13), joint="curve")
    else:
        d.line([(big * 0.31, big * 0.31), (big * 0.69, big * 0.69)], fill=ink, width=int(big * 0.13))
        d.line([(big * 0.69, big * 0.31), (big * 0.31, big * 0.69)], fill=ink, width=int(big * 0.13))
    return layer.resize((px, px), Image.LANCZOS)


def _runs(text):
    return [part for part in SPECIAL_RE.split(text) if part and part != "\ufe0f"]


def text_width(text, f):
    total = 0
    for part in _runs(text):
        if SPECIAL_RE.fullmatch(part):
            total += round(f.size * 1.15)
        else:
            total += f.getlength(part)
    return total


def draw_text(img, xy, text, f, fill, align="left", icon_color=None, draw=None):
    """Draw text (with colour emoji and check/cross icons) with its top at y."""
    x, y = xy
    width = text_width(text, f)
    if align == "center":
        x -= width / 2
    elif align == "right":
        x -= width
    draw = draw or ImageDraw.Draw(img, "RGBA")
    if not SPECIAL_RE.search(text):
        draw.text((x, y), text, font=f, fill=fill)
        return width
    for part in _runs(text):
        if SPECIAL_RE.fullmatch(part):
            px = round(f.size * 1.05)
            if part in ICONS:
                sprite = icon_sprite(ICONS[part], px, icon_color or fill[:3])
            else:
                sprite = emoji_sprite(part, px)
            img.paste(sprite, (round(x + (f.size * 1.15 - sprite.width) / 2), round(y + f.size * 0.12 + (px - sprite.height) / 2)), sprite)
            x += f.size * 1.15
        else:
            draw.text((x, y), part, font=f, fill=fill)
            x += f.getlength(part)
    return width


def wrap(text, f, max_width):
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if text_width(trial, f) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit(text, kind, max_width, max_height, size, minimum=13, leading=1.22):
    """Largest font size (<= size) whose wrapped text fits the box."""
    while True:
        f = font(kind, size)
        lines = wrap(text, f, max_width)
        height = len(lines) * size * leading
        widest = max((text_width(line, f) for line in lines), default=0)
        if (height <= max_height and widest <= max_width) or size <= minimum:
            return f, lines, size * leading
        size -= 1


def draw_lines(img, x, y, lines, f, fill, leading, align="left", draw=None):
    draw = draw or ImageDraw.Draw(img, "RGBA")
    for index, line in enumerate(lines):
        draw_text(img, (x, y + index * leading), line, f, fill, align, draw=draw)
    return y + len(lines) * leading


# --------------------------------------------------------------- sprites

def paste(img, sprite, x, y, alpha=1.0):
    if alpha <= 0.01:
        return
    x, y = round(x), round(y)
    if alpha >= 0.99:
        img.paste(sprite, (x, y), sprite)
        return
    mask = sprite.getchannel("A").point(lambda v, a=alpha: int(v * a))
    img.paste(sprite, (x, y), mask)


def paste_center(img, sprite, cx, cy, scale=1.0, alpha=1.0, angle=0.0):
    if scale <= 0.02 or alpha <= 0.01:
        return
    if angle:
        sprite = sprite.rotate(angle, resample=Image.BICUBIC)
    if abs(scale - 1) > 0.005:
        sprite = sprite.resize((max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale))), Image.BILINEAR)
    paste(img, sprite, cx - sprite.width / 2, cy - sprite.height / 2, alpha)


@lru_cache(maxsize=1024)
def panel(w, h, radius=18, fill=(23, 27, 42, 235), outline=None, outline_w=2, glow=None, glow_r=14, shadow=True):
    """Anti-aliased rounded panel; returns (sprite, pad). Paste at (x - pad, y - pad)."""
    pad = glow_r * 2 if (glow or shadow) else 2
    ss = 2
    big = Image.new("RGBA", ((w + pad * 2) * ss, (h + pad * 2) * ss), (0, 0, 0, 0))
    box = [pad * ss, pad * ss, (pad + w) * ss - 1, (pad + h) * ss - 1]
    base = Image.new("RGBA", big.size, (0, 0, 0, 0))
    if glow:
        g = ImageDraw.Draw(base)
        g.rounded_rectangle(box, radius=radius * ss, fill=rgba(glow, 150))
        base = base.filter(ImageFilter.GaussianBlur(glow_r * ss * 0.55))
    elif shadow:
        g = ImageDraw.Draw(base)
        g.rounded_rectangle([box[0], box[1] + 5 * ss, box[2], box[3] + 5 * ss], radius=radius * ss, fill=(0, 0, 0, 120))
        base = base.filter(ImageFilter.GaussianBlur(7 * ss))
    big = Image.alpha_composite(big, base)
    d = ImageDraw.Draw(big)
    d.rounded_rectangle(box, radius=radius * ss, fill=fill, outline=outline, width=outline_w * ss if outline else 0)
    return big.resize((w + pad * 2, h + pad * 2), Image.LANCZOS), pad


def draw_panel(img, x, y, w, h, alpha=1.0, scale=1.0, **kwargs):
    sprite, pad = panel(int(w), int(h), **kwargs)
    if scale != 1.0:
        paste_center(img, sprite, x + w / 2, y + h / 2, scale, alpha)
    else:
        paste(img, sprite, x - pad, y - pad, alpha)


@lru_cache(maxsize=512)
def text_sprite(text, kind, size, fill, glow=None, stroke=0, stroke_fill=(0, 0, 0)):
    f = font(kind, size)
    width = int(text_width(text, f)) + 8 + 60
    height = int(size * 1.5) + 60
    layer = Image.new("RGBA", (width, height), tuple(fill[:3]) + (0,))
    if glow:
        halo = Image.new("RGBA", layer.size, rgb(glow) + (0,))
        hd = ImageDraw.Draw(halo)
        hd.text((34, 28), text, font=f, fill=rgba(glow, 255), stroke_width=max(2, size // 22), stroke_fill=rgba(glow, 255))
        halo = halo.filter(ImageFilter.GaussianBlur(max(5, size // 7)))
        layer = Image.alpha_composite(layer, halo)
        layer = Image.alpha_composite(layer, halo)
    d = ImageDraw.Draw(layer, "RGBA")
    if SPECIAL_RE.search(text):
        draw_text(layer, (34, 28), text, f, fill, draw=d)
    else:
        d.text((34, 28), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return layer


def put_text(img, text, cx, cy, kind, size, fill, glow=None, scale=1.0, alpha=1.0, angle=0.0, stroke=0):
    sprite = text_sprite(text, kind, size, tuple(fill), glow, stroke)
    paste_center(img, sprite, cx, cy, scale, alpha, angle)
    return sprite.width - 68


@lru_cache(maxsize=64)
def glow_blob(radius, color, strength=90):
    size = radius * 2
    gradient = Image.radial_gradient("L").resize((size, size), Image.BILINEAR)
    alpha = gradient.point(lambda v: int(strength * (1 - min(1.0, v / 178)) ** 2))
    layer = Image.new("RGBA", (size, size), rgb(color) + (0,))
    layer.putalpha(alpha)
    return layer


# --------------------------------------------------------------- robots

@lru_cache(maxsize=256)
def robot(color, size=200, mood="happy", prop=None, blink=False, lock=False):
    ss = 3
    S = int(size * ss)
    k = S / 120.0
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    base, dark, light = rgb(color), shade(color, 0.5), shade(color, 1.45)
    eye = mix(color, (255, 255, 255), 0.65)

    def R(x0, y0, x1, y1):
        return [x0 * k, y0 * k, x1 * k, y1 * k]

    def line(points, fill, width):
        d.line([(x * k, y * k) for x, y in points], fill=fill, width=int(width * k), joint="curve")

    def dot(x, y, r, fill, outline=None):
        d.ellipse([(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k], fill=fill, outline=outline, width=int(1.5 * k))

    # legs, arms, body
    for x in (46, 66):
        d.rounded_rectangle(R(x, 100, x + 10, 114), radius=4 * k, fill=dark)
        d.rounded_rectangle(R(x - 2, 111, x + 12, 117), radius=3 * k, fill=shade(color, 0.4))
    line([(40, 72), (25, 90)], dark, 8)
    dot(25, 90, 5, light)
    line([(80, 72), (95, 90)], dark, 8)
    dot(95, 90, 5, light)
    d.rounded_rectangle(R(38, 62, 82, 104), radius=14 * k, fill=base, outline=dark, width=int(2 * k))
    d.rounded_rectangle(R(46, 72, 74, 95), radius=8 * k, fill=shade(color, 0.7))
    dot(60, 83, 5, (255, 255, 255), outline=light)
    d.rectangle(R(54, 57, 66, 63), fill=dark)

    # head
    d.rounded_rectangle(R(30, 22, 90, 60), radius=16 * k, fill=base, outline=dark, width=int(2 * k))
    d.rounded_rectangle(R(24, 32, 31, 50), radius=3 * k, fill=dark)
    d.rounded_rectangle(R(89, 32, 96, 50), radius=3 * k, fill=dark)
    d.rounded_rectangle(R(36, 29, 84, 53), radius=10 * k, fill=(12, 14, 26))
    if prop != "hat":
        line([(60, 22), (60, 13)], dark, 3)
        dot(60, 10, 5, light, outline=(255, 255, 255))

    # eyes and mouth
    ex = (50, 70)
    if blink:
        for x in ex:
            line([(x - 5, 41), (x + 5, 41)], eye, 2.6)
    elif mood == "dizzy":
        for x in ex:
            line([(x - 4, 37), (x + 4, 45)], eye, 2.4)
            line([(x + 4, 37), (x - 4, 45)], eye, 2.4)
    else:
        r = 6.4 if mood in ("wow", "worried") else 5.4
        for x in ex:
            dot(x, 41, r, eye)
            dot(x + 1.5, 39.5, 1.9, (255, 255, 255))
    if mood == "happy":
        d.arc(R(53, 42, 67, 52), 20, 160, fill=eye, width=int(2.2 * k))
    elif mood == "wow":
        d.ellipse(R(56.5, 46, 63.5, 52), outline=eye, width=int(2 * k))
    elif mood == "worried":
        line([(43, 36), (55, 32)], eye, 2.2)
        line([(77, 36), (65, 32)], eye, 2.2)
        d.arc(R(54, 47, 66, 56), 200, 340, fill=eye, width=int(2 * k))
        dot(99, 28, 3.2, (120, 190, 255))
    elif mood == "dizzy":
        line([(54, 49), (58, 47), (62, 49), (66, 47)], eye, 2)

    # props
    if prop == "clipboard":
        d.rounded_rectangle(R(93, 72, 119, 108), radius=3 * k, fill=(150, 104, 60))
        d.rounded_rectangle(R(95, 76, 117, 106), radius=2 * k, fill=(236, 240, 248))
        d.rounded_rectangle(R(99, 70, 113, 78), radius=2 * k, fill=(170, 178, 190))
        for y in (84, 91):
            line([(98, y), (114, y)], (120, 130, 150), 2)
        line([(99, 98), (103, 102), (111, 94)], rgb("green"), 2.4)
    elif prop == "magnifier":
        dot(105, 82, 11, (150, 220, 255, 70), outline=(215, 235, 255))
        d.ellipse(R(94, 71, 116, 93), outline=(215, 235, 255), width=int(3 * k))
        line([(112, 90), (119, 100)], (215, 235, 255), 4.5)
    elif prop == "wrench":
        line([(98, 104), (113, 80)], (205, 212, 224), 5.5)
        dot(115, 77, 7, (205, 212, 224))
        dot(118, 74, 3.4, (12, 14, 26))
    elif prop == "hat":
        d.rounded_rectangle(R(44, 18, 76, 28), radius=3 * k, fill=(34, 36, 58))
        d.polygon([(26 * k, 18 * k), (60 * k, 7 * k), (94 * k, 18 * k), (60 * k, 29 * k)], fill=(46, 48, 76), outline=light)
        line([(90, 18), (90, 34)], rgb("yellow"), 2)
        dot(90, 36, 3, rgb("yellow"))
    if lock:
        yellow = rgb("yellow")
        d.arc(R(5, 56, 21, 78), 180, 360, fill=shade("yellow", 0.7), width=int(3.4 * k))
        d.rounded_rectangle(R(2, 67, 24, 87), radius=4 * k, fill=yellow, outline=shade("yellow", 0.6), width=int(1.5 * k))
        dot(13, 76, 2.6, (12, 14, 26))
        line([(13, 77), (13, 81)], (12, 14, 26), 2)
    return im.resize((size, size), Image.LANCZOS)


def draw_robot(img, color, cx, cy, size, t, phase=0.0, mood="happy", prop=None, lock=False, scale=1.0,
               alpha=1.0, bob=6.0, tilt=3.0, shadow=True):
    blink = ((t + phase * 1.7) % 3.4) < 0.13
    sprite = robot(color, int(size), mood, prop, blink, lock)
    dy = math.sin(t * 2.6 + phase) * bob
    angle = math.sin(t * 1.7 + phase * 1.3) * tilt
    if shadow:
        sh = Image.new("RGBA", (int(size * 0.7), int(size * 0.14)), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([0, 0, sh.width - 1, sh.height - 1], fill=(0, 0, 0, 90))
        paste_center(img, sh, cx, cy + size * 0.46, scale * (1 - dy / 90), alpha)
    paste_center(img, sprite, cx, cy + dy, scale, alpha, angle)


# ----------------------------------------------------------- backgrounds

@lru_cache(maxsize=16)
def _art_source(name, blur, dim):
    image = Image.open(ART_DIR / f"{name}.jpg").convert("RGB")
    if blur:
        image = image.resize((image.width // 2, image.height // 2), Image.LANCZOS).filter(ImageFilter.GaussianBlur(9))
        image = image.resize((1536, 1024), Image.BILINEAR)
    if dim:
        image = Image.blend(image, Image.new("RGB", image.size, (6, 8, 16)), dim)
    return image


@lru_cache(maxsize=4)
def _gradient_base():
    base = Image.new("RGB", (W, H))
    px = ImageDraw.Draw(base)
    for y in range(H):
        t = y / (H - 1)
        px.line([(0, y), (W, y)], fill=(round(13 - 5 * t), round(15 - 6 * t), round(30 - 12 * t)))
    dots = Image.new("RGBA", (W + 64, H + 64), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for gx in range(0, W + 64, 64):
        for gy in range(0, H + 64, 64):
            dd.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(120, 140, 200, 46))
    return base, dots


@lru_cache(maxsize=8)
def _band(height, top_alpha, bottom_alpha, from_top=False):
    layer = Image.new("RGBA", (W, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(height):
        p = y / max(1, height - 1)
        if from_top:
            p = 1 - p
        d.line([(0, y), (W, y)], fill=(4, 6, 14, round(top_alpha + (bottom_alpha - top_alpha) * p)))
    return layer


@lru_cache(maxsize=2)
def _vignette():
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(60):
        a = int(110 * (1 - i / 60) ** 2.2)
        d.rectangle([i * 3, i * 2, W - i * 3, H - i * 2], outline=(2, 3, 10, a), width=3)
    return layer


class Background:
    """Animated backdrop: gradient + dot grid + glows, or a Ken Burns art image."""

    def __init__(self, art=None, mode="dim", tint="cyan", seed=0, motion="in", duration=12.0):
        self.art, self.mode, self.tint, self.motion, self.duration = art, mode, tint, motion, max(duration, 1)
        rnd = random.Random(seed)
        self.sparks = [(rnd.random() * W, rnd.random() * H, 8 + rnd.random() * 22, 1 + rnd.random() * 3,
                        rnd.random() * 6.28, rnd.choice(["cyan", "purple", "pink", "blue", "yellow"]))
                       for _ in range(34)]
        self.seed = seed
        if art:
            blur, dim = (False, 0.04) if mode == "vivid" else (True, 0.5)
            self.source = _art_source(art, blur, dim)
        else:
            self.base, self.dots = _gradient_base()

    def frame(self, t, shake=0.0):
        if self.art:
            return self._art_frame(t, shake)
        img = self.base.copy()
        ox, oy = int(t * 9) % 64, int(t * 5) % 64
        layer = self.dots.crop((ox, oy, ox + W, oy + H))
        img.paste(layer, (0, 0), layer)
        tint, other = rgb(self.tint), COLORS["purple"]
        blob = glow_blob(300, self.tint, 70)
        paste(img, blob, 160 + math.sin(t * 0.35 + self.seed) * 120 - 300, 140 + math.cos(t * 0.3) * 70 - 300)
        paste(img, glow_blob(340, "purple", 60), 1040 + math.cos(t * 0.3 + self.seed) * 110 - 340, 560 + math.sin(t * 0.4) * 60 - 340)
        self._sparkles(img, t)
        return img

    def _sparkles(self, img, t):
        d = ImageDraw.Draw(img, "RGBA")
        for x, y, speed, size, phase, color in self.sparks:
            yy = (y - t * speed) % (H + 20) - 10
            xx = x + math.sin(t * 0.6 + phase) * 18
            a = int(70 + 60 * math.sin(t * 2 + phase))
            d.ellipse([xx - size, yy - size, xx + size, yy + size], fill=rgba(color, a))

    def _art_frame(self, t, shake):
        p = ease_in_out(prog(t, 0, self.duration))
        zoom = (1.0 + 0.14 * p) if self.motion == "in" else (1.14 - 0.14 * p)
        pan = (p - 0.5) * 60 * (1 if self.motion == "in" else -1)
        src_w, src_h = self.source.size
        box_w = src_w / zoom
        box_h = box_w * H / W
        cx = src_w / 2 + pan
        cy = src_h / 2
        if shake:
            cx += math.sin(t * 61) * 22 * shake
            cy += math.cos(t * 53) * 16 * shake
        x0 = clamp(cx - box_w / 2, 0, src_w - box_w)
        y0 = clamp(cy - box_h / 2, 0, src_h - box_h)
        img = self.source.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + box_w, y0 + box_h))
        if self.mode == "vivid":
            paste(img, _vignette(), 0, 0)
        else:
            self._sparkles(img, t)
        return img


def bottom_band(img, height=190, strength=215):
    layer = _band(height, 0, strength)
    img.paste(layer, (0, H - height), layer)


def top_band(img, height=250, strength=205):
    layer = _band(height, strength, 0)
    img.paste(layer, (0, 0), layer)


# ---------------------------------------------------- particles, wipes

class Confetti:
    def __init__(self, seed=7, count=110):
        rnd = random.Random(seed)
        names = ["cyan", "purple", "pink", "orange", "green", "yellow", "blue", "red"]
        self.pieces = [
            (rnd.random() * W, rnd.random() * 1.6, 160 + rnd.random() * 260, rnd.random() * 6.28,
             (rnd.random() - 0.5) * 9, 7 + rnd.random() * 9, rnd.choice(names), rnd.random() * 60 + 20)
            for _ in range(count)
        ]

    def draw(self, img, t, start):
        if t < start:
            return
        d = ImageDraw.Draw(img, "RGBA")
        for x, delay, speed, phase, spin, size, color, sway in self.pieces:
            age = t - start - delay
            if age < 0:
                continue
            y = -20 + age * speed
            if y > H + 30:
                continue
            cx = x + math.sin(age * 2.2 + phase) * sway
            angle = phase + age * spin
            dx, dy = math.cos(angle) * size, math.sin(angle) * size * 0.55
            ex, ey = -dy * 0.6, dx * 0.6
            d.polygon([(cx - dx - ex, y - dy - ey), (cx + dx - ex, y + dy - ey),
                       (cx + dx + ex, y + dy + ey), (cx - dx + ex, y - dy + ey)], fill=rgba(color, 235))


def curtain(img, cover, color, opening):
    """Diagonal two-tone wipe. cover: 0..1 progress. closing sweeps in from the left;
    opening starts full and slides off to the right."""
    if cover <= 0:
        return
    skew = 180
    span = W + skew * 2
    d = ImageDraw.Draw(img, "RGBA")
    main, edge = rgba(color, 255), rgba(mix(color, "white", 0.55), 255)
    deep = rgba(shade(color, 0.55), 255)
    if opening:
        x = (1 - cover) * span - skew
        for offset, fill in ((70, deep), (30, edge), (0, main)):
            d.polygon([(x - offset, 0), (W + skew, 0), (W + skew, H), (x - skew - offset, H)], fill=fill)
    else:
        x = cover * span - skew
        for offset, fill in ((70, deep), (30, edge), (0, main)):
            d.polygon([(-skew, 0), (x + offset, 0), (x - skew + offset, H), (-skew, H)], fill=fill)


# ---------------------------------------------------------------- chrome

@lru_cache(maxsize=64)
def pill(text, color, size=18, filled=True, pad_x=18, pad_y=7):
    f = font("bold", size)
    w = int(text_width(text, f)) + pad_x * 2
    h = int(size * 1.3) + pad_y * 2
    sprite, pad = panel(w, h, radius=h // 2, fill=rgba(color, 255) if filled else (12, 14, 26, 210),
                        outline=None if filled else rgba(color, 255), outline_w=2, shadow=True)
    out = sprite.copy()
    ink = (10, 12, 22, 255) if filled else rgba(color)
    draw_text(out, (pad + pad_x, pad + pad_y - 1), text, f, ink, draw=ImageDraw.Draw(out, "RGBA"))
    return out, pad, w, h


def chrome(img, t, chapter, index, count, tag, tag_color, progress, marks):
    sprite, pad, w, h = pill(f"{index:02}/{count:02}  {chapter}", "cyan", 18, False)
    paste(img, sprite, 26 - pad, 20 - pad)
    sprite, pad, w, h = pill(tag, tag_color, 16, True)
    paste(img, sprite, W - 26 - w - pad, 20 - pad)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, H - 9, W, H], fill=(8, 10, 18, 200))
    bar = int(W * progress)
    d.rectangle([0, H - 9, bar, H], fill=rgba("cyan", 255))
    d.rectangle([max(0, bar - 120), H - 9, bar, H], fill=rgba("purple", 255))
    d.rectangle([bar - 3, H - 11, bar + 3, H + 2], fill=(255, 255, 255, 255))
    for m in marks:
        d.line([(int(W * m), H - 9), (int(W * m), H)], fill=(10, 12, 22, 255), width=2)
