"""Scene renderers, part 2: board, lanes, score, timeline, terminal, table."""

import math
from functools import lru_cache

from PIL import Image, ImageDraw

from gfx import (back_out, draw_lines, draw_robot, draw_text, emoji_sprite, ease_in_out, ease_out, fit, font, icon_sprite,
                 mix, panel, paste, paste_center, pill, pop, prog, put_text, rgba, shade, text_width, wrap, W, H)
from scenes_base import (INK, MUTED, SOFT, WHITE, Scene, appear, arrow, glow_ring)

# ----------------------------------------------------------------- board

LIGHT_BG = (247, 249, 253, 255)
LIGHT_INK = (28, 34, 48, 255)
LIGHT_MUTED = (104, 116, 138, 255)
LIGHT_LINE = (210, 217, 230, 255)
BLUE = (47, 111, 235, 255)

ISSUES = [
    ("ISS-101", "Checkout stops on an empty basket", "payments", "open"),
    ("ISS-102", "Keyboard focus disappears in the menu", "accessibility", "open"),
    ("ISS-103", "Export heading has a typo", "reporting", "open"),
    ("ISS-104", "Search ignores uppercase words", "search", "in-progress"),
    ("ISS-105", "Receipt uses the wrong sample currency", "payments", "closed"),
    ("ISS-106", "Small-screen chart overlaps its legend", "reporting", "in-progress"),
    ("ISS-107", "Image alternative text is missing", "accessibility", "open"),
    ("ISS-108", "Saved search loses its label", "search", "closed"),
]
STATUS_COLORS = {"open": (221, 244, 230, 255), "in-progress": (255, 240, 205, 255), "closed": (230, 232, 238, 255)}
BOARD_X, BOARD_Y, BOARD_W, BOARD_H = 60, 100, 870, 530
CARD_W, CARD_H, CARD_GAP = 196, 130, 12
GRID_X, GRID_Y = 24, 244


def _chip(draw, xy, text, f, fill, ink):
    x, y = xy
    w = int(text_width(text, f)) + 16
    draw.rounded_rectangle([x, y, x + w, y + 22], radius=11, fill=fill)
    draw.text((x + 8, y + 2), text, font=f, fill=ink)
    return w + 6


@lru_cache(maxsize=1)
def board_window():
    sprite, pad = panel(BOARD_W, BOARD_H, radius=16, fill=LIGHT_BG, glow="cyan", glow_r=14)
    sprite = sprite.copy()
    d = ImageDraw.Draw(sprite, "RGBA")
    ox, oy = pad, pad
    d.rounded_rectangle([ox, oy, ox + BOARD_W - 1, oy + 38], radius=16, fill=(226, 231, 241, 255))
    d.rectangle([ox, oy + 22, ox + BOARD_W - 1, oy + 38], fill=(226, 231, 241, 255))
    for i, c in enumerate(((255, 95, 95), (255, 189, 68), (60, 200, 90))):
        d.ellipse([ox + 16 + i * 22, oy + 12, ox + 28 + i * 22, oy + 24], fill=c + (255,))
    d.rounded_rectangle([ox + 150, oy + 7, ox + BOARD_W - 150, oy + 31], radius=12, fill=(247, 249, 253, 255))
    draw_text(sprite, (ox + BOARD_W / 2, oy + 9), "http://127.0.0.1:3000", font("mono", 15), LIGHT_MUTED, "center", draw=d)
    draw_text(sprite, (ox + 24, oy + 56), "Issue triage board", font("black", 30), LIGHT_INK, draw=d)
    draw_text(sprite, (ox + 24, oy + 94), "Harbor & Pine support queue", font("reg", 16), LIGHT_MUTED, draw=d)
    # missing export slot
    sx0, sy0, sx1, sy1 = ox + BOARD_W - 24 - 200, oy + 52, ox + BOARD_W - 24, oy + 96
    for i in range(int((sx1 - sx0) / 12)):
        d.line([(sx0 + i * 12, sy0), (sx0 + i * 12 + 6, sy0)], fill=LIGHT_MUTED, width=2)
        d.line([(sx0 + i * 12, sy1), (sx0 + i * 12 + 6, sy1)], fill=LIGHT_MUTED, width=2)
    for j in range(int((sy1 - sy0) / 12) + 1):
        d.line([(sx0, sy0 + j * 12), (sx0, min(sy1, sy0 + j * 12 + 6))], fill=LIGHT_MUTED, width=2)
        d.line([(sx1, sy0 + j * 12), (sx1, min(sy1, sy0 + j * 12 + 6))], fill=LIGHT_MUTED, width=2)
    draw_text(sprite, ((sx0 + sx1) / 2, sy0 + 12), "Export (not built yet)", font("reg", 17), LIGHT_MUTED, "center", draw=d)
    draw_text(sprite, (ox + 24, oy + 116), "Search title, description, or category", font("bold", 14), LIGHT_MUTED, draw=d)
    d.rounded_rectangle([ox + 24, oy + 138, ox + BOARD_W - 24 - 160, oy + 174], radius=9, fill=(255, 255, 255, 255),
                        outline=LIGHT_LINE, width=2)
    draw_text(sprite, (ox + 38, oy + 146), "Try keyboard or payments", font("reg", 17), (150, 160, 178, 255), draw=d)
    d.rounded_rectangle([ox + BOARD_W - 24 - 150, oy + 138, ox + BOARD_W - 24 - 82, oy + 174], radius=9, fill=BLUE)
    draw_text(sprite, (ox + BOARD_W - 24 - 116, oy + 146), "Search", font("bold", 17), (255, 255, 255, 255), "center", draw=d)
    d.rounded_rectangle([ox + BOARD_W - 24 - 72, oy + 138, ox + BOARD_W - 24, oy + 174], radius=9,
                        fill=(232, 236, 245, 255))
    draw_text(sprite, (ox + BOARD_W - 24 - 36, oy + 146), "Clear", font("bold", 17), LIGHT_INK, "center", draw=d)
    d.rounded_rectangle([ox + 24, oy + 188, ox + BOARD_W - 24, oy + 228], radius=10, fill=(226, 238, 255, 255))
    draw_text(sprite, (ox + 40, oy + 197), "At a glance   Detailed counts unlock in Lab 3", font("bold", 17),
              (40, 90, 190, 255), draw=d)
    return sprite, pad


@lru_cache(maxsize=16)
def issue_card(index):
    issue_id, title, category, status = ISSUES[index]
    sprite, pad = panel(CARD_W, CARD_H, radius=12, fill=(255, 255, 255, 255), outline=LIGHT_LINE, outline_w=2,
                        shadow=True, glow_r=5)
    sprite = sprite.copy()
    d = ImageDraw.Draw(sprite, "RGBA")
    draw_text(sprite, (pad + 12, pad + 9), issue_id, font("bold", 14), LIGHT_MUTED, draw=d)
    f, lines, lead = fit(title, "bold", CARD_W - 24, 56, 17, minimum=13, leading=1.2)
    draw_lines(sprite, pad + 12, pad + 34, lines, f, LIGHT_INK, lead, draw=d)
    cf = font("bold", 12)
    x = pad + 12
    y = pad + CARD_H - 30
    x += _chip(d, (x, y), category, cf, (226, 238, 255, 255), (40, 90, 190, 255))
    _chip(d, (x, y), status, cf, STATUS_COLORS[status], (60, 70, 90, 255))
    return sprite, pad


class BoardScene(Scene):
    intro = False
    TARGETS = {
        "export": ((BOARD_X + 646, BOARD_Y + 52 + 14), (BOARD_X + 846, BOARD_Y + 96 + 14)),
        "search": ((BOARD_X + 24, BOARD_Y + 138 + 14), (BOARD_X + 846, BOARD_Y + 174 + 14)),
        "summary": ((BOARD_X + 24, BOARD_Y + 188 + 14), (BOARD_X + 846, BOARD_Y + 228 + 14)),
        "badge": ((BOARD_X + GRID_X - 4, BOARD_Y + GRID_Y + 14 - 4),
                  (BOARD_X + GRID_X + 4 * CARD_W + 3 * CARD_GAP + 4, BOARD_Y + GRID_Y + 14 + 2 * CARD_H + CARD_GAP + 4)),
    }
    SLOTS = {"export": 166, "search": 240, "summary": 314, "badge": 470}

    def setup(self):
        cues = self.p["cues"]
        self.drop_at = self.cue(cues["drop"])
        self.untriaged_at = self.cue(cues["untriaged"])
        self.callouts = self.p["callouts"]
        self.call_times = self.cues(self.callouts, start=4.0, step=2.0)

    def draw(self, img, t):
        wp = pop(t, 0.15, 0.7)
        sprite, pad = board_window()
        paste_center(img, sprite, BOARD_X + BOARD_W / 2, BOARD_Y + BOARD_H / 2 + (1 - min(wp, 1)) * 30, min(wp, 1.03),
                     min(1.0, wp * 2))
        d = ImageDraw.Draw(img, "RGBA")
        for i in range(len(ISSUES)):
            start = self.drop_at + i * 0.12
            p = pop(t, start, 0.45)
            if p <= 0.02:
                continue
            col, row = i % 4, i // 4
            x = BOARD_X + GRID_X + col * (CARD_W + CARD_GAP)
            y = BOARD_Y + GRID_Y + 14 + row * (CARD_H + CARD_GAP)
            card, cpad = issue_card(i)
            paste(img, card, x - cpad, y - cpad - (1 - min(p, 1)) * 60, min(1.0, p * 1.6))
            if p >= 0.95:
                glow = 0.5 + 0.5 * math.sin((t - self.untriaged_at) * 6) if t >= self.untriaged_at else 0.0
                fill = (255, 214, 140, 255) if t >= self.untriaged_at else (232, 234, 240, 255)
                fill = tuple(round(a + (b - a) * glow) for a, b in zip((232, 234, 240, 255), fill))
                bx0, by0 = x + CARD_W - 78, y + 8
                d.rounded_rectangle([bx0, by0, bx0 + 70, by0 + 20], radius=10, fill=fill)
                draw_text(img, (bx0 + 35, by0 + 3), "untriaged", font("bold", 12), (90, 70, 20, 255) if t >= self.untriaged_at
                          else LIGHT_MUTED, "center", draw=d)
        for item, when in zip(self.callouts, self.call_times):
            p = pop(t, when, 0.5)
            if p <= 0.02:
                continue
            color = item["color"]
            (x0, y0), (x1, y1) = self.TARGETS[item["target"]]
            cy = self.SLOTS[item["target"]]
            line_p = prog(t, when, 0.4)
            d.line([(956, cy), (956 + (x1 + 6 - 956) * line_p, cy + (y0 + (y1 - y0) / 2 - cy) * line_p)],
                   fill=rgba(color, 230), width=3)
            glow_ring(img, (x0, y0, x1, y1), color, t - when, min(1.0, line_p))
            sprite, cpad = panel(284, 56, radius=28, fill=(18, 22, 38, 245), outline=rgba(color), outline_w=3,
                                 glow=color, glow_r=9)
            out = sprite.copy()
            f, lines, lead = fit(item["text"], "bold", 240, 40, 24)
            draw_lines(out, cpad + 142, cpad + (56 - lead * len(lines)) / 2, lines, f, rgba(WHITE), lead, align="center",
                       draw=ImageDraw.Draw(out, "RGBA"))
            paste_center(img, out, 1098, cy, min(p, 1.05))
        draw_robot(img, self.accent, 1110, 596, 120, t, phase=0.4, mood="worried" if t < self.untriaged_at else "happy",
                   prop="clipboard", scale=pop(t, 0.9, 0.6))


# ----------------------------------------------------------------- lanes

class LanesScene(Scene):
    def setup(self):
        cues = self.p["cues"]
        self.at = {k: self.cue(v) for k, v in cues.items()}

    def draw(self, img, t):
        d = ImageDraw.Draw(img, "RGBA")
        p = pop(t, self.at["contracts"], 0.55)
        if p > 0.02:
            text = self.p["contracts_text"]
            f = font("bold", 29)
            w = min(1100, int(text_width(text, f)) + 100)
            sprite, pad = panel(w, 58, radius=29, fill=(26, 20, 48, 245), outline=rgba("purple"), outline_w=3,
                                glow="purple", glow_r=10)
            out = sprite.copy()
            draw_text(out, (pad + w / 2, pad + 9), "\U0001F4DC " + text, f, rgba(WHITE), "center",
                      draw=ImageDraw.Draw(out, "RGBA"))
            paste_center(img, out, W / 2, 106 - (1 - min(p, 1)) * 20, min(p, 1.04))
        lane_boxes = [(90, 176, 340, 326), (460, 176, 340, 326)]
        for i, (lane, (x, y, w, h)) in enumerate(zip(self.p["lanes"], lane_boxes)):
            p = pop(t, self.at["lanes"] + i * 0.5, 0.55)
            if p <= 0.02:
                continue
            sprite, pad = panel(w, h, radius=24, fill=(18, 22, 38, 235), outline=rgba(lane["color"]), outline_w=3,
                                glow=lane["color"], glow_r=12)
            paste_center(img, sprite, x + w / 2, y + h / 2, min(p, 1.04), min(1.0, p * 2))
            if p < 0.6:
                continue
            draw_robot(img, lane["color"], x + w / 2, y + 100, 140, t, phase=i * 1.1, prop="wrench")
            pl, ppad, pw, ph = pill(lane["name"], lane["color"], 24, True)
            paste_center(img, pl, x + w / 2, y + 205)
            f, lines, lead = fit(lane["owns"], "reg", w - 40, 36, 22)
            draw_lines(img, x + w / 2, y + 236, lines, f, rgba(SOFT), lead, align="center")
            wt = pop(t, self.at["worktrees"] + i * 0.15, 0.5)
            if wt > 0.02:
                tag, tpad, tw, th = pill("\U0001F4C2 own worktree", "cyan", 20, False)
                paste_center(img, tag, x + w / 2, y + 288, min(wt, 1.05))
        ip = pop(t, self.at["integrator"], 0.55)
        ix, iy, iw, ih = 860, 176, 330, 326
        if ip > 0.02:
            sprite, pad = panel(iw, ih, radius=24, fill=(18, 22, 38, 235), outline=rgba("pink"), outline_w=3,
                                glow="pink", glow_r=12)
            paste_center(img, sprite, ix + iw / 2, iy + ih / 2, min(ip, 1.04), min(1.0, ip * 2))
            if ip >= 0.6:
                draw_robot(img, "pink", ix + iw / 2, iy + 100, 140, t, phase=2.2, prop="hat")
                pl, ppad, pw, ph = pill(self.p["integrator"], "pink", 24, True)
                paste_center(img, pl, ix + iw / 2, iy + 205)
                f, lines, lead = fit("Wires the pieces together at the end", "reg", iw - 40, 60, 22)
                draw_lines(img, ix + iw / 2, iy + 236, lines, f, rgba(SOFT), lead, align="center")
            flow = prog(t, self.at["integrator"] + 0.3, 0.9)
            for i, (x, y, w, h) in enumerate(lane_boxes):
                color = self.p["lanes"][i]["color"]
                sx = x + w / 2
                pts = [(sx, y + h), (sx, 526), (ix + iw / 2, 526), (ix + iw / 2, iy + ih)]
                self._poly_progress(d, pts, color, flow, t + i * 0.4)
        pp = pop(t, self.at["ports"], 0.55)
        if pp > 0.02:
            label = "\u26A0\uFE0F Worktrees do NOT isolate:"
            lf = font("bold", 26)
            lw = int(text_width(label, lf))
            chips = [pill(c, "orange", 24, False) for c in self.p["ports_chips"]]
            total = lw + 18 + sum(c[2] for c in chips) + 14 * len(chips)
            x = (W - total) / 2
            put = Image.new("RGBA", (W, 70), (0, 0, 0, 0))
            draw_text(put, (x, 18), label, lf, rgba("orange"), draw=ImageDraw.Draw(put, "RGBA"))
            x += lw + 18
            for sprite, spad, sw, sh in chips:
                put.paste(sprite, (round(x - spad), round(35 - sh / 2 - spad)), sprite)
                x += sw + 14
            paste(img, put, 0, 584 - (1 - min(pp, 1)) * 16, min(1.0, pp * 1.5))

    @staticmethod
    def _poly_progress(d, pts, color, progress, t):
        lengths = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
        total = sum(lengths)
        target = total * progress
        done = 0.0
        for (a, b), length in zip(zip(pts, pts[1:]), lengths):
            if done >= target:
                break
            frac = min(1.0, (target - done) / length)
            e = (a[0] + (b[0] - a[0]) * frac, a[1] + (b[1] - a[1]) * frac)
            d.line([a, e], fill=rgba(color, 220), width=5)
            done += length
        if progress >= 1:
            pos = (t * 0.45) % 1 * total
            for (a, b), length in zip(zip(pts, pts[1:]), lengths):
                if pos <= length:
                    f = pos / length
                    cx, cy = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
                    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255, 255))
                    break
                pos -= length


# ----------------------------------------------------------------- score

class ScoreScene(Scene):
    intro = False
    def setup(self):
        self.rows = self.p["rows"]
        self.times = self.cues(self.rows, start=0.9, step=1.4)
        self.total_at = self.cue(self.p["total_cue"]) if self.p.get("total_cue") else self.times[-1] + 2
        self.badge_at = self.cue(self.p["badge_cue"], "ding") if self.p.get("badge_cue") else self.total_at + 2
        self.legend = self.p.get("legend") or []
        self.legend_times = self.cues(self.legend, start=self.badge_at + 1, step=1.2)

    def running(self, t):
        return sum(r["value"] * ease_out(prog(t, w + 0.15, 0.6)) for r, w in zip(self.rows, self.times))

    def draw(self, img, t):
        d = ImageDraw.Draw(img, "RGBA")
        issue = self.p["issue"]
        hp = pop(t, 0.15, 0.5)
        if hp > 0.02:
            sprite, pad = panel(690, 74, radius=20, fill=(18, 22, 38, 240), outline=rgba("cyan"), outline_w=3,
                                glow="cyan", glow_r=8)
            out = sprite.copy()
            od = ImageDraw.Draw(out, "RGBA")
            draw_text(out, (pad + 20, pad + 8), issue["id"], font("bold", 24), rgba("cyan"), draw=od)
            draw_text(out, (pad + 20, pad + 38), issue["title"], font("bold", 22), rgba(WHITE), draw=od)
            tag, tpad, tw, th = pill(issue["category"], "purple", 20, True)
            out.paste(tag, (pad + 690 - tw - 18 - tpad, pad + 37 - tpad), tag)
            paste_center(img, out, 70 + 345, 134, min(hp, 1.03), min(1.0, hp * 2))
        row_h, gap, top = 80, 12, 188
        for i, (row, when) in enumerate(zip(self.rows, self.times)):
            p = pop(t, when, 0.5)
            if p <= 0.02:
                continue
            sprite, pad = panel(690, row_h, radius=20, fill=(18, 22, 38, 240), outline=rgba("muted"), outline_w=2)
            out = sprite.copy()
            od = ImageDraw.Draw(out, "RGBA")
            emoji = emoji_sprite(row["emoji"], 46)
            out.paste(emoji, (pad + 18, pad + (row_h - emoji.height) // 2), emoji)
            draw_text(out, (pad + 82, pad + 21), row["label"], font("bold", 28), rgba(WHITE), draw=od)
            color = ("green", "cyan", "purple", "orange")[i % 4]
            fill = ease_out(prog(t, when + 0.1, 0.7))
            bar_x0, bar_x1 = pad + 420, pad + 570
            od.rounded_rectangle([bar_x0, pad + 31, bar_x1, pad + 49], radius=9, fill=(40, 46, 66, 255))
            if fill > 0.02:
                od.rounded_rectangle([bar_x0, pad + 31, bar_x0 + (bar_x1 - bar_x0) * row["value"] / 60 * fill, pad + 49],
                                     radius=9, fill=rgba(color))
            draw_text(out, (pad + 666, pad + 14), f"+{row['value']}", font("black", 44), rgba(color), "right", draw=od)
            paste_center(img, out, 70 + 345, top + i * (row_h + gap) + row_h / 2 - (1 - min(p, 1)) * 30, min(p, 1.04))
        total = self.running(t)
        cx, cy, r = 1005, 300, 118
        bump = 1 + 0.07 * max(0.0, 1 - abs(t - self.total_at - 0.2) / 0.4) if t >= self.total_at else 1
        r = int(r * bump)
        color = mix("green", "red", min(1.0, total / 100) ** 1.4)
        d.ellipse([cx - r - 18, cy - r - 18, cx + r + 18, cy + r + 18], fill=(18, 22, 38, 225))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(48, 54, 76, 255), width=20)
        if total > 0.5:
            d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * min(1.0, total / 100) - 0.5, fill=rgba(color),
                  width=20)
        draw_text(img, (cx, cy - 52), str(round(total)), font("black", 100), rgba(WHITE), "center", draw=d)
        draw_text(img, (cx, cy + 50), "points", font("bold", 28), rgba(SOFT), "center", draw=d)
        bp = pop(t, self.badge_at, 0.6)
        if bp > 0.02:
            sprite, bpad, bw, bh = pill(self.p["badge"], "red", 64, True, 46, 12)
            paste_center(img, sprite, cx, 500, min(bp, 1.1), 1.0, math.sin(t * 5) * 3)
            put_text(img, "fix it first!", cx, 570, "bold", 28, rgba("red"), alpha=min(1.0, bp))
        if self.legend:
            sprites = [pill(l["text"], l["color"], 22, False) for l in self.legend]
            total_w = sum(s[2] for s in sprites) + 16 * (len(sprites) - 1)
            x = (W - total_w) / 2
            for s, when in zip(sprites, self.legend_times):
                sprite, spad, sw, sh = s
                p = pop(t, when, 0.5)
                if p > 0.02:
                    paste_center(img, sprite, x + sw / 2, 626, min(p, 1.05), min(1.0, p * 2))
                x += sw + 16


# -------------------------------------------------------------- timeline

class TimelineScene(Scene):
    def setup(self):
        self.segments = self.p["segments"]
        self.times = self.cues(self.segments, start=0.9, step=1.4)
        total = sum(s["minutes"] for s in self.segments)
        x, self.layout = 70, []
        for s in self.segments:
            w = 1140 * s["minutes"] / total
            self.layout.append((x, w))
            x += w
        self.total_at = (self.times[-1] + 1.4) if self.p.get("total_label") else None

    def draw(self, img, t):
        self.heading(img, t, self.p["title"])
        n = len(self.segments)
        big = n <= 4
        bar_y, bar_h = 300, 86
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([66, bar_y - 4, 1214, bar_y + bar_h + 4], radius=20, fill=(10, 12, 22, 190))
        for i, (seg, (x, w), when) in enumerate(zip(self.segments, self.layout, self.times)):
            grow = ease_out(prog(t, when, 0.7))
            if grow <= 0.01:
                continue
            gw = max(2, (w - 4) * grow)
            d.rounded_rectangle([x + 2, bar_y, x + 2 + gw, bar_y + bar_h], radius=16, fill=rgba(seg["color"]))
            if grow > 0.6:
                a = min(1.0, (grow - 0.6) / 0.4)
                label = seg["label"]
                f = font("black", 30 if big else 22)
                while text_width(label, f) > w - 12 and f.size > 12:
                    f = font("black", f.size - 2)
                draw_text(img, (x + w / 2, bar_y + (16 if big else 14)), label, f, (10, 12, 22, int(255 * a)), "center",
                          draw=d)
                mins = f"{seg['minutes']} min"
                f2 = font("bold", 24 if big else 17)
                draw_text(img, (x + w / 2, bar_y + (50 if big else 46)), mins, f2, (10, 12, 22, int(255 * a)), "center",
                          draw=d)
                emoji = emoji_sprite(seg["emoji"], 72 if big else 48)
                bounce = math.sin(t * 3 + i) * 5
                paste_center(img, emoji, x + w / 2, bar_y - (58 if big else 40) + bounce - (1 - a) * 20, min(1.0, a * 1.3),
                             a)
                f3, lines, lead = fit(seg["sub"], "bold", w - 12, 80, 24 if big else 18, minimum=13)
                sub = Image.new("RGBA", (W, 100), (0, 0, 0, 0))
                draw_lines(sub, x + w / 2, 0, lines, f3, rgba(WHITE, int(255 * a)), lead, align="center",
                           draw=ImageDraw.Draw(sub, "RGBA"))
                img.paste(sub, (0, bar_y + bar_h + 22), sub)
        if self.total_at is not None:
            p = pop(t, self.total_at, 0.6)
            if p > 0.02:
                sprite, pad, w, h = pill(self.p["total_label"], self.accent, 30, True, 32, 11)
                paste_center(img, sprite, W / 2, 566 - (1 - min(p, 1)) * 20, min(p, 1.05))


# -------------------------------------------------------------- terminal

TERM_COLORS = {"cmd": (240, 246, 252, 255), "out": (190, 200, 214, 255), "ok": (86, 211, 100, 255),
               "note": (139, 148, 158, 255), "warn": (255, 152, 85, 255)}


class TerminalScene(Scene):
    intro = False
    X, Y, WIDTH, HEIGHT = 60, 96, 800, 560

    def setup(self):
        self.lines = self.p["lines"]
        self.times = self.cues(self.lines, start=0.8, step=1.2, kind=None)
        for line, when in zip(self.lines, self.times):
            if line["kind"] in ("cmd", "ok", "warn"):
                self.tm.mark(when, "pop")
        self.side = self.p.get("side", [])
        self.side_times = self.cues(self.side, start=3.0, step=2.0)
        for size in range(24, 15, -1):
            char_w, layout = self.wrap_lines(size)
            rows = sum(len(r) for _, r in layout)
            if rows * (size + 9) + 6 * len(layout) <= self.HEIGHT - 84:
                break
        self.size, self.char_w, self.layout, self.line_h = size, char_w, layout, size + 9

    def wrap_lines(self, size):
        char_w = font("mono", size).getlength("M")
        max_chars = int((self.WIDTH - 60) / char_w)
        layout = []
        for line in self.lines:
            prefix = "PS> " if line["kind"] == "cmd" else ""
            text = line["text"]
            rows = []
            width = max_chars - len(prefix)
            while len(text) > width:
                cut = text.rfind(" ", 0, width)
                cut = width if cut < 12 else cut
                rows.append(text[:cut])
                text = text[cut:].lstrip()
            rows.append(text)
            layout.append((prefix, rows))
        return char_w, layout

    def visible_chars(self, line, when, t, total):
        if line["kind"] != "cmd":
            return total
        dur = min(1.6, max(0.5, total * 0.02))
        return int(total * prog(t, when, dur))

    def draw(self, img, t):
        d = ImageDraw.Draw(img, "RGBA")
        wp = pop(t, 0.15, 0.55)
        sprite, pad = panel(self.WIDTH, self.HEIGHT, radius=16, fill=(12, 15, 24, 248), outline=rgba("muted", 255),
                            outline_w=2, glow="cyan", glow_r=10)
        paste_center(img, sprite, self.X + self.WIDTH / 2, self.Y + self.HEIGHT / 2, min(wp, 1.03), min(1.0, wp * 2))
        if wp < 0.9:
            return
        d.rounded_rectangle([self.X, self.Y, self.X + self.WIDTH, self.Y + 38], radius=16, fill=(34, 40, 58, 255))
        d.rectangle([self.X, self.Y + 22, self.X + self.WIDTH, self.Y + 38], fill=(34, 40, 58, 255))
        for i, c in enumerate(((255, 95, 95), (255, 189, 68), (60, 200, 90))):
            d.ellipse([self.X + 16 + i * 22, self.Y + 13, self.X + 28 + i * 22, self.Y + 25], fill=c + (255,))
        draw_text(img, (self.X + self.WIDTH / 2, self.Y + 8), self.p["title"], font("bold", 17), rgba(SOFT), "center", draw=d)
        mono = font("mono", self.size)
        y = self.Y + 56
        cursor = None
        for line, (prefix, rows), when in zip(self.lines, self.layout, self.times):
            if t < when:
                break
            total = len(prefix) + sum(len(r) for r in rows)
            remaining = self.visible_chars(line, when, t, total)
            color = TERM_COLORS[line["kind"]]
            for r, text in enumerate(rows):
                if r == 0 and prefix:
                    draw_text(img, (self.X + 24, y), prefix, mono, rgba("cyan", 255), draw=d)
                    body = text[: max(0, remaining - len(prefix))]
                    draw_text(img, (self.X + 24 + len(prefix) * self.char_w, y), body, mono, color, draw=d)
                    cursor = (self.X + 24 + (len(prefix) + len(body)) * self.char_w, y)
                    remaining -= len(prefix) + len(body)
                else:
                    indent = len(prefix) if line["kind"] == "cmd" else 0
                    body = text[: max(0, remaining)]
                    draw_text(img, (self.X + 24 + indent * self.char_w, y), body, mono, color, draw=d)
                    cursor = (self.X + 24 + (indent + len(body)) * self.char_w, y)
                    remaining -= len(body)
                y += self.line_h
            y += 6
        if cursor and int(t * 2.4) % 2 == 0:
            d.rectangle([cursor[0] + 2, cursor[1] + 3, cursor[0] + 4 + self.size * 0.55, cursor[1] + self.size + 5],
                        fill=(240, 246, 252, 230))
        for i, (item, when) in enumerate(zip(self.side, self.side_times)):
            p = pop(t, when, 0.55)
            if p <= 0.02:
                continue
            sprite, spad = panel(340, 96, radius=22, fill=(18, 22, 38, 245), outline=rgba(item["color"]), outline_w=3,
                                 glow=item["color"], glow_r=10)
            out = sprite.copy()
            od = ImageDraw.Draw(out, "RGBA")
            emoji = emoji_sprite(item["emoji"], 50)
            out.paste(emoji, (spad + 16, spad + (96 - emoji.height) // 2), emoji)
            f, lines, lead = fit(item["text"], "bold", 240, 76, 25)
            draw_lines(out, spad + 84, spad + (96 - lead * len(lines)) / 2, lines, f, rgba(WHITE), lead, draw=od)
            paste_center(img, out, 1060 + (1 - min(p, 1)) * 60, 180 + i * 120, min(p, 1.04), min(1.0, p * 2))
        draw_robot(img, self.accent, 1060, 520, 190, t, phase=1.4, mood="happy", prop="wrench", scale=pop(t, 0.8, 0.7))


# ----------------------------------------------------------------- table

TONE_TEXT = {"red": "red", "orange": "orange", "green": "green", "muted": "muted", "cyan": "cyan", "purple": "purple"}


class TableScene(Scene):
    def setup(self):
        self.rows = self.p["rows"]
        self.times = self.cues(self.rows, start=0.9, step=1.3)

    def draw(self, img, t):
        self.heading(img, t, self.p["title"])
        d = ImageDraw.Draw(img, "RGBA")
        n = len(self.rows)
        row_h = {5: 70, 6: 64, 7: 58}.get(n, 52)
        size = 24 if n <= 6 else 22
        widths = [w * 1140 for w in self.p["widths"]]
        xs = [70]
        for w in widths[:-1]:
            xs.append(xs[-1] + w)
        hp = appear(t, 0.35, 0.5)
        if hp > 0.01:
            d.rounded_rectangle([70, 140, 1210, 140 + 42], radius=12, fill=rgba(self.accent, int(235 * hp)))
            for x, head in zip(xs, self.p["headers"]):
                draw_text(img, (x + 16, 148), head.upper(), font("black", 20), (10, 12, 22, int(255 * hp)), draw=d)
        for i, (row, when) in enumerate(zip(self.rows, self.times)):
            p = pop(t, when, 0.5)
            if p <= 0.02:
                continue
            y = 192 + i * (row_h + 6)
            tone = row.get("tone", "cyan")
            sprite, pad = panel(1140, row_h, radius=14, fill=(18, 22, 38, 240), outline=rgba(tone, 200), outline_w=2)
            out = sprite.copy()
            od = ImageDraw.Draw(out, "RGBA")
            od.rounded_rectangle([pad, pad, pad + 10, pad + row_h], radius=5, fill=rgba(tone))
            for c, (x, w, cell) in enumerate(zip(xs, widths, row["cells"])):
                head = self.p["headers"][c]
                mono = head == "Command" or (head == "Fix" and "$env" in cell)
                kind = "monob" if head == "Command" else ("mono" if mono else "bold" if c == 0 or head == "Level" else "reg")
                color = rgba(tone) if head in ("Level", "Score") else rgba(WHITE if c == 0 else SOFT)
                f, lines, lead = fit(cell, kind, w - 30, row_h - 8, size if kind not in ("mono", "monob") else size - 3,
                                     minimum=13, leading=1.15)
                draw_lines(out, pad + (x - 70) + 20, pad + (row_h - lead * len(lines)) / 2, lines, f, color, lead, draw=od)
            paste(img, out, 70 - pad + (1 - min(p, 1)) * 220, y - pad, min(1.0, p * 1.5))
