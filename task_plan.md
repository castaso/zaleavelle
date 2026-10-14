# Task Plan: zaleavelle PRD

Comprehensive PRD for the zaleavelle DTC skincare brand — single-file English landing page.

## Goal

Produce a complete, verifiable PRD that covers e-commerce conversion, landing page optimization, brand/content strategy, and technical hardening, with quantified acceptance criteria and milestone roadmap.

## Next Step

Phase 16 brand overhaul committed. Next: field Lighthouse run (PRD T4/T5), then social proof (L2) and owner verification of store catalog parity for the four showcase scents (Q10).

## Current Phase

Phase 16: Brand overhaul — botanical palette, English page, verified harness

## Phases

### Phase 1: Requirements & Discovery

- [x] Audit index.html IA (nav, sections, CTAs, anchor targets)
- [x] Audit copy: Indonesian tone, product names, price formatting, taglines
- [x] Audit links: Shopee/IG/TikTok/WA URLs, UTM presence, deep links
- [x] Audit placeholders: picsum seeds, stock images, TODO comments
- [x] Audit a11y: alt text, contrast ratios, semantic HTML, aria labels
- [x] Audit mobile: responsive breakpoints, sticky CTA, font scaling
- [x] Log all findings in findings.md
- **Status:** complete

### Phase 2: PRD Draft — 4 Tracks

- [x] Write Problem/Goals/Non-Goals with 3 measurable metrics
- [x] Write User personas + journeys (Gen-Z ID, first-time → Shopee/WA)
- [x] Track 1: E-com lite — E1-E6, UTM taxonomy, analytics events
- [x] Track 2: Landing opt — L1-L7, image pipeline, FAQ draft
- [x] Track 3: Brand/content — B1-B5, locked brand system tokens
- [x] Track 4: Tech split — T1-T10, performance budget, SEO meta
- [x] Write acceptance criteria per requirement
- [x] Write milestones M1-M3 with build slices
- [x] Write risks (4) + open questions (5) tables
- **Status:** complete

### Phase 3: Verify & Polish

- [x] Run grep-based gate checks (G1-G7, G9-G10): all PASS
- [x] Fixed G3: expanded UTM table with full utm_string column
- [x] Fixed G7: replaced "placeholder" with "sample" to avoid false positive
- [x] Fixed G6: added 5th decision row
- [x] Fixed subsection numbering throughout PRD
- [x] Adversarial re-read: no improvement needed
- [x] Filled EVIDENCE: for 9 of 10 gates
- [x] G8: ledger N/N written to progress.md
- **Status:** complete

### Phase 4: Handover

- [x] Gate-check ledger: 10 of 10 PASS
- [x] All numbers re-measured (grep counts verified)
- [x] M1 build slices proposed (7 slices)
- **Status:** complete

### Phase 5: M1 Conversion Foundation (build)

- [x] Slice 1a/1b: product CTAs → Shopee primary + WA secondary, UTM per PRD §6.2
- [x] Slice 1c: analytics stub (dataLayer queue + guarded GA4 loader + click handlers)
- [x] Slice 1d: sticky CTA becomes product-aware via IO
- [x] Slice 1e: JSON-LD Organization + 4 Products
- [x] Slice 1f: favicon.svg + site.webmanifest + theme-color
- [x] Slice 1g: title/meta/OG/Twitter per PRD §9.3
- [x] Verify: grep checks + JSON/XML validation + node --check — all PASS
- **Status:** complete

### Phase 6: Official logo integration

- [x] Step 2: manifesto brand card with `assets/zaleavelle-logo.jpg` (320×320, 1:1, tilt + hard shadow per shape system)
- [x] Step 0 (user): requested SVG — received `C:\Sandbox\zaleavelle.svg`, analyzed: raster-wrapper (embedded 320px JPEG, no vector paths), does NOT unblock Steps 1/3/4
- [x] Asset-request spec drafted (true vector or transparent PNG ≥1200px) — received true-vector `zaleavelle.svg` (black paths, transparent, no raster)
- [x] Step 1: nav wordmark `<img src="assets/zaleavelle-mark.svg">` + sizing CSS + dark-mode invert; stale TODO comment replaced
- [x] Step 2b: manifesto brand card JPG → SVG; superseded `assets/zaleavelle-logo.jpg` removed
- [ ] Step 3 (blocked on tooling): no SVG→PNG rasterizer on machine (rsvg/inkscape/magick/cairosvg all absent) — OG stays on interim picsum URL
- [x] Step 4: favicon decision — keep serif-“z” `favicon.svg` (full wordmark unreadable at 32px)
- **Status:** complete

### Phase 7: M2 image mapping (scent-canonical)

- **Status:** complete (see progress.md session)

### Phase 8: Supabase maintenance module

- **Status:** complete (code; live verify folded into Phase 9)

### Phase 9: Settings fields v2 + Shopee sync

- **Status:** complete (code; live verify pending with Phase 10)

### Phase 10: Lite Scarlett rebuild (taste skill)

- **Status:** complete (code; live verify pending with Phase 11)

### Phase 11: Square tiles + WA-only BELI

- [x] Tiles square (`.p-media` 1/1, cover crops; no re-export needed)
- [x] Bright Petal zoom-out hook (CSS + static class + renderer `img_zoom` flag; needs `img_zoom` column in SQL v3)
- [x] All `+ Keranjang`/Shopee purchase CTAs removed (tiles ×4, nav, sticky); single BELI → WA everywhere
- [x] Sticky tracker retargeted to `[data-cta="whatsapp"]`; social-grid Shopee channel link kept intentionally
- [x] Verify: 0 Keranjang, 1 shopee data-cta (social only), square ×2, zoom-out ×4, JS clean
- [ ] Owner SQL v3 (v2 + compare_at_price + last_synced_at + img_zoom) + deploy + URLs + compare prices → verify → commit
- **Status:** in_progress

### Phase 12: Remove marketplace → CASTADOO Shop

- [x] Slice 12a: `#produk` Best Seller grid + tabs → `#shop` banner (dark card, CASTADOO CTA + WA support, 3 trust points); hero/promo/kontak `#produk` anchors → `#shop`; nav `Belanja` → CASTADOO URL; sticky CTA + tracker + sentinel JS/CSS deleted
- [x] Slice 12b: Shopee purged (social-grid link → `Toko Resmi`/CASTADOO, wall icon removed, all `data-cta="shopee"` gone); WA-buy CTAs replaced by `data-cta="odoo"` (nav ×2, promo, banner, kontak); WA kept as support only (banner + kontak)
- [x] Slice 12c: backend deleted — maint cog/panel HTML + CSS + JS, Supabase CDN + config, storefront data layer (`zvDb/zvCardHTML/zvRenderProducts/zvFetchProducts/zvBoot/zvTabs`), `supabase/` dir (incl. `shopee-sync` edge function); boot is now static `zvInitReveals()` + promo carousel; restored `.btn-sm` (nav still uses it)
- [x] Slice 12d verify: 0 `#produk`/maint/supabase/sticky/p-card refs; 1 `shopee` ref left intentionally (JSON-LD `sameAs`, SEO untouched per owner); 5 CASTADOO refs; 4 `data-cta="odoo"`; all `#` anchors resolve; `node --check` clean on all 3 inline blocks; 1139 → 560 lines
- **Status:** complete (committed `33b0de1`)

### Phase 13: SEO content from BPOM doc

- [x] Doc fetched via export URL; raw 7-product table logged to findings.md (external content rule)
- [x] Slice 13a: title 58 / description 134 chars keyword-rich + canonical + `robots.txt` + `sitemap.xml` (new files)
- [x] Slice 13b: JSON-LD rebuilt — Org + 7 Products (doc descriptions, BPOM + volume `additionalProperty`, images for 4 photographed scents, CASTADOO `offers` without price; stale slot-carryover prices removed) + `FAQPage` (6 Q&As)
- [x] Slice 13c: visible `#faq` after ritual (trust list: Niacinamide/sarang walet/calendula + 7 BPOM + 6 `<details>` verbatim-matching schema); ritual + banner renamed to doc-canonical `Feminine Blush Pink`
- [x] Slice 13d verify: JSON-LD parses (9 nodes); FAQ visible==schema; 0 stale prices; 0 bare `Feminine Blush`; `node --check` ×3 clean; all `#` anchors resolve; PRD v2.4
- **Status:** complete (committed `645c3c7`)

### Phase 14: Mobile-ready

- [x] Slice 14a: hamburger drawer <968px (toggle 44px, full-screen, ESC / in-page / mq close, `body.nav-lock`); skip-link + `focus-visible`
- [x] Slice 14b: phone stacking — full-width CTAs <600px, 1-col social/trust/steps, tilts flattened, gutters 1.1rem, 380px type scale
- [x] Slice 14c: touch — 44px targets (btn/dots/FAQ/hamburger), promo swipe, `touch-action: manipulation`, `(hover: none)` hover kill, iOS safe-area + `viewport-fit=cover`
- [x] Slice 14d: PRD v2.5 (L8-L10, T6/T7/T11-T13, M9, §7.4)
- **Status:** complete (committed `54e498f`)

### Phase 15: Custom-domain storefront migration

- [x] Slice 15a: 13 shop URLs retargeted to `beli.zaleavelle.com/shop` (6 CTA href + 7 JSON-LD `offers.url`), `/shop` path preserved
- [x] Slice 15b: 13 storefront mentions renamed to CASTADOO; `data-cta="odoo"` and `odoo_profile` deliberately preserved for GA4 continuity
- [x] Slice 15c: PRD v2.6 (first-party custom domain decision row + new risk row); `GATES-CASTADOO.md` created with 12 gates
- [x] Slice 15d verify: 13 shop URLs, 0 stale vendor host repo-wide, 12/12 gates PASS
- **Status:** complete (committed `ee1d40c`)

### Phase 16: Brand overhaul — botanical palette, English page, verified harness

Owner supplied two brand documents (identity + colour palette) and asked for the page rebuilt on them. The shipped page used a deep-rose playful system (tilt, hard offset shadows, rotated stickers) that contradicted the documented personality: elegant, graceful, serene, fresh. Owner decisions taken in session: full overhaul; page to English; apricot accent with espresso text; purely marketing with every transaction on `beli.zaleavelle.com`; wordmark recolour approved; self-hosted fonts; promo carousel deleted outright.

- [x] Slice 16a: token rebuild on the documented palette, with two documented values **rejected on measured contrast** — white-on-apricot 1.74:1 (so buttons take espresso text at 4.71:1) and the documented taupe `#8A786E` at 3.64:1 (darkened to `#6B5C53`, 5.53:1). Apricot is banned as a border stroke at 1.50:1; `#B4601F` at 3.92:1 is used instead
- [x] Slice 16b: English migration across body copy, `lang`, title, description, OG/Twitter, 7 JSON-LD product descriptions, Organization slogan, 6 FAQ answers, webmanifest. `lang="en"`
- [x] Slice 16c: retire the v2.6 visual system wholesale (tilt, offset shadows, stickers, bob, mesh drift, promo carousel); collapse six buy-intent labels into one "Shop now"; dials 9/8/3 → 7/5/3
- [x] Slice 16d: self-host Cormorant Garamond + Geist (89 KB latin woff2, preloaded). The old stack named `Bodoni MT`/`Didot`, neither of which exists on iOS or Android, so most visitors were silently rendering Georgia
- [x] Slice 16e: new sections — editorial 4-scent showcase (no prices, no per-tile buy buttons), Ingredients band, Cleanse/Treat/Seal timeline replacing `01 · Bersihkan` labels, founder origin paragraph (closes PRD B2)
- [x] Slice 16f: fix 5 defects found by rendering, not reading — invalid `site.webmanifest` JSON; wordmark SVG declaring mm dimensions against a square canvas (nav rendered it at ~⅓ size); `aspect-ratio` defeated by `<img>` height attributes; drawer moved outside `<header>` so it never opened; `100dvh` hero stretching on tall viewports
- [x] Slice 16g: tooling — `tools/check.py` (41 mechanical checks), `build-web-images.py`, `vendor-fonts.py`, `svg-bounds.py`
- [x] Slice 16h verify: 41/41 harness checks; storefront integrity re-measured (13 shop URLs, 6 `data-cta="odoo"`, 7 lowercase odoo); rendered at 1440px and a true 390px viewport; PRD v2.7; `GATES-BRAND.md` added (16 gates)
- [ ] Field Lighthouse on mobile (PRD T4/T5) — never run on any version of this page
- [x] Slice 17a: opening film — scroll-scrubbed `luxury.mp4` as the first section above the hero. Hybrid engine: mp4 seek on desktop, 8 WebP sprite sheets on canvas for mobile / coarse-pointer / saveData (seeking a video on a phone stutters). IntersectionObserver-gated rAF loop keeps the B3 no-scroll-listener tell at 0. Contained 16:9 frame (the shot is a seven-bottle lineup; cover-crop cuts outer bottles on portrait). Alabaster heading card reuses a measured contrast pair. Poster is frame 0 exactly for a pop-free crossfade. Pin collapses under reduced motion and no-JS
- [x] Slice 17b: tooling — `tools/build-scrub-assets.py` (poster, 12-frame-GOP mp4 at 2.2 MB, 4675 KB of sprite sheets; byte budgets asserted, non-zero exit over budget); `tools/check.py` B8 extended to verify the JS-referenced sprite paths that no `src=`/`href=` scan can see (41 → 42 checks)
- [x] Slice 17c verify: 42/42 harness checks; headless CDP run with zero installs (node global WebSocket) showing seek position matching scroll math to the centisecond at three offsets and the mobile canvas advancing 89,788 px between two stops; R5 gate + evidence in `GATES-BRAND.md`
- [x] Slice 17d: dark treatment on the film section. Stage background `--surface-film: #000000` (pure cinema black; film's vignette edges dissolve into it). All assets re-graded via ffmpeg `eq=brightness=-0.04:contrast=1.05:gamma=0.9:saturation=0.94` so the film sits in the dark stage without a hard brightness break. Alabaster card kept (existing measured 7.08:1 pair, no new contrast rows). `meta theme-color` and `site.webmanifest` theme/background flipped to `#000000` with a documented S7 gate amendment. CSS header theme-lock comment amended with owner override 2026-10-13. Dark is a section, not a mode — PRD "Not planned" and GATES-SC SC1 (0 theme-toggling matches) left intact; static dark CSS keeps SC1 at 0
- [x] Slice 17d verify: `python tools/check.py` 42/42 with S7 asserting `#000000`; B6 wordmark pure-black ban unaffected (stage ban is wordmark-only). CDP run confirmed black stage `rgb(0, 0, 0)` with card `rgb(242,238,230)`/`rgb(94,75,67)`, desktop `currentTime` 6.56 at scrollY 2000, mobile canvas opacity 1; dark stills at 0/4/7.9 s reviewed by owner
- **Status:** complete (film harness-verified; field Lighthouse open)

## Key Questions

1. ~~Should product CTAs link directly to Shopee product pages, or to a WhatsApp chat flow?~~ → Resolved for M1: Shopee primary + WA secondary (PRD recommendation)
2. ~~Is i18n (ID/EN toggle) in scope, or ID-only for launch?~~ → Resolved in Phase 16: owner chose English-only. The page is English throughout; Indonesian is a possible follow-up, not a launch requirement
3. Should we split index.html into modular files now, or defer to post-launch?
4. NEW: `assets/` photos use BODY WASH/LOTION/SERUM taxonomy — how do they map to the 4 landing products? (blocks M2/L1)
5. NEW: who compresses the 0.75–2MB asset images to WebP before the M2 swap? (T9)

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| CASTADOO Shop as sole storefront (Phase 12) | Owner interview 2026-09-24: remove marketplace section altogether, replace with https://shop.zaleavelle.com/shop CTA banner |
| Sticky CTA deleted, not converted | Owner chose "Nav to CASTADOO, sticky removed" — no floating buy button in CASTADOO era |
| JSON-LD Product schema kept (tech debt) | Owner chose "Leave SEO untouched" — 4 Product nodes still reference prices/images with no on-page catalog; follow-up: strip to Organization or point offers at CASTADOO |
| Ritual/promo copy follows BPOM doc (Phase 13) | Owner chose "Follow the doc" — `Feminine Blush Pink` canonical everywhere; CASTADOO parity still owner-side (Q10) |
| FAQ after ritual, trust + 6 Q&As (Phase 13) | Owner chose placement/size; schema mirrors visible text verbatim for FAQPage eligibility |
| Mobile-first breakpoints 968 / 600 / 380 (Phase 14) | Persona is Gen-Z ID mobile; desktop nav unchanged; drawer replaces hidden-links-only pattern |
| Offers without price accepted (Phase 13) | No prices in source doc; inventing forbidden — valid schema, no Product rich results |
| Supabase backend deleted, not dormant | Owner chose delete/disable — no products table fetch, no maintenance panel, no shopee-sync function |
| Solo mode (not orchestrated) | PRD doc task ~30min, tree depth 3, no code integration needed |
| Single GATES.md (not gates/) | Below 30min threshold; subagent overhead not justified |
| ID-only default with EN appendix | Superseded by the Phase 16 English-only decision |
| Q1 Shopee primary + WA secondary (M1 default) | PRD recommendation; per-product Shopee links use store URL + UTM until per-product URLs provided |
| Q5 single WA number with pre-filled product text | PRD recommendation; one agent number 6282121262593 |
| Q3 defer file split to post-M3 | Keep single-file for M1; no build step |
| Analytics without GA4 ID: dataLayer queue + guarded loader | No 404s, no dead requests; set window.ZV_GA_ID to enable |
| favicon.svg + site.webmanifest instead of .ico/.png | No binary tooling in repo; SVG favicon satisfies T3 intent |
| Full overhaul over re-skin (Phase 16) | The documented personality is incompatible with the shipped tilt/sticker system; a re-skin would have produced a mismatch |
| Apricot CTA with espresso text, not white (Phase 16) | White on `#F6B78E` measures 1.74:1. Espresso text on the same fill measures 4.71:1 and keeps the documented swatch |
| `#B4601F` for borders and icons, not apricot (Phase 16) | Apricot on the alabaster base is 1.50:1 and invisible as a stroke. Decorative rules may stay low-contrast; control borders need 3:1 |
| Secondary taupe darkened to `#6B5C53` (Phase 16) | The documented `#8A786E` is 3.64:1 on alabaster and fails AA for body text |
| Sage `#D7E0D1` kept as a load-bearing surface | Without the one cool botanical tone the page reads as generic cream, the default failure mode for this brand category |
| English-only (Phase 16) | Owner decision; supersedes the ID-first default recorded below |
| Self-hosted fonts, 89 KB (Phase 16) | `Bodoni MT` and `Didot` do not exist on iOS or Android, so the old stack silently rendered Georgia for most visitors |
| Light theme only, no dark mode (Phase 16) | PRD S1 lite-only decision retained and made explicit; deliberately overrides the design-skill dual-mode default |
| Product showcase is editorial, not commerce (Phase 16) | Owner confirmed purely marketing. Images and descriptions only, so the no-prices boundary holds |
| Promo carousel deleted rather than restyled (Phase 16) | One slide reused the OG image as page content and another duplicated an existing CTA intent |
| Verification harness over ad-hoc greps (Phase 16) | 41 mechanical checks make contrast, tell-sweep and schema integrity re-runnable after any future edit |
| Hybrid film engine: mp4 seek desktop, sprite sheets mobile (Phase 17) | Seeking a `<video>` element on a phone visibly stutters and the persona is mobile-first; the sprite path costs 4.7 MB only for the visitors who need it |
| rAF loop, not a scroll listener, for the film | The B3 tell bans scroll listeners; an observer-gated rAF loop reading the section rect keeps the tell at 0 with no dodge |
| Contained 16:9 frame, not full-bleed cover | The footage is a seven-bottle lineup; cover-crop cuts the outermost bottles out of frame on portrait |
| Film poster is frame 0 exactly | The first scrub frame then cannot pop when the engine takes over; same scale as the sprite cells |
| Byte budgets asserted in `tools/build-scrub-assets.py` | Bloat cannot ship silently; the pipeline exits non-zero over budget |
| Dark film stage, not a theme toggle (Phase 17) | Owner decision 2026-10-13. The dark treatment is a section, so PRD "Dark mode: Not planned" and GATES-SC SC1 (0 matches for `data-theme|themeBtn|zv-theme|prefers-color-scheme|theme-toggle`) both hold; a static CSS dark value keeps SC1 at zero matches |
| `--surface-film: #000000` over the graded black | Graded footage alone left the sticky stage washing into the page on light backgrounds; a named dark surface token scopes the treatment to the film without a second theme |
| ffmpeg grade `eq=brightness=-0.04:contrast=1.05:gamma=0.9:saturation=0.94` | Applied to poster, mp4 and all 8 sprite sheets so the still, desktop path and mobile path never diverge in grade |
| Alabaster card kept in the dark treatment | The `#F2EEE6` / `#5E4B43` pair is already measured at 7.08:1; a scrim over dark footage would have needed a fresh B9 row |
| `meta theme-color` + webmanifest theme moved to `#000000` | Matches the first painted surface. Documented as an S7 amendment (owner override 2026-10-13) rather than a silent gate change |
| CSS theme-lock comment amended, not removed | The Phase 16 light-only lock still governs the rest of the page; the override is scoped to the film section and dated |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| `site.webmanifest` was invalid JSON | Only noticed when rewriting the file | A corrupt byte in `name` meant PWA install was silently dead. Rewritten; `tools/check.py` now parses it on every run |
| Wordmark rendered at ~⅓ size | Visible in the first desktop screenshot | The SVG declared `width`/`height` in **millimetres** against a square Inkscape canvas, so its intrinsic ratio stayed 1:1. viewBox re-cut from measured ink bounds via `tools/svg-bounds.py` |
| Figure images rendered portrait despite `aspect-ratio` | Visible once the manifesto image loaded | `width`/`height` attributes on `<img>` become UA presentational hints; an unset CSS `height` let the literal attribute win. Fixed with explicit `height: auto` |
| Mobile drawer did not open | Clicked the toggle in a headless harness; `aria-expanded` flipped but no panel appeared | The element had been moved outside `<header>` while its `.nav.open .drawer` selector stayed. Moved back inside; `list-style: none` added |
| "390px" screenshots showed horizontal overflow | Screenshot appeared wrong | Not a page bug. Chrome clamps `--window-size` to ~496px minimum, so the capture was cropped rather than rendered narrow. Re-tested through an iframe harness giving a true 390px viewport |
| Two false-positive failures in `tools/check.py` | First harness run reported a decorative tilt and Indonesian residue | Own bugs, not page bugs: the tilt regex matched the FAQ chevron's functional 45° rotation, and the Indonesian scan spanned the whole JSON-LD block via `[^<]*`. Both patterns tightened |
| Heading ran to 3 lines on desktop | Hero screenshot | Column too narrow for the type scale. Widened the text column and eased the clamp so the headline resolves to exactly 2 lines |
| Headless CDP run: "browser never exposed a target" | First film verification attempt | An unrelated stale Chromium install already held port 9222, so Edge never bound. Switched to a fresh port and kill the process tree with `taskkill /T` instead of the parent |
| Film appeared letterboxed in rendered screenshots | Pixel check read (0,0,0) at the frame edges | Not a page bug: the source footage's own corners are a near-black vignette in every frame of source and encode. Compared an ffmpeg-extracted frame against the rendered pixels; both agree, nothing to fix |

## Notes

- Planning files in project root per planning-with-files convention.
- All external research goes to findings.md, never task_plan.md.
- Re-read this file before each phase transition.
