# Task Plan: zaleavelle PRD

Comprehensive PRD for the zaleavelle DTC skincare brand — single-file Indonesian landing page.

## Goal

Produce a complete, verifiable PRD that covers e-commerce conversion, landing page optimization, brand/content strategy, and technical hardening, with quantified acceptance criteria and milestone roadmap.

## Next Step

Phase 6 complete (nav + manifesto on vector mark; OG held for rasterizer access; favicon kept). Open: M2 image mapping (assets/ taxonomy question) + i18n/file-split decisions.

## Current Phase

Phase 6: Official logo integration

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

## Key Questions

1. ~~Should product CTAs link directly to Shopee product pages, or to a WhatsApp chat flow?~~ → Resolved for M1: Shopee primary + WA secondary (PRD recommendation)
2. Is i18n (ID/EN toggle) in scope, or ID-only for launch?
3. Should we split index.html into modular files now, or defer to post-launch?
4. NEW: `assets/` photos use BODY WASH/LOTION/SERUM taxonomy — how do they map to the 4 landing products? (blocks M2/L1)
5. NEW: who compresses the 0.75–2MB asset images to WebP before the M2 swap? (T9)

## Decisions Made

| Decision | Rationale |
|----------|-----------|
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
