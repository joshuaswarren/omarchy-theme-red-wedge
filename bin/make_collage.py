#!/usr/bin/env python3
"""Compose a 3x2 collage of the 9 era-poster variants into backgrounds.jpg.

Matches the layout dhh uses in omarchy-diablo-dreams-theme: thin dark gutter,
no captions, full-bleed cells, 3 columns x 2 rows, 1800x1200 total.
"""

import glob
from PIL import Image

COLS = 3
ROWS = 2
CELL_W = 600
CELL_H = 600
GUTTER = 2
OUT_W = COLS * CELL_W + (COLS - 1) * GUTTER
OUT_H = ROWS * CELL_H + (ROWS - 1) * GUTTER


def main():
    files = sorted(glob.glob("backgrounds/[1-9]-*.jpg"))
    assert len(files) == 9, f"expected 9 variant jpgs, got {len(files)}: {files}"
    bg = (10, 10, 10)
    canvas = Image.new("RGB", (OUT_W, OUT_H), bg)
    for idx, path in enumerate(files):
        col, row = divmod(idx, COLS)
        im = Image.open(path).convert("RGB")
        resized = im.resize((CELL_W, CELL_H), Image.LANCZOS)
        x0 = col * (CELL_W + GUTTER)
        y0 = row * (CELL_H + GUTTER)
        canvas.paste(resized, (x0, y0))
    canvas.save("backgrounds.jpg", "JPEG", quality=88, optimize=True)
    print(f"saved backgrounds.jpg ({OUT_W}x{OUT_H})")


if __name__ == "__main__":
    main()
