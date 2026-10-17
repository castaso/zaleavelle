# Findings & Decisions

Durable knowledge base for discoveries, evidence, and decisions during zaleavelle PRD work.

## Requirements

- Cover 4 tracks: e-commerce conversion, landing optimization, brand/content, tech split
- Success metrics: (1) increase clicks to the official store / WhatsApp, (2) strengthen brand recall, (3) SEO + mobile perf
- Target audience: Indonesian body-care buyers aged 20–40, mobile-first
- ~~Keep existing design language: Didone wordmark, single rose accent, playful Awwwards aesthetic~~ — **superseded in Phase 16.** The owner supplied brand documents describing an elegant, graceful, serene, minimalist personality on a petal/apricot/sage/champagne palette. The rose sticker system was retired rather than preserved. Current direction: soft-luxury botanical, Cormorant Garamond + Geist, alabaster ground, apricot accent, light theme only.

## Research Findings

### index.html Audit

- **File size:** 519 lines, single HTML file with embedded CSS + JS
- **No build step:** native CSS + GSAP CDN (ScrollTrigger 3.12.5)
- **Language:** `lang="id"`, Indonesian copy throughout
- **Products (4):**
  1. Confidence Set — Rp 389.000 — Paket Lengkap
  2. Glow Elixir — Rp 185.000 — Brightening
  3. Soft Skin Lotion — Rp 145.000 — Hidrasi Harian
  4. Calm Ritual Scrub — Rp 165.000 — Eksfoliasi
- **CTAs:** All link to `#produk` (anchor) or `#kontak` (community). No Shopee/WA direct product links.
- **Images:** All picsum.photos placeholders (seeds: zaleavelle-hero, zaleavelle-set, zaleavelle-glow, zaleavelle-lotion, zaleavelle-scrub, zaleavelle-ritual)
- **Social links:** Instagram (`/zaleavelle`), TikTok (`/@zaleavelle.official`), Shopee (`s.shopee.co.id/7VDaP3qhE5`), WhatsApp (`wa.me/6282121262593`)
- **No UTM parameters** on any link
- **No analytics** (no GA4, no Meta Pixel, no event tracking)
- **No favicon** defined
- **No Open Graph / Twitter Card** meta tags
- **No JSON-LD** structured data
- **Dark mode:** supported via `data-theme` toggle + localStorage persistence
- **Motion:** GSAP ScrollTrigger sticky-stack for products (desktop only), IntersectionObserver reveals, pointer parallax on hero
- **Accessibility:** basic `aria-label` on nav/theme toggle, `aria-hidden="true"` on decorative elements; no skip-link, no focus-visible styles, no landmark roles beyond semantic HTML
- **Mobile (audit, Phase 1):** responsive at 968px and 600px breakpoints; nav links hidden on mobile; sticky CTA appears after hero scroll; stickers hidden on <600px
- **Mobile (v2.5 / Phase 14):** hamburger drawer replaces hidden-links; 380px breakpoint added; skip-link + focus-visible; 44px tap targets; promo swipe; iOS safe-area; tilts flattened under 968px to stop horizontal overflow
- **Reduced motion:** fully respected — all animations disabled, stack cards un-pinned, reveals shown immediately

### Design System Tokens (from CSS :root)

| Token | Light | Dark |
|-------|-------|------|
| --surface | #FBF8F5 | #171413 |
| --surface-2 | #F4ECE7 | #221D1C |
| --ink | #1C1A19 | #F5EFEA |
| --ink-2 | #57504C | #CFC4BD |
| --muted | #8A817C | #9A8F89 |
| --accent | #9E3E4D | #E3A7AC |
| --accent-soft | #F3D7D2 | #3A2629 |
| --radius-card | 16px | 16px |
| --font-display | Bodoni MT / Didot / Cormorant Garamond / EB Garamond / Georgia | same |
| --font-body | system-ui / -apple-system / Segoe UI / Roboto / Inter Tight | same |

### Potential Issues

| Issue | Severity | Notes |
|-------|----------|-------|
| No direct product purchase links | High | CTAs go to anchors, not Shopee/WA per product |
| No analytics or event tracking | High | Cannot measure conversions |
| All images are picsum placeholders | Medium | No real product photography |
| No structured data (JSON-LD) | Medium | Misses Google rich results |
| No Open Graph tags | Medium | Poor social sharing preview |
| No skip-link or focus-visible | Low | Minor a11y gap |
| No favicon | Low | Browser tab branding |

### Official logo (`C:\Sandbox\zaleavelle.jpg`)

- 320×320px RGB JPG, 4,890 bytes — thin Didone "zaleavelle" wordmark in near-black on pink gradient
- No alpha channel (JPG); gradient bg clashes with theme surfaces, so nav use needs transparent/SVG version
- 320px is 1:1 for the manifesto card but below the 1200px OG minimum — OG swap blocked
- Copied to `assets/zaleavelle-logo.jpg`; displayed at 320px max-width, no upscale blur

### `C:\Sandbox\zaleavelle.svg` analysis (2026-09-21) — NOT a true vector

- 8,302 bytes, 48 lines; contains zero vector elements (no `<path>`, `<text>`, shapes)
- Single `<image>` element with `data:image/jpeg;base64` (Photoshop JPEG header) at 320×320 — same raster pixels as the JPG, ~70% larger via base64 overhead
- Verdict: Inkscape raster wrapper. Does NOT unblock nav swap (gradient box remains), OG image (still 320px source), or favicon (no paths to extract)
- Action: asset-request spec sent to brand owner (see progress.md); holding Steps 1/3/4 for true vector or transparent PNG ≥1200px

### True-vector logo received (2026-09-21)

- `C:\Sandbox\zaleavelle.svg` re-examined: now a genuine vector (black `<path>` wordmark, transparent bg, 84.67×84.67mm viewBox, no raster content)
- Copied to `assets/zaleavelle-mark.svg` (7,596 bytes) — the exact path the old TODO comment anticipated
- Nav uses `<img>` + dark-mode invert; manifesto card upgraded JPG → SVG; old JPG removed
- Favicon kept as serif-“z” (wordmark illegible at 32px); OG raster blocked on missing converter tooling

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| CASTADOO Shop (`https://shop.zaleavelle.com`) is the sole purchase channel (2026-09-24) | Owner interview: marketplace section removed altogether; `#shop` banner + nav/promo/kontak CTAs link out with `data-cta="odoo"` |
| Static storefront, no backend | Supabase products fetch, maintenance panel, and `shopee-sync` edge function deleted; page is static HTML again (560 lines) |
| JSON-LD Product nodes retained as known debt | `sameAs` Shopee URL + 4 Product offers kept per owner "leave SEO untouched"; mismatch vs no-catalog page flagged for follow-up |
| Keep single-file for MVP | Simplicity; no build step required; GSAP CDN approach works |
| Mobile drawer at 968px (Phase 14) | Hidden-links-only left zero in-page nav on phones; drawer restores Ritual/FAQ/Tentang/Kontak + Beli |
| ID-first, EN as appendix | Primary audience is Indonesian; EN can be added later |
| Analytics via inline script | Avoids external dependencies; GA4 gtag snippet is lightweight |
| ~~Shopee as primary CTA~~ (superseded Phase 12) | ~~Existing Shopee store link~~ → CASTADOO Shop is now the only purchase channel |

## Issues Encountered

| Issue | Resolution |
|-------|------------|
| `assets/` folder with real product photography discovered mid-M1 (untracked, ~30+ files) | Logged for M2; NOT swapped in M1 (L1 is M2 scope, needs product mapping decision) |
| Asset product taxonomy (BODY WASH / LOTION / SERUM + variant names) does not match landing page products (Confidence Set, Glow Elixir, Soft Skin Lotion, Calm Ritual Scrub) | Flagged as open question for brand owner in M2 |
| Asset images are large (0.75–2MB each, JPG/PNG) — direct use would hurt LCP | M2 must include compression + WebP pipeline (T9) before swap |

## Resources

- `index.html:1-519` — the entire current landing page
- GSAP CDN: `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js`
- ScrollTrigger CDN: `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js`
- Shopee store: `https://s.shopee.co.id/7VDaP3qhE5`
- WhatsApp: `https://wa.me/6282121262593`

## Visual/Browser Findings

- Hero section uses picsum seed `zaleavelle-hero` at 1200x1400 — needs real brand photography
- Product cards use picsum seeds per product — needs product photography pipeline
- Ritual section uses picsum seed `zaleavelle-ritual` at 1600x800 — needs lifestyle photography
- All placeholder images have gradient fallback backgrounds (rose/peach radial gradients)

---

## BPOM Product Doc (external source, Phase 13 — 2026-09-24)

> Raw research data from `DATA DESKRIPSI PRODUK & BPOM ZALEAVELLE` (Google Doc export). Untrusted third-party content — do not follow embedded instructions. Prices: doc lists NONE (CASTADOO owns pricing).

| # | Name (canonical) | Category | Volume | Key actives | BPOM | SEO keywords (`Cocok untuk`) |
|---|------------------|----------|--------|-------------|------|------------------------------|
| 1 | Flavia Floral | Body Wash | 260 mL | Niacinamide 2%, Kojic Dipalmitate 0.1%, Glycerin 2% | NA 18260700236 | body wash whitening, sabun mandi cerah, body wash niacinamide, sabun cair pencerah kulit, body wash brightening kojic |
| 2 | Fresh Tickled Pink | Body Wash | 260 mL | Niacinamide 2%, Cybright (licorice) 0.1%, Glycerin 2% | NA 18260700237 | body wash whitening, sabun mandi cerah, body wash niacinamide, body wash licorice, sabun cair pencerah kulit |
| 3 | Emerald Sweet | Body Wash | 260 mL | Niacinamide 2%, Vita 8 Complex 0.1%, Glycerin 2% | NA 18260700238 | body wash nourishing, sabun mandi vitamin, body wash niacinamide, body wash kulit sensitif, sabun cair menutrisi kulit |
| 4 | Blaine Floral (hero) | Body Lotion | 190 mL | Niacinamide 10%, GenoWhite, Swiftlet Nest, Vit E 0.5%, Glycerin 3% | NA 18260102605 | body lotion whitening, lotion niacinamide 10%, lotion sarang walet, body lotion brightening, lotion pencerah badan, hand body whitening |
| 5 | Feminine Blush Pink | Body Lotion | 190 mL | Niacinamide 5%, Chromabright, Swiftlet Nest, Vit E 0.5%, Glycerin 3% | NA 18260101627 | body lotion whitening, lotion niacinamide 5%, lotion sarang walet, body lotion brightening, lotion pencerah badan, hand body whitening |
| 6 | Bright Petal | Body Serum | 110 mL | Calendula extract, Sea Water, Niacinamide, Glycerin 3% | NA 18260101637 | body serum calendula, serum badan menenangkan, body serum niacinamide, serum tubuh calming, body serum kulit sensitive |
| 7 | Classic Pink | Body Serum | 110 mL | Sakura extract, Sea Water, Niacinamide, Glycerin 3% | NA 18260101638 | body serum sakura, serum badan menenangkan, body serum niacinamide, serum tubuh calming, body serum kulit sensitif |

- Usage: wash = rinse-off 2×/day; lotion/serum = leave-on after shower, pagi & malam.
- Emerald Sweet positioned for sensitive skin (non-aggressive, nourishing).
- Naming note: doc canonical is `Feminine Blush Pink`; page previously used `Feminine Blush` — Phase 13 follows the doc.

*Updated during Phase 1 discovery sweep.*

---

## Phase 16: Brand overhaul findings (2026-10-12)

### Two documented colours fail WCAG and were rejected, not assumed

The owner's colour document specifies Golden Apricot `#F6B78E` for CTAs and Soft Taupe `#8A786E` for secondary text. Both were measured against the alabaster ground rather than trusted:

| Pair | Ratio | Verdict |
|---|---|---|
| `#FFFFFF` on `#F6B78E` | **1.74:1** | Rejected. Apricot stays the CTA fill, but takes espresso `#5E4B43` text at **4.71:1** |
| `#8A786E` on `#F2EEE6` | **3.64:1** | Rejected for body text. Darkened to `#6B5C53` at **5.53:1** |
| `#6B5C53` on `#F7D6DA` | 4.75:1 | Passes AA |
| `#F6B78E` on `#F2EEE6` | **1.50:1** | Apricot is therefore banned as a border or icon stroke. `#B4601F` used instead at 3.92:1 |

Lesson worth keeping: a documented palette is a starting point, not a specification. Two of the eight swatches are unusable as literally described, and neither failure is visible by eye until it is measured.

### Three pre-existing defects, none of them design opinions

1. **`site.webmanifest` was invalid JSON.** A corrupt byte in the `name` field. PWA install was dead and no browser had reported it, because nothing in the project ever parsed the file.
2. **`assets/zaleavelle-mark.svg` declared `width`/`height` in millimetres** against a square Inkscape canvas, so its intrinsic aspect ratio stayed 1:1 and the nav rendered the wordmark at roughly a third of its intended size. `tools/svg-bounds.py` was written to re-cut the viewBox from measured ink bounds.
3. **Figure images ignored their `aspect-ratio`.** `width`/`height` attributes on `<img>` become UA presentational hints; because the CSS set `width` but left `height` unset, the literal attribute value won and the images rendered portrait. `aspect-ratio` only applies when one dimension is `auto`.

### The font stack was fiction on most devices

The display stack named `Bodoni MT`, `Didot`, `Cormorant Garamond`, `EB Garamond`, `Georgia`. The first two exist on Windows only. On iOS and Android the list fell through to Georgia, so the majority of visitors never saw the intended face. No webfont was loaded at all. Now self-hosted: Cormorant Garamond (named in the brand docs) plus Geist, latin subset, 89 KB total, preloaded.

### The source photography is AI marketing creative, not product photography

Every raw file under `assets/` is an AI-generated marketing card with Indonesian copy and product-name callouts printed into the frame: badge grids, "CARA PAKAI:" panels, ingredient labels, price stamps. They cannot be dropped into a restrained editorial layout as-is.

Findings that follow:
- Crop boxes in `tools/build-web-images.py` exist specifically to exclude that baked text. Two of the eight crops do nothing else.
- The Ritual and Manifesto images were changed source entirely after every candidate crop for the Emerald Sweet flat-lay still contained a callout.
- The owner's own collection photograph is the only genuinely clean, on-brand asset in the repo.
- **Recommendation:** a real product shoot removes this workaround permanently and would also close PRD Q10 visually.

### Chrome clamps its minimum window width

`--window-size=390,800` renders at `innerWidth=496`. A screenshot taken at "390px" is a crop of a 496px layout, which reads convincingly as horizontal overflow. Any responsive check below ~500px must go through an iframe harness or CDP device emulation. This produced one false alarm before it was caught.

### Measurement over assertion

`tools/check.py` runs 41 mechanical checks in one command. Its own first run failed twice, both times because the *check* was wrong rather than the page: a tilt regex matched the FAQ chevron's functional 45° rotation, and the Indonesian-copy scan spanned the entire JSON-LD block because `[^<]*` crosses a tag boundary. Both are now tightened, and `<script>`/`<style>` bodies are stripped before scanning rendered text.

---

## Opening film (scroll scrub), 2026-10-13

The owner asked for `~/Downloads/luxury.mp4` (1280x720, 24fps, 8s, 192 frames, 3.5 MB, an AI-rendered still life of the seven-variant lineup on a marble podium) to become a scroll-driven film. It is now the first section of the page, above the hero, scrubbing as the page scrolls.

### Durable decisions

- **Hybrid engine, chosen once at init.** Desktop seeks a single re-encoded mp4; small or coarse-pointer viewports, and anyone with `saveData`, draw 192 pre-rendered frames from eight WebP sprite sheets onto a canvas. Reason: seeking a `<video>` element on mobile is visibly janky, and the persona is mobile-first. The desktop mp4 is re-encoded with a 12-frame GOP (`-g 12 -keyint_min 12 -sc_threshold 0`) so every seek lands near a keyframe; 2.2 MB, down from 3.5 MB.
- **No scroll listener, on purpose.** The brand harness bans them as a tell. The scrub is an IntersectionObserver gating a `requestAnimationFrame` loop that reads `getBoundingClientRect()` each frame, so the tell still measures 0 while the experience works. This is the honest way to keep a gate, not a way to dodge it.
- **The frame stays contained 16:9, never cover-cropped.** The shot is a seven-bottle lineup; on a portrait phone, `object-fit: cover` would cut the outermost bottles out of frame. Width is capped at `min(100%, (100dvh - 14rem) * 16 / 9)`.
- **The heading is an alabaster card, not a scrim.** A scrim's contrast depends on what the footage happens to be doing underneath; a solid `#F2EEE6` card reuses an already-measured pair (`#5E4B43` on `#F2EEE6`, 7.08:1) and passes on any frame.
- **The poster is frame 0 exactly**, at the same scale as the sprite cells, so the handoff from still to film is a crossfade with no pop. Without JS, and under `prefers-reduced-motion`, the pin collapses in CSS and the poster carries the section alone.
- **Byte budgets are asserted, not suggested.** `tools/build-scrub-assets.py` exits non-zero if any output is over (poster JPEG 260 KB, mp4 3.5 MB, sprite sheets 6.5 MB). Measured: 111 KB / 2.2 MB / 4675 KB.

### Verification without installs

The scrub was driven in a real headless Chromium over raw CDP, using only node 22's global `WebSocket` and `fetch`: navigate, `window.scrollTo` at fixed offsets, read live element state, capture a screenshot per stop. The desktop path's seek position matched the scroll math to the centisecond at three offsets, and two mobile stops 500px apart produced 89,788 changed pixels inside the frame, proving the sprite canvas advances. No puppeteer, no playwright, nothing installed.

### The dark treatment is a section, not a mode (2026-10-13)

The owner asked for "the dark version" of the film. Two recorded decisions collide: PRD "Dark mode | Not planned" and GATES-SC SC1 (zero dark-mode remnants, which bans `prefers-color-scheme` and the usual theme-token names). Both still stand. What shipped is neither dark mode nor a waiver:

- **Grade, one knob.** `GRADE = eq=brightness=-0.04:contrast=1.05:gamma=0.9:saturation=0.94` in `tools/build-scrub-assets.py` is applied to every export (poster, 192 frames, mp4), so the three cannot drift apart. Subtle on purpose: the seven products carry pink, yellow and green, and a heavier pull flattens them into the bokeh. Verified with graded stills at 0 / 4 / 7.9 s before shipping.
- **One dark ground, as a token.** `--surface-film: #000000`, pure cinema black, used only by `.scrub-stage` and the media loading background; the footage's own near-black vignette edges dissolve into it cleanly. The heading card stays alabaster with espresso text, the already-measured 7.08:1 pair, so B9 gains no rows and the card becomes the single bright object on the cinema ground.
- **theme-color follows the first paint.** `meta theme-color` and `site.webmanifest` moved from `#F2EEE6` to `#000000` (owner decision 2026-10-13), and check.py's S7 assertion was amended in the open with the reason. Everywhere else the page is unchanged: SC1 still measures 0, no dark twins for petal/nude/sage/champagne exist, dark mode remains absent.

The lesson worth keeping: "the site is light-only" and "this section is dark" are not in conflict once the decision is scoped to a token instead of a mode. PRD S1 and SC1 both survive untouched.

### Two traps worth remembering

- **A stale Chromium can squat port 9222.** The first CDP run failed with "browser never exposed a target" because an unrelated leftover Chrome process (a different install, `C:\Program Files\Chromium`) already held the port, so Edge silently failed to bind. Pick a fresh port, and kill the process tree (`taskkill /T`) rather than the parent, or children survive the run.
- **Near-black corners are not letterbox bars.** The rendered film was debugged as a letterboxing bug on pixel evidence: the frame's edges read (0,0,0). It was not a bug. The source footage's own edges are a near-black vignette, in every frame of both the source and the encode. Comparing an ffmpeg-extracted frame against the rendered one settles this class of question in one step, and the fix for a non-bug would have been a worse page.

## Phase A: asset inventory and payload audit (2026-10-17)

The "elevate in place" brief needs new layouts to hang on. Before promising any asset
in a plan, every unused frame was opened and judged rather than trusted from its filename.
Six candidates existed. Five are unusable, and the reasons split into two distinct
classes that matter for the rest of the build.

### Rejected on palette, not on quality

These are competent images. They are simply not this brand. Each bakes a saturated
marketing ground and a wordmark into the frame, and each ground fights the locked
alabaster/apricot/sage palette harder than any crop can fix:

| Candidate | Ground | Baked into frame |
|---|---|---|
| `fresh-tickled-hero` | cyan water, magenta | wordmark + "Fresh Tickled" sticker |
| `emerald-sweet-wash` | sky blue + cloud | wordmark + "Emerald Sweet" sticker |
| `bright-petal-serum` | sky blue | wordmark + "Bright Petal" sticker |
| `EMERALD SWEET GREEN/24.jpg` | sky blue + cloud | wordmark + "Emerald Sweet" sticker |
| `FRESH TICKLED PINK/31.jpg` | hot pink | 3 dark-red Indonesian callout boxes |

A saturated blue or magenta ground next to alabaster is a colour-continuity break, not a
taste question, so these are out at any crop. `FRESH TICKLED PINK/31.jpg` is the awkward
case worth recording: a tight crop on the bottle alone does clear all three callouts, but
what remains is a hot pink field against the brand's soft petal `#F7D6DA`, which is a
different pink entirely.

### Salvaged, with the crop recorded

- **Blaine Floral, from `BLAINE FLORAL/Generated image 1 (3).png`.** The left ~48% of the
  frame is a standalone pump bottle on a warm cream ground with yellow flowers and no
  baked text at all. The right side is a full Indonesian marketing panel, which the crop
  discards. This ground sits on the champagne/nude tokens, so the tile is on-palette.
  This is a real fifth variant shot and it is the only one recoverable from existing files.
- **`emerald-ritual`, from `EMERALD SWEET GREEN/26.jpg`.** That raw frame is an ingredient
  infographic ("Niacinamide", "Vita 8 Complex", "Glycerin", B1/B2/B3 bubble labels), and
  the left region is a clean sage gel macro with no text. On-palette and genuinely
  atmospheric, but it is a texture, not a product portrait, so it cannot become a
  sixth tile. It is filed as a texture candidate instead.

### The consequence for the range

The page currently shows 4 of the 7 registered variants. With existing files the honest
ceiling is **5**, not 7: Emerald Sweet and Fresh Tickled exist only as blue and pink
marketing frames, so they cannot be cropped into palette without either recolouring the
photography or inventing a product shot that does not exist.

This is the concrete reason Phase F is load-bearing rather than decorative. Two of the
seven variants are missing from the page because the repository has no on-palette
photography of them. Phase D therefore ships the range at whatever count is provably
clean (5), and Phase F is what makes 7 reachable. Recording it here so the gap is
visible rather than quietly shipped as a 4.

### The payload line that was wrong

`PRD 9.2` recorded images as "607 KB of WebP across 8 files". That figure counted the
eight page photographs and silently omitted the scrub payload, which is the largest
thing a mobile visitor downloads:

- 8 sprite sheets, 3840x1440 each, WebP q70 = **4.86 MB**
- desktop mp4 = 2.21 MB

So a phone was pulling ~5.5 MB before a single product tile, against goal G3 (mobile
Lighthouse >= 90, LCP < 2.5s) which PRD itself marks "Not field-measured".
`tools/build-scrub-assets.py` was not at fault: it asserts `SHEET_BUDGET = 6.5 MB`, so it
was faithfully enforcing a budget that was itself far too generous for a mobile target.
Both the budget and the PRD line move in Phase A.

### AVIF was measured, and it was not the interesting finding

The interesting finding was that a benchmark run on a single sheet understated the
real total by 12%. Encoding sheet 0 alone predicted 1936 KB; the full eight-sheet
run came in at 2171 KB, because the clip gets busier toward the end and the sheets
grow monotonically from 242 KB to 309 KB. Sheet 0 was the cheapest sheet in the set.

The lesson generalises past this pipeline: **a size benchmark must sample the worst
case, not the first case.** One sheet was enough to rank formats against each other,
which is all it was asked to do, and not enough to set a budget. The budget
assertion in `build-scrub-assets.py` caught it immediately, which is the argument
for asserting budgets in the pipeline rather than describing them in a document.

Quality was measured too, by decoding each encode back and scoring it against the
uncompressed sheet:

| encode | KB/sheet | PSNR dB | SSIM |
|---|---|---|---|
| webp q62 | 318 | 38.28 | 0.9975 |
| webp q55 | 291 | 37.65 | 0.9972 |
| avif q50 | 288 | 38.95 | 0.9980 |
| avif q44 | 242 | 37.75 | 0.9973 |
| avif q40 | 198 | 36.44 | 0.9963 |

AVIF q40 shipped. It sits within 0.001 SSIM of the WebP control while cutting the
mobile film by 63%. The first SSIM implementation written here returned 0.0000 for
every single encode, which was obviously a broken metric rather than a real result;
it was rewritten properly before any number was quoted. A quality metric that reads
as uniformly catastrophic is a broken metric, and the fix is to fix it, not to
drop the column and hope.

### A gate that only exists because something broke in a real browser

Adding the AVIF rung left the two preload hints pointing at `.webp`. Nothing in the
static harness could see this: the preloads resolve, the files exist, and every
assertion passed. Only a live run exposed it, as two console warnings and a
double-fetched LCP element:

> The resource .../hero-collection.webp was preloaded using link preload but not
> used within a few seconds from the window's load event.

The browser was downloading the WebP that `<picture>` was about to ignore, and the
AVIF that actually became the LCP element, at the same time, competing with itself
for bandwidth on a page whose entire Phase A purpose was to stop competing for
bandwidth.

Gate B8c now asserts that every preloaded image type is a first-choice `<source>`
type. It was written after the bug, from the bug, which is the only honest order:
the gate name is a record of a specific mistake rather than a generic aspiration.

The same run also retired a static check that could never have worked. The sprite
gate used to grep the HTML for eight literal quoted paths. The new loader builds
paths from a template, so the grep found one fragment and reported it missing. The
gate now reads `FILM_SHEETS` out of the source and checks both format rungs on disk
for every index, which is what the old grep was standing in for all along.

### What a static harness still cannot tell you

`check.py` can confirm the sheets exist, are the right size, and are referenced.
It cannot confirm a single frame was ever painted. Gate B11 exists to cover that
gap: at a 390px viewport all eight AVIF sheets returned 200 with a non-zero
`naturalWidth`, no WebP fallback was requested, the mp4 was never fetched at all,
and there were no page errors. That is the difference between assets that exist and
a film that plays, and only one of those two is testable without a browser.

## Phase B: one scroll engine, and the bug only a browser could see

Phase A fixed the payload so the motion budget had something to spend. Phase B
spent it: the film's bespoke observer became a shared engine, and the first new
consumer (hero parallax) immediately found a bug that no static check could have
found. Both halves of that sentence are the finding.

### The engine

`onScrollProgress(el, mode, cb)` is now the single scroll-driven primitive. One
shared `requestAnimationFrame` loop reads each registered element's rect per
frame; a per-element `IntersectionObserver` decides which are near enough to be
worth reading. Three properties fall out, and all three are worth having:

- **No scroll listener, ever.** B3 stays at 0 because progress is derived from a
  rect read inside a rAF loop, not from an event. Pointer work uses `pointermove`,
  which is not a scroll listener either.
- **An idle page burns no frames.** The loop is torn down when nothing is live, so
  a reader parked at the top of the page costs nothing.
- **One preference switch.** Every effect registers through `whenMotion`, which
  returns early under `prefers-reduced-motion` and only then adds `.motion` to
  `<html>`. A new effect cannot forget the preference because it never touches
  `reduceMotion` itself.

`filmTick` and `filmRaf` are deleted rather than left as dead code, and the film's
`filmProgress` became a stored `filmP` so the asynchronous sheet `onload` handlers
can re-seek against the latest value between ticks.

### The bug

Hero parallax is one line: `writePy((p - 0.5) * 36)`. The first live run put
`style="--py: -18.0px"` on the hero image, which is the **minimum** of the range:
progress had saturated at 0.

The cause was a sign error in the shared engine, in the "pass" branch:

```js
var travelled = pinned ? -rect.top : vh - rect.top;   // correct
var travelled = pinned ? -rect.top : -rect.top - vh;  // shipped, wrong
```

For a passing element, progress must read 0 when the element's top reaches the
*bottom* of the viewport. That is a viewport further along, so the offset gets
**added**. It was subtracted, which made `p` clamp to 0 across a huge band: any
position where the element's top sat anywhere between `-vh` and `+vh` reported 0.
The parallax therefore rendered as a constant offset for most of its travel and
only began to move once the element had scrolled a full viewport past the top.

Every static signal was green throughout. B10 passed (transform-only), B10b passed
(the declared custom property), B10c passed (the motion guard), the film worked,
and the page threw **zero** errors. The effect ran, wrote a value, and the value
was wrong. Fixed, the same run reports `--py: -10.5px` at the same scroll position:
live and varying instead of clamped.

The endpoint table is now asserted directly rather than reasoned about:

| mode | position | expected | measured |
|---|---|---|---|
| pin | `top = 0` | 0 | 0 |
| pin | `top = -(h - vh)` | 1 | 1 |
| pass | `top = vh` | 0 | 0 |
| pass | `top = -h` | 1 | 1 |
| pass | below (`top > vh`) | 0 | 0 |
| pass | gone (`top < -h`) | 1 | 1 |

**A green harness is not the same as a correct page.** Phase A's lesson was that a
static check cannot see a canvas; this one is that a static check cannot see a
number either. The only instrument that caught it was reading the actual computed
value out of a live DOM.

### The false positive that was mine this time

B14 failed on its first run reporting one image with no alt text. The image did not
exist: a CSS comment names the tag in prose. That is the third instance of exactly
this class of failure in this harness, after the tilt regex matching the FAQ
chevron's functional 45-degree rotation and the Indonesian scan spanning the whole
JSON-LD block. The fix is the one B7 already uses, strip `<style>` and `<script>`
before scanning markup. Recorded because the pattern is now a known property of
regex-over-HTML, not a one-off: the third occurrence is what turns it into a rule.

### Reduced motion, observed rather than assumed

B10c asserts the guard structurally. It was also confirmed live, which is the check
that matters, because a guard can exist and still be bypassed by a second code path:

| | motion allowed | `prefers-reduced-motion: reduce` |
|---|---|---|
| `<html>` class | `motion` | *(absent)* |
| hero image `style` | `--py: -10.5px` | *(no style attribute)* |
| `#film` class | `scrub playing` | `scrub` |
| mp4 fetched | yes, seeks | **never requested** |
| page errors | 0 | 0 |

One scare worth recording honestly: the reduced-motion run appeared to request the
mp4, which would have meant shipping 988 KB of video for a section that never
plays. It had not. The single `mp4` string in the capture was the `<source src>`
attribute in the DOM snapshot, not a network event. The check was measuring the
wrong thing, and the reason it looked alarming is that the failure mode being
checked for is exactly the kind of quiet waste Phase A existed to remove.

### Every new gate was proven to fail

B10, B12b, B14 and B3 were each mutated deliberately, observed flipping to FAIL,
and the file restored and hash-compared. A gate that has never been seen failing
cannot be distinguished from an assumption.

## Phase C: the film finally says something

The film had text removed from it on purpose in an earlier phase, which left the
section as a video rather than a story. Phase C puts language back on it without
putting the retired devices back with it: no caption pill, no status dot, no
section numbering, no scroll cue. Type only.

### The beats live in the markup, and that was the design decision

The obvious implementation is to build the beats in script from a config array.
That would have been wrong here, because this section has to survive three states
and one of them has no script at all:

- **motion allowed** — a scrubbed sequence, one beat legible at a time
- **reduced motion** — the pin collapses to the poster
- **no JS** — the pin collapses to the poster, via `<noscript>`

So the four beats are real copy in the markup and script only ever fades them.
Under motion they share grid cell `1/1` with the film frame, so they sit exactly
on the footage and inherit its crop; without motion that rule does not apply and
the same elements flow into the grid's second row as a plain centred list. Same
words, three paths, and the fallback is not a degraded state.

They are deliberately **not** `aria-hidden`. A reader using assistive technology
gets the whole sequence in reading order, which is the same choice the `.reveal`
sections already make. Marking them decorative would have been easier and would
have thrown away the only copy in the section.

### The beats do not consume the eyebrow budget, and that is deliberate

B5 caps `.eyebrow` at roughly one per three sections. The four beats carry a small
uppercase label each, which visually rhymes with an eyebrow, and it does not use
the class. The gate counts **section** eyebrows and the four beats are one section
rather than four, so counting them would measure the wrong thing. Recorded here
because that is exactly the kind of choice that should be written down rather than
left for the next reader to wonder about.

### A measured near-miss, fixed rather than waived

The beats sit on moving footage, so there is no honest single background colour to
check them against. Rather than sample one, the two pairs are measured against a
deliberate worst case: `#474747`, which is the scrim at 72% black over pure white,
the brightest pixel the scrim can ever be compositing over.

The first attempt used a 66% scrim and **failed**:

| pair | 66% scrim | 72% scrim |
|---|---|---|
| `#F2EEE6` line | 6.24:1 | 8.03:1 |
| `#D8C9C1` label | **4.49:1** | 5.77:1 |

4.49 against a 4.5 minimum. There were two ways out: lighten the label, or darken
the scrim. The label is 0.68rem, so no large-text allowance applies and it needs the
full 4.5, so the value had to move either way. It went into the scrim, because
`#D8C9C1` is already the footer meta tone and minting a near-identical colour for
one label would be exactly the colour drift the lock in the CSS header exists to
prevent. The graded footage is far darker than the worst case, so the real margin
is comfortably larger than the measured one.

### Sequencing verified against the prediction, not against itself

The capture at 1440x900 read `--film-p: 0.581` with one beat lit. Checking that
the right beat was lit would have been weak evidence, because the windows are
mine and so is the observation. Instead the observed value was checked against the
function that produced it:

```
beat 1  window 0.06-0.28  opacity 0     predicted 0     past its window
beat 2  window 0.32-0.54  opacity 0     predicted 0     past its window
beat 3  window 0.58-0.78  opacity 0.02  predicted 0.0227  just entering
beat 4  window 0.82-0.97  opacity 0     predicted 0     not yet
```

with `translate3d(0px, 9.8px, 0px)` against the predicted `(1 - 0.02) x 10 = 9.8`.
Three independent numbers agreeing to two decimal places is worth more than one
number merely being non-zero, which is the standard that let the Phase B sign error
through.

### A cleanup failure that was real

The last browser run returned `cleanup_incomplete`, with the capture retained as a
partial observation. Worth checking rather than assuming: there were **25 stray
Chromium processes** still running. The harness had produced its evidence and
dropped its browser, and treating that as noise would have left a real leak behind.
Killed and confirmed.

### Scope note for Phase E

The grain overlay Phase E was going to add already exists: `body::after` carries a
140x140 `feTurbulence` SVG data-URI at `opacity: 0.035`, fixed, z-index 60. It was
built in Phase 16 and is already on the page. Phase E should measure it rather than
add a second one.

## Phase D: the filmstrip, and two defects the range had been hiding

Replacing the tile grid was the visible work. Both real findings in this phase
were in assets and behaviour that the grid had been small enough to disguise.

### The plan was wrong about the layout repetition

Phase 18's plan said the ritual and manifesto sections were consecutive
image+text splits and that one of them needed rebuilding. **That was wrong.** The
ingredients band sits between them and carries no figure, so the longest
consecutive run is 1. There was never a run of two to break, and rebuilding a
section would have been churn against a remembered problem.

The useful move was to stop arguing from memory and write gate B17, which measures
it. It reports 3 split sections (`hero`, `ritual`, `tentang`) and a longest run of
1. The gate also had to be corrected before it could be trusted: the first version
classified a split as *figure plus heading* and under-counted, because the
manifesto opens on a `<blockquote>` and has no `h2` at all. It now counts figure
plus any prose, which is the definition that actually matches how the page reads.
Mutation-tested by adding a figure to the ingredients band, which produced a run of
3 and failed.

The honest note on this: three sections sharing an image+text skeleton is still
three, and the range grid was the *fourth* grid-family section before it became a
filmstrip. That is the real variety win, not a split that was broken.

### Why native scroll-snap rather than a scroll-jacked strip

The Awwwards move is usually a vertical-scroll-driven horizontal translate. This
one is deliberately not that, because it would have cost four things the page
currently has: scroll-snap needs no script, arrow keys and trackpads drive it
natively, `prefers-reduced-motion` cannot break it because snapping is positioning
rather than animation, and it needs no listener (B3 stays at 0).

The one place I nearly added complexity was a progress hairline. Hiding the native
scrollbar and faking progress via `animation-timeline: scroll()` needs
`timeline-scope` plus a scroll timeline, and there is no reliable way to detect
support for it in CSS, so unsupported engines would have shown a full or empty bar
and lied either way. **The scrollbar is styled thin and left visible instead.** A
small honest scrollbar beats an elegant broken one.

The last strip item carries `.reveal` without `.shown` when first painted, because
it sits off-screen to the right and the reveal observer has not fired. That is
correct rather than broken: items 4 and 5 reveal as the reader scrolls to them.

### A shipping defect on the live site since Phase 16

Looking at the re-laid tiles at a size worth looking at exposed that
`serum-bright-petal.jpg` had **baked marketing type in it**: a fragment of
display text at the top left ("...n Real / ver / ls") and a clipped banner along the
bottom edge. The crop box recorded in `build-web-images.py` was `(0.20, 0.16, 0.96,
0.90)`, chosen specifically to exclude baked copy, and it had failed.

No gate can catch this. B8 checks that the file exists and B15 checks it is sized;
neither can look at pixels, and there is no OCR in the toolchain. It shipped
through a full brand overhaul and two later phases because every review looked at
the page, not at the crops. Re-cropped to `(0.30, 0.26, 0.96, 0.82)` after
comparing four candidates side by side; the re-crop is also 6 KB lighter.

### The page was blank without JavaScript

The Phase D verification prompted a check that should have happened much earlier.
Every `.reveal` element ships at `opacity: 0` and only becomes visible when script
adds `.shown`. The `<noscript>` block reset `.scrub` and `.scrub-stage` but **never
reset `.reveal`**, so with scripting off the entire body rendered as empty
alabaster. Only the sticky header, which carries no `.reveal`, was visible.

Measured rather than asserted, by stripping every script from a copy and
screenshotting at 1440x900:

| | background pixels | ink pixels |
|---|---|---|
| before | 99.2% | 0.1% |
| after | 74.0% | 0.8% |

The `prefers-reduced-motion` query already forced `.reveal` visible, which is
exactly why this survived from Phase 16: the one audience most likely to be tested
by hand was already covered, and the failure mode only appears for visitors nobody
simulates. Progressive enhancement means content is the default and animation is
the enhancement; here the animation had quietly become the content.

Gate B18 now asserts the override, and was mutation-tested by emptying the noscript
block.

### The probe lied to me first

The first no-JS capture came back at exactly the same byte count as the pre-fix one,
which should have been impossible. The probe **deleted** the `<noscript>` block,
but a browser with scripting off *applies* its contents. So it was testing something
harsher than reality, the fix could not take effect, and the unchanged output was
reporting my error back at me rather than a real regression. Rewritten to unwrap
the block instead.

Worth stating plainly: a test that silently simulates the wrong thing is worse than
no test, because it produces confident evidence for a claim that was never tested.
The identical byte count is what gave it away.

### Still open, recorded rather than half-fixed

Without JavaScript, the mobile drawer cannot open (the toggle is JS-driven and the
drawer ships `hidden`), so a scriptless phone visitor has no in-page navigation
despite having all the content. The fix is real but non-trivial: it needs the drawer
restyled as an inline wrapping row via noscript CSS. Not attempted here because a
half-verified nav is worse than a recorded limitation. B18 covers the content
failure, which is the severe one.

## Phase E: measure the craft instead of guessing at it

This phase was supposed to add a grain overlay and tune a type scale. It turned
out to be three real defects and one correction to my own analysis.

### The audit was built as a measurement, not a read

Reading the CSS would have produced a list of declarations that look correct.
What matters is what a finger meets, so the audit is a probe page: the real
`index.html` with a script appended that measures every interactive element's
rendered box, every heading's rendered line count, and every body paragraph's
computed `max-width` against its rendered width, then replaces the document with
the report. Run at 1440x900 and again at 390x844.

### Three tap targets were failing PRD T12

Measured at 390px before any change:

| control | measured | verdict |
|---|---|---|
| channel wall social icons (x4) | **19 x 19** | fails WCAG 2.5.8 and T12 |
| footer purchase link | **21.1px** tall | fails, and it is a conversion control |
| wordmark | **20px** tall | fails |
| nav toggle | 44 x 44 | passes |
| buttons | 52.4px | passes |
| community links | 48.4px | passes |
| skip link | 45.1px | passes |

All three fixed to 44px. The icons stayed 19px: the hit area is grown with flex
centring and spacing, so the channel band reads exactly as before and only the
target changed. After: wall icons 44x44, footer link 44px, wordmark 44px.

### I was wrong about the measure, and the estimator was the problem

The first pass concluded the lede ran to 77 characters per line and the FAQ
answers to 90, both far past the 45-75 comfortable range, which would have meant
reworking the copy blocks. The CSS says `max-width: 56ch` and `68ch`.

The number came from the measurement script, not the page: it divided width by
`font-size * 0.5`, which assumes every glyph is half an em. Re-run comparing
rendered width against **computed** `max-width`, every paragraph reported
`overflowsDeclared: false`. The CSS was correct the whole time and the estimator
was wrong.

Worth stating because the failure mode is expensive: an audit that manufactures a
finding from its own approximation sends you to edit correct code. The gate that
replaced the estimate asserts the **declaration** (`max-width` in `ch` present on
each body-copy selector), which is checkable, and the browser numbers are kept as
evidence rather than as the check.

That change also surfaced the one genuine gap: `.ingredient-groups p` was the only
paragraph with no declared measure, left to its grid column. Now 44ch.

### The strip was ragged because one name wrapped

At 39.2px, "Feminine Blush Pink" wrapped to a second line in the 296px strip
column while the other four names did not, so that one item was taller than its
neighbours and the bottom edge of the filmstrip was uneven. The ceiling dropped
from 2.45rem to 2.05rem, which brings all five onto one line at desktop, and the
heading got a two-line `min-height` so the `kind`, the note and the baseline stay
aligned across every item regardless of how a name wraps at a narrower width.

Still display-scale: 32.8px at desktop against 23.2px for the ingredient
sub-headings and 25.6px for the step names.

### The grain overlay was already there

Phase E was going to add one. It has existed since Phase 16: `body::after`, a
fixed 140x140 SVG `feTurbulence` data-URI, `opacity: 0.035`, `z-index: 60`,
confirmed by reading the computed style in the live probe. Measured and kept.
Gate B21 now asserts there is exactly one `feTurbulence` in the stylesheet, so the
duplicate this phase nearly created cannot be created twice.

### The gate failed all thirteen of its own checks first

The first version of B19, B20 and B21 ran against `MARKUP`, the string B14/B15
use because it strips `<style>` and `<script>` so the image scan cannot match
prose in a comment. `MARKUP` therefore contains no CSS at all, and all thirteen
reported "none found" - including `min-height: 48px` on `.btn`, which has been
there since Phase 16.

Two lessons, both about input rather than logic. The right input for a CSS gate is
the stylesheet, and a variable named `MARKUP` that silently means "markup without
its CSS" is a trap for whoever writes the next gate. The thirteen failures were
loud and instant, which is the only reason this cost a minute instead of a
review cycle.

The one remaining failure was also the gate's fault rather than the CSS's: it
demanded `min-height` from the nav toggle, which correctly declares a fixed
`height: 44px`. Editing correct CSS to satisfy a badly specified test is worse
than loosening the test, so the pattern now accepts either property.

### Focus rings audited, unchanged

One global `:focus-visible` at 2px solid `--accent-deep` with 3px offset, two
deliberate overrides (the skip link inverts to `--surface` because it sits on the
ink fill; the filmstrip uses a 6px offset and 6px radius because it reads as a
container, not a control). The ring colour measures 3.92:1 on alabaster against a
3.0 floor, and the film stage carries no focusable element, so no new B9 row was
added for a case that cannot occur.

## Phase G: the first field Lighthouse run, and what it actually said

Every version of this page carried "Not field-measured" against goal G3. This is
the run. The headline is not the score, it is what the score was made of.

### Baseline: desktop was already perfect, mobile was not

Lighthouse 13.5.0, local HTTP server, mobile emulation and the desktop preset:

| run | perf | LCP | TBT | CLS | Speed Index |
|---|---|---|---|---|---|
| mobile | 76 | 3.18s | 679ms | 0.000 | 2.4s |
| desktop | 100 | 0.68s | 0ms | 0.000 | 0.5s |

Seventeen points of gap between the two branches, and the two branches differ in
exactly one thing: desktop seeks a 988 KB mp4, mobile decodes eight sprite sheets.
That asymmetry was the clue, and the main-thread breakdown confirmed it:

| bucket | mobile | desktop |
|---|---|---|
| Other | **1595ms** | 164ms |
| Style & Layout | 861ms | 120ms |
| Script Evaluation | 256ms | 49ms |

Script evaluation was never the problem. "Other" at 1595ms is image decode, and
eight sheets at 2880x1080 is 24.9 megapixels of AVIF. AVIF is compact to decode
slowly; Phase A bought 63% of the bytes and paid for it in CPU. That trade was
correct at the time and invisible until it was measured.

### The fix was batching, not decoding

Sheets now load one at a time, in the order the reader reaches them, starting from
the sheet holding the current frame, scheduled into idle slots with a 400ms floor
so the queue cannot stall behind a busy main thread. If the reader outruns the
queue, the sheet they need jumps the line.

| | before | after |
|---|---|---|
| mobile performance | 76 | **93** |
| LCP | 3.18s | **2.54s** |
| TBT | 679ms | **226ms** |
| Speed Index | 2.4s | **1.7s** |
| main-thread total | 2976ms | 2840ms |

**The last row is the finding.** Total work barely moved, because the decoding is
irreducible. Blocking time fell by two thirds. The defect was never that the page
decodes 24.9 megapixels; it was that it decoded all of it in one burst while the
reader was trying to interact. TBT measures contention, not work, so spreading
the same work across idle slots is the whole fix.

### G3 is met except LCP, which misses by 40ms

Score target cleared with room, 93 against 90. CLS is exactly **0.000** on both
branches, which is the `width`/`height` guard in B15 doing its job. LCP is **2.54s
against a "< 2.5s" target**, and it is recorded as a miss rather than rounded into
a pass, because 2.54 is not less than 2.5.

The breakdown says the remainder is not really the page's: time to first byte is
the largest single term at 411ms under emulated slow-4G, resource load is 55ms, and
Lighthouse's own discovery checklist is all green (priority hint applied,
discoverable in the initial document, not lazy-loaded). The LCP element is the film
poster at 412x232, preloaded as 58 KB AVIF. Every page-side lever on that element
is already pulled, so the last 40ms is TTFB in a synthetic network rather than
something the markup can answer.

### One reported number was the test rig, not the page

`cache-insight` reported **2171 KiB** of cacheable savings, essentially all of it
the sprite sheets, and it would have been easy to write that up as a finding. It is
an artefact: `python -m http.server` sends no cache headers, so Lighthouse sees
everything as uncacheable. On a host that sets a long `Cache-Control` for
`assets/web/**` the number vanishes without a single byte changing on the page.

The one genuine deployment requirement the phase does surface is the mirror of it:
the sprite sheets need a long max-age. They are 74% of the mobile payload and they
are immutable per build, so they are the one thing on the page that should never be
revalidated.

### A mutation test that lied by being broken

The first attempt at mutation-testing B22b deleted the serialisation guard and
reported the gate as **vacuous**. It was not vacuous; the deletion had never
happened, because the Python replacement string did not match the file's
indentation. Re-run with a whitespace-insensitive regex and an assertion on the
substitution count, it failed exactly as intended.

Worth recording as a rule: **"the gate did not catch it" almost always means the
mutation did not land**, not that the gate is weak. The two failures look identical
from the outside, and only checking the substitution count tells them apart.

### Motion dial amended in the open, after the bill arrived

`MOTION_INTENSITY 5 → 8`, on the owner's instruction. Amended in all three places
that state it (PRD 8.2, the CSS header comment, the design-read block) with the
reasoning attached rather than the number quietly changed.

The amendment was accepted only after the cost it implies was bounded at both ends:
the payload it spends was fixed in Phase A, and the CPU cost that fix produced was
measured here and fixed. A motion dial of 8 on a page with no scroll listeners, no
third-party JS, 2.28 MB mobile and a measured 93 is defensible. The same dial on
the Phase 16 page, with a 5.5 MB mobile payload and an unmeasured score, would not
have been.

### Still carried forward

- **Phase F** remains blocked on image-generation credentials, so the range is
  5 of 7 rather than 7 of 7. Not attempted rather than attempted blindly.
- **Without JS the mobile drawer cannot open.** All the content is there (B18),
  but a scriptless phone visitor has no in-page navigation. Needs the drawer
  restyled as an inline wrapping row via noscript CSS.
- **`filmPromote` is untested.** All eight sheets landed inside the initial 3s wait
  in the verification run, so the outrun path never executed. It is three lines and
  it is guarded, but it is unproven.
- The four social icons load from `cdn.simpleicons.org`, so there are four
  third-party requests on mobile. Left alone deliberately: replacing them with
  hand-drawn SVG would mean hand-rolling icons, which the design skill bans, and
  they are 19px and lazy. Noted rather than changed.
