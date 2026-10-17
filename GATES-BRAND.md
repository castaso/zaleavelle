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

- [x] B10: Scroll- and pointer-driven effects are transform-only
  CHECK: `python tools/check.py`
  EXPECT: zero layout-property writes; effects funnel through `--mx`, `--my`, `--py`
  EVIDENCE: 0 layout writes; `['--mx', '--my', '--py']`. Writing `top` or `height` per frame is the easiest way to turn an effect into jank and it is invisible to every other gate here, so it is asserted directly. `--py` is written through `pxWriter` rather than a literal `setProperty("--py", ...)`, so the gate collects both spellings

- [x] B10c: Reduced motion has exactly one switch
  CHECK: `python tools/check.py`
  EXPECT: a single `whenMotion` guard, with `.motion` added inside it
  EVIDENCE: `single whenMotion guard, .motion added inside it`. Every effect registers through `whenMotion`, so a new effect cannot forget the preference. Confirmed live rather than by inspection: with `prefers-reduced-motion: reduce`, `<html>` carries **no** `motion` class, the hero image has **no** `style` attribute and no `--py` was ever written, and the film section stays `class="scrub"` without `playing`

- [x] B12: Zero third-party JS, with a tripwire on the one exception
  CHECK: `python tools/check.py`
  EXPECT: no `<script src>`, and the conditional GA4 loader stays dormant
  EVIDENCE: no remote script tags; `ZV_GA_ID=''`. The page carries exactly one third-party loader, GA4, and it ships nothing while the ID is empty. B12b is the tripwire: if someone sets the ID, "zero third-party JS" stops being true and the claim has to be re-examined against the performance budget rather than discovered in a field audit

- [x] B14: Every image has non-empty alt text
  CHECK: `python tools/check.py`
  EXPECT: 0 of 13 images missing alt
  EVIDENCE: 0 of 13. **This gate failed on its first run against a phantom image.** A CSS comment names the tag in prose ("the width/height attributes on these `<img>`") and the scan counted it. Same false-positive class as the tilt regex and the JSON-LD Indonesian scan, third instance in this harness, so the scan now strips `<style>`/`<script>` first, exactly as B7 already did

- [x] B15: Every image declares explicit width and height
  CHECK: `python tools/check.py`
  EXPECT: 0 of 13 missing a dimension
  EVIDENCE: 0 of 13. This is the CLS guard behind goal G3, and it is the gate that would catch a new section shipping an unsized image

- [x] B16: Every film beat has a timing window
  CHECK: `python tools/check.py`
  EXPECT: beat count equals window count
  EVIDENCE: 4 beats, 4 windows. Under motion a beat with no window would sit at `opacity: 0` for the entire film, so the copy would be present in the DOM and invisible on screen. This is the only failure mode the Phase C markup introduces, and asserting the two counts against each other catches it

## The film narrative

- [x] The beats read three ways, and all three were checked
  CHECK: REA browser scenario, headless Chromium, 1440x900, motion allowed and `prefers-reduced-motion: reduce`
  EXPECT: sequenced under motion; all four visible as a list otherwise
  EVIDENCE: under motion, `--film-p: 0.581` and exactly one beat lit, at `opacity: 0.02` against the `beatAlpha(0.581, 0.58, 0.78)` prediction of 0.0227, with `translate3d(0px, 9.8px, 0px)` matching `(1 - 0.02) x 10`. Under reduced motion and with no JS, `.motion` is absent so the beats fall out of the overlay and flow as a plain centred list under the poster, all four visible. The copy is in the markup, not generated, so all three paths carry the same words. Zero page errors in both runs

- [x] The beats are measured against a worst case, not a sampled colour
  CHECK: `python tools/check.py`
  EXPECT: both beat pairs at or above 4.5:1
  EVIDENCE: line `#F2EEE6` on `#474747` = 8.03:1, label `#D8C9C1` on `#474747` = 5.77:1. `#474747` is 72% black over pure white, the brightest background the scrim can produce over any pixel of footage. **The scrim started at 66%, where `#D8C9C1` measured 4.49:1 and failed.** The label is 0.68rem, so it needs the full 4.5 and no large-text allowance; the scrim moved to 72% rather than the label moving to a new colour, because `#D8C9C1` is already the footer meta tone and inventing a near-duplicate for one label would be colour drift

- [x] B18b: The noscript block restores mobile navigation
  CHECK: `python tools/check.py`, plus a rendered no-JS capture at 390x844
  EXPECT: a max-width:1080px override in `<noscript>` that unhides the drawer, makes it static and hides the toggle
  EVIDENCE: override present, mutation-tested by moving it off the 1080px breakpoint. Below 1080px the drawer is the **only** navigation and it is opened by script, so without this a scriptless phone visitor had every word of the page and no way to move between sections. The override turns the drawer into a plain inline list and drops the sticky behaviour with it, because a 400px sticky header over a phone screen is worse than a header that scrolls away. Confirmed by screenshot at 390x844 with every script stripped: wordmark, all six links with rules, and the Shop now CTA all render above the film. The `[hidden]` override needs `!important` because the main sheet gives that attribute a `display: none` it must beat

## Film loading, verified

- [x] `filmPromote` reorders the queue when the reader outruns it
  CHECK: REA browser scenario at 390x844 against a probe that jumps to 90% of the pin on `DOMContentLoaded`
  EXPECT: the sheet holding the landed-on frame is fetched ahead of any earlier sheet that is still queued
  EVIDENCE: sheet request order came back **0, 1, 2, 3, 4, 6, 5, 7** — a genuine inversion, and without promotion the queue is strictly sequential so `6` before `5` can only come from `filmPromote`. The landed position was `--film-p: 0.859`, and `floor(0.859 x 192 / 24) = 6`, so sheet 6 was exactly the right sheet to promote. All 8 sheets still requested, none dropped, `#film` at `scrub playing`, zero page errors. **This closes a gap Phase G left open**, where all 8 sheets landed inside the initial 3s wait and the outrun path never executed. The first prediction written for this test expected `sheet-7` first and was simply wrong about which frame 90% lands on

## The filmstrip

- [x] The range is a native horizontal scroller, not a scroll-jacked one
  CHECK: REA browser scenario at 1440x900, plus live 390x844
  EXPECT: 5 items in order, the strip overflows and is keyboard reachable, zero page errors
  EVIDENCE: 5 `<article class="strip-item">` in order with `h3` reading Flavia Floral, Feminine Blush Pink, **Blaine Floral**, Bright Petal, Classic Pink; `lotion-blaine.avif` returned 200; heading live as "Five ways to start"; no `range-grid` or `class="tile` anywhere in the rendered DOM. Chosen over a scroll-jacked strip because scroll-snap needs no script, arrows and trackpads drive it natively, it is unaffected by `prefers-reduced-motion` because snapping is positioning rather than animation, and the scrollbar is styled thin and left **visible** rather than hidden behind a faked progress fill

- [x] B17: No more than two image+text splits in a row
  CHECK: `python tools/check.py`
  EXPECT: longest consecutive run of figure-plus-prose sections at or below 2
  EVIDENCE: longest run **1**, across 3 split sections (`hero`, `ritual`, `tentang`). **The Phase 18 plan claimed ritual and manifesto were consecutive splits and that one had to be rebuilt. That was wrong.** The ingredients band sits between them and carries no figure, so there was never a run of two to break, and rebuilding a section would have been churn against a remembered problem. The gate exists so the claim is measured rather than believed. The first version of the gate also under-counted, requiring a heading and missing the manifesto, which opens on a `<blockquote>` and has no `h2`; it now counts figure plus any prose. Mutation-tested by adding a figure to the ingredients band, which produced a run of 3 and failed

- [x] B17b: The filmstrip is a labelled focusable region
  CHECK: `python tools/check.py`
  EXPECT: `tabindex="0"`, `role` and `aria-label` all present
  EVIDENCE: `<div class="filmstrip" tabindex="0" role="region" aria-label="The range">`. A horizontal scroller that cannot be focused is unreachable from the keyboard, and its focus ring is the one thing here that has to read as a container rather than a control

## Robustness

- [x] B18: The noscript block restores `.reveal`
  CHECK: `python tools/check.py`
  EXPECT: a `.reveal` override setting `opacity: 1` inside `<noscript>`
  EVIDENCE: override present. **This gate exists because the page was blank without JavaScript.** Every `.reveal` element ships at `opacity: 0` and only script adds `.shown`, so a scriptless visitor got nothing. Measured at 1440x900 by stripping every script from a copy: **99.2% of pixels were background, header only.** After the fix, 74.0% background and 0.8% ink against 0.1% before, with the range heading, lede and product tiles all rendering. The `prefers-reduced-motion` query already rescued those visitors, which is why the gap survived from Phase 16 unnoticed. Mutation-tested: emptying the noscript block flips it to FAIL

- [x] The simulation itself was wrong first
  CHECK: first no-JS probe was rebuilt after producing byte-identical output
  EXPECT: a faithful stand-in for a scriptless browser
  EVIDENCE: the probe initially **deleted** the `<noscript>` block, but a browser with scripting off *applies* its contents. That tested something harsher than reality and made the fix look like a no-op, since the second capture came back at the same 206132 bytes. Rewritten to unwrap the block instead. Recorded because a test that silently simulates the wrong thing is worse than no test

## Craft

- [x] B19: Every interactive control declares a minimum hit area
  CHECK: `python tools/check.py`, plus rendered geometry measured at 390x844
  EXPECT: wall icons, footer CTA, wordmark and nav toggle at 44px; buttons and community links at 48px
  EVIDENCE: measured **before** the fix at 390x844, three controls failed: the channel wall social icons at **19x19**, the footer purchase link at **21.1px** tall and the wordmark at **20px** tall. All three are below WCAG 2.5.8 (24px) and PRD T12 (44px), and the footer link is a conversion control. After: wall icons **44x44**, footer link **44px**, wordmark **44px**. Icons and artwork were not enlarged; the hit area is grown with flex centring so the band reads the same. Mutation-tested by deleting the wall's `min-height` and confirming the gate flips to FAIL. The gate accepts `min-height` or `height` because the nav toggle correctly declares a fixed `height: 44px` and forcing `min-height` would have meant editing correct CSS to satisfy the test

- [x] B20: Body copy declares its own measure
  CHECK: `python tools/check.py`, plus computed `max-width` measured at 390x844 and 1440x900
  EXPECT: a `ch` measure on all six body-copy selectors
  EVIDENCE: `.lede` 56ch, `.steps p` 46ch, `.faq details p` 68ch, `.strip-item p` 34ch, `.manifesto .origin` 52ch, and `.ingredient-groups p` **44ch, added in Phase E** as the only paragraph that had been left to its grid column. Every measured paragraph reports `overflowsDeclared: false`. **A first pass at this audit wrongly flagged the lede and FAQ paragraphs at 77ch and 90ch.** That came from a rough `width / (font-size * 0.5)` approximation in the measurement script, not from the page. Re-measuring with computed `max-width` showed the CSS was correct throughout; the estimator was the thing that was wrong

- [x] B21: Exactly one film-grain layer
  CHECK: `python tools/check.py`
  EXPECT: exactly one `feTurbulence` in the stylesheet
  EVIDENCE: 1 found. The grain overlay was going to be added in Phase E and already exists from Phase 16: a fixed 140x140 SVG `feTurbulence` data-URI on `body::after` at `opacity: 0.035`, `z-index: 60`, measured live in Chromium. Phase E measured and kept it. This gate exists so the second one is never added on top of it

- [x] Every new gate was proven to fail before being trusted
  CHECK: mutate a copy of `index.html`, run the harness, restore, compare SHA-256
  EXPECT: each mutation flips its gate from PASS to FAIL
  EVIDENCE: B10 (layout write injected), B12b (`ZV_GA_ID` set to `G-ABC123`), B14 (`alt=""`) and B3 (scroll listener added) each failed as intended, and `index.html` restored to its original hash afterwards. A gate that has never been observed failing is an assumption wearing a gate's clothes

---

## Field performance

- [x] Field Lighthouse run, mobile and desktop (PRD G3, first ever on this page)
  CHECK: Lighthouse 13.5.0 over a local HTTP server, mobile emulation and the desktop preset
  EXPECT: performance ≥ 90, LCP < 2.5s, CLS < 0.1
  EVIDENCE: **mobile 93** (perf), a11y 96, best-practices 100, SEO 100; **desktop 100**, a11y 96, best-practices 100, SEO 100. **CLS 0.000 on both**, which is gate B15's `width`/`height` guard doing its job. **LCP 2.54s mobile, 0.61s desktop.** G3 is therefore met on score and CLS and missed on LCP by 40ms, recorded as a miss rather than rounded into a pass. The LCP breakdown puts the largest term at time-to-first-byte (411ms under emulated slow-4G) with resource load at 55ms, and discovery already optimal: `fetchpriority=high` applied, request discoverable in the initial document, not lazy-loaded. The LCP element is the film poster at 412x232, preloaded as 58 KB AVIF

- [x] B22, B22b, B22c: the sprite path stays queued and serialised
  CHECK: `python tools/check.py`
  EXPECT: a `filmQueued` queue, a `filmPump` serialisation guard, and an idle-scheduled pump with a timeout floor
  EVIDENCE: all three present, mutation-tested. Mobile scored **76 before** this shape and **93 after**, because requesting eight 2880x1080 sheets at once is 24.9 megapixels of decode and Lighthouse attributed ~1.6s of main-thread time to it against 0.16s on desktop. Verified live at 390px: all eight sheets fetched, each `request-finished` immediately preceding the next `request` so only one was ever in flight, `#film` reached `scrub playing`, canvas unhidden at 480x270, `--film-p: 0.747` with beat 3 at opacity 0.74, zero page errors. **Not exercised: `filmPromote`,** the outrun case, because all eight sheets landed inside the initial 3s wait before any scrolling

- [x] The largest cost was batching, not decoding
  CHECK: compare `mainthread-work-breakdown` before and after
  EXPECT: the diagnosis names a specific, fixable cost
  EVIDENCE: main-thread **total** barely moved, 2976ms → 2840ms, while total **blocking** time fell 679ms → 226ms and mobile performance rose 76 → 93. The decode work is irreducible; what was wrong was doing eight of them in one burst. Fixing the batching rather than the decoding is what bought the 17 points

- [x] One reported number is a test artefact and is not counted
  CHECK: read `cache-insight` against the test server's behaviour
  EXPECT: distinguish page defects from harness artefacts
  EVIDENCE: Lighthouse reported 2171 KiB of cacheable savings, all of it the sprite sheets. `python -m http.server` sends no cache headers, so that is the test rig and not the page; on a host setting long `Cache-Control` for `assets/web/**` it disappears. **The one real deployment requirement this phase surfaces: the sprite sheets need a long max-age.** They are 74% of the mobile payload and are immutable per build

---

## Regression guard

- [x] R1: The full harness passes
  CHECK: `python tools/check.py`
  EXPECT: `75 of 75 checks passed`
  EVIDENCE: 75 of 75 checks passed (42 after Phase A, 52 after B, 55 after C, 58 after D, 71 after E, 74 after G, 75 after the Phase G carry-over)

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