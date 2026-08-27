#!/usr/bin/env python3
"""Numeric verification of the Red Wedge asset set.

The vision-quota path is unavailable this week, so this script proves the
visual contract geometrically:
  1. exact dimensions of every output;
  2. nine content-unique backgrounds;
  3. red/black/paper area ratios match the checker-of-anchors plan;
  4. every pair of 600x400 thumbnails differs strongly;
  5. targeted color probes (text sits on its intended field).
"""

import hashlib
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG = os.path.join(ROOT, "backgrounds")

SLUGS = ["sunburst", "starcog", "wedge", "banner", "target",
         "grid", "redfield", "manifesto", "macro"]

# Buckets: paper clan (bright), ink clan (dark), red clan.
PAPER_RGB = [(0xef, 0xe5, 0xd0), (0xe2, 0xd3, 0xb3)]
SLUGS = ["sunburst", "starcog", "wedge", "grid", "target",
         "banner", "redfield", "macro", "manifesto"]


INK_RGB = [(0x21, 0x1c, 0x18)]
RED_RGB = [(0xc3, 0x3d, 0x2e), (0xa0, 0x2f, 0x22)]


def nearest_clan(px):
    r, g, b = px[:3]
    best, clan = 1e9, None
    for c in PAPER_RGB:
        d = (r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2
        if d < best:
            best, clan = d, "paper"
    for c in INK_RGB:
        d = (r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2
        if d < best:
            best, clan = d, "ink"
    for c in RED_RGB:
        d = (r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2
        if d < best:
            best, clan = d, "red"
    return clan


def ratios(path, step=24):
    im = Image.open(path).convert("RGB")
    counts = {"paper": 0, "ink": 0, "red": 0}
    px = im.load()
    for y in range(0, im.height, step):
        for x in range(0, im.width, step):
            counts[nearest_clan(px[x, y])] += 1
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}


def probe(path, points):
    im = Image.open(path).convert("RGB")
    px = im.load()
    return {
        name: (nearest_clan(px[x, y]), want, nearest_clan(px[x, y]) == want)
        for name, (x, y), want in points
    }


def main():
    ok = True

    # 1. dimensions
    dims = {
        "backgrounds/red-wedge.png": (3840, 2160),
        "backgrounds.jpg": (1800, 1200),
        "preview.png": (1800, 1012),
        "preview-unlock.png": (1800, 1012),
        "unlock.png": (512, 512),
    }
    for i, slug in enumerate(SLUGS, start=1):
        dims[f"backgrounds/{i}-{slug}.jpg"] = (3840, 2560)
    for rel, want in dims.items():
        im = Image.open(os.path.join(ROOT, rel))
        good = im.size == want
        ok &= good
        print(f"{'OK ' if good else 'FAIL'} {rel} {im.size} (want {want})")

    # 2. uniqueness
    hashes = set()
    for i, slug in enumerate(SLUGS, start=1):
        p = os.path.join(BG, f"{i}-{slug}.jpg")
        hashes.add(hashlib.sha256(Image.open(p).tobytes()).hexdigest())
    good = len(hashes) == 9
    ok &= good
    plan = {
        "sunburst": (0.05, 0.03, 0.75),
        "starcog": (0.01, 0.50, 0.08),
        "wedge": (0.15, 0.03, 0.35),
        "grid": (0.01, 0.45, 0.05),
        "target": (0.06, 0.07, 0.35),
        "banner": (0.03, 0.25, 0.40),
        "redfield": (0.38, 0.10, 0.08),
        "macro": (0.10, 0.18, 0.05),
        "manifesto": (0.15, 0.015, 0.45),
    }
    print("poster       red    ink    paper")
    for i, slug in enumerate(SLUGS, start=1):
        r = ratios(os.path.join(BG, f"{i}-{slug}.jpg"))
        wr, wi, wp = plan[slug]
        good = r["red"] >= wr and r["ink"] >= wi and r["paper"] >= wp
        ok &= good
        print(f"{'OK ' if good else 'FAIL'}  {slug:10} "
              f"{r['red']:.2f}  {r['ink']:.2f}  {r['paper']:.2f}")

    # 4. pairwise thumbnail distinctness
    thumbs = []
    for i, slug in enumerate(SLUGS, start=1):
        im = Image.open(os.path.join(BG, f"{i}-{slug}.jpg")).convert("L")
        thumbs.append(im.resize((600, 400), Image.LANCZOS))
    worst, worst_pair = 1e9, None
    pairs = list(itertools.combinations(list(enumerate(thumbs)), 2))
    for (a, ta), (b, tb) in pairs:
        pa, pb = ta.load(), tb.load()
        diff = sum(abs(pa[x, y] - pb[x, y])
                   for y in range(0, 400, 4) for x in range(0, 600, 4))
        diff /= 150 * 100
        if diff < worst:
            worst, worst_pair = diff, (SLUGS[a], SLUGS[b])
    good = worst >= 15.0
    ok &= good
    print(f"{'OK ' if good else 'FAIL'} min pairwise thumb diff {worst:.1f}/255 "
          f"({worst_pair[0]} vs {worst_pair[1]})")

    # 5. targeted probes
    checks = [
        ("backgrounds/7-redfield.jpg", [
            ("band-left-of-text", (700, 875), "paper"),
            ("below-band-is-red", (1920, 1600), "red"),
            ("above-band-is-red", (1920, 60), "red"),
            ("ink-band", (600, 2300), "ink"),
        ]),
        ("backgrounds/3-wedge.jpg", [
            ("wedge-body", (700, 2300), "red"),
            ("paper-field", (3300, 600), "paper"),
        ]),
        ("backgrounds/4-grid.jpg", [
            ("dark-field", (2370, 100), "ink"),
            ("ring-star-cell", (570, 546), "red"),
            ("paper-cell", (300, 1900), "paper"),
        ]),
        ("backgrounds/5-target.jpg", [
            ("ink-band", (1920, 265), "ink"),
            ("red-band", (1920, 570), "red"),
            ("center-star", (1920, 1240), "red"),
        ]),
        ("backgrounds/2-starcog.jpg", [
            ("ink-field", (3300, 2100), "ink"),
            ("gear-body", (1180, 1700), "paper"),
        ]),
        ("backgrounds/8-macro.jpg", [
            ("ring-band-bottom", (1920, 2520), "ink"),
            ("star-core", (2100, 1100), "red"),
            ("wedge-slice", (300, 2400), "red"),
        ]),
        ("backgrounds/6-banner.jpg", [
            ("ink-panel", (100, 1500), "ink"),
            ("cream-field", (2000, 1500), "paper"),
        ]),
        ("backgrounds/1-sunburst.jpg", [
            ("sun-disc", (2560, 730), "red"),
            ("below-horizon", (2000, 1700), "paper"),
        ]),
        ("backgrounds/9-manifesto.jpg", [
            ("red-plate", (450, 2200), "red"),
            ("paper-right", (2000, 1800), "paper"),
        ]),
        ("preview.png", [
            ("top-bar", (600, 20), "paper"),
            ("editor-title-bar", (500, 88), "ink"),
            ("editor-body", (200, 300), "paper"),
        ]),
    ]
    for rel, points in checks:
        res = probe(os.path.join(ROOT, rel), points)
        for pname, (got, want, good) in res.items():
            ok &= good
            print(f"{'OK ' if good else 'FAIL'} {rel}:{pname} "
                  f"got {got} want {want}")

    print("VERIFY:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
