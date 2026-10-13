"""zaleavelle verification harness.

One command, every mechanical gate in one place:

    python tools/check.py

Exit code 0 means every check passed. Each check prints PASS or FAIL with the
measured value, so the output can be pasted straight into GATES-BRAND.md as
evidence. Nothing here needs a network connection or a browser.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
SHOP = "https://beli.zaleavelle.com/shop"

results = []


def check(gate, label, ok, detail):
    results.append((gate, ok))
    print("%s  %-6s %-52s %s" % ("PASS" if ok else "FAIL", gate, label, detail))


def count(pattern, text=None, flags=0):
    return len(re.findall(pattern, text if text is not None else HTML, flags))


# ---------------------------------------------------------------- storefront
check("S1", "shop URL references", HTML.count(SHOP) == 13, "13 = 7 offers + 6 CTAs, got %d" % HTML.count(SHOP))
check("S2", "shopee confined to JSON-LD sameAs", count("(?i)shopee") == 1, "1 occurrence")

# ---------------------------------------------------------------- structure
title = re.search(r"<title>([^<]*)</title>", HTML).group(1)
desc = re.search(r'<meta name="description" content="([^"]*)"', HTML).group(1)
check("S3", "title within 60 chars", len(title) <= 60, "%d chars" % len(title))
check("S3", "description within 155 chars", len(desc) <= 155, "%d chars" % len(desc))
check("S3", "canonical present", 'rel="canonical"' in HTML, "https://zaleavelle.com/")

ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S).group(1))
graph = ld["@graph"]
products = [n for n in graph if n["@type"] == "Product"]
check("S4", "JSON-LD parses, 9 nodes", len(graph) == 9, "%d nodes" % len(graph))
check("S4", "seven Products", len(products) == 7, "%d products" % len(products))
check("S4", "all offers on the shop host", all(p["offers"]["url"] == SHOP for p in products), "7 of 7")
check("S4", "no prices anywhere in schema", all("price" not in p["offers"] for p in products), "0 prices")

faq = [n for n in graph if n["@type"] == "FAQPage"][0]["mainEntity"]
visible = [(a.strip(), b.strip()) for a, b in re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", HTML, re.S)]
matched = sum(1 for q in faq if (q["name"], q["acceptedAnswer"]["text"]) in visible)
check("S6", "visible FAQ matches schema verbatim", matched == len(faq), "%d of %d" % (matched, len(faq)))

hrefs = {h for h in re.findall(r'href="(#[^"]*)"', HTML)}
ids = set(re.findall(r' id="([^"]*)"', HTML))
missing = sorted(h for h in hrefs if h.lstrip("#") not in ids)
check("S8", "every in-page anchor resolves", not missing, "missing: %s" % (missing or "none"))

scripts = re.findall(r"(?s)<script(?![^>]*application/ld\+json)(?![^>]*src=)[^>]*>(.*?)</script>", HTML)
check("S5", "inline script blocks present", len(scripts) == 2, "%d blocks" % len(scripts))

manifest = json.load(open(os.path.join(ROOT, "site.webmanifest"), encoding="utf-8"))
check("S7", "manifest parses as JSON", True, "name=%r" % manifest["name"])
# The page base is the opening film's dark ground, not alabaster: the film is
# the first paint (owner decision, 2026-10-13). The rest stays light.
check("S7", "manifest theme matches page base", manifest["theme_color"] == "#000000", manifest["theme_color"])
# ---------------------------------------------------------------- brand tells
em = count("\u2014") + count("\u2013")
check("B1", "zero em-dashes and en-dashes", em == 0, "%d found" % em)

emoji = re.findall(r"[\U0001F300-\U0001FAFF\u2190-\u21FF\u2705\u2733\u2734\u2726\u2739]", HTML)
check("B2", "zero emoji or dingbat glyphs", not emoji, "found: %s" % (emoji or "none"))

tells = {
    "scroll cue": r"(?i)>\s*(gulir|scroll to explore|scroll)\b",
    "overlay caption pill": r"promo-cap|class=\"sticker",
    # A tilt signature is a fractional rotation on a block. Whole-number
    # rotations on icons (the 45deg FAQ chevron) are functional and allowed.
    "decorative tilt": r"rotate\(\s*-?\d+\.\d+deg",
    "decorative status dot": r"promo-dot",
    "version stamp": r"(?i)v\d+\.\d+\.\d+|build \d+",
    "section numbering": r"\b0\d\s*&#183;|\b0\d\s*[|]",
    "scroll listener": r"addEventListener\([\"']scroll",
}
for label, pattern in tells.items():
    hits = count(pattern)
    check("B3", "no %s" % label, hits == 0, "%d found" % hits)

cta_labels = sorted({l.strip() for l in
                     re.findall(r'data-cta="odoo"[^>]*>([^<]*?)\s*<', HTML)})
check("B4", "one label for every shop CTA", len(cta_labels) == 1, "%s" % cta_labels)

wa_labels = sorted({l.strip() for l in
                    re.findall(r'data-cta="whatsapp"[^>]*>([^<]*?)\s*<', HTML)})
check("B4", "one label for every WhatsApp CTA", len(wa_labels) == 1, "%s" % wa_labels)

sections = count(r'<(?:section|footer|header)\b')
eyebrows = count(r'class="eyebrow"')
cap = -(-sections // 3)
check("B5", "eyebrow count within one per three sections", eyebrows <= cap,
      "%d eyebrows across %d regions, cap %d" % (eyebrows, sections, cap))

wordmark = open(os.path.join(ROOT, "assets", "zaleavelle-mark.svg"), encoding="utf-8").read()
check("B6", "wordmark carries no pure black", "#000000" not in wordmark, "espresso #5E4B43")

# Scan rendered text only. Schema URLs live inside <script>, where `[^<]*`
# would otherwise span the whole block and match "beli.zaleavelle.com".
VISIBLE = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", HTML)
leftovers = ["Belanja", "Ritual tiga", "Kulit sehat", "Pertanyaan", "Komunitas",
             "Tentang", "Kontak", "Jelajahi", "gulir", "Toko Resmi kami",
             "apakah", "beli", "dengan", "yang", "sedangkan"]
hits = [w for w in leftovers if re.search(r">[^<]*\b%s\b[^<]*<" % w, VISIBLE, re.I)]
check("B7", "no Indonesian copy left in rendered text", not hits, "found: %s" % (hits or "none"))

# ---------------------------------------------------------------- assets
missing_assets = [p for p in set(re.findall(r'(?:src|href)="((?:assets|favicon)[^"]*)"', HTML))
                  if not os.path.exists(os.path.join(ROOT, p))]
check("B8", "every referenced asset exists", not missing_assets, "missing: %s" % (missing_assets or "none"))

sizes = []
for m in re.finditer(r'src="assets/web/([^"]+)\.jpg"', HTML):
    path = os.path.join(ROOT, "assets", "web", m.group(1) + ".jpg")
    if os.path.exists(path):
        sizes.append(os.path.getsize(path))
check("B8", "page weight stays under the PRD budget", sum(sizes) < 2 * 1024 * 1024,
      "%d KB of JPEG across %d images" % (sum(sizes) // 1024, len(sizes)))

# The film's sprite sheets are referenced from JS strings, never from src or
# href attributes, so the scan above cannot see them. Verify them here.
scrub_paths = sorted(set(re.findall(r'"(assets/web/scrub/[^"]+)"', HTML)))
missing_scrub = [p for p in scrub_paths if not os.path.exists(os.path.join(ROOT, p))]
check("B8", "scrub sprite sheets referenced by JS exist",
      len(scrub_paths) == 8 and not missing_scrub,
      "%d sheets, missing: %s" % (len(scrub_paths), missing_scrub or "none"))

# ---------------------------------------------------------------- contrast
def luminance(hex_colour):
    c = hex_colour.lstrip("#")
    parts = [int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    parts = [p / 12.92 if p <= 0.03928 else ((p + 0.055) / 1.055) ** 2.4 for p in parts]
    return 0.2126 * parts[0] + 0.7152 * parts[1] + 0.0722 * parts[2]


def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


CONTRAST = [
    ("primary button", "#5E4B43", "#F6B78E", 4.5),
    ("body copy", "#5E4B43", "#F2EEE6", 4.5),
    ("secondary copy", "#6B5C53", "#F2EEE6", 4.5),
    ("secondary on petal", "#6B5C53", "#F7D6DA", 4.5),
    ("secondary on nude", "#6B5C53", "#FCE8D6", 4.5),
    ("body on sage", "#5E4B43", "#D7E0D1", 4.5),
    ("body on champagne", "#5E4B43", "#E6C9A3", 4.5),
    ("button hover", "#FFFFFF", "#B4601F", 4.5),
    ("footer body", "#F2EEE6", "#5E4B43", 4.5),
    ("footer meta", "#D8C9C1", "#5E4B43", 4.5),
    ("focus ring", "#B4601F", "#F2EEE6", 3.0),
]
for label, fg, bg, minimum in CONTRAST:
    r = ratio(fg, bg)
    check("B9", "contrast %s" % label, r >= minimum, "%s on %s = %.2f:1 (min %.1f)" % (fg, bg, r, minimum))

# ---------------------------------------------------------------- report
print("-" * 84)
failed = [g for g, ok in results if not ok]
print("%d of %d checks passed" % (len(results) - len(failed), len(results)))
sys.exit(1 if failed else 0)