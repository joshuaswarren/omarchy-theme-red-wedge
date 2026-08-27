"""Offline desktop preview (1800x1012) and lock-screen preview.

Drawn, not captured: the hero poster behind a top bar and three staged
panels (code editor, btop, file manager), all in the locked palette
(paper / ink / red and shades). Information density is comparable to
the reference theme preview. Nothing here is a live screenshot.
"""

from PIL import Image

from rw import (
    Sheet, PAPER, PAPER_DEEP, INK, RED, RED_DEEP,
    LATO_BLACK, LATO_HEAVY, MONO, MONO_BOLD, MONO_OBLIQUE,
)

PW, PH = 1800, 1012

# Code buffer shown in the editor panel: (segments, font style).
KW, STR, CMT, PLN, BLD, NUM = "kw", "str", "cmt", "pln", "bld", "num"
CODE = [
    [("# the people's desktop, funded by the 0.001%", CMT)],
    [("class", KW), (" Oligarchy", BLD), (":", PLN)],
    [("    patrons", PLN), (" = ", PLN), ("8", NUM),
     ("            # plus two", CMT)],
    [("    code", PLN), ("    = ", PLN), ('"public"', STR)],
    [("    wealth", PLN), ("  = ", PLN), ('"private"', STR)],
    [],
    [("    def", KW), (" redistribute", BLD), ("(self, iso):", PLN)],
    [("        for", KW), (" patron ", PLN), ("in", KW),
     (" self.patrons:", PLN)],
    [("            iso += patron.contribute(", PLN), ("0", NUM), (")", PLN)],
    [("        return", KW), (" iso          ", PLN),
     ("# price: $0.00", CMT)],
    [],
    [("people = Oligarchy()", PLN)],
    [('people.redistribute("omarchy.iso")', PLN)],
]

FILES = [
    ("patrons/", "folder", "—", ""),
    ("isos/", "folder", "—", ""),
    ("manifestos/", "folder", "—", ""),
    ("oligarchy.py", "doc", "4 KB", INK),
    ("omarchy.iso", "iso", "1.8 GB", RED),
    ("wealth.txt", "doc", "0 B", RED_DEEP),
    ("REDISTRIBUTE.md", "doc", "12 KB", INK),
]

STYLES = {
    KW: (RED, None),
    STR: (RED_DEEP, None),
    CMT: (INK, MONO_OBLIQUE),
    PLN: (INK, None),
    BLD: (INK, MONO_BOLD),
    NUM: (RED, None),
}


def _panel(s, x, y, w, h, title):
    """Window chrome: hard ink shadow, paper body, ink title bar."""
    s.rect(x + 8, y + 10, x + w + 8, y + h + 10, fill=INK)
    s.rect(x, y, x + w, y + h, fill=PAPER, outline=INK, w=2)
    s.rect(x, y, x + w, y + 30, fill=INK)
    for i, col in enumerate((RED, PAPER, RED_DEEP)):
        s.disc(x + 18 + i * 17, y + 15, 4.5, col)
    s.text(x + w / 2, y + 15, title, s.font(MONO, 12), PAPER)


def _chip(s, x, y, label, color):
    s.rect(x, y - 5, x + 9, y + 4, fill=color)
    s.text(x + 15, y, label, s.font(MONO, 12), INK, anchor="lm")
    return x + 15 + s.tw(label, s.font(MONO, 12)) + 14


def build_preview(hero):
    """Compose the 1800x1012 desktop preview over the hero poster."""
    s = Sheet(PW, PH)
    s.img.paste(hero.resize((PW * s.ss, PH * s.ss), Image.LANCZOS), (0, 0))

    # ── top bar ─────────────────────────────────────────────────────────────
    s.rect(0, 0, PW, 44, fill=PAPER, outline=PAPER, w=1)
    s.line(0, 44, PW, 44, INK, 2)
    s.ring_star(26, 22, 13, 5.5, ring_w=3.5)
    s.text(48, 22, "OLIGARCHY", s.font(LATO_BLACK, 17), INK, anchor="lm")
    s.text(160, 22, "· the people's desktop", s.font(MONO, 12), RED_DEEP,
           anchor="lm")
    s.text(PW / 2, 22, "13:37", s.font(LATO_BLACK, 20), INK, anchor="mm")
    x = PW - 24
    for label, col in reversed(
        [("BAT 100%", INK), ("ISO 4.2 GB", RED_DEEP), ("MEM 21%", INK),
         ("CPU 3%", RED)]
    ):
        wlab = s.tw(label, s.font(MONO, 12))
        s.text(x, 22, label, s.font(MONO, 12), INK, anchor="rm")
        s.rect(x - wlab - 19, 17, x - wlab - 10, 26, fill=col)
        x -= wlab + 34

    # ── editor panel ────────────────────────────────────────────────────────
    ex, ey, ew, eh = 48, 74, 880, 610
    _panel(s, ex, ey, ew, eh, "oligarchy.py — omarchy")
    body = s.font(MONO, 15)
    lead = 27 * s.ss
    y0 = ey + 58
    for i, segs in enumerate(CODE, start=1):
        yy = y0 + (i - 1) * lead / s.ss
        s.text(ex + 52, yy, f"{i:2d}", s.font(MONO, 12), RED_DEEP, anchor="rm")
        xx = ex + 84
        for text, style in segs:
            color, fpath = STYLES[style]
            fnt = s.font(fpath or MONO, 15)
            s.text(xx, yy, text, fnt, color, anchor="lm")
            xx += s.tw(text, fnt)
    s.line(ex + 66, ey + 40, ex + 66, ey + eh - 34, PAPER_DEEP, 2)
    s.rect(ex, ey + eh - 26, ex + ew, ey + eh, fill=PAPER_DEEP)
    s.line(ex, ey + eh - 26, ex + ew, ey + eh - 26, INK, 1)
    s.text(ex + 14, ey + eh - 13, "PYTHON · UTF-8 · THE PEOPLE'S EDITOR",
           s.font(MONO, 11), INK, anchor="lm")
    s.text(ex + ew - 14, ey + eh - 13, "PRICE: $0.00", s.font(MONO, 11),
           RED, anchor="rm")

    # ── btop panel ──────────────────────────────────────────────────────────
    bx, by, bw, bh = 1004, 74, 748, 396
    _panel(s, bx, by, bw, bh, "btop — the people's monitor")
    s.text(bx + 20, by + 52, "CPU  8 CORES", s.font(LATO_HEAVY, 13), RED,
           anchor="lm")
    loads = [12, 34, 8, 56, 22, 41, 9, 63]
    for i, pct in enumerate(loads):
        cx0 = bx + 150 + i * 72
        s.rect(cx0, by + 44, cx0 + 62, by + 60, fill=PAPER, outline=INK, w=1)
        s.rect(cx0, by + 44, cx0 + 62 * pct / 100, by + 60, fill=RED)
    s.text(bx + 20, by + 92, "MEM 21%", s.font(LATO_HEAVY, 13), RED, anchor="lm")
    s.rect(bx + 150, by + 84, bx + 560, by + 100, fill=PAPER, outline=INK, w=1)
    s.rect(bx + 150, by + 84, bx + 150 + 410 * 0.21, by + 100, fill=RED)
    s.text(bx + 580, by + 92, "4.2 GB / 20 GB", s.font(MONO, 11), INK,
           anchor="lm")
    s.text(bx + 20, by + 130, "NET", s.font(LATO_HEAVY, 13), RED, anchor="lm")
    vals = [4, 8, 6, 12, 9, 15, 11, 18, 13, 20, 16, 22, 17, 24, 19, 14, 10, 7]
    pts = [(bx + 150 + i * 24, by + 152 - v * 2) for i, v in enumerate(vals)]
    s.d.line([(px * s.ss, py * s.ss) for px, py in pts], fill=INK,
             width=int(2 * s.ss))
    lx, ly = pts[-1]
    s.disc(lx, ly, 4, RED)
    hdr = s.font(MONO_BOLD, 11)
    s.text(bx + 20, by + 190, "  PID  COMMAND        CPU%  MEM", hdr,
           RED_DEEP, anchor="lm")
    procs = [
        (" 1337  omarchy         3.1   212M", INK),
        (" 2026  redistribute     2.4    64M", INK),
        ("    8  patrons          0.8    12M", INK),
        ("    2  plus_two         0.4     8M", INK),
        ("    1  the_people       0.1     4M", RED_DEEP),
    ]
    for i, (row, col) in enumerate(procs):
        s.text(bx + 20, by + 214 + i * 22, row, s.font(MONO, 12), col,
               anchor="lm")
    s.text(bx + 20, by + bh - 16, "UPTIME 5Y PLAN · SHIPPED WEEKLY",
           s.font(MONO, 11), INK, anchor="lm")

    # ── file manager panel (staged over btop's foot) ────────────────────────
    fx, fy, fw, fh = 1004, 452, 748, 546
    _panel(s, fx, fy, fw, fh, "files — /home/the_people")
    s.rect(fx + 2, fy + 32, fx + 192, fy + fh - 2, fill=PAPER_DEEP)
    s.line(fx + 192, fy + 32, fx + 192, fy + fh - 2, INK, 1)
    s.text(fx + 18, fy + 56, "PLACES", s.font(MONO, 11), RED, anchor="lm")
    places = ["Home", "Patrons", "ISOs", "Manifestos", "Wallpapers", "Trash"]
    for i, name in enumerate(places):
        yy = fy + 88 + i * 34
        if i == 0:
            s.rect(fx + 2, yy - 12, fx + 8, yy + 12, fill=RED)
            s.text(fx + 26, yy, name, s.font(LATO_HEAVY, 14), RED, anchor="lm")
        else:
            s.text(fx + 26, yy, name, s.font(LATO_HEAVY, 14), INK, anchor="lm")
        s.poly([(fx + 12, yy + 6), (fx + 12, yy - 4), (fx + 20, yy - 4),
                (fx + 24, yy), (fx + 24, yy + 6)], fill=INK)
    lx0 = fx + 216
    s.text(lx0 + 8, fy + 56, "NAME", s.font(MONO_BOLD, 11), RED_DEEP,
           anchor="lm")
    s.text(fx + fw - 130, fy + 56, "SIZE", s.font(MONO_BOLD, 11), RED_DEEP,
           anchor="lm")
    for i, (name, kind, size, scol) in enumerate(FILES):
        yy = fy + 92 + i * 40
        if kind == "folder":
            s.poly([(lx0, yy + 7), (lx0, yy - 4), (lx0 + 9, yy - 4),
                    (lx0 + 13, yy), (lx0 + 26, yy), (lx0 + 26, yy + 7)],
                   fill=INK)
        else:
            s.rect(lx0, yy - 8, lx0 + 20, yy + 8, fill=PAPER, outline=scol, w=2)
            s.poly([(lx0 + 12, yy - 8), (lx0 + 20, yy), (lx0 + 12, yy)],
                   fill=scol if kind == "iso" else PAPER)
        s.text(lx0 + 40, yy, name,
               s.font(LATO_HEAVY, 14), scol if kind != "folder" else INK,
               anchor="lm")
        s.text(fx + fw - 130, yy, size, s.font(MONO, 12), INK, anchor="lm")
        if i < len(FILES) - 1:
            s.line(lx0, yy + 20, fx + fw - 100, yy + 20, PAPER_DEEP, 1)
    s.rect(fx, fy + fh - 26, fx + fw, fy + fh, fill=PAPER_DEEP)
    s.text(fx + 14, fy + fh - 13, "9 ITEMS \u00b7 0 DOLLARS \u00b7 SEVERAL BILLIONAIRES",
           s.font(MONO, 11), INK, anchor="lm")
    s.text(fx + fw - 14, fy + fh - 13, "FREE", s.font(MONO, 11), RED,
           anchor="rm")

    # ── one desktop icon, bottom-left over free wallpaper ───────────────────
    s.ring_star(96, 790, 30, 13, ring_w=8)
    s.text(96, 842, "oligarchy", s.font(MONO, 11), INK, anchor="mm")

    return s.finish()


def build_unlock_preview(hero):
    """Compose the 1800x1012 lock-screen preview."""
    s = Sheet(PW, PH)
    base = hero.resize((PW * s.ss, PH * s.ss), Image.LANCZOS)
    s.img.paste(base, (0, 0))
    scrim = Image.new("L", s.img.size, 42)
    s.img.paste(Image.new("RGB", s.img.size, INK), (0, 0), scrim)

    s.text(PW / 2, 330, "13:37", s.font(LATO_BLACK, 190), INK)
    s.text(PW / 2, 470, "THURSDAY \u00b7 SERIES 2026", s.font(LATO_HEAVY, 34),
           INK, tracking=10)
    s.ring_star(PW / 2, 640, 85, 36, ring_w=22)
    s.rect(PW / 2 - 190, 760, PW / 2 + 190, 816, fill=PAPER, outline=INK, w=2)
    for i in range(6):
        s.disc(PW / 2 - 150 + i * 30, 788, 5, INK)
    s.rect(PW / 2 + 44, 777, PW / 2 + 48, 799, fill=RED)
    s.text(PW / 2, 878, "THE PEOPLE'S DESKTOP \u00b7 FUNDED BY THE 0.001%",
           s.font(LATO_HEAVY, 22), INK, tracking=8)
    s.fine(PW / 2, 956, size=12, tracking=2)

    # Side cards keep the flanks from reading empty.
    for x0, label, big, small in (
        (120, "TODAY", "SHIP THE ISO", "weekly, like clockwork"),
        (1240, "NEXT", "REDISTRIBUTE WEALTH", "one at a time"),
    ):
        s.rect(x0, 690, x0 + 440, 870, fill=PAPER, outline=INK, w=2)
        s.rect(x0, 690, x0 + 440, 722, fill=INK)
        s.text(x0 + 20, 706, label, s.font(MONO, 12), PAPER, anchor="lm")
        s.text(x0 + 220, 770, big, s.font(LATO_BLACK, 30), INK)
        s.text(x0 + 220, 824, small, s.font(MONO, 12), RED_DEEP, anchor="mm")
    return s.finish()


def build_unlock_glyph():
    """512x512 RGBA glyph: ink ring, red star. Used by the lock screen."""
    s = Sheet(512, 512, bg=(0, 0, 0, 0), mode="RGBA")
    c = 256
    s.ring(c, c, 235, 56, INK)
    s.star(c, c, 112, RED)
    return s.finish()


def build_terminal():
    """Drawn terminal preview, 1800x1012, replacing the old 1920x1080 shot."""
    s = Sheet(PW, PH)
    _panel(s, 60, 46, PW - 120, PH - 92, "foot — the people's terminal")
    tx, ty = 110, 110
    lead = 36
    mono = s.font(MONO, 17)
    dim = s.font(MONO_OBLIQUE, 15)
    rows = [
 ("user@oligarchy", "hl"),
 ("------------------------------------------", "dim"),
 ("OS       Omarchy Quattro \u00b7 Series 2026", ""),
 ("Host     The People's Desktop", ""),
 ("Kernel   oligarchy-6.17.2-red-wedge", ""),
 ("Uptime   5 year plan (2 weeks in)", ""),
 ("Shell    redistribute", ""),
 ("Theme    Red Wedge [paper / ink / red]", ""),
 ("Funds    0 dollars \u00b7 several billionaires", ""),
 ("Stars    8 big + 2 small (the patrons)", ""),
 ("", ""),
 ("$ omarchy-theme-install red-wedge", "hl"),
 ("  \u2192 redistributing billionaire wealth ... done", ""),
 ("  \u2192 one ISO at a time", ""),
 ("  [||||||||||||||||||____] 80%", "bar"),
 ("", ""),
 ("# approved by the central committee", "dim"),
    ]
    for i, (row, kind) in enumerate(rows):
        y = ty + i * lead
        if kind == "hl":
            s.text(tx, y, row, s.font(MONO_BOLD, 17), RED, anchor="lm")
        elif kind == "dim":
            s.text(tx, y, row, dim, INK, anchor="lm")
        elif kind == "bar":
            s.text(tx, y, row, mono, INK, anchor="lm")
        else:
            s.text(tx, y, row, mono, INK, anchor="lm")
    s.ring_star(PW - 220, 220, 120, 50, ring_w=32)
    s.patrons(PW - 420, 420, r_big=16, r_small=11, gap=48)
    return s.finish()
