#!/usr/bin/env python3
"""Render 9 era-poster variants of the Red Wedge theme.

Same construction as generate.py, but the headline + fine-print text varies
across 9 historical agitprop eras. The collage is composed by make_collage.py
in the same 3x2 layout dhh uses in omarchy-diablo-dreams-theme.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from generate import (
    W, H, SS, CW, CH,
    PAPER, INK, RED, RED_DEEP,
    LATO_BLACK, LATO_HEAVY, MONO,
    star, text_at, rotated_text,
)


# (era, headline1, headline2, redline3, fineprint)
VARIANTS = [
    ("1919", "BEAT THE WHITES",  "WITH THE RED WEDGE",   "WORKERS UNITE",        "CENTRAL COMMITTEE \u00b7 MOSCOW \u00b7 1919"),
    ("1925", "THE PEASANTS",     "READ THE GAZETTE",     "EVERY VILLAGE A PRESS", "CENTRAL COMMITTEE \u00b7 1925"),
    ("1929", "FIVE YEAR PLAN",   "FOUR YEARS AHEAD",     "OUTPUT DOUBLED",        "CENTRAL COMMITTEE \u00b7 1929"),
    ("1931", "STAKHANOV",        "RECORD BROKEN",        "FIVE HUNDRED PERCENT",  "CENTRAL COMMITTEE \u00b7 1931"),
    ("1935", "ON THE STEPPES",   "THE FIVE YEAR LINE",   "WORKERS LEAD",          "CENTRAL COMMITTEE \u00b7 1935"),
    ("1941", "MOTHERLAND",       "CALLS YOU",            "THE FRONT HOLDS",       "CENTRAL COMMITTEE \u00b7 1941"),
    ("1961", "GAGARIN",          "IS IN ORBIT",          "THE FUTURE IS OURS",    "CENTRAL COMMITTEE \u00b7 1961"),
    ("1971", "LENIN",            "CENTENNIAL",           "TWENTY-FIVE MILLION",   "CENTRAL COMMITTEE \u00b7 1971"),
    ("1989", "PERESTROIKA",      "OPENNESS",             "NO MORE SECRETS",       "CENTRAL COMMITTEE \u00b7 1989"),
]


def render_variant(h1, h2, h3, fineprint):
    img = Image.new("RGB", (CW, CH), PAPER)
    d = ImageDraw.Draw(img)

    def font(path, size):
        return ImageFont.truetype(path, size * SS)

    WEDGE_DEG = 10
    d.polygon(
        [(0, CH), (0, int(1500 * SS)), (int(2980 * SS), int(1275 * SS)), (int(1500 * SS), CH)],
        fill=RED,
    )
    for off, wd in ((90, 6), (150, 2)):
        x0, y0 = 0, (1500 - off) * SS
        x1, y1 = 2980 * SS, (1275 - off) * SS
        d.line([(x0, y0), (x1, y1)], fill=INK, width=wd * SS)

    OCX, OCY, OR = 880, 620, 350
    d.ellipse(
        [(OCX - OR) * SS, (OCY - OR) * SS, (OCX + OR) * SS, (OCY + OR) * SS],
        outline=INK,
        width=92 * SS,
    )
    star(d, OCX * SS, OCY * SS, 150 * SS, RED)

    rotated_text(
        2340, 780,
        [
            (h1, font(LATO_BLACK, 150), INK),
            (h2, font(LATO_BLACK, 150), INK),
            (h3, font(LATO_BLACK, 96), RED),
        ],
        WEDGE_DEG,
    )

    text_at(3060, 1630, "ELITE CAPITAL \u00b7 PUBLIC CODE", font(LATO_HEAVY, 54), INK, tracking=14)
    text_at(3060, 1730, "ZERO DOLLARS \u00b7 SEVERAL BILLIONAIRES", font(LATO_HEAVY, 44), RED_DEEP, tracking=10)

    cream_line = Image.new("RGBA", (2400 * SS, 200 * SS), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cream_line)
    cd.text((0, 0), "OMARCHY \u00b7 THE PEOPLE'S DESKTOP, FUNDED BY THE 0.001%", font=font(LATO_HEAVY, 52), fill=PAPER)
    cream_line = cream_line.rotate(4.3, resample=Image.BICUBIC, expand=True)
    img.paste(cream_line, (int(240 * SS), int(1810 * SS)), cream_line)

    sx = 3060 - 5 * 66
    for i in range(8):
        star(d, (sx + i * 66) * SS, 1860 * SS, 22 * SS, RED)
    for i in range(2):
        star(d, (sx + 8 * 66 + 22 + i * 50) * SS, 1864 * SS, 13 * SS, RED_DEEP)

    text_at(2620, 2110, fineprint, font(MONO, 26), INK, tracking=4)

    return img.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    os.makedirs("backgrounds", exist_ok=True)
    for i, (era, h1, h2, h3, fineprint) in enumerate(VARIANTS, start=1):
        out = render_variant(h1, h2, h3, fineprint)
        path = f"backgrounds/{i}-{era}-poster.jpg"
        out.convert("RGB").save(path, "JPEG", quality=88, optimize=True)
        print(f"saved {path}")
