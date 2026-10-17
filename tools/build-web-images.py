"""One-off export pipeline: raw brand photography -> web-optimised assets.

Run once, outputs committed. No build step, no new dependencies (Pillow only).

    python tools/build-web-images.py

Crops are chosen to exclude baked-in Indonesian marketing copy baked into the
raw AI-generated creatives (badge grids, "CARA PAKAI:" panels, price stamps).
Product labels printed on the physical bottle are part of the product and stay.

Outputs AVIF + WebP + JPEG siblings so the page can serve <picture> in three
rungs. AVIF first: on this palette's soft, low-contrast photography it measured
roughly 25% smaller than WebP at equal perceived quality, and the poster pair in
build-scrub-assets.py came in at 58 KB AVIF against 78 KB WebP.

JPEG is retained as the final rung rather than dropped, because it is the only
one of the three that no engine lacks.
"""

import glob
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "web")

BL = sorted(glob.glob(os.path.join(ROOT, "assets/BODY LOTION/BLAINE FLORAL/*.png")))[4]
FB = sorted(glob.glob(os.path.join(ROOT, "assets/BODY LOTION/FEMININE BLUSH/*.png")))[0]
# Phase D. The right 56% of this frame is a full Indonesian marketing panel
# (display type, benefit icons, a Main Ingredients strip, social row, BPOM
# stamp). The left 44% is a standalone pump bottle on warm cream with yellow
# flowers and no baked text at all, which puts it on the champagne/nude tokens.
# This is the only fifth-variant shot recoverable from the existing files;
# Emerald Sweet and Fresh Tickled exist solely as off-palette blue and pink
# marketing frames. Verified at 0.47 (a dark object intrudes on the right edge)
# and at 0.42 (needlessly tight), so 0.44.
BLAINE_PRODUCT = os.path.join(ROOT, "assets/BODY LOTION/BLAINE FLORAL/Generated image 1 (3).png")

# Full-range collection shot, hand-picked by the owner, dropped in Downloads.
COLLECTION = os.path.expanduser("~/Downloads/Bodycare Collection with lighting.png")

# name, source, crop box as (left, top, right, bottom) fractions, output size, quality
# The hero is the LCP element, so it gets a tighter byte budget than the rest.
JOBS = [
    # Hero: full seven-product range. Never cropped tighter than this or a
    # bottle leaves frame, so the hero column is 4:3 rather than portrait.
    ("hero-collection", COLLECTION, (0.06, 0.00, 0.94, 1.00), (1240, 930), 74),
    ("wash-flavia", os.path.join(ROOT, "assets/BODY WASH/FLAVIA FLORAL/29.jpg"),
     (0.28, 0.10, 0.62, 0.95), (900, 1125), 82),
    ("lotion-blush", FB, (0.28, 0.00, 0.95, 0.95), (900, 1125), 82),
    ("serum-bright-petal", os.path.join(ROOT, "assets/BODY SERUM/BRIGHT PETAL/18.jpg"),
     # Re-cropped in Phase D. The original (0.20, 0.16, 0.96, 0.90) failed the
     # job this file exists to do: it kept a fragment of baked marketing display
     # type at the top left and a clipped banner along the bottom edge, on the
     # live site since Phase 16. Found by looking at the tile, which no gate can
     # do. These fractions clear both and keep the bottle, petals and gel.
     (0.30, 0.26, 0.96, 0.82), (900, 1125), 82),
    ("serum-classic-pink", os.path.join(ROOT, "assets/BODY SERUM/CLASSIC PINK/21.jpg"),
     (0.12, 0.12, 0.94, 0.86), (900, 1125), 82),
    # Phase D: fifth variant, cropped out of a marketing frame rather than a
    # product frame. See BLAINE_PRODUCT above for why this one is different.
    ("lotion-blaine", BLAINE_PRODUCT, (0.02, 0.02, 0.44, 0.98), (900, 1125), 82),
    # Ritual lifestyle. Every other candidate in assets/ is a marketing
    # infographic with Indonesian ingredient callouts printed into the frame,
    # which reads as noise next to a text column. This crop drops the baked
    # wordmark along the bottom edge and leaves a clean still life.
    ("ritual-cherry", os.path.join(ROOT, "assets/BODY SERUM/CLASSIC PINK/14.jpg"),
     (0.02, 0.02, 0.98, 0.88), (1600, 900), 78),
    # Gift-set still life. Same reason: the only other clean frame in the set.
    ("manifesto-petal", BL, (0.20, 0.02, 0.98, 0.92), (1200, 800), 80),
]


def crop_to(im, box, size):
    """Centre-crop `im` to the `box` fractions, then cover-fit onto `size`."""
    w, h = im.size
    im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    tw, th = size
    scale = max(tw / im.width, th / im.height)
    im = im.resize((max(tw, int(im.width * scale)), max(th, int(im.height * scale))),
                   Image.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


# The hero is the LCP element, so it gets a tighter byte budget than the rest.
# AVIF quality is not on the same scale as WebP's; these are tuned per format.
AVIF_Q = 50


def main():
    os.makedirs(OUT, exist_ok=True)
    total = {"avif": 0, "webp": 0, "jpg": 0}
    for name, src, box, size, q in JOBS:
        im = crop_to(Image.open(src).convert("RGB"), box, size)
        for ext, fmt, kwargs in (
            ("avif", "AVIF", {"quality": AVIF_Q, "speed": 6}),
            ("webp", "WEBP", {"quality": q, "method": 6}),
            ("jpg", "JPEG", {"quality": q + 4, "optimize": True, "progressive": True}),
        ):
            path = os.path.join(OUT, name + "." + ext)
            im.save(path, fmt, **kwargs)
            total[ext] += os.path.getsize(path)
        row = []
        for ext in ("jpg", "webp", "avif"):
            row.append("%s %3dKB" % (ext, os.path.getsize(os.path.join(OUT, name + "." + ext)) // 1024))
        print("%-24s %-10s %s" % (name, "x".join(map(str, size)), "  ".join(row)))
    print("-" * 62)
    print("payload total:  avif %d KB   webp %d KB   jpeg %d KB"
          % (total["avif"] // 1024, total["webp"] // 1024, total["jpg"] // 1024))


if __name__ == "__main__":
    main()