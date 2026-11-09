"""Scene renderers, part 1: title, art, statement, team, cards, pairs, steps, checklist, stamps."""

import math

from PIL import Image, ImageDraw

from gfx import (Confetti, bottom_band, draw_robot, draw_text, emoji_sprite, fit, draw_lines, font, icon_sprite, mix,
                 panel, paste, paste_center, pill, pop, prog, put_text, rgba, text_width, top_band, back_out, ease_out,
                 wrap, shade, W, H, COLORS)
from scenes_base import (INK, MUTED, SOFT, WHITE, Scene, appear, arrow, centered_text, fit_font, flow_rows, put_panel,
                         text_block)


def emoji_at(img, ch, cx, cy, px, scale=1.0, alpha=1.0, angle=0.0):
    paste_center(img, emoji_sprite(ch, int(px)), cx, cy, scale, alpha, angle)


class TitleScene(Scene):
    mode = "vivid"
    intro = False

    def setup(self):
        self.emoji_cues = self.cues(self.p.get("emojis", []), start=1.4, step=0.5)

    def draw(self, img, t):
        top_band(img, 400, 225)
        bottom_band(img, 230, 190)
        lines = self.p["lines"]
        glows = [self.accent, "pink", self.accent]
        top = 128 if len(lines) > 1 else 180
        for i, line in enumerate(lines):
            size = 112
            while text_width(line, font("black", size)) > 1120 and size > 60:
                size -= 4
            p = pop(t, 0.2 + i * 0.3, 0.6)
            put_text(img, line, W / 2, top + i * 122, "black", size, rgba(WHITE), glow=glows[i % 3],
                     scale=p, angle=math.sin(t * 1.3 + i) * 0.8 * min(1, p))
        sub_y = top + len(lines) * 122 + 18
        p = appear(t, 0.2 + len(lines) * 0.3 + 0.2, 0.5)
        if p > 0.01 and self.p.get("sub"):
            f = font("bold", 34)
            w = int(text_width(self.p["sub"], f)) + 60
            sprite, pad = panel(w, 56, radius=28, fill=(8, 10, 22, 215), shadow=False)
            out = sprite.copy()
            draw_text(out, (pad + w / 2, pad + 8), self.p["sub"], f, rgba(WHITE), "center",
                      draw=ImageDraw.Draw(out, "RGBA"))
            paste_center(img, out, W / 2, sub_y + 16, min(p, 1), p)
        badge = self.p.get("badge")
        if badge:
            sprite, pad, w, h = pill(badge, self.accent, 26, True, 28, 10)
            bp = pop(t, 0.9 + len(lines) * 0.3, 0.5)
            paste_center(img, sprite, W / 2, 646 + math.sin(t * 2) * 3, bp)
        n = len(self.p.get("emojis", []))
        for i, (item, when) in enumerate(zip(self.p.get("emojis", []), self.emoji_cues)):
            p = pop(t, when, 0.6)
            if p <= 0:
                continue
            cx = W / 2 + (i - (n - 1) / 2) * 190
            cy = 562 + math.sin(t * 2.4 + i * 1.7) * 9
            emoji_at(img, item["ch"], cx, cy, 78, scale=p, angle=math.sin(t * 1.8 + i) * 6)


class ArtScene(Scene):
    mode = "vivid"
    intro = False

    def setup(self):
        self.chips = self.p["chips"]
        self.times = self.cues(self.chips, start=0.9, step=0.8)
        self.shake_at = self.cue(self.p.get("shake_cue"), "boom")
        self.confetti_at = self.cue(self.p.get("confetti_cue"), "ding") if self.p.get("confetti_cue") else None
        self.confetti = Confetti(seed=self.index + 11) if self.p.get("confetti") else None
        self.sprites = [pill(f"{c['emoji']} {c['text']}", c["color"], 28, True, 22, 9) for c in self.chips]
        gap = 16
        widths = [s[2] for s in self.sprites]
        self.rows = flow_rows(widths, 1180, gap)
        self.gap = gap

    def shake(self, t):
        if self.shake_at is None or t < self.shake_at:
            return 0.0
        return max(0.0, 1 - (t - self.shake_at) / 0.9)

    def draw(self, img, t):
        bottom_band(img, 300, 225)
        rows = len(self.rows)
        row_h = 62
        top = 676 - rows * row_h - (rows - 1) * 6 + 6
        for r, row in enumerate(self.rows):
            total = sum(self.sprites[i][2] for i in row) + self.gap * (len(row) - 1)
            x = (W - total) / 2
            cy = top + r * (row_h + 6) + row_h / 2
            for i in row:
                sprite, pad, w, h = self.sprites[i]
                p = pop(t, self.times[i], 0.5)
                if p > 0.02:
                    paste_center(img, sprite, x + w / 2, cy - (1 - min(p, 1)) * 24, p)
                x += w + self.gap
        if self.confetti and self.confetti_at is not None:
            self.confetti.draw(img, t, self.confetti_at)


class StatementScene(Scene):
    own_robot = True
    intro_width = 760
    def setup(self):
        self.words = self.p["words"]
        self.times = self.cues(self.words, start=0.8, step=1.0)
        self.sub_at = self.cue(self.p.get("sub_cue")) if self.p.get("sub_cue") else 3.5

    def draw(self, img, t):
        n = len(self.words)
        ys = {2: [210, 400], 3: [175, 335, 495]}.get(n, [180 + 150 * i for i in range(n)])
        for i, word in enumerate(self.words):
            p = pop(t, self.times[i], 0.55)
            if p <= 0.02:
                continue
            f = font("black", 84)
            w = int(text_width(word["text"], f)) + 90
            h = 118
            sprite, pad = panel(w, h, radius=26, fill=(18, 22, 38, 240), outline=rgba(word["color"]), outline_w=4,
                                glow=word["color"], glow_r=14)
            out = sprite.copy()
            d = ImageDraw.Draw(out, "RGBA")
            draw_text(out, (pad + 45, pad + 6), word["text"], f, rgba(word["color"]), draw=d,
                      icon_color=word["color"])
            angle = (-2.2, 1.8, -1.4)[i % 3] + math.sin(t * 1.5 + i) * 0.5
            dx = (1 - min(p, 1)) * (-420 if i % 2 == 0 else 420)
            paste_center(img, out, W / 2 + (-60 if i % 2 == 0 else 60) + dx, ys[i], min(p, 1.05), 1.0, angle)
        if self.p.get("sub"):
            p = appear(t, self.sub_at, 0.6)
            if p > 0.01:
                sub_w = 1180 if n >= 3 else 960
                size = 38
                while size > 22 and text_width(self.p["sub"], font("bold", size)) > sub_w:
                    size -= 1
                put_text(img, self.p["sub"], W / 2 - (0 if n >= 3 else 110), 612, "bold", size, rgba(WHITE),
                         glow=self.accent, alpha=p)
        draw_robot(img, self.accent, 1120, 560, 150, t, phase=1.0, mood="happy", prop="clipboard",
                   scale=pop(t, 1.0, 0.6) if n < 3 else 0.0)


class TeamScene(Scene):
    def setup(self):
        self.nodes = self.p["nodes"]
        self.times = self.cues(self.nodes, start=0.8, step=1.4)
        self.footer_at = self.cue(self.p["footer"]["cue"]) if self.p.get("footer") else None

    def pos(self, i):
        n = len(self.nodes) - 1
        if i == 0:
            return W / 2, 180, 140
        return W * (i - 0.5) / n, 410, 128

    def draw(self, img, t):
        d = ImageDraw.Draw(img, "RGBA")
        top_x, top_y, _ = self.pos(0)
        for i in range(1, len(self.nodes)):
            cx, cy, size = self.pos(i)
            p = prog(t, self.times[i], 0.5)
            if p > 0:
                color = self.nodes[i]["color"]
                x0, y0, x1, y1 = top_x, top_y + 72, cx, cy - size * 0.55
                ex, ey = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
                d.line([(x0, y0), (ex, ey)], fill=rgba(color, 190), width=5)
                if p >= 1:
                    q = (t * 0.8 + i * 0.23) % 1
                    d.ellipse([x0 + (x1 - x0) * q - 7, y0 + (y1 - y0) * q - 7, x0 + (x1 - x0) * q + 7,
                               y0 + (y1 - y0) * q + 7], fill=rgba(color, 255))
        for i, node in enumerate(self.nodes):
            cx, cy, size = self.pos(i)
            p = pop(t, self.times[i], 0.6)
            if p <= 0.02:
                continue
            draw_robot(img, node["color"], cx, cy, size, t, phase=i * 1.3, mood="happy", prop=node.get("prop"),
                       lock=bool(node.get("lock")), scale=min(p, 1.08))
            sprite, pad, w, h = pill(node["name"], node["color"], 24, True)
            if i == 0:
                paste_center(img, sprite, top_x + 330, cy - 22, min(p, 1))
                f, lines, lead = fit(node["role"], "reg", 440, 70, 26)
                draw_lines(img, top_x + 330 - w / 2 + 4, cy + 14, lines, f, rgba(SOFT), lead)
            else:
                paste_center(img, sprite, cx, cy + size * 0.66 + 4, min(p, 1))
                width = W / (len(self.nodes) - 1) - 30
                f, lines, lead = fit(node["role"], "reg", width, 64, 22)
                draw_lines(img, cx, cy + size * 0.66 + 36, lines, f, rgba(SOFT), lead, align="center")
        if self.p.get("footer"):
            p = appear(t, self.footer_at, 0.5)
            if p > 0.01:
                text = self.p["footer"]["text"]
                f = font("bold", 30)
                w = int(text_width(text, f)) + 70
                sprite, pad = panel(w, 56, radius=28, fill=(18, 22, 38, 240), outline=rgba(self.accent), outline_w=3,
                                    glow=self.accent, glow_r=10)
                out = sprite.copy()
                draw_text(out, (pad + 35, pad + 7), text, f, rgba(WHITE), draw=ImageDraw.Draw(out, "RGBA"))
                paste_center(img, out, W / 2, 640 - (1 - p) * 20, 1.0, p)


class CardsScene(Scene):
    def setup(self):
        self.items = self.p["items"]
        self.times = self.cues(self.items, start=0.8, step=1.2)
        self.footer_at = self.cue(self.p["footer"]["cue"]) if isinstance(self.p.get("footer"), dict) else (
            self.duration * 0.7 if self.p.get("footer") else None)
        self.pre = self.p.get("pre", [])
        self.pre_times = self.cues(self.pre, start=0.8, step=1.4)

    def draw_pre(self, img, t):
        """Lead-in chips that fill the narration before the main cards arrive, then clear the stage."""
        fade = 1 - ease_out(prog(t, self.times[0] - 0.55, 0.4))
        if fade <= 0.01:
            return
        n = len(self.pre)
        w, h, gap = 262, 190, 22
        x0 = (W - (n * w + (n - 1) * gap)) / 2
        for i, (chip, when) in enumerate(zip(self.pre, self.pre_times)):
            p = pop(t, when, 0.5)
            if p <= 0.02:
                continue
            sprite, pad = panel(w, h, radius=24, fill=(18, 22, 38, 242), outline=rgba(chip["color"]), outline_w=3,
                                glow=chip["color"], glow_r=12)
            out = sprite.copy()
            od = ImageDraw.Draw(out, "RGBA")
            emoji = emoji_sprite(chip["emoji"], 64)
            out.paste(emoji, (pad + (w - emoji.width) // 2, pad + 16), emoji)
            f, lines, lead = fit(chip["text"], "bold", w - 36, h - 104, 28, minimum=18)
            draw_lines(out, pad + w / 2, pad + 98, lines, f, rgba(chip["color"]), lead, align="center", draw=od)
            bob = math.sin(t * 2.2 + i) * 4
            paste_center(img, out, x0 + i * (w + gap) + w / 2, 330 + bob - (1 - min(p, 1)) * 36, min(p, 1.06),
                         min(p, 1) * fade)

    def layout(self):
        n = len(self.items)
        if n <= 3:
            w, h, gap = 350, 400, 30
            x0 = (W - (n * w + (n - 1) * gap)) / 2
            return [(x0 + i * (w + gap), 160, w, h) for i in range(n)]
        w, h, gap = 560, 196, 22
        x0 = (W - (2 * w + gap)) / 2
        return [(x0 + (i % 2) * (w + gap), 150 + (i // 2) * (h + gap), w, h) for i in range(n)]

    def draw(self, img, t):
        self.heading(img, t, self.p["title"])
        if self.pre:
            self.draw_pre(img, t)
        d = ImageDraw.Draw(img, "RGBA")
        wide = len(self.items) > 3
        for i, (item, (x, y, w, h)) in enumerate(zip(self.items, self.layout())):
            p = pop(t, self.times[i], 0.55)
            if p <= 0.02:
                continue
            sprite, pad = panel(w, h, radius=24, fill=(18, 22, 38, 242), outline=rgba(item["color"]), outline_w=3,
                                glow=item["color"], glow_r=12)
            out = sprite.copy()
            od = ImageDraw.Draw(out, "RGBA")
            if wide:
                emoji = emoji_sprite(item["emoji"], 80)
                out.paste(emoji, (pad + 26, pad + (h - emoji.height) // 2), emoji)
                body = item.get("body")
                text_w = w - 160
                if body:
                    draw_text(out, (pad + 130, pad + 20), item["title"], fit_font(item["title"], "bold", 32, text_w),
                              rgba(item["color"]), draw=od)
                    f, lines, lead = fit(body, "reg", text_w, h - 84, 24)
                    draw_lines(out, pad + 130, pad + 68, lines, f, rgba(SOFT), lead, draw=od)
                else:
                    f, lines, lead = fit(item["title"], "bold", text_w, h - 40, 34, minimum=20)
                    block = len(lines) * lead
                    draw_lines(out, pad + 130, pad + (h - block) / 2, lines, f, rgba(item["color"]), lead, draw=od)
            else:
                emoji = emoji_sprite(item["emoji"], 110)
                out.paste(emoji, (pad + (w - emoji.width) // 2, pad + 36), emoji)
                draw_text(out, (pad + w / 2, pad + 168), item["title"], fit_font(item["title"], "black", 44, w - 40),
                          rgba(item["color"]), align="center", draw=od)
                if item.get("body"):
                    f, lines, lead = fit(item["body"], "reg", w - 56, h - 250, 27)
                    draw_lines(out, pad + w / 2, pad + 240, lines, f, rgba(SOFT), lead, align="center", draw=od)
            bob = math.sin(t * 2 + i) * 4
            paste_center(img, out, x + w / 2, y + h / 2 + bob - (1 - min(p, 1)) * 40, min(p, 1.06))
        footer = self.p.get("footer")
        if footer:
            text = footer["text"] if isinstance(footer, dict) else footer
            p = appear(t, self.footer_at, 0.5)
            if p > 0.01:
                put_text(img, text, W / 2, 628, "bold", 32, rgba(WHITE), glow=self.accent, alpha=p)


class PairsScene(Scene):
    ROW_H, GAP, TOP = 84, 14, 142

    def setup(self):
        self.rows = self.p["rows"]
        self.times = self.cues(self.rows, start=0.8, step=2.0)

    def draw(self, img, t):
        self.heading(img, t, self.p["title"])
        d = ImageDraw.Draw(img, "RGBA")
        for i, row in enumerate(self.rows):
            y = self.TOP + i * (self.ROW_H + self.GAP)
            start = self.times[i]
            p = pop(t, start, 0.5)
            if p <= 0.02:
                continue
            x_shift = (1 - min(p, 1)) * -300
            sprite, pad = panel(520, self.ROW_H, radius=18, fill=(40, 20, 28, 238), outline=rgba("red"), outline_w=3)
            out = sprite.copy()
            f, lines, lead = fit(row["myth"], "bold", 480, self.ROW_H - 16, 25)
            od = ImageDraw.Draw(out, "RGBA")
            block = len(lines) * lead
            draw_lines(out, pad + 20, pad + (self.ROW_H - block) / 2, lines, f, rgba(WHITE), lead, draw=od)
            fact_p = ease_out(prog(t, start + 1.3, 0.5))
            if fact_p > 0:
                lx0 = pad + 14
                lx1 = pad + 14 + (520 - 28) * fact_p
                od.line([(lx0, pad + self.ROW_H / 2), (lx1, pad + self.ROW_H / 2)], fill=rgba("red", 240), width=4)
            paste(img, out, 60 - pad + x_shift, y - pad, min(p, 1))
            if fact_p > 0.02:
                arrow(img, (600, y + self.ROW_H / 2), (686, y + self.ROW_H / 2), "green", 6, 16, progress=fact_p)
                sprite, pad = panel(520, self.ROW_H, radius=18, fill=(16, 38, 28, 238), outline=rgba("green"),
                                    outline_w=3, glow="green", glow_r=8)
                out = sprite.copy()
                f, lines, lead = fit(row["fact"], "bold", 480, self.ROW_H - 16, 25)
                od = ImageDraw.Draw(out, "RGBA")
                block = len(lines) * lead
                draw_lines(out, pad + 20, pad + (self.ROW_H - block) / 2, lines, f, rgba(WHITE), lead, draw=od)
                paste_center(img, out, 960 + (1 - fact_p) * 80, y + self.ROW_H / 2, 1.0, fact_p)


class StepsScene(Scene):
    def setup(self):
        self.items = self.p["items"]
        self.times = self.cues(self.items, start=0.8, step=1.4)
        self.footer_at = self.cue(self.p["footer"]["cue"]) if self.p.get("footer") else None

    def draw(self, img, t):
        self.heading(img, t, self.p["title"])
        n = len(self.items)
        cols = min(3, n)
        rows = math.ceil(n / cols)
        w, gap = 360, 30
        h = 196 if rows <= 2 else 150
        x0 = (W - (cols * w + (cols - 1) * gap)) / 2
        for i, item in enumerate(self.items):
            p = pop(t, self.times[i], 0.55)
            if p <= 0.02:
                continue
            col, row = i % cols, i // cols
            x, y = x0 + col * (w + gap), 148 + row * (h + 24)
            color = ACCENTS[i % len(ACCENTS)]
            sprite, pad = panel(w, h, radius=22, fill=(18, 22, 38, 242), outline=rgba(color), outline_w=3,
                                glow=color, glow_r=10)
            out = sprite.copy()
            od = ImageDraw.Draw(out, "RGBA")
            od.ellipse([pad + 16, pad + 16, pad + 60, pad + 60], fill=rgba(color))
            draw_text(out, (pad + 38, pad + 24), str(i + 1), font("black", 28), INK, align="center", draw=od)
            emoji = emoji_sprite(item["emoji"], 44)
            out.paste(emoji, (pad + w - 58, pad + 16), emoji)
            draw_text(out, (pad + 72, pad + 22), item["title"], fit_font(item["title"], "bold", 28, w - 72 - 64, 18),
                      rgba(color), draw=od)
            f, lines, lead = fit(item["body"], "reg", w - 40, h - 86, 22)
            draw_lines(out, pad + 20, pad + 76, lines, f, rgba(SOFT), lead, draw=od)
            paste_center(img, out, x + w / 2, y + h / 2 - (1 - min(p, 1)) * 36, min(p, 1.06))
        if self.p.get("footer"):
            p = appear(t, self.footer_at, 0.5)
            if p > 0.01:
                put_text(img, self.p["footer"]["text"], W / 2, 628, "bold", 32, rgba(WHITE), glow=self.accent,
                         alpha=p)


ACCENTS = ["cyan", "purple", "pink", "orange", "green", "blue"]


class ChecklistScene(Scene):
    own_robot = True
    intro_width = 700
    ROW_H, GAP, TOP = 88, 14, 150

    def setup(self):
        self.items = self.p["items"]
        self.times = self.cues(self.items, start=0.9, step=1.6)

    def draw(self, img, t):
        self.heading(img, t, self.p["title"])
        for i, item in enumerate(self.items):
            y = self.TOP + i * (self.ROW_H + self.GAP)
            p = pop(t, max(0.2, self.times[i] - 0.3), 0.5)
            if p <= 0.02:
                continue
            done = prog(t, self.times[i] + 0.2, 0.35)
            color = "green" if done > 0.5 else "muted"
            sprite, pad = panel(830, self.ROW_H, radius=20, fill=(18, 22, 38, 240),
                                outline=rgba(color), outline_w=3, glow="green" if done > 0.5 else None, glow_r=8)
            out = sprite.copy()
            od = ImageDraw.Draw(out, "RGBA")
            od.rounded_rectangle([pad + 20, pad + 22, pad + 64, pad + 66], radius=10, outline=rgba("muted"), width=3)
            f, lines, lead = fit(item["text"], "bold", 700, 40, 28)
            draw_lines(out, pad + 86, pad + (14 if item.get("sub") else (self.ROW_H - lead * len(lines)) / 2), lines,
                       f, rgba(WHITE), lead, draw=od)
            if item.get("sub"):
                f2, lines2, lead2 = fit(item["sub"], "reg", 700, 34, 20)
                draw_lines(out, pad + 86, pad + 14 + lead * len(lines) + 2, lines2, f2, rgba(SOFT), lead2, draw=od)
            paste_center(img, out, 70 + 415 - (1 - min(p, 1)) * 200, y + self.ROW_H / 2, min(p, 1))
            if done > 0:
                k = back_out(done)
                paste_center(img, icon_sprite("check", 44, "green"), 70 + 42, y + 44, k)
        draw_robot(img, self.accent, 1100, 360, 240, t, phase=0.5, mood="happy",
                   prop="magnifier" if self.spec.get("art") else "clipboard",
                   scale=pop(t, 0.5, 0.7))


class StampsScene(Scene):
    own_robot = True
    def setup(self):
        self.items = self.p["items"]
        self.times = self.cues(self.items, start=0.8, step=1.5, kind="boom")
        self.footer_at = self.cue(self.p["footer"]["cue"]) if self.p.get("footer") else None

    def draw(self, img, t):
        n = len(self.items)
        for i, item in enumerate(self.items):
            when = self.times[i]
            if t < when:
                continue
            age = t - when
            k = 1 + 1.3 * max(0.0, 1 - age / 0.25) ** 2
            alpha = min(1.0, age / 0.12)
            f = font("black", 56)
            w = int(text_width(item["text"], f)) + 70
            h = 120
            sprite, pad = panel(w, h, radius=16, fill=(14, 18, 30, 235), outline=rgba(item["color"]), outline_w=6,
                                glow=item["color"], glow_r=14)
            out = sprite.copy()
            draw_text(out, (pad + 35, pad + 20), item["text"], f, rgba(item["color"]),
                      draw=ImageDraw.Draw(out, "RGBA"))
            cx = W * (i + 0.5) / n
            angle = (-6, 4, -3)[i % 3]
            paste_center(img, out, cx, 280, k, alpha, angle)
            if item.get("sub"):
                sp = appear(t, when + 0.3, 0.5)
                f2, lines, lead = fit(item["sub"], "reg", W / n - 60, 120, 28)
                if sp > 0.01:
                    sub = Image.new("RGBA", (W, 140), (0, 0, 0, 0))
                    draw_lines(sub, cx, 6, lines, f2, rgba(SOFT, int(255 * sp)), lead, align="center",
                               draw=ImageDraw.Draw(sub, "RGBA"))
                    img.paste(sub, (0, 380), sub)
        if self.p.get("footer"):
            p = appear(t, self.footer_at, 0.5)
            if p > 0.01:
                sprite, pad, w, h = pill(self.p["footer"]["text"], self.accent, 30, True, 30, 10)
                paste_center(img, sprite, W / 2, 586 - (1 - p) * 20, min(p, 1), p)
        draw_robot(img, self.accent, 120, 600, 110, t, phase=2.0, mood="wow", scale=pop(t, 0.5, 0.6), shadow=False)
