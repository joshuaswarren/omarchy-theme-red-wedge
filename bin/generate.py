#!/usr/bin/env python3
"""Render every Red Wedge asset. Deterministic: fixed seeds, no RNG elsewhere.

Outputs (repo-root relative):
  backgrounds/red-wedge.png   hero wallpaper, 3840x2160 (16:9)
  backgrounds/<n>-<slug>.jpg  nine uniform sources, 3840x2560 (3:2)
  backgrounds.jpg             3x3 contact sheet, exactly 1800x1200,
                              600x400 cells, edge-to-edge, no gutters/labels
  preview.png                 drawn desktop preview, exactly 1800x1012
  preview-unlock.png          drawn lock-screen preview, 1800x1012
  unlock.png                  512x512 RGBA lock glyph
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image
from preview import (build_preview, build_terminal, build_unlock_glyph,
                     build_unlock_preview)
from posters import POSTERS, poster_wedge
from rw import HERO_W, HERO_H, SRC_W, SRC_H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    bg_dir = os.path.join(ROOT, "backgrounds")
    os.makedirs(bg_dir, exist_ok=True)

    # Hero wallpaper, 16:9.
    hero = poster_wedge(HERO_W, HERO_H)
    hero_path = os.path.join(bg_dir, "red-wedge.png")
    hero.save(hero_path)
    print(f"saved {hero_path} {hero.size[0]}x{hero.size[1]}")

    # Nine uniform 3:2 sources.
    hashes = []
    for i, (slug, fn) in enumerate(POSTERS, start=1):
        img = fn()
        assert img.size == (SRC_W, SRC_H), f"{slug}: {img.size}"
        path = os.path.join(bg_dir, f"{i}-{slug}.jpg")
        img.save(path, "JPEG", quality=90, optimize=True)
        digest = hashlib.sha256(img.tobytes()).hexdigest()[:16]
        hashes.append(digest)
        print(f"saved {path} {img.size[0]}x{img.size[1]} sha256:{digest}")
    assert len(set(hashes)) == 9, "backgrounds are not content-unique"

    # Contact sheet: true 3x3, exact 1800x1200, 600x400 cells, no gutters.
    cell_w, cell_h = 600, 400
    sheet = Image.new("RGB", (3 * cell_w, 3 * cell_h))
    for i, (slug, _fn) in enumerate(POSTERS, start=1):
        src = Image.open(os.path.join(bg_dir, f"{i}-{slug}.jpg"))
        col, row = (i - 1) % 3, (i - 1) // 3
        sheet.paste(src.resize((cell_w, cell_h), Image.LANCZOS),
                    (col * cell_w, row * cell_h))
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
