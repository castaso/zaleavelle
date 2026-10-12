"""One-off: vendor Cormorant Garamond + Geist as latin-subset woff2.

Run once, outputs committed. Fetches only the `latin` subset blocks from the
Google Fonts CSS API (unicode-range 0000-00FF) so the page carries roughly
130KB of self-hosted type instead of a third-party stylesheet.

    python tools/vendor-fonts.py
"""

import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "fonts")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")

FAMILIES = [
    ("Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400", "cormorant-garamond"),
    ("Geist:wght@300;400;500", "geist"),
]

# Only the plain latin block. latin-ext pulls ~8KB extra for four accents the
# English page never renders.
LATIN = "U+0000-00FF"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def latin_blocks(css):
    """Yield (style, src) for every @font-face whose unicode-range is exactly
    the latin subset. Both families ship as variable fonts, so every weight
    resolves to the same file and is deduplicated by the caller."""
    out = []
    for block in re.findall(r"@font-face\s*\{[^}]*\}", css):
        ur = re.search(r"unicode-range:\s*([^;]+);", block)
        if not ur or LATIN not in ur.group(1):
            continue
        style = re.search(r"font-style:\s*(\w+);", block).group(1)
        src = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
        out.append((style, src))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    for query, slug in FAMILIES:
        css = fetch("https://fonts.googleapis.com/css2?family=%s&display=swap" % query).decode()
        seen = set()
        for style, url in latin_blocks(css):
            name = "%s%s.woff2" % (slug, "-italic" if style == "italic" else "")
            if name in seen:
                continue
            seen.add(name)
            with open(os.path.join(OUT, name), "wb") as fh:
                fh.write(fetch(url))
            print("%-32s %3d KB" % (name, os.path.getsize(os.path.join(OUT, name)) // 1024))


if __name__ == "__main__":
    main()