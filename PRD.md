# PRD: zaleavelle — Product Requirements Document

> Version 2.0 · 2026-09-21
> Author: opencode (AI-assisted)
> Status: Code complete through Phase 9 (pushed `b298697`); live verify pending SETUP-SQL v2 + function deploy + listing URLs

---

## 1. Problem Statement

zaleavelle is an Indonesian DTC skincare brand with a single-file landing page (`index.html`, ~900 lines) showcasing 4 scent-named products (Emerald Sweet, Blaine Floral, Feminine Blush, Bright Petal). Since v1.0 the page gained conversion infrastructure (Shopee/WA CTAs with UTM, analytics events, product-aware sticky CTA), real product photography, a vector wordmark, and a Supabase-backed maintenance module (code complete, backend pending).

**Core problem:** The backend that powers dynamic products is not yet live (table + deploy outstanding), prices ride on an unconfirmed slot-carryover assumption, and the page still lacks social proof — so conversion can't be measured or trusted end-to-end yet.

## 2. Goals

| # | Goal | Metric | Target |
|---|------|--------|--------|
| G1 | Increase product-to-purchase clicks | Click-through rate from product cards to Shopee/WA | ≥ 8% of product card views |
| G2 | Strengthen brand recall | Time on page + return visits (GA4) | ≥ 90s avg session, ≥ 15% return rate within 30 days |
| G3 | Improve SEO + mobile performance | Lighthouse Performance score (mobile), LCP, CLS | ≥ 90 score, LCP < 2.5s, CLS < 0.1 |

## 3. Non-Goals

| # | Non-Goal | Rationale |
|---|----------|-----------|
| NG1 | Full e-commerce checkout on-site | Shopee is the payment/logistics backbone; no cart on zaleavelle |
| NG2 | User accounts / login | Out of scope for MVP; community engagement via social only |
| NG3 | Multi-language at launch | ID-first; EN can be added in a follow-up i18n track |
| NG4 | Mobile app | Web-only; PWA is a future consideration |
| NG5 | Paid ad creative pipeline | PRD covers owned landing page, not ad campaigns |

## 4. Users & Journeys

### 4.1 Primary Persona: Gen-Z ID Skincare Buyer

- **Age:** 18-26, Indonesian, mobile-first
- **Discovery:** TikTok / Instagram Reels → landing page → Shopee or WhatsApp
- **Motivation:** Simple routine, affordable, aesthetic packaging, peer validation
- **Friction points:** Unclear which scent to buy first, no social proof on page, displayed prices unconfirmed (slot-carryover assumption), stock counts are provisional seed values

### 4.2 User Journey (Target State)

```
Ad / Social Post → zaleavelle landing page
  → Hero: brand promise + CTA
  → Product section: browse 4 products
  → Product card CTA → Shopee product page (UTM tagged)
  → OR WhatsApp: "Halo, mau tanya [product name]"
  → Purchase
  → Return visit: community section → IG/TikTok follow
```

## 5. Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Single-file HTML for MVP | No build step required; GSAP CDN approach works; simplicity over modularity |
| ID-first language | Primary audience is Indonesian; EN can be added via i18n follow-up track |
| Shopee as primary CTA | Existing Shopee store link present; highest conversion path for ID market |
| GA4 gtag for analytics | Lightweight, free, industry standard; avoids third-party analytics bloat |
| WebP with JPG fallback | Modern format for perf; JPG fallback for older browsers |
| Supabase as product backend | Cross-device CRUD without a custom server; free tier suffices for 4 SKUs |
| Open-write RLS, no access gate | Owner decision; JSON backup is the safety net; revisit one-admin login later |
| Scent names canonical | Photos sell scent-named SKUs; old set/serum/lotion/scrub names retired in M2 |
| Slot-carryover prices | Unconfirmed assumption until the real price list arrives; single table to swap |
| SVG favicon over ICO/PNG | No binary tooling in repo; full wordmark illegible at 32px, serif-“z” kept |
| Stock-zero badge semantics | Card stays with Stok Habis badge + disabled pill; layout and numbering stable |
| Shopee pull-on-demand sync | Edge function fills form only; manual fields win; no silent overwrites |
| Single-file kept post-M3 | Split still deferred; Supabase CDN scripts attach without a build step |

## 6. Track 1: E-Commerce Conversion

### 6.1 Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| E1 | Each product card CTA links to its Shopee listing with UTM params | `href` contains `shopee.co.id` + `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` per product |
| E2 | Each product card has a secondary WhatsApp CTA | "Tanya via WhatsApp" link with pre-filled product name in `wa.me` URL |
| E3 | UTM taxonomy defined and documented | Table in PRD with source/medium/campaign/content per CTA |
| E4 | Event tracking on CTA clicks | `gtag('event', ...)` fires on every Shopee/WA link click with product name + price |
| E5 | Sticky mobile CTA shows product-specific action | After scrolling past hero, sticky CTA says "Beli [product] di Shopee" |
| E6 | Price formatting standardized | Use `Rp XXX.XXX` format (Indonesian thousand separator with dot) — already correct in current code |

### 6.2 UTM Taxonomy

| Product | utm_source | utm_medium | utm_campaign | utm_content | Full utm_string |
|---------|------------|------------|--------------|-------------|-----------------|
| Emerald Sweet | zaleavelle | referral | product_launch | emerald_sweet_cta | `utm_source=zaleavelle&utm_medium=referral&utm_campaign=product_launch&utm_content=emerald_sweet_cta` |
| Blaine Floral | zaleavelle | referral | product_launch | blaine_floral_cta | `utm_source=zaleavelle&utm_medium=referral&utm_campaign=product_launch&utm_content=blaine_floral_cta` |
| Feminine Blush | zaleavelle | referral | product_launch | feminine_blush_cta | `utm_source=zaleavelle&utm_medium=referral&utm_campaign=product_launch&utm_content=feminine_blush_cta` |
| Bright Petal | zaleavelle | referral | product_launch | bright_petal_cta | `utm_source=zaleavelle&utm_medium=referral&utm_campaign=product_launch&utm_content=bright_petal_cta` |
| General CTA | zaleavelle | referral | landing_page | hero_cta / nav_cta | `utm_source=zaleavelle&utm_medium=referral&utm_campaign=landing_page&utm_content=hero_cta` |

### 6.3 Analytics Events

```javascript
// On Shopee/WA CTA click
gtag('event', 'select_item', {
  item_name: 'Emerald Sweet',
  item_category: 'Body Wash',
  price: 389000,
  currency: 'IDR'
});
```

## 7. Track 2: Landing Page Optimization

### 7.1 Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| L1 | Replace all picsum sample images with real brand photography | ✅ Done M2 — zero `picsum.photos` URLs; 7 local exports in `assets/web/` |
| L2 | Add social proof / UGC section | ⬜ Open — ≥ 3 customer testimonials with names, or IG embed grid |
| L3 | Add FAQ section | ⬜ Open — page has no FAQ block yet (draft copy in §7.3) |
| L4 | Polish Indonesian copy | 🔶 Partial — M2 rewrote cards/ritual to scent names; full tone pass still open |
| L5 | Improve sticky CTA logic | ✅ Done M1 — IO-driven, product-aware, hides in contact section |
| L6 | Add favicon | ✅ Done M1 — crisp SVG serif-“z” + `site.webmanifest` (ICO/PNG skipped, no binary tooling) |
| L7 | Add Open Graph + Twitter Card meta tags | ✅ Done — absolute `https://zaleavelle.com/og-image.jpg` (CNAME drift noted in risks) |

### 7.2 Image Pipeline

| Image | Dimensions | Source file | Weight |
|-------|-----------|-------------|--------|
| Hero | 1080×1350 | `assets/web/fresh-tickled-hero` (.webp + .jpg) | 110 / 192 KB |
| Emerald Sweet card | 900×1125 | `assets/web/emerald-sweet-wash` (.webp + .jpg) | 48 / 93 KB |
| Blaine Floral card | 900×900 | `assets/web/blaine-floral-lotion` (.webp + .jpg), `object-position: 70%` | 74 / 119 KB |
| Feminine Blush card | 900×900 | `assets/web/feminine-blush-lotion` (.webp + .jpg) | 59 / 101 KB |
| Bright Petal card | 800×1000 | `assets/web/bright-petal-serum` (.webp + .jpg) | 62 / 102 KB |
| Ritual lifestyle | 1600×800 | `assets/web/emerald-ritual` (.webp + .jpg, center crop) | 49 / 109 KB |
| OG image | 1200×630 | `assets/web/og-image.jpg` (crawlers need raster) | 76 KB |
| Favicon | vector | `favicon.svg` serif-“z” + `site.webmanifest` | <1 KB |
| Reserve (unused) | — | Classic Pink, Flavia Floral + alternate shots in `assets/` | — |

### 7.3 FAQ Content (Draft)

1. **Varian aroma apa saja yang tersedia?** — Emerald Sweet (body wash), Blaine Floral dan Feminine Blush (body lotion), Bright Petal (body serum).
2. **Apakah aman untuk kulit sensitif?** — Ya, semua produk zaleavelle diformulasi lembut tanpa paraben.
3. **Bagaimana cara pesan?** — Klik tombol Shopee untuk checkout langsung, atau chat kami via WhatsApp.
4. **Kapan hasilnya terlihat?** — Kebanyakan pelanggan melihat perbedaan dalam 2-4 minggu.
5. **Apakah ada program reseller?** — Hubungi WhatsApp kami untuk info kerja sama.

## 8. Track 3: Brand & Content

### 8.1 Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| B1 | Expand ritual section with before/after or routine timeline | Visual timeline or step-by-step with real imagery |
| B2 | Strengthen manifesto section | Add founder story or brand origin (2-3 sentences) |
| B3 | Community section links all work | All 4 social links open in new tab, correct URLs, UTM tagged |
| B4 | Add newsletter / WhatsApp broadcast signup | Email input or WA link for "Tips skincare mingguan" |
| B5 | Marquee text reviewed | Current: "glow — lembap — tenang" — confirm with brand owner |

### 8.2 Brand System (Locked)

| Token | Value | Usage |
|-------|-------|-------|
| Accent (light) | `#9E3E4D` | Buttons, links, emphasis, stickers |
| Accent (dark) | `#E3A7AC` | Same roles in dark theme |
| Display font | Bodoni MT / Didot / Cormorant Garamond / EB Garamond / Georgia | Hero h1, section h2, blockquote, product names |
| Body font | system-ui stack | Paragraphs, nav, CTAs |
| Mono font | ui-monospace / SF Mono / JetBrains Mono | Eyebrows, labels, prices |
| Card radius | 16px | Product cards, ritual steps |
| Button radius | 999px (pill) | All buttons |
| Shadow accent | `color-mix(in srgb, var(--accent) 35%, transparent)` | Hard-offset shadows on cards, hero media |
| Motion spring | `cubic-bezier(0.16, 1, 0.3, 1)` | All transitions |
| z-scale | nav 40 / stack cards 1-4 / sticky CTA 45 / grain 60 | Stacking context |

**Shape rule:** Tilt + hard offset shadow is the system. Applied consistently on product cards and hero media. No second accent color. No neon glows. No AI-purple.

## 9. Track 4: Technical Hardening

### 9.1 Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| T1 | Add JSON-LD Product schema for all 4 products | ✅ Done — scent-named nodes with local image URLs |
| T2 | Add JSON-LD Organization schema | ✅ Done — with `sameAs` social links |
| T3 | Add favicon + manifest | ✅ Done — `favicon.svg` + `site.webmanifest` + theme-color |
| T4 | Lighthouse Performance ≥ 90 (mobile) | ⬜ Open — run and paste score in progress.md |
| T5 | Lighthouse Accessibility ≥ 90 | ⬜ Open — run and paste score in progress.md |
| T6 | Add skip-link for keyboard navigation | ⬜ Open — jumps to `<main>` |
| T7 | Add `focus-visible` styles | 🔶 Partial — maintenance cog has focus ring; page-wide ring styles still open |
| T8 | Consider CSS/JS split | ✅ Resolved — single-file kept (Supabase scripts attach CDN-side) |
| T9 | Image optimization pipeline | ✅ Done — 7 exports, WebP + JPG via `<picture>` |
| T10 | Meta description + title optimized | ✅ Done — 56 / 110 chars; scent names; absolute OG URL |

### 9.2 Performance Budget

| Metric | Target | Current (estimated) |
|--------|--------|---------------------|
| Lighthouse Performance | ≥ 90 | ~80-90 est. (local images help; +Supabase fetch and 3 CDN scripts unmeasured) |
| Lighthouse Accessibility | ≥ 90 | ~75-85 est. (cog has focus ring; no skip-link yet) |
| Lighthouse SEO | ≥ 95 | ~90 est. (OG + JSON-LD + favicon live; custom domain detached — see risks) |
| Lighthouse Best Practices | ≥ 90 | ~85 est. (all images local HTTPS; third-party CDNs remain) |
| LCP | < 2.5s | Unknown (hero is 192KB JPG / 110KB WebP; needs field measurement) |
| CLS | < 0.1 | Likely ~0 (no dynamic layout shifts; DB render replaces equal-size cards) |
| Total page weight | < 500KB (excl. images) | ~60KB HTML+CSS+JS (GSAP + Supabase from CDN) |

### 9.3 SEO Meta (Target State)

```html
<title>zaleavelle — Skincare Sederhana, Percaya Diri yang Alami</title>
<meta name="description" content="Body wash, body lotion, dan body serum zaleavelle: Emerald Sweet, Blaine Floral, Feminine Blush, Bright Petal.">
<meta property="og:title" content="zaleavelle — Naturally Confident">
<meta property="og:description" content="Rutinitas kulit sederhana, autentik, dan penuh perhatian.">
<meta property="og:image" content="https://zaleavelle.com/og-image.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="manifest" href="site.webmanifest">
```

## 10. Track 5: Maintenance Module (Supabase)

Owner decisions: Supabase backend, no access gate (obscurity only), full CRUD, open-write RLS accepted with JSON backup path.

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| M1 | `products` table holds the catalog (sku, slug, name, category, price_idr, stock, bpom, volume, description, image_webp/jpg/alt, img_focus, shopee_url, wa_number, sort_order, active, last_synced_at) | Live probe returns 4 seeded scent rows |
| M2 | Page renders cards from DB, auto-numbered, static HTML stays as fallback | 4 cards with DB data on success; 4 static cards with backend blocked |
| M3 | Hover-reveal cog bottom-left opens CRUD panel | opacity 0 → visible on hover/focus; faint on touch; ESC closes |
| M4 | Panel edits/adds/deletes/toggles products with live page refresh | Round-trip clean; validation mirrors DB CHECKs |
| M5 | Image upload to `product-images` Storage bucket or paste-URL | Public URL lands in both image fields |
| M6 | JSON backup download of all rows | File downloads with 4+ rows |
| M7 | Stock-zero renders Stok Habis badge + disabled pill (layout stable) | stock=0 card shows badge, no data-cta links |
| M8 | "Tarik dari Shopee" pull-on-demand via `shopee-sync` edge function fills name/price/image/stock | Sync fills form only; save stamps last_synced_at |
| M9 | Go-live checklist: SETUP-SQL v2 → deploy function → 4 listing URLs → probe → seed → sync/OOS test | All green before announcing the module live |

## 11. Milestones

| Milestone | Scope | Status |
|-----------|-------|--------|
| **M1: Conversion Foundation** | Track 1 (E1-E6) + Track 4 (T1-T3, T10) | ✅ Shipped |
| **M2: Content & Polish** | Track 2 (L1, L5-L7 done; L2/L3 open) + Track 3 (B3 done; B1/B2/B4/B5 open) | 🔶 Partial |
| **M3: Performance & Accessibility** | Track 4 (T4-T7) + full Lighthouse pass | ⬜ Open |
| **M4: Catalog & Brand Assets** | Scent-canonical rename, 7 web exports, vector wordmark, OG raster | ✅ Shipped |
| **M5: Maintenance Go-Live** | Track 5 (M1-M9): SQL → deploy → URLs → probe → seed → sync/OOS test | ⬜ Blocked on 3 owner inputs |

### M1 Build Slices (Proposed)

| Slice | Files | Description |
|-------|-------|-------------|
| 1a | `index.html` | Add Shopee/WA links to 4 product cards (E1-E2) |
| 1b | `index.html` | Add UTM params to all links (E3) |
| 1c | `index.html` | Add `gtag` snippet + click event handlers (E4) |
| 1d | `index.html` | Update sticky CTA logic for product-specific text (E5) |
| 1e | `index.html` | Add JSON-LD Product + Organization schemas (T1-T2) |
| 1f | `favicon.ico`, `manifest.json` | Favicon + PWA manifest (T3) |
| 1g | `index.html` | Optimize `<title>` and meta description (T10) |

## 12. Risks & Open Questions

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| ~~Product images unavailable~~ | Resolved M2 — 7 local exports live | Reserve shots documented in §7.2 |
| GSAP CDN dependency (no self-hosted) | CDN outage breaks sticky-stack | Acceptable for MVP; static fallback layout holds content |
| Shopee product URLs may change | Broken CTAs / stale sync | Single store link per product today; per-product URLs required for sync — update in panel |
| CNAME/custom-domain drift | OG + JSON-LD absolute URLs 404 if domain detached (observed 2026-09-21) | Repoint to canonical host or reattach domain; verify with a link checker |
| Open-write RLS abuse | Anyone can edit products via anon endpoint | CHECK constraints narrow damage; JSON backup button; revisit one-admin login |
| Shopee API blocking sync | "Tarik dari Shopee" fails on bot-guards | Inline error + manual fill fallback; no silent overwrites by design |
| Provisional seed stock (100) | False availability signal | Owner sets real counts before go-live; flagged in panel docs |
| Slot-carryover prices unconfirmed | Wrong prices displayed | Single table to swap once the real price list arrives |

### Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| Q1 | Shopee primary vs WhatsApp chat for CTAs? | — | ✅ Resolved: Shopee primary, WA secondary |
| Q2 | Is i18n (ID/EN toggle) in scope for MVP? | Brand owner | Open — recommend: ID-only, EN as follow-up |
| Q3 | Split index.html into modules now or post-launch? | Developer | Open — single-file kept; revisit if panel code grows |
| Q4 | Product photography mapping? | — | ✅ Resolved: scent-canonical, 4 SKUs mapped, reserve logged |
| Q5 | Same WA number for all products? | — | ✅ Resolved: single number, pre-filled message |
| Q6 | Real per-scent price list? | Brand owner | Open — slot-carryover assumed; blocks price trust |
| Q7 | Real per-product Shopee listing URLs (for sync)? | Brand owner | Open — blocks M9 sync test |
| Q8 | Edge-function deploy route (CLI vs dashboard)? | Brand owner | Open — blocks M9 go-live |

## 13. Out of Scope (Deferred)

| Item | Deferred To | Rationale |
|------|-------------|-----------|
| Shopping cart on-site | Post-MVP | Shopee handles checkout |
| User accounts | Post-MVP | No loyalty program yet |
| Blog / content hub | Phase 2 | SEO content strategy is separate work |
| Multi-language | Phase 2 i18n track | ID-first launch |
| Scheduled Shopee auto-sync | Future | Pull-on-demand suffices for 4 SKUs |
| A/B testing infrastructure | Post go-live | Need baseline metrics first |

## 14. Appendix: Current State Audit

| Component | Current | Target |
|-----------|---------|--------|
| Products | 4 scent cards, Shopee + WA links, DB-driven when backend live | Real price list to confirm slot-carryover |
| Images | 7 local exports (38–192KB) + OG raster, zero picsum | None — reserve logged |
| Analytics | gtag stub + select_item tracking live; GA ID unset | Set `ZV_GA_ID` to activate |
| SEO meta | Full OG + JSON-LD + SVG favicon; absolute URLs host-sensitive | Reattach domain or repoint after CNAME drift |
| Accessibility | Cog has focus ring; page lacks skip-link + full focus-visible | M3 |
| Performance | Local images; Supabase fetch unmeasured | M3 Lighthouse pass |
| Social proof | None | Testimonials or IG embed |
| FAQ | Draft copy only (§7.3), no page block | Page section |
| CTA logic | Product-specific Shopee/WA links + product-aware sticky | None |
| Maintenance | Code live, static fallback active; DB + deploy pending | M9 go-live checklist |

---

*This PRD is versioned in `PRD.md` at project root. Update after each milestone completion.*
