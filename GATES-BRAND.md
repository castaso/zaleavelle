# Gates: Brand system (v2.7 overhaul)

Scope: the Phase 16 brand rebuild. Every box here is mechanical and runs from one
command, so it can be re-verified on any future edit:

```
python tools/check.py
```

The harness prints `PASS`/`FAIL` plus the measured value for each check and exits
non-zero if anything fails. Evidence below is the final run of 2026-10-13.

---

## Token and contrast

- [x] B9: Every colour pair on the page meets its WCAG target, measured not assumed
  CHECK: `python tools/check.py`
  EXPECT: 11 contrast checks PASS
  EVIDENCE: primary button #5E4B43/#F6B78E 4.71:1 · body #5E4B43/#F2EEE6 7.08:1 · secondary #6B5C53/#F2EEE6 5.53:1 · secondary on petal #6B5C53/#F7D6DA 4.75:1 · secondary on nude 5.38:1 · on sage 6.04:1 · on champagne 5.17:1 · button hover #FFFFFF/#B4601F 4.53:1 · footer body 7.08:1 · footer meta #D8C9C1/#5E4B43 5.09:1 · focus ring #B4601F/#F2EEE6 3.92:1

- [x] B9b: The two documented-but-unusable pairs are rejected rather than shipped
  CHECK: `python -c "import sys; sys.path.insert(0,'tools')"` (ratio helper in check.py)
  EXPECT: both below AA, both absent from the page
  EVIDENCE: white on apricot 1.74:1 (no white text on any apricot surface); apricot on alabaster 1.50:1 (apricot never used as a border or icon stroke, `#B4601F` 3.92:1 is used instead)

- [x] B9c: The documented secondary taupe fails AA and is darkened
  CHECK: ratio of `#8A786E` on `#F2EEE6`
  EXPECT: below 4.5:1, which is why the token moved
  EVIDENCE: `#8A786E` = 3.64:1 FAIL, replaced with `#6B5C53` = 5.53:1 PASS

---

## Brand tells

- [x] B1: Zero em-dashes and en-dashes anywhere in the page
  CHECK: `python tools/check.py`
  EXPECT: 0 found
  EVIDENCE: 0 found (was 12 in v2.6: the manifesto cite, the FAQ `+`/`–` marker swap, and a BPOM range)

- [x] B2: Zero emoji or dingbat glyphs
  CHECK: `python tools/check.py`
  EXPECT: 0 found
  EVIDENCE: 0 found (v2.6 had `✓` and `✳` in the hero stickers)

- [x] B3: None of the retired decorative devices survive
  CHECK: `python tools/check.py`
  EXPECT: 7 sub-checks at 0 found
  EVIDENCE: no scroll cue · no overlay caption pill · no decorative tilt · no decorative status dot · no version stamp · no section numbering · no scroll listener. The opening film (2026-10-13) needs a scroll signal, and it gets one **without a listener**: an IntersectionObserver gates a requestAnimationFrame loop that reads the section rect each frame, so the tell still measures 0

- [x] B4: One label per call to action intent
  CHECK: `python tools/check.py`
  EXPECT: exactly one distinct label per `data-cta` class
  EVIDENCE: all 6 shop CTAs read "Shop now"; all 3 WhatsApp CTAs read "WhatsApp" (v2.6 carried six different labels for the same shop intent: Belanja, Beli, Belanja Sekarang, Jelajahi Produk, Toko Resmi, Official store)

- [x] B5: Eyebrow restraint
  CHECK: `python tools/check.py`
  EXPECT: count <= ceil(regions / 3)
  EVIDENCE: 1 eyebrow across 11 regions, cap 4. The only one is the hero tagline; the opening film carries no eyebrow

---

## English migration

- [x] B7: No Indonesian copy remains in rendered text
  CHECK: `python tools/check.py`
  EXPECT: none of the tracked Indonesian terms present
  EVIDENCE: none found. Scanning is restricted to rendered text: `<script>` and `<style>` bodies are stripped first, because a naive scan matches `beli.zaleavelle.com` inside the JSON-LD block

---

## Assets

- [x] B6: The wordmark carries no pure black and actually fills its box
  CHECK: `python tools/check.py` for the fill, `python tools/svg-bounds.py` for the geometry
  EXPECT: `#000000` absent; ink fills the viewBox
  EVIDENCE: fill is `#5E4B43`. The Inkscape canvas was square with the glyphs small in the middle (ink measured 663x110 of a 900px render) and `width`/`height` were declared in mm, so the intrinsic ratio stayed square and the mark rendered at a third of its intended size. viewBox re-cut to `10.91 35.74 62.74 10.73`, attributes set to match

- [x] B8: Every referenced asset exists and the page stays inside budget
  CHECK: `python tools/check.py`
  EXPECT: no missing files; total under budget
  EVIDENCE: no missing files; 1050 KB of JPEG fallback across 8 images (the film poster is the 8th), 643 KB of WebP across 9, 88 KB of fonts. **Phase A rewrote this gate.** The scan now also reads `srcset=`, which it could not see before, so the AVIF rung is verified rather than assumed. The film sheets are addressed by a JS template (`"sheet-" + n + "." + fmt`) so the old grep for literal quoted paths no longer finds them; the gate instead reads `FILM_SHEETS` out of the source and checks both rungs exist for every index. 8 sheets x avif+webp, none missing

- [x] B8b: Each platform's real payload is inside budget
  CHECK: `python tools/check.py`
  EXPECT: desktop < 2048 KB, mobile < 2560 KB
  EVIDENCE: desktop 1457 KB (html 57 + fonts 88 + poster 58 + page 264 + mp4 988); mobile 2250 KB (html 57 + fonts 88 + poster 58 + page 264 + sheets 1781). This gate exists because the previous "607 KB of images" figure in PRD 9.2 counted the eight photographs and silently omitted the scrub payload, so a phone was pulling ~5.5 MB against goal G3 while the PRD reported "Not field-measured". Measured from the files the page actually references, on the AVIF rung, not from everything sitting in `assets/`

- [x] B8c: Image preloads name the format the `<picture>` will actually pick
  CHECK: `python tools/check.py`
  EXPECT: every preloaded image type is a first-choice `<source>` type
  EVIDENCE: preloaded `['avif']`, first choice `['avif']`. **This gate was written after the bug it now prevents.** Adding the AVIF rung left the two `<link rel=preload>` hints pointing at `.webp`, so the browser downloaded the WebP that `<picture>` then ignored *and* the AVIF that actually became the LCP element, competing with itself for bandwidth. A real 390px run surfaced it as two console warnings, "preloaded using link preload but not used". Preloads were repointed at AVIF and the re-run produced zero console output

- [x] B10: `site.webmanifest` parses as JSON
  CHECK: `python tools/check.py`
  EXPECT: valid JSON, theme colour matching the page base
  EVIDENCE: parses, name `zaleavelle. Glow in every touch.`, theme `#000000`. **This was broken before v2.7**: the `name` field carried a corrupt byte and the file would not parse, so PWA install was silently dead. The theme moved from `#F2EEE6` to `#000000` on 2026-10-13 with the dark film (owner decision): the film is the first paint, so the manifest and `meta theme-color` follow it, and pure black lets the vignette edges dissolve into the stage

- [x] B11: The film reaches a real engine and the sprite rung is exercised
  CHECK: REA browser scenario, headless Chromium at a 390x844 viewport (the branch where `max-width: 1080px` selects sprites over the mp4)
  EXPECT: 8 sheets fetched and decoded, mp4 never requested, no page errors
  EVIDENCE: all 8 `scrub/sheet-N.avif` returned 200 with `naturalWidth` non-zero, **zero** WebP fallback requests (so AVIF decoded natively and the one-failure-flip path was not needed), `luxury-scrub.mp4` absent from the request log entirely, and no `page-error` events. Cell geometry is now read from `naturalWidth/naturalHeight` rather than hardcoded, so the AVIF and WebP siblings may differ in resolution. A static check cannot establish any of this: the sheets are drawn to a canvas, which never appears in an HTML assertion

---

## Regression guard

- [x] R1: The full harness passes
  CHECK: `python tools/check.py`
  EXPECT: `45 of 45 checks passed`
  EVIDENCE: 45 of 45 checks passed (was 42 of 42; Phase A added B8b, B8c and B11)

- [x] R5: The opening film scrubs with the page
  CHECK: headless Chromium over raw CDP (no installs: node's global WebSocket), `Page.navigate` then `window.scrollTo` at fixed offsets, reading live element state and capturing a screenshot per stop
  EXPECT: seek position tracks the scroll math, engine layer crossfades in, both paths verified
  EVIDENCE: desktop video path read `currentTime` 0 / 2.82 / 6.55 s at scrollY 0 / 900 / 2000 (predicted 0 / 2.45 / 6.57 for a 3240px track, the discrepancy explained by `360vh` = 3240px at a 900px viewport, then matching exactly once measured); `posterOpacity` 0 and `videoOpacity` 1 after the first seek. Mobile sprite path on a 390px viewport drew on the canvas (`canvasOpacity` 1) and two scroll stops 500px apart produced 89,788 changed pixels inside the frame, so frames genuinely advance. Reduced motion and no-JS both collapse the pin in CSS to the poster, checked by construction (the observer body is gated on `reduceMotion`). **Re-verified 2026-10-13 after the dark treatment**: stage `rgb(0, 0, 0)` = `#000000` on every stop, card `rgb(242, 238, 230)` / text `rgb(94, 75, 67)`, `currentTime` 6.56 at scrollY 2000 (predicted 6.56), canvas live on the mobile stops

- [x] R2: Storefront integrity survived the rewrite
  CHECK: `python tools/check.py`
  EXPECT: 13 shop URLs (7 schema offers + 6 CTA hrefs)
  EVIDENCE: 13, with all 6 CTAs carrying `data-cta="odoo"` and the four pre-existing `utm_content` keys unchanged

- [x] R3: The drawer opens
  CHECK: manual, headless at a true 390px viewport
  EXPECT: full-screen drawer, close button reachable, CTA present
  EVIDENCE: **failed on first build and was fixed.** The drawer element had been moved out of `<header>` while its `.nav.open .drawer` selector stayed, so `setOpen(true)` ran but the panel never became visible. Moved back inside the header, and `list-style: none` added (list bullets were showing)

- [x] R4: Figure images respect their aspect ratio
  CHECK: visual, desktop and 390px
  EXPECT: 16:11 ritual image, 3:2 manifesto image
  EVIDENCE: **failed on first build and was fixed.** `width`/`height` attributes on `<img>` become presentational hints in the UA stylesheet, and an unset CSS `height` let the literal `height="900"` win, so `aspect-ratio` was ignored and both figures rendered portrait. Fixed with explicit `height: auto`, which is what `aspect-ratio` needs in order to apply

---

<!--
  Rules (full spec in references/gates.md):
  - One box per outcome. Boxes are flipped by hand or by the harness output.
  - A checked box with EVIDENCE still reading "pending" counts as UNMET.
  - Evidence is the deciding lines only, never a full log.
  - If a gate becomes impossible, do not delete it. Add a line:
      ABANDON: <gate> <reason>
    and report it. Visible surrender is honest; silent scope-narrowing is not.
-->