#!/usr/bin/env python3
"""Generate the Red Wedge poster wallpaper.

Constructivist propaganda poster: DHH's own tagline "Redistributing
billionaire wealth, one ISO at a time" set in Lato Black on aged poster
cream, with the red wedge and the Omarchy O as a star-punched ring.
Supersampled 2x, LANCZOS downscale (see ../omarchy-theme-legal-tender
lessons: view every render; keep geometry bold but sparse).
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 2160
SS = 2
CW, CH = W * SS, H * SS

PAPER = "#efe5d0"
INK = "#211c18"
RED = "#c33d2e"
RED_DEEP = "#a02f22"

LATO_BLACK = "/usr/share/fonts/truetype/lato/Lato-Black.ttf"
LATO_HEAVY = "/usr/share/fonts/truetype/lato/Lato-Heavy.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

img = Image.new("RGB", (CW, CH), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size * SS)


def star(draw, cx, cy, r, color, rot=-90):
    pts = []
    for i in range(10):
        ang = math.radians(rot + i * 36)
        rr = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)


def text_at(x, y, s, fnt, color, tracking=0, anchor="mm"):
    if tracking == 0:
        d.text((x * SS, y * SS), s, font=fnt, fill=color, anchor=anchor)
        return
    total = sum(d.textlength(c, font=fnt) for c in s) + tracking * SS * (len(s) - 1)
    cx = x * SS - total / 2
    for c in s:
        w = d.textlength(c, font=fnt)
        d.text((cx, y * SS), c, font=fnt, fill=color, anchor="lm")
        cx += w + tracking * SS


def rotated_text(cx, cy, lines, deg):
    """Render (text, font, color) lines to a block, rotate, paste centered."""
    pad = 40 * SS
    widths, heights = [], []
    for s, fnt, _ in lines:
        box = fnt.getbbox(s)
        widths.append(box[2] - box[0])
        heights.append(box[3] - box[1] + 24 * SS)
    bw, bh = max(widths) + pad * 2, sum(heights) + pad * 2
    block = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    bd = ImageDraw.Draw(block)
    y = pad
    for (s, fnt, color), hgt in zip(lines, heights):
        bd.text((pad, y), s, font=fnt, fill=color)
        y += hgt
    block = block.rotate(deg, resample=Image.BICUBIC, expand=True)
    img.paste(block, (int(cx * SS - block.width / 2), int(cy * SS - block.height / 2)), block)


WEDGE_DEG = 10  # everything leans on this axis

# ── The red wedge ────────────────────────────────────────────────────────────
d.polygon(
    [(0, CH), (0, int(1500 * SS)), (int(2980 * SS), int(1275 * SS)), (int(1500 * SS), CH)],
    fill=RED,
)
# Echo rules above the wedge, parallel to its top edge.
for off, wd in ((90, 6), (150, 2)):
    x0, y0 = 0, (1500 - off) * SS
    x1, y1 = 2980 * SS, (1275 - off) * SS
    d.line([(x0, y0), (x1, y1)], fill=INK, width=wd * SS)

# ── The O: black ring, red star punched through ──────────────────────────────
OCX, OCY, OR = 880, 620, 350
d.ellipse(
    [(OCX - OR) * SS, (OCY - OR) * SS, (OCX + OR) * SS, (OCY + OR) * SS],
    outline=INK,
    width=92 * SS,
)
star(d, OCX * SS, OCY * SS, 150 * SS, RED)

# ── Headline, leaning on the wedge axis ──────────────────────────────────────
rotated_text(
    2340,
    780,
    [
        ("REDISTRIBUTING", font(LATO_BLACK, 150), INK),
        ("BILLIONAIRE WEALTH", font(LATO_BLACK, 150), INK),
        ("ONE ISO AT A TIME", font(LATO_BLACK, 96), RED),
    ],
    WEDGE_DEG,
)

# ── Slogans on the cream field ───────────────────────────────────────────────
text_at(3060, 1630, "ELITE CAPITAL \u00b7 PUBLIC CODE", font(LATO_HEAVY, 54), INK, tracking=14)
text_at(3060, 1730, "ZERO DOLLARS \u00b7 SEVERAL BILLIONAIRES", font(LATO_HEAVY, 44), RED_DEEP, tracking=10)

# ── Inside the wedge: the distro line, cream on red ──────────────────────────
cream_line = Image.new("RGBA", (2400 * SS, 200 * SS), (0, 0, 0, 0))
cd = ImageDraw.Draw(cream_line)
cd.text((0, 0), "OMARCHY \u00b7 THE PEOPLE'S DESKTOP, FUNDED BY THE 0.001%", font=font(LATO_HEAVY, 52), fill=PAPER)
cream_line = cream_line.rotate(4.3, resample=Image.BICUBIC, expand=True)
img.paste(cream_line, (int(240 * SS), int(1810 * SS)), cream_line)

# ── Stars: eight founding patrons, then two more ─────────────────────────────
sx = 3060 - 5 * 66
for i in range(8):
    star(d, (sx + i * 66) * SS, 1860 * SS, 22 * SS, RED)
for i in range(2):
    star(d, (sx + 8 * 66 + 22 + i * 50) * SS, 1864 * SS, 13 * SS, RED_DEEP)

# ── Fine print ───────────────────────────────────────────────────────────────
text_at(
    2620,
    2110,
    "APPROVED BY THE CENTRAL COMMITTEE OF THE OMACOM FOUNDATION \u00b7 SERIES 2026",
    font(MONO, 26),
    INK,
    tracking=4,
)

img.resize((W, H), Image.LANCZOS).save("backgrounds/red-wedge.png")
print("saved backgrounds/red-wedge.png")

# ── Lock-screen glyph: ring and star ─────────────────────────────────────────
U = 512
ug = Image.new("RGBA", (U * SS, U * SS), (0, 0, 0, 0))
ud = ImageDraw.Draw(ug)
c = U * SS / 2
ud.ellipse([c - 0.46 * U * SS, c - 0.46 * U * SS, c + 0.46 * U * SS, c + 0.46 * U * SS], outline=INK, width=int(0.11 * U * SS))
star(ud, c, c, 0.22 * U * SS, RED)
ug.resize((U, U), Image.LANCZOS).save("unlock.png")
print("saved unlock.png")
