"""One-off export pipeline: the opening film -> scrubbing web assets.

Run once, outputs committed. No build step. Needs ffmpeg on PATH and Pillow.

The page scrubs one source clip in two ways:

  - desktop: a single h264 mp4 seeks to video.currentTime as the page scrolls,
    so the encode carries a keyframe every 12 frames (0.5s) to keep seeks cheap.
  - mobile: the 192 frames composed into eight sprite sheets, drawn onto a
    <canvas>, because seeking a <video> on mobile is visibly janky.

Sheets ship as AVIF with a WebP sibling. AVIF measured smaller *and* faster
than WebP on this footage, because a graded, soft, bokeh-heavy clip is exactly
the content AVIF's transform handles well. Both formats are written so the
sprite payload works on engines without AVIF.

Cell geometry is derived from the loaded image's own natural size on the page
side, not hardcoded, so the two formats are free to differ in resolution.

The poster is frame 0 exactly, so the first scrub frame never pops when the
engine takes over. The poster is the LCP element and therefore carries the
tightest budget.

The dark grade (owner decision, 2026-10-13) is one filter applied to every
export, so poster, frames and video cannot drift apart. It is subtle on
purpose: the seven products carry the pink, yellow and green story, and a
heavier pull flattens them into the bokeh.

Byte budgets are asserted, not suggested: the script fails if any output is
over, so bloat cannot ship silently. The mobile budget was tightened in Phase A
from 6.5 MB to 2.0 MB after the shipped sheets were measured at 4.86 MB, which
contradicted PRD goal G3 (mobile Lighthouse >= 90).
"""

import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.expanduser("~/Downloads/luxury.mp4")
OUT_WEB = os.path.join(ROOT, "assets", "web")
OUT_SCRUB = os.path.join(OUT_WEB, "scrub")

# Cells were 640x360 through Phase 17. 480x270 is 0.5625x the pixels, which is
# where the mobile payload stopped being the largest thing a phone downloads.
# On a 390px-wide viewport a 480px cell is still ~1.2x CSS pixels, so the film
# stays sharp enough on a phone while the sprite total drops below 2 MB.
CELL_W, CELL_H = 480, 270
COLS, ROWS = 6, 4
CELLS = COLS * ROWS  # 24 frames per sheet
FRAMES = 192

GRADE = "eq=brightness=-0.04:contrast=1.05:gamma=0.9:saturation=0.94"

POSTER_BUDGET = 260 * 1024
MP4_BUDGET = 1.5 * 1024 * 1024

# Phase A: measured, not guessed, and measured across all eight sheets rather
# than the first one. An early benchmark encoded sheet 0 alone and predicted
# 1936 KB; the full run came in at 2171 KB, because the clip gets busier and the
# sheets grow monotonically (242 KB -> 309 KB). Sampling the cheapest sheet
# underestimates by ~12%.
#
# The knob chosen was quality rather than cell size. On a graded, soft clip,
# banding is more objectionable than slight softness, and the bottles need to
# read. q40 still measures SSIM 0.9963 / PSNR 36.4 dB against the uncompressed
# sheet. The WebP sibling is the non-AVIF fallback and is allowed a looser
# ceiling because a modern engine never downloads it.
SHEET_AVIF_Q = 40
SHEET_WEBP_Q = 50
SHEET_AVIF_BUDGET = 2.0 * 1024 * 1024
SHEET_WEBP_BUDGET = 2.5 * 1024 * 1024

# The desktop clip is only ever decoded by a browser with a real video pipeline,
# and it is never scrubbed per-frame on a phone, so 960x540 at crf 30 is well
# inside perceptual tolerance for a graded soft clip.
MP4_W, MP4_H = 960, 540
MP4_CRF = 30


def run(cmd):
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, check=True)


def kb(path):
    return os.path.getsize(path) // 1024


def main():
    if not os.path.exists(SOURCE):
        raise SystemExit("missing source: %s" % SOURCE)
    os.makedirs(OUT_SCRUB, exist_ok=True)
    over = []

    with tempfile.TemporaryDirectory() as tmp:
        # Poster: frame 0 at full 1280x720. JPEG + AVIF + WebP so the page can
        # use <picture>. This is the first paint and the LCP element.
        poster_png = os.path.join(tmp, "poster.png")
        run(["ffmpeg", "-v", "error", "-i", SOURCE, "-vf", GRADE,
             "-frames:v", "1", poster_png, "-y"])
        poster = Image.open(poster_png).convert("RGB")
        jpg = os.path.join(OUT_WEB, "luxury-poster.jpg")
        webp = os.path.join(OUT_WEB, "luxury-poster.webp")
        avif = os.path.join(OUT_WEB, "luxury-poster.avif")
        poster.save(jpg, "JPEG", quality=76, optimize=True, progressive=True)
        poster.save(webp, "WEBP", quality=78, method=6)
        poster.save(avif, "AVIF", quality=52, speed=6)
        if os.path.getsize(jpg) > POSTER_BUDGET:
            over.append("poster jpg")
        print("%-22s %-10s jpg %3dKB  webp %3dKB  avif %3dKB" % (
            "luxury-poster", "x".join(map(str, poster.size)), kb(jpg), kb(webp), kb(avif)))

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
        avif_total = 0
        webp_total = 0
        for s in range(sheets):
            sheet = Image.new("RGB", (COLS * CELL_W, ROWS * CELL_H))
            for c in range(CELLS):
                idx = s * CELLS + c
                if idx >= FRAMES:
                    break
                cell = Image.open(os.path.join(frames_dir, names[idx])).convert("RGB")
                sheet.paste(cell, ((c % COLS) * CELL_W, (c // COLS) * CELL_H))
            apath = os.path.join(OUT_SCRUB, "sheet-%d.avif" % s)
            wpath = os.path.join(OUT_SCRUB, "sheet-%d.webp" % s)
            sheet.save(apath, "AVIF", quality=SHEET_AVIF_Q, speed=6)
            sheet.save(wpath, "WEBP", quality=SHEET_WEBP_Q, method=6)
            avif_total += os.path.getsize(apath)
            webp_total += os.path.getsize(wpath)
            print("%-22s %dx%d  avif %3dKB  webp %3dKB" % (
                "scrub/sheet-%d" % s, sheet.width, sheet.height, kb(apath), kb(wpath)))
        if avif_total > SHEET_AVIF_BUDGET:
            over.append("sprite sheets (avif)")
        if webp_total > SHEET_WEBP_BUDGET:
            over.append("sprite sheets (webp fallback)")
        print("-" * 56)
        print("sprite payload  avif %d KB   webp fallback %d KB"
              % (avif_total // 1024, webp_total // 1024))

    # Desktop video: a 12-frame GOP so every seek lands near a keyframe.
    mp4 = os.path.join(OUT_WEB, "luxury-scrub.mp4")
    run(["ffmpeg", "-v", "error", "-i", SOURCE, "-vf",
         GRADE + ",scale=%d:%d:flags=lanczos" % (MP4_W, MP4_H),
         "-c:v", "libx264", "-crf", str(MP4_CRF), "-preset", "slow",
         "-g", "12", "-keyint_min", "12", "-sc_threshold", "0",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", mp4, "-y"])
    if os.path.getsize(mp4) > MP4_BUDGET:
        over.append("desktop mp4")
    print("%-22s %3dKB  (%dx%d crf %d)"
          % ("luxury-scrub.mp4", kb(mp4), MP4_W, MP4_H, MP4_CRF))
    print("-" * 56)
    print("source clip          : %3dKB  (1280x720, 24fps, 8s, 192 frames)"
          % kb(SOURCE))

    if over:
        raise SystemExit("over budget: " + ", ".join(over))
    print("all budgets asserted and met")


if __name__ == "__main__":
    main()