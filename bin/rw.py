"""Shared drawing library for the Red Wedge theme.

Root-bug fix: the old generate.py bound every helper to a module-global
``img``/``d``, so variant scripts drew on the wrong canvas. Here all state
lives in a Sheet instance and every drawing method targets that Sheet's own
image. Posters (3840x2560 3:2), the 16:9 hero, the desktop preview
(1800x1012) and the unlock glyph (512) all use the same class.

Palette is locked to three constructivist inks plus shades of those inks:
aged paper, near-black, party red. Coordinates are design-space; the Sheet
scales to its supersampled canvas internally.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

# ── Locked palette ───────────────────────────────────────────────────────────
PAPER = "#efe5d0"      # aged poster cream
PAPER_DEEP = "#e2d3b3"  # cream shade (shadow paper)
INK = "#211c18"        # near-black poster ink
RED = "#c33d2e"        # party red
RED_DEEP = "#a02f22"   # red shade

# ── Type ─────────────────────────────────────────────────────────────────────
LATO_BLACK = "/usr/share/fonts/truetype/lato/Lato-Black.ttf"
LATO_HEAVY = "/usr/share/fonts/truetype/lato/Lato-Heavy.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
MONO_OBLIQUE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf"

FINE_PRINT = (
    "APPROVED BY THE CENTRAL COMMITTEE OF THE OMACOM FOUNDATION"
    " \u00b7 SERIES 2026"
)

# Nine uniform sources, 3:2, >= 3840 wide (contract 2026-08-27).
SRC_W, SRC_H = 3840, 2560
# Desktop wallpaper hero stays 16:9.
HERO_W, HERO_H = 3840, 2160


class Sheet:
    """An explicit canvas + draw context. All coordinates design-space."""

    def __init__(self, w, h, bg=PAPER, ss=2, mode="RGB"):
        self.w, self.h, self.ss = w, h, ss
        self.img = Image.new(mode, (w * ss, h * ss), bg)
        self.d = ImageDraw.Draw(self.img)

    # ── type ────────────────────────────────────────────────────────────────
    def font(self, path, size):
        return ImageFont.truetype(path, int(size * self.ss))

    def tw(self, s, fnt, tracking=0):
        """Width of s in design units."""
        if not s:
            return 0.0
        total = sum(fnt.getlength(c) for c in s) + tracking * self.ss * (len(s) - 1)
        return total / self.ss

    def text(self, x, y, s, fnt, color, tracking=0, anchor="mm"):
        if tracking == 0:
            bb = self.d.textbbox((x * self.ss, y * self.ss), s, font=fnt,
                                 anchor=anchor)
            self._in_frame(bb, f"s {s[:24]!r}")
            self.d.text((x * self.ss, y * self.ss), s, font=fnt, fill=color,
                        anchor=anchor)
            return
        widths = [fnt.getlength(c) for c in s]
        total = sum(widths) + tracking * self.ss * (len(s) - 1)
        cx = x * self.ss
        if anchor[0] == "m":
            cx -= total / 2
        elif anchor[0] == "r":
            cx -= total
        ref = self.d.textbbox((cx, y * self.ss), s, font=fnt,
                              anchor="l" + anchor[1])
        self._in_frame((cx, ref[1], cx + total, ref[3]), f"s {s[:24]!r}")
        for c, wd in zip(s, widths):
            self.d.text((cx, y * self.ss), c, font=fnt, fill=color,
                        anchor="l" + anchor[1])
            cx += wd + tracking * self.ss

    def block(self, lines, deg, pad=50):
        """Render [(text, font, color)] to an RGBA block, rotate, return it."""
        widths, heights = [], []
        for s, fnt, _ in lines:
            box = fnt.getbbox(s)
            widths.append(box[2] - box[0])
            heights.append(box[3] - box[1] + 30 * self.ss)
        bw = max(widths) + 2 * pad * self.ss
        bh = sum(heights) + 2 * pad * self.ss
        tile = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        y = pad * self.ss
        for (s, fnt, color), hgt in zip(lines, heights):
            td.text((pad * self.ss, y), s, font=fnt, fill=color)
            y += hgt
        return tile.rotate(deg, resample=Image.BICUBIC, expand=True)

    def paste(self, cx, cy, im):
        x0 = cx * self.ss - im.width / 2
        y0 = cy * self.ss - im.height / 2
        self._in_frame((x0, y0, x0 + im.width, y0 + im.height), "block")
        self.img.paste(im, (int(x0), int(y0)), im)

    def _in_frame(self, bb, label):
        """Assert a placed element's bbox lies inside the frame."""
        if bb[0] < 0 or bb[1] < 0 or bb[2] > self.img.width or bb[3] > self.img.height:
            raise ValueError(
                f"{label} out of frame: bbox {bb} vs "
                f"{self.img.width}x{self.img.height}"
            )

    # ── shapes ──────────────────────────────────────────────────────────────
    def poly(self, pts, fill):
        self.d.polygon([(x * self.ss, y * self.ss) for x, y in pts], fill=fill)

    def line(self, x0, y0, x1, y1, fill, w):
        self.d.line([(x0 * self.ss, y0 * self.ss), (x1 * self.ss, y1 * self.ss)],
                    fill=fill, width=int(w * self.ss))

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, w=1):
        self.d.rectangle([x0 * self.ss, y0 * self.ss, x1 * self.ss, y1 * self.ss],
                         fill=fill, outline=outline, width=int(w * self.ss))

    def disc(self, cx, cy, r, fill):
        self.d.ellipse([(cx - r) * self.ss, (cy - r) * self.ss,
                        (cx + r) * self.ss, (cy + r) * self.ss], fill=fill)

    def ring(self, cx, cy, r, w, color):
        self.d.ellipse([(cx - r) * self.ss, (cy - r) * self.ss,
                        (cx + r) * self.ss, (cy + r) * self.ss],
                       outline=color, width=int(w * self.ss))

    def star(self, cx, cy, r, color, rot=-90):
        pts = []
        for i in range(10):
            ang = math.radians(rot + i * 36)
            rr = r if i % 2 == 0 else r * 0.4
            pts.append(((cx + rr * math.cos(ang)) * self.ss,
                        (cy + rr * math.sin(ang)) * self.ss))
        self.d.polygon(pts, fill=color)

    def ring_star(self, cx, cy, r, sr, ring_w=None, ring_color=INK, star_color=RED):
        """The Omarchy O: ink ring, red star punched through."""
        self.ring(cx, cy, r, ring_w if ring_w is not None else r * 0.26, ring_color)
        self.star(cx, cy, sr, star_color)

    def ray(self, cx, cy, ang_deg, r0, r1, w, color):
        """Tapered ray triangle from radius r0 to r1 at ang_deg, half-width w."""
        a = math.radians(ang_deg)
        px, py = math.cos(a), math.sin(a)
        qx, qy = -py, px
        pts = [
            (cx + r0 * px + w * qx, cy + r0 * py + w * qy),
            (cx + r1 * px, cy + r1 * py),
            (cx + r0 * px - w * qx, cy + r0 * py - w * qy),
        ]
        self.poly(pts, color)

    def gear(self, cx, cy, r_out, r_root, teeth, fill):
        pts = []
        step = 360.0 / (teeth * 2)
        for i in range(teeth * 2):
            ang = math.radians(i * step - 90)
            rr = r_out if i % 2 == 0 else r_root
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        self.poly(pts, fill)

    # ── theme gags ──────────────────────────────────────────────────────────
    def patrons(self, x, y, big=8, small=2, r_big=22, r_small=13, gap=66,
                color=RED, small_color=None):
        """Row of 8 big + 2 small stars: the founding patrons, plus two."""
        small_color = small_color or RED_DEEP
        for i in range(big):
            self.star(x + i * gap, y, r_big, color)
        x2 = x + big * gap + r_big + r_small + 14
        for i in range(small):
            self.star(x2 + i * (2 * r_small + 24), y + 4, r_small, small_color)

    def patrons_w(self, big=8, small=2, r_big=22, r_small=13, gap=66):
        x2 = big * gap + r_big + r_small + 14
        return x2 + (small - 1) * (2 * r_small + 24) + r_small

    def fine(self, x, y, s=FINE_PRINT, color=INK, size=26, anchor="mm", tracking=6):
        self.text(x, y, s, self.font(MONO, size), color,
                  tracking=tracking, anchor=anchor)

    # ── finish ──────────────────────────────────────────────────────────────
    def grain(self, seed=7, strength=22):
        """Deterministic speckle toward ink; keeps the printed-paper feel."""
        rng = random.Random(seed)
        tw = 384
        vals = bytes(rng.randrange(0, strength + 1) for _ in range(tw * tw))
        tile = Image.frombytes("L", (tw, tw), vals)
        mask = Image.new("L", self.img.size)
        for y in range(0, self.img.size[1], tw):
            for x in range(0, self.img.size[0], tw):
                mask.paste(tile, (x, y))
        self.img.paste(Image.new("RGB", self.img.size, INK), (0, 0), mask)

    def finish(self, grain_seed=None, grain_strength=22):
        if grain_seed is not None:
            self.grain(grain_seed, grain_strength)
        return self.img.resize((self.w, self.h), Image.LANCZOS)
