"""One-off export pipeline: the opening film -> scrubbing web assets.

Run once, outputs committed. No build step. Needs ffmpeg on PATH and Pillow.

    python tools/build-scrub-assets.py

The page scrubs one source clip in two ways:

  - desktop: a single h264 mp4 seeks to video.currentTime as the page scrolls,
    so the encode carries a keyframe every 12 frames (0.5s) to keep seeks cheap.
  - mobile: the 192 frames composed into eight WebP sprite sheets, drawn onto
    a <canvas>, because seeking a <video> on mobile is visibly janky.

The poster is frame 0 exactly, at the same scale as the sprite cells, so the
first scrub frame never pops when the engine takes over.

The dark grade (owner decision, 2026-10-13) is one filter applied to every
export, so poster, frames and video cannot drift apart. It is subtle on
purpose: the seven products carry the pink, yellow and green story, and a
heavier pull flattens them into the bokeh.

Byte budgets are asserted, not suggested: the script fails if any output is
over, so bloat cannot ship silently.
"""

import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.expanduser("~/Downloads/luxury.mp4")
OUT_WEB = os.path.join(ROOT, "assets", "web")
OUT_SCRUB = os.path.join(OUT_WEB, "scrub")

CELL_W, CELL_H = 640, 360
COLS, ROWS = 6, 4
CELLS = COLS * ROWS  # 24 frames per sheet
FRAMES = 192

GRADE = "eq=brightness=-0.04:contrast=1.05:gamma=0.9:saturation=0.94"

POSTER_BUDGET = 260 * 1024
MP4_BUDGET = 3.5 * 1024 * 1024
SHEET_BUDGET = 6.5 * 1024 * 1024


def run(cmd):
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    if not os.path.exists(SOURCE):
        raise SystemExit("missing source: %s" % SOURCE)
    os.makedirs(OUT_SCRUB, exist_ok=True)
    over = []

    with tempfile.TemporaryDirectory() as tmp:
        # Poster: frame 0 at full 1280x720, JPEG + WebP so the page can use
        # <picture>. This is the first paint and the LCP element.
        poster_png = os.path.join(tmp, "poster.png")
        run(["ffmpeg", "-v", "error", "-i", SOURCE, "-vf", GRADE,
             "-frames:v", "1", poster_png, "-y"])
        poster = Image.open(poster_png).convert("RGB")
        jpg = os.path.join(OUT_WEB, "luxury-poster.jpg")
        webp = os.path.join(OUT_WEB, "luxury-poster.webp")
        poster.save(jpg, "JPEG", quality=76, optimize=True, progressive=True)
        poster.save(webp, "WEBP", quality=78, method=6)
        j, w = os.path.getsize(jpg), os.path.getsize(webp)
        if j > POSTER_BUDGET:
            over.append("poster jpg")
        print("%-20s %-10s jpg %3dKB  webp %3dKB" % (
            "luxury-poster", "x".join(map(str, poster.size)), j // 1024, w // 1024))

        # Frames for the sprite sheets, scaled once here rather than per sheet.
        frames_dir = os.path.join(tmp, "frames")
        os.makedirs(frames_dir)
        run(["ffmpeg", "-v", "error", "-i", SOURCE,
             "-vf", GRADE + ",scale=%d:%d:flags=lanczos" % (CELL_W, CELL_H),
             os.path.join(frames_dir, "f-%03d.png")])
        names = sorted(os.listdir(frames_dir))
        if len(names) != FRAMES:
            raise SystemExit("expected %d frames, dumped %d" % (FRAMES, len(names)))

        sheets = -(-FRAMES // CELLS)  # 8
        total = 0
        for s in range(sheets):
            sheet = Image.new("RGB", (COLS * CELL_W, ROWS * CELL_H))
            for c in range(CELLS):
                idx = s * CELLS + c
                if idx >= FRAMES:
                    break
                cell = Image.open(os.path.join(frames_dir, names[idx])).convert("RGB")
                sheet.paste(cell, ((c % COLS) * CELL_W, (c // COLS) * CELL_H))
            path = os.path.join(OUT_SCRUB, "sheet-%d.webp" % s)
            sheet.save(path, "WEBP", quality=70, method=6)
            size = os.path.getsize(path)
            total += size
            print("%-20s %dx%d  %3dKB" % (
                "scrub/sheet-%d.webp" % s, sheet.width, sheet.height, size // 1024))
        if total > SHEET_BUDGET:
            over.append("sprite sheets")
        print("-" * 46)
        print("sprite payload total : %d KB" % (total // 1024))

    # Desktop video: a 12-frame GOP so every seek lands near a keyframe.
    mp4 = os.path.join(OUT_WEB, "luxury-scrub.mp4")
    run(["ffmpeg", "-v", "error", "-i", SOURCE, "-vf", GRADE,
         "-c:v", "libx264", "-crf", "26", "-preset", "slow",
         "-g", "12", "-keyint_min", "12", "-sc_threshold", "0",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", mp4, "-y"])
    size = os.path.getsize(mp4)
    if size > MP4_BUDGET:
        over.append("desktop mp4")
    print("%-20s %3dKB" % ("luxury-scrub.mp4", size // 1024))
    print("-" * 46)
    print("source clip          : %3dKB  (1280x720, 24fps, 8s, 192 frames)" % (
        os.path.getsize(SOURCE) // 1024))

    if over:
        raise SystemExit("over budget: " + ", ".join(over))


if __name__ == "__main__":
    main()
