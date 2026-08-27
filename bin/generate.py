#!/usr/bin/env python3
"""Render every Red Wedge asset. Deterministic: fixed seeds, no RNG elsewhere.

Outputs (repo-root relative):
  backgrounds/red-wedge.png   hero wallpaper, 3840x2160 (16:9)
  backgrounds/<n>-<slug>.jpg  nine native-16:9 sources, 3840x2160
  backgrounds.jpg             3x3 contact sheet, exactly 1800x1200,
                              600x400 cells, each a whole-image 600x338
                              letterbox with a 31px top/bottom matte
  preview.png                 drawn desktop preview, exactly 1800x1012
  preview-unlock.png          drawn lock-screen preview, 1800x1012
  unlock.png                  512x512 RGBA lock glyph

Native-16:9 repair (2026-08-27): the hero and the nine posters share one
canvas size now (see rw.SRC_W/SRC_H), so the hero is just the "wedge"
poster rendered once and saved to two paths -- no second render, no
aspect mismatch for Quickshell's PreserveAspectCrop to clip.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image
from preview import (build_preview, build_terminal, build_unlock_glyph,
                     build_unlock_preview)
from posters import POSTERS
from rw import PAPER

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CELL_W, CELL_H = 600, 400
LETTERBOX_H = 338  # round(CELL_W * SRC_H / SRC_W); 31px matte top+bottom
MATTE = PAPER


def letterbox_cell(img):
    """Whole 16:9 image, resized to fill 600x338, centered in a 600x400
    cell with a matte bar top and bottom. Never crops."""
    cell = Image.new("RGB", (CELL_W, CELL_H), MATTE)
    fit = img.resize((CELL_W, LETTERBOX_H), Image.LANCZOS)
    cell.paste(fit, (0, (CELL_H - LETTERBOX_H) // 2))
    return cell


def main():
    bg_dir = os.path.join(ROOT, "backgrounds")
    os.makedirs(bg_dir, exist_ok=True)

    # Nine native-16:9 sources, one render each; "wedge" doubles as the hero.
    hero = None
    hashes = []
    for i, (slug, fn) in enumerate(POSTERS, start=1):
        img = fn()
        path = os.path.join(bg_dir, f"{i}-{slug}.jpg")
        img.save(path, "JPEG", quality=90, optimize=True)
        digest = hashlib.sha256(img.tobytes()).hexdigest()[:16]
        hashes.append(digest)
        print(f"saved {path} {img.size[0]}x{img.size[1]} sha256:{digest}")
        if slug == "wedge":
            hero = img
    assert len(set(hashes)) == 9, "backgrounds are not content-unique"
    assert hero is not None, "wedge poster missing, cannot derive hero"

    hero_path = os.path.join(bg_dir, "red-wedge.png")
    hero.save(hero_path)
    print(f"saved {hero_path} {hero.size[0]}x{hero.size[1]}")

    # Contact sheet: true 3x3, exact 1800x1200, each cell a whole-image
    # letterbox (no crop) -- native 16:9 source into a 600x400 cell.
    sheet = Image.new("RGB", (3 * CELL_W, 3 * CELL_H))
    for i, (slug, _fn) in enumerate(POSTERS, start=1):
        src = Image.open(os.path.join(bg_dir, f"{i}-{slug}.jpg"))
        col, row = (i - 1) % 3, (i - 1) // 3
        sheet.paste(letterbox_cell(src), (col * CELL_W, row * CELL_H))
    assert sheet.size == (1800, 1200)
    sheet.save(os.path.join(ROOT, "backgrounds.jpg"), "JPEG", quality=90,
               optimize=True)
    print(f"saved backgrounds.jpg {sheet.size[0]}x{sheet.size[1]}")

    # Previews and lock glyph.
    pv = build_preview(hero)
    assert pv.size == (1800, 1012)
    pv.save(os.path.join(ROOT, "preview.png"))
    print(f"saved preview.png {pv.size[0]}x{pv.size[1]}")

    ul = build_unlock_preview(hero)
    ul.save(os.path.join(ROOT, "preview-unlock.png"))
    print(f"saved preview-unlock.png {ul.size[0]}x{ul.size[1]}")

    term = build_terminal()
    assert term.size == (1800, 1012)
    term.save(os.path.join(ROOT, "preview-terminal.png"))
    print(f"saved preview-terminal.png {term.size[0]}x{term.size[1]}")

    glyph = build_unlock_glyph()
    glyph.save(os.path.join(ROOT, "unlock.png"))
    print(f"saved unlock.png {glyph.size[0]}x{glyph.size[1]}")


if __name__ == "__main__":
    main()
