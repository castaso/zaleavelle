"""Measure the true ink bounding box of an SVG so its viewBox can be tightened.

The wordmark ships from Inkscape with a square canvas and the glyphs sitting
small in the middle, which renders it far too small in the nav. This renders
the file once through headless Edge and reports the pixel bounds of non-empty
content, so the viewBox can be re-cut to the artwork.

    python tools/svg-bounds.py assets/zaleavelle-mark.svg
"""

import os
import subprocess
import sys
import tempfile

from PIL import Image

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def edge():
    for path in EDGE_CANDIDATES:
        if os.path.exists(path):
            return path
    raise SystemExit("no Chromium browser found")


def main(svg_path, pad=2):
    svg = os.path.abspath(svg_path)
    size = 900
    page = ("<html><body style='margin:0;background:#fff'>"
            "<img src='file:///%s' style='width:%dpx;height:%dpx'>"
            "</body></html>" % (svg.replace("\\", "/"), size, size))

    with tempfile.TemporaryDirectory() as tmp:
        page_file = os.path.join(tmp, "p.html")
        shot = os.path.join(tmp, "p.png")
        with open(page_file, "w", encoding="utf-8") as fh:
            fh.write(page)
        subprocess.run(
            [edge(), "--headless=new", "--no-sandbox", "--disable-gpu",
             "--user-data-dir=" + os.path.join(tmp, "prof"),
             "--hide-scrollbars", "--virtual-time-budget=5000",
             "--window-size=%d,%d" % (size, size + 40),
             "--screenshot=" + shot, page_file],
            capture_output=True, timeout=120)

        im = Image.open(shot).convert("L").crop((0, 0, size, size))
        # Ink is anything darker than the white page behind it.
        mask = im.point(lambda v: 255 if v < 245 else 0)
        box = mask.getbbox()
        if not box:
            raise SystemExit("nothing rendered")

    left, top, right, bottom = box
    w, h = size, size
    frac_l, frac_t = left / w, top / h
    frac_r, frac_b = right / w, bottom / h
    pad_x = pad / w
    pad_y = pad / h

    print("rendered %dx%d" % (w, h))
    print("ink px   : left %d  top %d  right %d  bottom %d" % box)
    print("ink size : %dx%d px" % (right - left, bottom - top))
    print("viewBox  : %s" % (
        "%.4f %.4f %.4f %.4f" % (
            max(0.0, frac_l - pad_x),
            max(0.0, frac_t - pad_y),
            min(1.0, frac_r + pad_x),
            min(1.0, frac_b + pad_y))))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/zaleavelle-mark.svg")