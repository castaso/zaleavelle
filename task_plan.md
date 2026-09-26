# Task Plan: zaleavelle PRD

Comprehensive PRD for the zaleavelle DTC skincare brand — single-file Indonesian landing page.

## Goal

Produce a complete, verifiable PRD that covers e-commerce conversion, landing page optimization, brand/content strategy, and technical hardening, with quantified acceptance criteria and milestone roadmap.

## Next Step

Phase 14 mobile-ready code + PRD v2.5 complete. Next: visual check at 375/390/430 + commit.

## Current Phase

Phase 14: Mobile-ready landing

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

### Phase 12: Remove marketplace → Odoo Shop

- [x] Slice 12a: `#produk` Best Seller grid + tabs → `#shop` banner (dark card, Odoo CTA + WA support, 3 trust points); hero/promo/kontak `#produk` anchors → `#shop`; nav `Belanja` → Odoo URL; sticky CTA + tracker + sentinel JS/CSS deleted
- [x] Slice 12b: Shopee purged (social-grid link → `Toko Resmi`/Odoo, wall icon removed, all `data-cta="shopee"` gone); WA-buy CTAs replaced by `data-cta="odoo"` (nav ×2, promo, banner, kontak); WA kept as support only (banner + kontak)
- [x] Slice 12c: backend deleted — maint cog/panel HTML + CSS + JS, Supabase CDN + config, storefront data layer (`zvDb/zvCardHTML/zvRenderProducts/zvFetchProducts/zvBoot/zvTabs`), `supabase/` dir (incl. `shopee-sync` edge function); boot is now static `zvInitReveals()` + promo carousel; restored `.btn-sm` (nav still uses it)
- [x] Slice 12d verify: 0 `#produk`/maint/supabase/sticky/p-card refs; 1 `shopee` ref left intentionally (JSON-LD `sameAs`, SEO untouched per owner); 5 Odoo refs; 4 `data-cta="odoo"`; all `#` anchors resolve; `node --check` clean on all 3 inline blocks; 1139 → 560 lines
- **Status:** in_progress (code complete, uncommitted; browser visual check + commit pending)

### Phase 13: SEO content from BPOM doc

- [x] Doc fetched via export URL; raw 7-product table logged to findings.md (external content rule)
- [x] Slice 13a: title 58 / description 134 chars keyword-rich + canonical + `robots.txt` + `sitemap.xml` (new files)
- [x] Slice 13b: JSON-LD rebuilt — Org + 7 Products (doc descriptions, BPOM + volume `additionalProperty`, images for 4 photographed scents, Odoo `offers` without price; stale slot-carryover prices removed) + `FAQPage` (6 Q&As)
- [x] Slice 13c: visible `#faq` after ritual (trust list: Niacinamide/sarang walet/calendula + 7 BPOM + 6 `<details>` verbatim-matching schema); ritual + banner renamed to doc-canonical `Feminine Blush Pink`
- [x] Slice 13d verify: JSON-LD parses (9 nodes); FAQ visible==schema; 0 stale prices; 0 bare `Feminine Blush`; `node --check` ×3 clean; all `#` anchors resolve; PRD v2.4
- **Status:** in_progress (code complete, uncommitted; browser visual check + commit pending)

### Phase 14: Mobile-ready

- [x] Slice 14a: hamburger drawer <968px (toggle 44px, full-screen, ESC / in-page / mq close, `body.nav-lock`); skip-link + `focus-visible`
- [x] Slice 14b: phone stacking — full-width CTAs <600px, 1-col social/trust/steps, tilts flattened, gutters 1.1rem, 380px type scale
- [x] Slice 14c: touch — 44px targets (btn/dots/FAQ/hamburger), promo swipe, `touch-action: manipulation`, `(hover: none)` hover kill, iOS safe-area + `viewport-fit=cover`
- [x] Slice 14d: PRD v2.5 (L8-L10, T6/T7/T11-T13, M9, §7.4)
- **Status:** in_progress (code complete; preview + commit pending)

## Key Questions

1. ~~Should product CTAs link directly to Shopee product pages, or to a WhatsApp chat flow?~~ → Resolved for M1: Shopee primary + WA secondary (PRD recommendation)
2. Is i18n (ID/EN toggle) in scope, or ID-only for launch?
3. Should we split index.html into modular files now, or defer to post-launch?
4. NEW: `assets/` photos use BODY WASH/LOTION/SERUM taxonomy — how do they map to the 4 landing products? (blocks M2/L1)
5. NEW: who compresses the 0.75–2MB asset images to WebP before the M2 swap? (T9)

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Odoo Shop as sole storefront (Phase 12) | Owner interview 2026-09-24: remove marketplace section altogether, replace with https://zaleavelle.odoo.com/shop CTA banner |
| Sticky CTA deleted, not converted | Owner chose "Nav to Odoo, sticky removed" — no floating buy button in Odoo era |
| JSON-LD Product schema kept (tech debt) | Owner chose "Leave SEO untouched" — 4 Product nodes still reference prices/images with no on-page catalog; follow-up: strip to Organization or point offers at Odoo |
| Ritual/promo copy follows BPOM doc (Phase 13) | Owner chose "Follow the doc" — `Feminine Blush Pink` canonical everywhere; Odoo parity still owner-side (Q10) |
| FAQ after ritual, trust + 6 Q&As (Phase 13) | Owner chose placement/size; schema mirrors visible text verbatim for FAQPage eligibility |
| Mobile-first breakpoints 968 / 600 / 380 (Phase 14) | Persona is Gen-Z ID mobile; desktop nav unchanged; drawer replaces hidden-links-only pattern |
| Offers without price accepted (Phase 13) | No prices in source doc; inventing forbidden — valid schema, no Product rich results |
| Supabase backend deleted, not dormant | Owner chose delete/disable — no products table fetch, no maintenance panel, no shopee-sync function |
| Solo mode (not orchestrated) | PRD doc task ~30min, tree depth 3, no code integration needed |
| Single GATES.md (not gates/) | Below 30min threshold; subagent overhead not justified |
| ID-only default with EN appendix | Simplifies MVP; EN can be added via i18n track later |
| Q1 Shopee primary + WA secondary (M1 default) | PRD recommendation; per-product Shopee links use store URL + UTM until per-product URLs provided |
| Q5 single WA number with pre-filled product text | PRD recommendation; one agent number 6282121262593 |
| Q3 defer file split to post-M3 | Keep single-file for M1; no build step |
| Analytics without GA4 ID: dataLayer queue + guarded loader | No 404s, no dead requests; set window.ZV_GA_ID to enable |
| favicon.svg + site.webmanifest instead of .ico/.png | No binary tooling in repo; SVG favicon satisfies T3 intent |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| (none yet) | — | — |

## Notes

- Planning files in project root per planning-with-files convention.
- All external research goes to findings.md, never task_plan.md.
- Re-read this file before each phase transition.
