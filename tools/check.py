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
SHOP = "https://shop.zaleavelle.com"

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
                  | set(re.findall(r'srcset="((?:assets|favicon)[^"]*)"', HTML))
                  if not os.path.exists(os.path.join(ROOT, p))]
check("B8", "every referenced asset exists", not missing_assets, "missing: %s" % (missing_assets or "none"))

sizes = []
for m in re.finditer(r'src="assets/web/([^"]+)\.jpg"', HTML):
    path = os.path.join(ROOT, "assets", "web", m.group(1) + ".jpg")
    if os.path.exists(path):
        sizes.append(os.path.getsize(path))
check("B8", "page weight stays under the PRD budget", sum(sizes) < 2 * 1024 * 1024,
      "%d KB of JPEG across %d images" % (sum(sizes) // 1024, len(sizes)))

# The film's sheets are addressed by a template in JS ("sheet-" + n + "." + fmt),
# so a grep for literal quoted paths no longer finds them. The gate now reads the
# count out of the source and checks that both rungs exist on disk for every
# index, which is what the old grep was actually standing in for.
sheet_count = int(re.search(r"var FILM_SHEETS = (\d+);", HTML).group(1))
missing_scrub = ["sheet-%d.%s" % (n, f)
                 for n in range(sheet_count) for f in ("avif", "webp")
                 if not os.path.exists(os.path.join(ROOT, "assets", "web", "scrub",
                                                    "sheet-%d.%s" % (n, f)))]
check("B8", "scrub sheets exist in both rungs", sheet_count == 8 and not missing_scrub,
      "%d sheets x avif+webp, missing: %s" % (sheet_count, missing_scrub or "none"))

# ------------------------------------------------- per-platform payload (B8b)
# Phase A. The old figure in PRD 9.2 counted the eight page photographs and
# omitted the scrub payload, which is the largest thing a phone downloads. A
# mobile visitor was pulling ~5.5 MB against goal G3. These are the two real
# totals, measured from the files the page actually references, on the AVIF rung.
def total(paths):
    return sum(os.path.getsize(p) for p in paths if os.path.exists(p))


html_bytes = len(HTML.encode("utf-8"))
fonts = total([os.path.join(ROOT, "assets", "fonts", f)
               for f in os.listdir(os.path.join(ROOT, "assets", "fonts"))
               if f.endswith(".woff2")])
# Referenced rungs only: unused exports sitting on disk are not page weight.
avif_refs = sorted(set(re.findall(r'srcset="(assets/web/[^"]+\.avif)"', HTML)))
poster = total([os.path.join(ROOT, p) for p in avif_refs if "poster" in p])
pageimg = total([os.path.join(ROOT, p) for p in avif_refs if "poster" not in p])
mp4 = total([os.path.join(ROOT, "assets", "web", "luxury-scrub.mp4")])
sheets = total([os.path.join(ROOT, "assets", "web", "scrub", f)
                for f in os.listdir(os.path.join(ROOT, "assets", "web", "scrub"))
                if f.endswith(".avif")])

desktop = html_bytes + fonts + poster + pageimg + mp4
mobile = html_bytes + fonts + poster + pageimg + sheets
for label, value, cap in (("desktop", desktop, 2.0 * 1024 * 1024),
                          ("mobile", mobile, 2.5 * 1024 * 1024)):
    check("B8b", "%s payload within budget" % label, value < cap,
          "%d KB (html %d + fonts %d + poster %d + page %d + %s) cap %d KB"
          % (value // 1024, html_bytes // 1024, fonts // 1024, poster // 1024,
             pageimg // 1024, "mp4 %d" % (mp4 // 1024) if label == "desktop"
             else "sheets %d" % (sheets // 1024), int(cap) // 1024))

# A preload must name the format the <picture> will actually pick. Getting this
# wrong is not cosmetic: preloading the WebP while the sources prefer AVIF made
# the LCP element download twice and compete with itself for bandwidth, which
# Chrome reported as "preloaded but not used". Caught in a real 390px run.
first_choice = set()
for pic in re.findall(r"<picture>(.*?)</picture>", HTML, re.S):
    t = re.search(r'<source[^>]*type="image/([a-z0-9+]+)"', pic)
    if t:
        first_choice.add(t.group(1))
preloaded = set(re.findall(r'<link rel="preload"[^>]*as="image"[^>]*type="image/([a-z0-9+]+)"', HTML))
check("B8c", "image preloads target the first-choice format",
      preloaded and preloaded <= first_choice,
      "preloaded %s, first choice %s" % (sorted(preloaded), sorted(first_choice)))

# ------------------------------------------------- motion and JS hygiene (B10, B12)
JS = "\n".join(re.findall(
    r"(?s)<script(?![^>]*application/ld\+json)(?![^>]*src=)[^>]*>(.*?)</script>", HTML))

# Scroll- and pointer-driven effects must not write layout properties. A
# transform-only effect is composited without a reflow; writing `top` or
# `height` per frame is the single easiest way to turn an effect into jank, and
# it is invisible to every other gate on this page.
layout_writes = re.findall(
    r"\.style\.(top|left|right|bottom|width|height|margin|marginTop|marginLeft|"
    r"marginRight|marginBottom|padding|paddingTop)\s*=", JS)
check("B10", "scroll and pointer effects write transform only",
      not layout_writes, "%d layout writes: %s"
      % (len(layout_writes), sorted(set(layout_writes)) or "none"))

# The effects that do exist must funnel through custom properties, so the
# compositor-friendly path is the only one available by construction. One of
# them (--py) is written through pxWriter, so both spellings are collected.
fx_props = set(re.findall(r'setProperty\("(--[a-z0-9-]+)"', JS))
fx_props |= set(re.findall(r'pxWriter\([^,]+,\s*"(--[a-z0-9-]+)"', JS))
fx_props |= set(re.findall(r'numWriter\([^,]+,\s*"(--[a-z0-9-]+)"', JS))
check("B10b", "effects drive declared custom properties only",
      fx_props and fx_props <= {"--mx", "--my", "--py", "--film-p"},
      "%s" % sorted(fx_props))

# A beat added to the markup without a matching timing window would sit at
# opacity 0 for the whole film under motion, so the two counts are asserted
# against each other rather than trusted to stay in step.
beats = len(re.findall(r'<p class="film-beat">', HTML))
windows = len(re.findall(r"\[\s*0?\.\d+\s*,\s*0?\.\d+\s*\]", JS))
check("B16", "every film beat has a timing window", beats and beats == windows,
      "%d beats, %d windows" % (beats, windows))

# Reduced motion has exactly one switch, and the script must add the .motion
# class inside that guard rather than beside it.
check("B10c", "motion class is gated on the reduced-motion switch",
      'if (reduceMotion) return;' in JS
      and re.search(r"function whenMotion\(fn\) \{\s*if \(reduceMotion\) return;\s*"
                    r"document\.documentElement\.classList\.add\(\"motion\"\);\s*fn\(\);",
                    JS) is not None,
      "single whenMotion guard, .motion added inside it")

# Zero third-party JS. No script tag may load a remote origin.
remote_scripts = re.findall(r'<script[^>]+src="([^"]+)"', HTML)
check("B12", "no script tag loads a remote origin", not remote_scripts,
      "found: %s" % (remote_scripts or "none"))

# The page carries one conditional third-party loader, GA4, and it ships
# nothing while the ID is empty. This gate is the tripwire: if someone sets the
# ID, "zero third-party JS" stops being true and the claim has to be revisited
# against the performance budget rather than discovered in a field audit.
ga = re.search(r'window\.ZV_GA_ID\s*=\s*"([^"]*)"', JS)
check("B12b", "conditional GA4 loader is dormant",
      ga is not None and ga.group(1) == "",
      "ZV_GA_ID=%r" % (ga.group(1) if ga else "not found"))

# ------------------------------------------------- image hygiene (B14, B15)
# Scan rendered markup only. A CSS comment that names the tag in prose ("the
# width/height attributes on these <img>") is not an element, and treating it as
# one is the third instance of this exact false positive in this harness.
MARKUP = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", HTML)
imgs = re.findall(r"<img\b[^>]*>", MARKUP)
bad_alt = [i for i in imgs if not re.search(r'alt="[^"]+"', i)]
check("B14", "every image has non-empty alt text", not bad_alt,
      "%d of %d images missing alt" % (len(bad_alt), len(imgs)))

# Explicit intrinsic size on every image is the CLS guard (PRD G3).
missing_dims = [i for i in imgs if not re.search(r'width="\d+', i)
                or not re.search(r'height="\d+', i)]
check("B15", "every image declares width and height", not missing_dims,
      "%d of %d images missing a dimension" % (len(missing_dims), len(imgs)))

# ------------------------------------------------- layout family (B17)
# Measured rather than remembered. The Phase 18 plan asserted that the ritual
# and manifesto sections were consecutive image+text splits and that one of them
# had to be rebuilt. That was wrong: the ingredients band sits between them and
# carries no figure, so there is no run of two to break.
#
# "Split" means a section carrying a figure alongside real text. The first
# version of this gate also required a heading and under-counted, because the
# manifesto opens with a blockquote and has no h2 at all. Counting figure plus
# any prose is the definition that actually matches how the page reads.
split_flags, labels = [], []
for attrs, inner in re.findall(r"<section\b([^>]*)>(.*?)</section>", MARKUP, re.S):
    sid = re.search(r'id="([^"]+)"', attrs)
    labels.append(sid.group(1) if sid else "hero")
    has_figure = "<figure" in inner
    has_prose = re.search(r"<(h[1-3]|p|blockquote|ol|ul)\b", inner) is not None
    split_flags.append(has_figure and has_prose)

longest = run = 0
for flag in split_flags:
    run = run + 1 if flag else 0
    longest = max(longest, run)
splits = [labels[i] for i, f in enumerate(split_flags) if f]

check("B17", "no more than two image+text splits in a row", longest <= 2,
      "longest run %d; %d split sections at %s" % (longest, len(splits), splits))

# The strip is a focusable scroll region, which only works if it can actually be
# focused and labelled. Asserted rather than eyeballed.
strip = re.search(r'<div class="filmstrip"[^>]*>', HTML)
check("B17b", "filmstrip is a labelled focusable region",
      strip is not None and 'tabindex="0"' in strip.group(0)
      and "role=" in strip.group(0) and "aria-label=" in strip.group(0),
      strip.group(0) if strip else "no .filmstrip found")

# The noscript block is the only thing between a scriptless visitor and a blank
# page. Every .reveal element ships at opacity 0 and only script makes it visible,
# so a missing override here does not degrade the page, it empties it. Measured
# before the Phase D fix: 99.2% background pixels, header only.
noscript = re.search(r"(?s)<noscript>(.*?)</noscript>", HTML)
check("B18", "noscript restores reveal visibility",
      noscript is not None
      and re.search(r"\.reveal\s*\{[^}]*opacity:\s*1", noscript.group(1)) is not None,
      "reveal override present"
      if noscript and ".reveal" in noscript.group(1)
      else "MISSING: scriptless visitors see an empty page")

# B18 covers the content. This covers the navigation: below 1080px the drawer is
# the only nav and it is opened by script, so without an override a scriptless
# phone visitor had every word of the page and no way to move between sections.
if noscript:
    ns = noscript.group(1)
    mobile_nav = re.search(r"@media\s*\(max-width:\s*1080px\)\s*\{(.*?)\}\s*\}", ns, re.S)
    nav_block = mobile_nav.group(1) if mobile_nav else ""
    check("B18b", "noscript restores mobile navigation",
          bool(nav_block) and ".drawer" in nav_block and "position: static" in nav_block
          and "nav-toggle" in nav_block,
          "drawer becomes an inline list and the toggle is hidden"
          if ".drawer" in nav_block else "MISSING: scriptless phone has no navigation")
else:
    check("B18b", "noscript restores mobile navigation", False, "no noscript block")

# ------------------------------------------------- craft (B19, B20, B21)
# The stylesheet on its own. MARKUP deliberately strips <style> so the image
# scan cannot match prose in a comment, which makes it the wrong input for gates
# that assert CSS declarations. Using MARKUP here made all thirteen of the first
# draft of these checks report "none found", including min-height on .btn, which
# has existed since Phase 16.
CSS = "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", HTML, re.S))

# Tap targets. CSS declarations are not the same as rendered geometry, and only
# one of the two is what a finger meets, so the declarations are asserted here
# and the rendered numbers were measured in a browser at 390x844. Three
# controls failed that measurement before this gate existed: the social icons in
# the channel wall (19x19), the footer purchase link (21.1px tall) and the
# wordmark (20px tall).
# Either property is acceptable, because what matters is the rendered box. The
# nav toggle declares a fixed `height: 44px` and measured 44x44; insisting on
# `min-height` would have forced a pointless edit to correct CSS.
TAP_TARGETS = [
    ("channel wall icon", r"\.wall-logos a\s*\{[^}]*(?:min-)?height:\s*(\d+)px", 44),
    ("footer purchase link", r"\.foot-meta a\s*\{[^}]*(?:min-)?height:\s*(\d+)px", 44),
    ("wordmark", r"\.wordmark\s*\{[^}]*(?:min-)?height:\s*(\d+)px", 44),
    ("nav toggle", r"\.nav-toggle\s*\{[^}]*(?:min-)?height:\s*(\d+)px", 44),
    ("button", r"\.btn\s*\{[^}]*(?:min-)?height:\s*(\d+)px", 48),
    ("community link", r"\.social a\s*\{[^}]*(?:min-)?height:\s*(\d+)px", 48),
]
for label, pat, floor in TAP_TARGETS:
    m = re.search(pat, CSS)
    ok = m is not None and int(m.group(1)) >= floor
    check("B19", "%s declares a %dpx hit area" % (label, floor), ok,
          "%s px declared" % (m.group(1) if m else "none"))

# Body copy must declare its own measure. Left to the container, a paragraph
# takes whatever width the grid gives it, and the comfortable reading range is
# roughly 45-75 characters.
BODY_COPY = [".lede", ".steps p", ".faq details p", ".ingredient-groups p",
             ".strip-item p", ".manifesto .origin"]
for sel in BODY_COPY:
    m = re.search(re.escape(sel) + r"\s*\{[^}]*max-width:\s*(\d+)ch", CSS)
    check("B20", "%s declares a measure" % sel, m is not None,
          "%sch" % (m.group(1) if m else "none"))

# The film-grain layer already exists from Phase 16 (a fixed 140x140
# feTurbulence data-URI on body::after at 0.035). Phase E measured it and kept
# it rather than adding a second, so this asserts there is exactly one.
grain = len(re.findall(r"feTurbulence", CSS))
check("B21", "exactly one film-grain layer", grain == 1, "%d found" % grain)

# ------------------------------------------------- film loading (B22)
# The sprite path used to request all eight sheets at once. Each is 2880x1080,
# so that is 24.9 megapixels of decode and it cost 679ms of blocking time on a
# throttled phone (mobile Lighthouse 76). These assert the loader is still
# queued and serialised, which is the shape that fixes it.
check("B22", "sprite sheets load through a queue",
      "var filmQueued" in JS and "function filmPump" in JS,
      "queue present" if "filmQueued" in JS else "MISSING: sheets will burst again")
check("B22b", "only one sheet is in flight at a time",
      "if (filmPending > 0 || !filmQueued.length) return;" in JS,
      "filmPump is serialised")
check("B22c", "the next pump waits for an idle slot",
      "requestIdleCallback" in JS and "timeout: 400" in JS,
      "idle-scheduled with a 400ms floor so the queue cannot stall")

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
    # Phase C film beats. These sit on moving footage, not a known colour, so
    # they are measured against a deliberate worst case rather than a sampled
    # one: #474747 is 72% black over pure white, which is the brightest
    # background the beat scrim can possibly produce. The graded footage is far
    # darker than this, so the real margin is larger than the measured one.
    # The scrim started at 66%, where #D8C9C1 measured 4.49:1 and failed; the
    # label is 0.68rem, so it needs the full 4.5 and the scrim moved instead.
    ("film beat line on worst-case scrim", "#F2EEE6", "#474747", 4.5),
    ("film beat label on worst-case scrim", "#D8C9C1", "#474747", 4.5),
]
for label, fg, bg, minimum in CONTRAST:
    r = ratio(fg, bg)
    check("B9", "contrast %s" % label, r >= minimum, "%s on %s = %.2f:1 (min %.1f)" % (fg, bg, r, minimum))

# ---------------------------------------------------------------- report
print("-" * 84)
failed = [g for g, ok in results if not ok]
print("%d of %d checks passed" % (len(results) - len(failed), len(results)))
sys.exit(1 if failed else 0)