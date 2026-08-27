"""Nine constructivist posters for the Red Wedge theme.

Native-16:9 repair (2026-08-27): all nine render at 3840x2160, identical to
the desktop hero, so Quickshell's Image.PreserveAspectCrop never strips
content on a 16:9 output. Composition, not scaling: heights were recut for
the shorter canvas (2160 vs the old 2560), not squeezed. The set is locked
to three constructivist inks: aged paper, near-black, party red (plus
shades). Cells are distinguished by red:black:paper area ratios in a
checker-like ordering, not by color:

    row 1  bright sunburst | dark starcog    | mid canonical wedge
    row 2  dark grid       | mid target      | dark banner
    row 3  red field       | dark macro      | bright manifesto

Diagonals alternate direction (wedge rises, redfield band falls).
Copy keeps the Oligarchy joke and DHH's line; no real persons, no
leaders, nothing copyrighted. Text is secondary: every thumbnail reads
by silhouette alone. `rw.Sheet.text/paste/ring_star/patrons` assert every
critical placement stays inside the 5% safe margin -- a bad coordinate
raises at render time instead of shipping a clipped poster.
"""

import math

from rw import (
    Sheet, PAPER, PAPER_DEEP, INK, RED, RED_DEEP,
    LATO_BLACK, LATO_HEAVY, MONO,
    SRC_W, SRC_H,
)

CX, CY = SRC_W / 2, SRC_H / 2  # 1920, 1080


def poster_sunburst():
    """Bright anchor. Rising red sun, ink rays, horizon rule."""
    s = Sheet(SRC_W, SRC_H)
    cx, cy = 2560, 680
    for i in range(18):
        ang = -178 + i * (176 / 17)
        r1 = 680 if i % 2 else 900
        s.ray(cx, cy, ang, 380, r1, 34, INK)
    s.disc(cx, cy, 300, RED)
    s.disc(cx, cy, 64, INK)
    s.ring(cx, cy, 230, 12, PAPER)
    s.line(0, 1020, SRC_W, 1020, INK, 12)
    s.ring_star(340, 290, 85, 36, ring_w=24)
    f1 = s.font(LATO_BLACK, 170)
    f2 = s.font(LATO_HEAVY, 42)
    s.text(240, 1350, "ZERO", f1, INK, anchor="lm")
    s.text(240, 1520, "DOLLARS", f1, RED, anchor="lm")
    s.text(240, 1660, "SEVERAL BILLIONAIRES FUND IT ANYWAY", f2, INK,
           tracking=8, anchor="lm")
    s.patrons(240, 1780, r_big=15, r_small=10, gap=42)
    s.text(3600, 1660, "ELITE CAPITAL \u00b7 PUBLIC CODE", s.font(LATO_HEAVY, 42),
           INK, tracking=10, anchor="rm")
    s.fine(CX, 1980, size=22, anchor="mm")
    return s.finish(grain_seed=101)


def poster_starcog():
    """Dark anchor. Ink field, paper gear, red star of industry."""
    s = Sheet(SRC_W, SRC_H, bg=INK)
    s.ring_star(340, 290, 80, 34, ring_w=22, ring_color=PAPER)
    s.gear(1180, 1080, 520, 450, 14, PAPER)
    s.star(1180, 1080, 310, RED)
    for i in range(8):
        a = math.radians(i * 45 - 90)
        s.disc(1180 + 430 * math.cos(a), 1080 + 430 * math.sin(a), 20, INK)
    fb = s.font(LATO_BLACK, 120)
    fm = s.font(LATO_BLACK, 150)
    fs = s.font(LATO_HEAVY, 50)
    s.text(1980, 700, "THE PEOPLE'S", fb, PAPER, anchor="lm")
    s.text(1980, 860, "MACHINE", fm, PAPER, anchor="lm")
    s.line(1980, 990, 3560, 990, RED, 10)
    s.text(1980, 1080, "RUNS ON ZERO DOLLARS", fs, PAPER, tracking=8, anchor="lm")
    s.text(1980, 1170, "AND SEVERAL BILLIONAIRES", s.font(LATO_HEAVY, 42),
           PAPER, tracking=6, anchor="lm")
    s.patrons(1980, 1300, r_big=17, r_small=11, gap=50,
              color=PAPER, small_color=PAPER_DEEP)
    s.fine(CX, 1980, color=PAPER_DEEP, size=22, anchor="mm")
    return s.finish(grain_seed=102)


def poster_wedge(w=SRC_W, h=SRC_H):
    """Canonical composition: the red wedge itself. Also the 16:9 hero."""
    s = Sheet(w, h)
    s.poly([(0, h), (0, 1500), (2980, 1275), (1500, h)], RED)
    for off, wd in ((90, 12), (150, 6), (210, 4)):
        s.line(0, 1500 - off, 2980, 1275 - off, INK, wd)
    s.ring_star(880, 620, 350, 150, ring_w=92)
    s.paste(2340, 780, s.block(
        [
            ("REDISTRIBUTING", s.font(LATO_BLACK, 130), INK),
            ("BILLIONAIRE WEALTH", s.font(LATO_BLACK, 130), INK),
            ("ONE ISO AT A TIME", s.font(LATO_BLACK, 82), RED),
        ],
        6,
    ))
    s.text(3060, 1650, "ELITE CAPITAL \u00b7 PUBLIC CODE",
           s.font(LATO_HEAVY, 50), INK, tracking=12)
    s.text(3060, 1750, "ZERO DOLLARS \u00b7 SEVERAL BILLIONAIRES",
           s.font(LATO_HEAVY, 40), RED_DEEP, tracking=8)
    s.paste(1500, 1700, s.block(
        [("OMARCHY \u00b7 THE PEOPLE'S DESKTOP, FUNDED BY THE 0.001%",
          s.font(LATO_HEAVY, 38), PAPER)],
        3,
    ))
    s.patrons(2730, 1860)
    s.fine(2620, 1985, size=22)
    return s.finish(grain_seed=103)


def poster_grid():
    """Dark blueprint grid: paper rules on ink, red star of the plan."""
    s = Sheet(SRC_W, SRC_H, bg=INK)
    for x in (240, 1020, 1800, 2580, 3360):
        s.line(x, 140, x, 1900, PAPER, 8)
    for y in (140, 680, 1220, 1900):
        s.line(240, y, 3360, y, PAPER, 8)
    s.ring_star(560, 400, 210, 90, ring_w=54, ring_color=PAPER)
    s.text(2370, 350, "FIVE YEAR PLAN", s.font(LATO_BLACK, 100), PAPER,
           anchor="lm")
    s.text(2370, 480, "SHIPPED WEEKLY", s.font(LATO_BLACK, 72), PAPER_DEEP,
           anchor="lm")
    hatch = Sheet(760, 540, bg=INK)
    for off in range(-540, 760, 40):
        hatch.line(off, 540, off + 540, 0, PAPER, 6)
    s.img.paste(hatch.img, (int(240 * s.ss), int(680 * s.ss)))
    s.star(1240, 950, 220, RED)
    s.patrons(1040, 1170, r_big=11, r_small=8, gap=32,
              color=PAPER, small_color=PAPER_DEEP)
    s.disc(2370, 950, 220, PAPER)
    s.star(2370, 950, 125, RED)
    fm = s.font(LATO_HEAVY, 36)
    s.text(3200, 850, "CODE PUBLIC", fm, PAPER, tracking=4)
    s.text(3200, 950, "PRICE ZERO", fm, PAPER, tracking=4)
    s.text(3200, 1050, "STARS EIGHT", fm, PAPER, tracking=4)
    s.line(2900, 1130, 3480, 1130, RED, 6)
    s.rect(240, 1220, 1020, 1900, fill=PAPER)
    s.paste(630, 1450, s.block([("OMARCHY", s.font(LATO_BLACK, 78), INK)], 90))
    s.line(1020, 1330, 2660, 1330, RED, 6)
    s.text(1920, 1450, "THE PEOPLE'S DESKTOP", s.font(LATO_HEAVY, 46), PAPER)
    s.text(1920, 1550, "FUNDED BY THE 0.001%", s.font(LATO_HEAVY, 34),
           PAPER_DEEP, tracking=6)
    s.line(1020, 1620, 2660, 1620, PAPER, 3)
    fnt = s.font(MONO, 15)
    s.text(1920, 1720, "APPROVED BY THE CENTRAL COMMITTEE", fnt, PAPER,
           tracking=2)
    s.text(1920, 1780, "OF THE OMACOM FOUNDATION \u00b7 SERIES 2026", fnt,
           PAPER, tracking=2)
    return s.finish(grain_seed=106)


def poster_target():
    """Concentric target: take aim, ship isos."""
    s = Sheet(SRC_W, SRC_H)
    cx, cy = CX, CY
    for r, col in ((700, INK), (600, PAPER), (480, RED), (380, PAPER),
                   (280, RED), (180, PAPER)):
        s.disc(cx, cy, r, col)
    s.star(cx, cy, 160, RED)
    s.text(CX, 260, "BILLIONAIRES BUY ISLANDS", s.font(LATO_HEAVY, 48),
           INK, tracking=10)
    s.text(CX, 1870, "WE SHIP ISOS FREE", s.font(LATO_BLACK, 92), RED)
    s.fine(CX, 1975, size=18)
    return s.finish(grain_seed=105)


def poster_banner():
    """Ink banner panel, vertical wordmark, ring and star on cream."""
    s = Sheet(SRC_W, SRC_H)
    s.rect(0, 0, 900, SRC_H, fill=INK)
    s.star(450, 220, 66, RED)
    s.paste(450, 1080, s.block([("OMARCHY", s.font(LATO_BLACK, 210), PAPER)], 90))
    s.text(450, 1970, "SERIES 2026", s.font(MONO, 26), PAPER,
           tracking=8, anchor="mm")
    s.text(1020, 260, "ELITE CAPITAL \u00b7 PUBLIC CODE", s.font(LATO_HEAVY, 44),
           INK, tracking=12, anchor="lm")
    s.ring_star(2760, 700, 320, 135, ring_w=84)
    s.patrons(1020, 1180)
    fb = s.font(LATO_BLACK, 130)
    s.text(1020, 1360, "THE PEOPLE'S", fb, INK, anchor="lm")
    s.text(1020, 1520, "DESKTOP", fb, INK, anchor="lm")
    s.text(1020, 1650, "FUNDED BY THE 0.001%", s.font(LATO_HEAVY, 50),
           RED_DEEP, tracking=8, anchor="lm")
    s.poly([(3000, SRC_H), (SRC_W, SRC_H), (SRC_W, 1500)], RED)
    s.fine(1020, 1980, size=22, anchor="lm")
    return s.finish(grain_seed=104)


def poster_redfield():
    s = Sheet(SRC_W, SRC_H, bg=RED)
    s.poly([(0, 300), (SRC_W, 780), (SRC_W, 1350), (0, 870)], PAPER)
    s.line(0, 870, SRC_W, 1350, INK, 10)
    s.paste(CX, 810, s.block(
        [("REDISTRIBUTING BILLIONAIRE WEALTH", s.font(LATO_BLACK, 90), INK)],
        -8,
    ))
    s.ring_star(3470, 280, 95, 40, ring_w=26, ring_color=PAPER,
                star_color=PAPER)
    s.rect(0, 1680, SRC_W, SRC_H, fill=INK)
    s.text(CX, 1790, "ONE ISO AT A TIME", s.font(LATO_BLACK, 100), PAPER)
    s.patrons(1560, 1900, r_big=13, r_small=9, gap=36,
              color=PAPER, small_color=PAPER_DEEP)
    s.fine(CX, 1985, color=PAPER, size=18)
    return s.finish(grain_seed=107, grain_strength=40)


def poster_macro():
    """Macro detail. The Omarchy O fills the frame, cropped by the edges."""
    s = Sheet(SRC_W, SRC_H)
    s.ring(CX, CY, 850, 230, INK)
    s.star(CX, CY, 560, RED)
    s.text(CX, CY, "OMARCHY", s.font(LATO_BLACK, 95), PAPER)
    s.poly([(0, SRC_H), (900, SRC_H), (0, 1300)], RED)
    s.text(250, 1900, "THE O IS FOR OLIGARCHY", s.font(LATO_HEAVY, 42),
           PAPER, tracking=6, anchor="lm")
    s.fine(250, 1985, color=PAPER, size=18, tracking=2, anchor="lm")
    return s.finish(grain_seed=109)


def poster_manifesto():
    """Bright anchor. Red plate, type block, ink emblem -- reads at any scale."""
    s = Sheet(SRC_W, SRC_H)
    s.rect(0, 0, 820, SRC_H, fill=RED)
    s.star(410, 200, 62, PAPER)
    s.paste(410, 1080, s.block(
        [("MANIFESTO", s.font(LATO_BLACK, 92), PAPER)], 90))
    fm = s.font(LATO_HEAVY, 46)
    lines = [
        "THE PEOPLE OWN THE DESKTOP.",
        "THE BILLIONAIRES OWN THE BILL.",
        "THE CODE IS PUBLIC.",
        "THE PRICE IS ZERO.",
        "THE WEALTH IS OPTIONAL.",
        "THE ISO IS WEEKLY.",
        "ALL POWER TO THE TERMINAL.",
    ]
    for i, ln in enumerate(lines):
        s.text(960, 400 + i * 92, ln, fm, INK, tracking=4, anchor="lm")
    s.line(900, 350, 900, 1000, RED_DEEP, 12)
    s.text(960, 1100, "REDISTRIBUTING BILLIONAIRE WEALTH, ONE ISO AT A TIME",
           s.font(LATO_HEAVY, 40), RED_DEEP, tracking=3, anchor="lm")
    s.patrons(960, 1230, r_big=18, r_small=12, gap=52)
    s.ring_star(2980, 620, 300, 130, ring_w=78)
    s.star(3400, 1500, 105, INK)
    s.poly([(SRC_W, SRC_H), (3140, SRC_H), (SRC_W, 1700)], RED)
    s.fine(960, 1980, size=22, anchor="lm")
    return s.finish(grain_seed=108)


# Collage order = checker of tonal anchors (bright/dark/mid, red, bright, dark).
POSTERS = [
    ("sunburst", poster_sunburst),
    ("starcog", poster_starcog),
    ("wedge", poster_wedge),
    ("grid", poster_grid),
    ("target", poster_target),
    ("banner", poster_banner),
    ("redfield", poster_redfield),
    ("macro", poster_macro),
    ("manifesto", poster_manifesto),
]
