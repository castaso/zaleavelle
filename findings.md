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
