"""One-off export pipeline: raw brand photography -> web-optimised assets.

Run once, outputs committed. No build step, no new dependencies (Pillow only).

    python tools/build-web-images.py

Crops are chosen to exclude baked-in Indonesian marketing copy baked into the
raw AI-generated creatives (badge grids, "CARA PAKAI:" panels, price stamps).
Product labels printed on the physical bottle are part of the product and stay.

Outputs WebP + JPEG siblings so the page can serve <picture>.
"""

import glob
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "web")

BL = sorted(glob.glob(os.path.join(ROOT, "assets/BODY LOTION/BLAINE FLORAL/*.png")))[4]
FB = sorted(glob.glob(os.path.join(ROOT, "assets/BODY LOTION/FEMININE BLUSH/*.png")))[0]

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
     (0.20, 0.16, 0.96, 0.90), (900, 1125), 82),
    ("serum-classic-pink", os.path.join(ROOT, "assets/BODY SERUM/CLASSIC PINK/21.jpg"),
     (0.12, 0.12, 0.94, 0.86), (900, 1125), 82),
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


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, src, box, size, q in JOBS:
        im = crop_to(Image.open(src).convert("RGB"), box, size)
        jpg = os.path.join(OUT, name + ".jpg")
        webp = os.path.join(OUT, name + ".webp")
        im.save(jpg, "JPEG", quality=q + 4, optimize=True, progressive=True)
        im.save(webp, "WEBP", quality=q, method=6)
        j = os.path.getsize(jpg) // 1024
        w = os.path.getsize(webp) // 1024
        total += w
        print("%-24s %-10s jpg %3dKB  webp %3dKB" % (name, "x".join(map(str, size)), j, w))
    print("-" * 46)
    print("webp payload total: %d KB" % total)


if __name__ == "__main__":
    main()