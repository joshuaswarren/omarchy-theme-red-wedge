"""Nine constructivist posters for the Red Wedge theme.

All nine render at one uniform 3:2 resolution (3840x2560, >= 3840 wide).
The set is locked to three constructivist inks: aged paper, near-black,
party red (plus shades of those). Cells are distinguished by
red:black:paper area ratios in a checker-like ordering, not by color:

    row 1  bright sunburst | dark starcog    | mid canonical wedge
    row 2  dark banner     | mid target      | bright grid
    row 3  red field       | bright manifesto| dark macro

Diagonals alternate direction (wedge rises, redfield band falls).
Copy keeps the Oligarchy joke and DHH's line; no real persons, no
leaders, nothing copyrighted. Text is secondary: every thumbnail reads
by silhouette alone.
"""

from rw import (
    Sheet, PAPER, PAPER_DEEP, INK, RED, RED_DEEP,
    LATO_BLACK, LATO_HEAVY, MONO,
    SRC_W, SRC_H,
)


def poster_sunburst():
    """Bright anchor. Rising red sun, ink rays, horizon rule."""
    s = Sheet(SRC_W, SRC_H)
    for i in range(18):
        ang = -178 + i * (176 / 17)
        r1 = 950 if i % 2 else 1300
        s.ray(2560, 980, ang, 560, r1, 44, INK)
    s.disc(2560, 980, 500, RED)
    s.disc(2560, 980, 90, INK)
    s.ring(2560, 980, 380, 14, PAPER)
    s.line(0, 1560, 3840, 1560, INK, 14)
    s.ring_star(330, 330, 110, 46, ring_w=30)
    f1 = s.font(LATO_BLACK, 240)
    f2 = s.font(LATO_HEAVY, 54)
    s.text(200, 1790, "ZERO", f1, INK, anchor="lm")
    s.text(200, 2020, "DOLLARS", f1, RED, anchor="lm")
    s.text(200, 2200, "SEVERAL BILLIONAIRES FUND IT ANYWAY", f2, INK,
           tracking=8, anchor="lm")
    s.patrons(200, 2340, r_big=18, r_small=12, gap=52)
    s.text(3640, 2200, "ELITE CAPITAL \u00b7 PUBLIC CODE", s.font(LATO_HEAVY, 54),
           INK, tracking=10, anchor="rm")
    s.fine(200, 2480, size=24, anchor="lm")
    return s.finish(grain_seed=101)


def poster_starcog():
    """Dark anchor. Ink field, paper gear, red star of industry."""
    s = Sheet(SRC_W, SRC_H, bg=INK)
    s.ring_star(300, 260, 100, 42, ring_w=26, ring_color=PAPER)
    s.gear(1180, 1240, 660, 580, 14, PAPER)
    s.star(1180, 1240, 400, RED)
    import math
    for i in range(8):
        a = math.radians(i * 45 - 90)
        s.disc(1180 + 545 * math.cos(a), 1240 + 545 * math.sin(a), 22, INK)
    fb = s.font(LATO_BLACK, 150)
    fm = s.font(LATO_BLACK, 190)
    fs = s.font(LATO_HEAVY, 64)
    s.text(1980, 780, "THE PEOPLE'S", fb, PAPER, anchor="lm")
    s.text(1980, 970, "MACHINE", fm, PAPER, anchor="lm")
    s.line(1980, 1130, 3620, 1130, RED, 10)
    s.text(1980, 1240, "RUNS ON ZERO DOLLARS", fs, PAPER, tracking=8, anchor="lm")
    s.text(1980, 1350, "AND SEVERAL BILLIONAIRES", s.font(LATO_HEAVY, 54),
           PAPER, tracking=6, anchor="lm")
    s.patrons(1980, 1520, r_big=20, r_small=13, gap=58,
              color=PAPER, small_color=PAPER_DEEP)
    s.fine(1980, 2470, color=PAPER_DEEP, size=24, anchor="lm")
    return s.finish(grain_seed=102)


def poster_wedge(w=SRC_W, h=SRC_H):
    """Canonical composition: the red wedge itself. Also the 16:9 hero."""
    s = Sheet(w, h)
    k = h / 2160.0

    def Y(y):
        return y * k

    s.poly([(0, h), (0, Y(1500)), (2980, Y(1275)), (1500, h)], RED)
    for off, wd in ((90, 12), (150, 6), (210, 4)):
        s.line(0, Y(1500 - off), 2980, Y(1275 - off), INK, wd)
    s.ring_star(880, Y(620), 350, 150, ring_w=92)
    s.paste(2340, Y(780), s.block(
        [
            ("REDISTRIBUTING", s.font(LATO_BLACK, 150), INK),
            ("BILLIONAIRE WEALTH", s.font(LATO_BLACK, 150), INK),
            ("ONE ISO AT A TIME", s.font(LATO_BLACK, 96), RED),
        ],
        10,
    ))
    s.text(3060, Y(1630), "ELITE CAPITAL \u00b7 PUBLIC CODE",
           s.font(LATO_HEAVY, 54), INK, tracking=14)
    s.text(3060, Y(1730), "ZERO DOLLARS \u00b7 SEVERAL BILLIONAIRES",
           s.font(LATO_HEAVY, 44), RED_DEEP, tracking=10)
    s.paste(1035, Y(1890), s.block(
        [("OMARCHY \u00b7 THE PEOPLE'S DESKTOP, FUNDED BY THE 0.001%",
          s.font(LATO_HEAVY, 52), PAPER)],
        4.3,
    ))
    s.patrons(2730, Y(1860))
    s.fine(2620, Y(2110))
    return s.finish(grain_seed=103)


def poster_banner():
    """Ink banner panel, vertical wordmark, ring and star on cream."""
    s = Sheet(SRC_W, SRC_H)
    s.rect(0, 0, 1010, 2560, fill=INK)
    s.star(505, 210, 80, RED)
    s.paste(505, 1330, s.block([("OMARCHY", s.font(LATO_BLACK, 300), PAPER)], 90))
    s.text(505, 2440, "SERIES 2026", s.font(MONO, 30), PAPER,
           tracking=8, anchor="mm")
    s.text(1150, 300, "ELITE CAPITAL \u00b7 PUBLIC CODE", s.font(LATO_HEAVY, 56),
           INK, tracking=12, anchor="lm")
    s.ring_star(2600, 830, 420, 180, ring_w=110)
    s.patrons(1150, 1430)
    fb = s.font(LATO_BLACK, 170)
    s.text(1150, 1620, "THE PEOPLE'S", fb, INK, anchor="lm")
    s.text(1150, 1810, "DESKTOP", fb, INK, anchor="lm")
    s.text(1150, 1960, "FUNDED BY THE 0.001%", s.font(LATO_HEAVY, 64),
           RED_DEEP, tracking=8, anchor="lm")
    s.poly([(2980, 2560), (3840, 2560), (3840, 1760)], RED)
    s.fine(1150, 2440, size=24, anchor="lm")
    return s.finish(grain_seed=104)


def poster_target():
    """Concentric target: take aim, ship isos."""
    s = Sheet(SRC_W, SRC_H)
    cx, cy = 1920, 1240
    for r, col in ((1050, INK), (900, PAPER), (740, RED), (600, PAPER),
                   (460, RED), (320, PAPER)):
        s.disc(cx, cy, r, col)
    s.star(cx, cy, 230, RED)
    s.text(1920, 150, "BILLIONAIRES BUY ISLANDS", s.font(LATO_HEAVY, 62),
           INK, tracking=12)
    s.text(1920, 2400, "WE SHIP ISOS FREE", s.font(LATO_BLACK, 110), RED)
    s.fine(1920, 2500, size=20)
    return s.finish(grain_seed=105)


def poster_grid():
    """Dark blueprint grid: paper rules on ink, red star of the plan."""
    s = Sheet(SRC_W, SRC_H, bg=INK)
    for x in (120, 1020, 1920, 2820, 3720):
        s.line(x, 120, x, 2440, PAPER, 10)
    for y in (120, 973, 1827, 2440):
        s.line(120, y, 3720, y, PAPER, 10)
    s.ring_star(570, 546, 260, 110, ring_w=68, ring_color=PAPER)
    s.text(2370, 470, "FIVE YEAR PLAN", s.font(LATO_BLACK, 130), PAPER)
    s.text(2370, 640, "SHIPPED WEEKLY", s.font(LATO_BLACK, 95), PAPER_DEEP)
    hatch = Sheet(900, 853, bg=INK)
    for off in range(-853, 900, 48):
        hatch.line(off, 853, off + 853, 0, PAPER, 7)
    s.img.paste(hatch.img, (int(120 * s.ss), int(973 * s.ss)))
    s.star(1470, 1330, 300, RED)
    s.patrons(1240, 1640, r_big=13, r_small=9, gap=38,
              color=PAPER, small_color=PAPER_DEEP)
    s.disc(2370, 1330, 300, PAPER)
    s.star(2370, 1330, 170, RED)
    fm = s.font(LATO_HEAVY, 42)
    s.text(3270, 1180, "CODE PUBLIC", fm, PAPER, tracking=4)
    s.text(3270, 1320, "PRICE ZERO", fm, PAPER, tracking=4)
    s.text(3270, 1460, "STARS EIGHT", fm, PAPER, tracking=4)
    s.line(2950, 1560, 3590, 1560, RED, 8)
    s.rect(120, 1827, 1020, 2440, fill=PAPER)
    s.paste(570, 2133, s.block([("OMARCHY", s.font(LATO_BLACK, 105), INK)], 90))
    s.line(1020, 1930, 2820, 1930, RED, 8)
    s.text(1920, 2080, "THE PEOPLE'S DESKTOP", s.font(LATO_HEAVY, 58), PAPER)
    s.text(1920, 2200, "FUNDED BY THE 0.001%", s.font(LATO_HEAVY, 44),
           PAPER_DEEP, tracking=6)
    s.line(1020, 2290, 2820, 2290, PAPER, 3)
    fnt = s.font(MONO, 19)
    s.text(3270, 2010, "APPROVED BY THE CENTRAL COMMITTEE", fnt, PAPER, tracking=2)
    s.text(3270, 2080, "OF THE OMACOM FOUNDATION \u00b7 SERIES 2026", fnt,
           PAPER, tracking=2)
    return s.finish(grain_seed=106)


def poster_redfield():
    s = Sheet(SRC_W, SRC_H, bg=RED)
    s.poly([(0, 150), (3840, 1000), (3840, 1900), (0, 1050)], PAPER)
    s.line(0, 1050, 3840, 1900, INK, 12)
    s.paste(1920, 1025, s.block(
        [("REDISTRIBUTING BILLIONAIRE WEALTH", s.font(LATO_BLACK, 118), INK)],
        -12.5,
    ))
    s.ring_star(3650, 200, 110, 46, ring_w=28, ring_color=PAPER,
                star_color=PAPER)
    s.rect(0, 2050, 3840, 2560, fill=INK)
    s.text(1920, 2190, "ONE ISO AT A TIME", s.font(LATO_BLACK, 150), PAPER)
    s.patrons(1660, 2370, r_big=18, r_small=12, gap=52,
              color=PAPER, small_color=PAPER_DEEP)
    s.fine(1920, 2480, color=PAPER, size=22)
    return s.finish(grain_seed=107, grain_strength=40)


def poster_manifesto():
    """Bright anchor. Red plate, type block, ink emblem — reads at any scale."""
    s = Sheet(SRC_W, SRC_H)
    s.rect(0, 0, 900, 2560, fill=RED)
    s.star(450, 170, 80, PAPER)
    s.paste(450, 1330, s.block(
        [("MANIFESTO", s.font(LATO_BLACK, 120), PAPER)], 90))
    fm = s.font(LATO_HEAVY, 58)
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
        s.text(1060, 540 + i * 108, ln, fm, INK, tracking=4, anchor="lm")
    s.line(990, 480, 990, 1300, RED_DEEP, 14)
    s.text(1060, 1450, "REDISTRIBUTING BILLIONAIRE WEALTH, ONE ISO AT A TIME",
           s.font(LATO_HEAVY, 54), RED_DEEP, tracking=4, anchor="lm")
    s.patrons(1060, 1610, r_big=22, r_small=15, gap=64)
    s.ring_star(3050, 620, 340, 150, ring_w=90)
    s.star(3450, 1900, 130, INK)
    s.poly([(3840, 2560), (3140, 2560), (3840, 1760)], RED)
    s.fine(1060, 2470, size=24, anchor="lm")
    return s.finish(grain_seed=108)


def poster_macro():
    """Macro detail. The Omarchy O fills the frame, cropped by the edges."""
    s = Sheet(SRC_W, SRC_H)
    s.ring(1920, 1240, 1500, 400, INK)
    s.star(1920, 1240, 950, RED)
    s.text(1920, 1240, "OMARCHY", s.font(LATO_BLACK, 130), PAPER)
    s.poly([(0, 2560), (1500, 2560), (0, 1000)], RED)
    s.text(170, 2300, "THE O IS FOR OLIGARCHY", s.font(LATO_HEAVY, 56),
           PAPER, tracking=6, anchor="lm")
    s.fine(170, 2470, color=PAPER, size=20, tracking=2, anchor="lm")
    return s.finish(grain_seed=109)


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
