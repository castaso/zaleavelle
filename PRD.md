# PRD: zaleavelle — Product Requirements Document

> Version 2.3 · 2026-09-24
> Author: opencode (AI-assisted)
> Status: Phase 12 code complete (marketplace removed → Odoo Shop sole storefront, page fully static); uncommitted

---

## 1. Problem Statement

zaleavelle is an Indonesian DTC skincare brand with a single-file landing page (`index.html`, ~560 lines, fully static). Since v2.2 the on-page marketplace was removed altogether (Phase 12, owner interview 2026-09-24): no product grid, no Supabase backend, no maintenance panel, no sticky CTA. Purchase happens exclusively on the Odoo Shop (`https://zaleavelle.odoo.com/shop`), reached via a `#shop` banner plus nav/promo/kontak CTAs (`data-cta="odoo"`). Ritual/promo copy still names the 4 scents (Emerald Sweet, Blaine Floral, Feminine Blush, Bright Petal) editorially; prices live only on Odoo.

**Core problem:** Conversion now depends on a third-party storefront the page doesn't control — Odoo catalog names/prices must match the landing copy, JSON-LD still advertises 4 on-page Products that no longer exist (SEO mismatch debt), and the page still lacks social proof — so click-through to Odoo can't be measured or trusted end-to-end yet.

## 2. Goals

| # | Goal | Metric | Target |
|---|------|--------|--------|
| G1 | Increase landing-to-shop clicks | Click-through rate from Odoo CTAs (`data-cta="odoo"`) to `zaleavelle.odoo.com/shop` | ≥ 8% of `#shop` banner views |
| G2 | Strengthen brand recall | Time on page + return visits (GA4) | ≥ 90s avg session, ≥ 15% return rate within 30 days |
| G3 | Improve SEO + mobile performance | Lighthouse Performance score (mobile), LCP, CLS | ≥ 90 score, LCP < 2.5s, CLS < 0.1 |

## 3. Non-Goals

| # | Non-Goal | Rationale |
|---|----------|-----------|
| NG1 | Full e-commerce checkout on-site | Odoo Shop is the payment/logistics backbone; no cart on zaleavelle |
| NG2 | User accounts / login | Out of scope for MVP; community engagement via social only |
| NG3 | Multi-language at launch | ID-first; EN can be added in a follow-up i18n track |
| NG4 | Mobile app | Web-only; PWA is a future consideration |
| NG5 | Paid ad creative pipeline | PRD covers owned landing page, not ad campaigns |

## 4. Users & Journeys

### 4.1 Primary Persona: Gen-Z ID Skincare Buyer

- **Age:** 18-26, Indonesian, mobile-first
- **Discovery:** TikTok / Instagram Reels → landing page → Odoo Shop (or WhatsApp for questions)
- **Motivation:** Simple routine, affordable, aesthetic packaging, peer validation
- **Friction points:** Must leave the landing page to see prices/stock; no social proof on page; Odoo catalog names must match the scents named in ritual copy

### 4.2 User Journey (Target State)

```
Ad / Social Post → zaleavelle landing page
  → Hero: brand promise + CTA
  → Shop banner (#shop): catalog pitch + trust points
  → CTA → Odoo Shop (https://zaleavelle.odoo.com/shop, new tab)
  → OR WhatsApp support: "Halo zaleavelle!"
  → Purchase on Odoo
  → Return visit: community section → IG/TikTok follow
```

## 5. Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Single-file HTML for MVP | No build step required; simplicity over modularity |
| ID-first language | Primary audience is Indonesian; EN can be added via i18n follow-up track |
| ~~Shopee as primary CTA~~ → Odoo Shop sole storefront (v2.3) | Owner interview 2026-09-24: marketplace removed altogether; all buy CTAs link out to `zaleavelle.odoo.com/shop` |
| GA4 gtag for analytics | Lightweight, free, industry standard; avoids third-party analytics bloat |
| WebP with JPG fallback | Modern format for perf; JPG fallback for older browsers |
| ~~Supabase as product backend~~ → static page, no backend (v2.3) | Phase 12 deleted the data layer, maintenance panel, and `shopee-sync` function; DB table left untouched server-side |
| ~~Open-write RLS, no access gate~~ → retired with backend (v2.3) | No client writes remain; revisit only if a backend returns |
| Scent names canonical | Photos sell scent-named SKUs; old set/serum/lotion/scrub names retired in M2 |
| ~~Slot-carryover prices~~ → Odoo is price source of truth (v2.3) | No prices on the landing page anymore; Odoo catalog owns pricing/stock |
| SVG favicon over ICO/PNG | No binary tooling in repo; full wordmark illegible at 32px, serif-“z” kept |
| ~~Stock-zero badge semantics~~ → retired with cards (v2.3) | Stock display lives on Odoo now |
| ~~Shopee pull-on-demand sync~~ → retired with backend (v2.3) | `shopee-sync` edge function deleted |
| ~~WA-only purchase flow~~ → Odoo-primary, WA support-only (v2.3) | WA CTAs remain only as support (banner + kontak); no `wa.me` buy links |
| ~~Square tiles + serum zoom hook~~ → retired with grid (v2.3) | `#produk` section replaced by `#shop` banner |
| Single-file kept post-M3 | Split still deferred; page is static with zero backend scripts |

## 6. Track 1: E-Commerce Conversion

### 6.1 Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| E1 | Every buy CTA links out to the Odoo Shop in a new tab | `href="https://zaleavelle.odoo.com/shop"` with `target="_blank" rel="noopener"` and `data-cta="odoo"`; WA CTAs exist support-only (banner + kontak) |
| E2 | Shopee fully removed from shopper UI | Zero `data-cta="shopee"`, zero `s.shopee.co.id` links outside JSON-LD `sameAs` (known SEO debt, owner-deferred) |
| E3 | UTM taxonomy defined and documented | Table in PRD (§6.2) with source/medium/campaign/content per Odoo CTA placement |
| E4 | Event tracking on CTA clicks | `select_item` queued on every `[data-cta]` click with product name + `utm_content`; works with real GA4 once `ZV_GA_ID` is set |
| E5 | ~~Sticky CTA~~ → deleted (v2.3) | No floating buy button; nav `Belanja` + `#shop` banner carry the purchase intent |
| E6 | ~~Price formatting~~ → no prices on-page (v2.3) | Odoo catalog is the single source of truth for price/stock |

### 6.2 UTM Taxonomy (Odoo era — per placement, v2.3)

| Placement | utm_source | utm_medium | utm_campaign | utm_content |
|-----------|------------|------------|--------------|-------------|
| Nav `Belanja` link | zaleavelle | referral | landing_page | nav_link |
| Nav `Beli` button | zaleavelle | referral | landing_page | nav_cta |
| Promo brand slide | zaleavelle | referral | landing_page | promo_cta |
| `#shop` banner primary | zaleavelle | referral | landing_page | shop_banner |
| `#shop` banner WA support | zaleavelle | referral | landing_page | shop_support |
| Kontak `Toko Resmi` | zaleavelle | referral | landing_page | odoo_profile |

> Per-product `*_cta` contents (emerald_sweet_cta, …) retired with the grid — no per-product CTAs remain on-page.

### 6.3 Analytics Events

```javascript
// On Odoo CTA click (delegated [data-cta] listener queues select_item)
gtag('event', 'select_item', {
  item_name: 'Odoo Shop',
  item_category: 'odoo',
  price: 0,
  currency: 'IDR',
  utm_content: 'shop_banner'
});
```

## 7. Track 2: Landing Page Optimization

### 7.1 Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| L1 | Replace all picsum sample images with real brand photography | ✅ Done M2 — zero `picsum.photos` URLs; 7 local exports in `assets/web/` (card images now unused after Phase 12, kept for promo/OG) |
| L2 | Add social proof / UGC section | ⬜ Open — ≥ 3 customer testimonials with names, or IG embed grid |
| L3 | Add FAQ section | ⬜ Open — page has no FAQ block yet (draft copy in §7.3) |
| L4 | Polish Indonesian copy | 🔶 Partial — ritual/promo copy kept (product names editorial-only); `#shop` banner copy new in Phase 12 |
| L5 | ~~Improve sticky CTA logic~~ → sticky deleted (v2.3) | Phase 12 removed `#stickyCta` + tracker; purchase intent lives in nav + `#shop` banner |
| L6 | Add favicon | ✅ Done M1 — crisp SVG serif-“z” + `site.webmanifest` (ICO/PNG skipped, no binary tooling) |
| L7 | Add Open Graph + Twitter Card meta tags | ✅ Done — absolute `https://zaleavelle.com/og-image.jpg` (CNAME drift noted in risks) |

### 7.2 Image Pipeline

| Image | Dimensions | Source file | Weight | Status v2.3 |
|-------|-----------|-------------|--------|-------------|
| Hero | 1080×1350 | `assets/web/fresh-tickled-hero` (.webp + .jpg) | 110 / 192 KB | Live |
| Emerald Sweet card | 900×1125 | `assets/web/emerald-sweet-wash` (.webp + .jpg) | 48 / 93 KB | Unused on-page (grid deleted); kept on disk |
| Blaine Floral card | 900×900 | `assets/web/blaine-floral-lotion` (.webp + .jpg), `object-position: 70%` | 74 / 119 KB | Unused on-page; kept on disk |
| Feminine Blush card | 900×900 | `assets/web/feminine-blush-lotion` (.webp + .jpg) | 59 / 101 KB | Unused on-page; kept on disk |
| Bright Petal card | 800×1000 | `assets/web/bright-petal-serum` (.webp + .jpg) | 62 / 102 KB | Unused on-page; kept on disk |
| Ritual lifestyle | 1600×800 | `assets/web/emerald-ritual` (.webp + .jpg, center crop) | 49 / 109 KB | Live (ritual figure + promo slide 1) |
| OG image | 1200×630 | `assets/web/og-image.jpg` (crawlers need raster) | 76 KB | Live (meta + promo slide 2) |
| Favicon | vector | `favicon.svg` serif-“z” + `site.webmanifest` | <1 KB | Live |
| Reserve (unused) | — | Classic Pink, Flavia Floral + alternate shots in `assets/` | — | — |

### 7.3 FAQ Content (Draft)

1. **Varian aroma apa saja yang tersedia?** — Emerald Sweet (body wash), Blaine Floral dan Feminine Blush (body lotion), Bright Petal (body serum).
2. **Apakah aman untuk kulit sensitif?** — Ya, semua produk zaleavelle diformulasi lembut tanpa paraben.
3. **Bagaimana cara pesan?** — Klik tombol Belanja untuk checkout di Toko Resmi (Odoo Shop), atau chat kami via WhatsApp.
4. **Kapan hasilnya terlihat?** — Kebanyakan pelanggan melihat perbedaan dalam 2-4 minggu.
5. **Apakah ada program reseller?** — Hubungi WhatsApp kami untuk info kerja sama.

## 8. Track 3: Brand & Content

### 8.1 Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| B1 | Expand ritual section with before/after or routine timeline | Visual timeline or step-by-step with real imagery |
| B2 | Strengthen manifesto section | Add founder story or brand origin (2-3 sentences) |
| B3 | Community section links all work | IG / TikTok / Toko Resmi (Odoo) / WhatsApp open in new tab, correct URLs, `data-cta` tagged |
| B4 | Add newsletter / WhatsApp broadcast signup | Email input or WA link for "Tips skincare mingguan" |
| B5 | ~~Marquee text reviewed~~ → marquee deleted (Phase 10) | No marquee on-page; brand rhythm lives in stickers/eyebrows |

### 8.2 Brand System (Locked)

| Token | Value | Usage |
|-------|-------|-------|
| Accent (light) | `#9E3E4D` | Buttons, links, emphasis, stickers |
| Accent (dark) | `#E3A7AC` | Same roles in dark theme |
| Display font | Bodoni MT / Didot / Cormorant Garamond / EB Garamond / Georgia | Hero h1, section h2, blockquote, product names |
| Body font | system-ui stack | Paragraphs, nav, CTAs |
| Mono font | ui-monospace / SF Mono / JetBrains Mono | Eyebrows, labels, prices |
| Card radius | 16px | Ritual steps, shop-points |
| Button radius | 999px (pill) | All buttons |
| Shadow accent | `color-mix(in srgb, var(--accent) 35%, transparent)` | Hard-offset shadows on shop banner, community card, hero media |
| Motion spring | `cubic-bezier(0.16, 1, 0.3, 1)` | All transitions |
| z-scale | nav 40 / grain 60 | Stacking context (sticky CTA + stack cards removed v2.3) |

**Shape rule:** Tilt + hard offset shadow is the system. Applied consistently on the `#shop` banner, community card, and hero media. No second accent color. No neon glows. No AI-purple.

## 9. Track 4: Technical Hardening

### 9.1 Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| T1 | ~~JSON-LD Product schema for all 4 products~~ → known debt (v2.3) | Nodes still live but no on-page catalog; follow-up: strip to Organization-only or point `offers.url` at Odoo |
| T2 | Add JSON-LD Organization schema | ✅ Done — with `sameAs` social links (Shopee URL retained, owner-deferred) |
| T3 | Add favicon + manifest | ✅ Done — `favicon.svg` + `site.webmanifest` + theme-color |
| T4 | Lighthouse Performance ≥ 90 (mobile) | ⬜ Open — run and paste score in progress.md (no backend fetch anymore; should measure clean) |
| T5 | Lighthouse Accessibility ≥ 90 | ⬜ Open — run and paste score in progress.md |
| T6 | Add skip-link for keyboard navigation | ⬜ Open — jumps to `<main>` |
| T7 | Add `focus-visible` styles | ⬜ Open — maintenance cog (the one focus-ringed element) deleted in Phase 12; page-wide ring styles still open |
| T8 | Consider CSS/JS split | ✅ Resolved — single-file kept, zero backend scripts |
| T9 | Image optimization pipeline | ✅ Done — 7 exports, WebP + JPG via `<picture>` |
| T10 | Meta description + title optimized | ✅ Done — 56 / 110 chars; scent names; absolute OG URL |

### 9.2 Performance Budget

| Metric | Target | Current (estimated) |
|--------|--------|---------------------|
| Lighthouse Performance | ≥ 90 | ~85-95 est. (local images; zero backend fetch; zero third-party scripts — only simpleicons images) |
| Lighthouse Accessibility | ≥ 90 | ~75-85 est. (no skip-link yet) |
| Lighthouse SEO | ≥ 95 | ~85-90 est. (OG + JSON-LD live BUT Product-nodes-without-catalog mismatch is a downgrade risk; custom domain detached — see risks) |
| Lighthouse Best Practices | ≥ 90 | ~90 est. (all images local HTTPS; no third-party JS) |
| LCP | < 2.5s | Unknown (hero is 192KB JPG / 110KB WebP; needs field measurement) |
| CLS | < 0.1 | Likely ~0 (fully static; no dynamic rendering at all) |
| Total page weight | < 500KB (excl. images) | ~35KB HTML+CSS+JS (no external JS) |

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

## 10. Track 5: Maintenance Module (Supabase) — RETIRED in v2.3

> Phase 12 deleted the entire module (maintenance cog/panel, Supabase data layer, `shopee-sync` edge function, `supabase/` dir). Requirements M1-M9 below are historical record only — all superseded. The server-side `products` table was left untouched (no SQL drop performed).

| ID | Requirement | Status v2.3 |
|----|-------------|-------------|
| M1 | `products` table catalog | Retired — page no longer reads any table |
| M2 | DB-rendered cards, static fallback | Retired — no cards, no rendering; page is static |
| M3 | Hover-reveal cog + CRUD panel | Retired — cog/panel deleted |
| M4 | Panel CRUD with live refresh | Retired |
| M5 | Image upload / paste-URL | Retired |
| M6 | JSON backup download | Retired |
| M7 | Stock-zero Stok Habis badge | Retired — stock display lives on Odoo |
| M8 | "Tarik dari Shopee" via `shopee-sync` | Retired — function deleted |
| M9 | Go-live checklist (SQL → deploy → URLs → probe → seed → test) | Cancelled — owner inputs no longer needed |

## 11. Track 6: Lite Scarlett Storefront (taste skill) — SUPERSEDED in v2.3

> The tabbed BEST SELLER grid this track built was removed in Phase 12. S1-S3 (lite teardown, marquee deletion, promo carousel) survive; S4-S6 (grid, compare badges, unified tile CTAs, sticky text) are retired with the grid; S7 (GSAP removed) still holds.

| ID | Requirement | Status v2.3 |
|----|-------------|-------------|
| S1 | Lite-only: no dark mode anywhere | ✅ Holds |
| S2 | Marquee deleted | ✅ Holds |
| S3 | Promo hero carousel (3 slides, dots, autoplay) | ✅ Holds (slide-3 CTA retargeted to Odoo) |
| S4 | BEST SELLER tabbed grid | Retired — replaced by `#shop` Odoo banner |
| S5 | Discount badge from real `compare_at_price` | Retired with cards |
| S6 | CTA intents unified / sticky product text | Retired — sticky deleted; single Odoo intent everywhere |
| S7 | GSAP removed | ✅ Holds |

## 12. Milestones

| Milestone | Scope | Status |
|-----------|-------|--------|
| **M1: Conversion Foundation** | Track 1 (E1-E6) + Track 4 (T1-T3, T10) | ✅ Shipped |
| **M2: Content & Polish** | Track 2 (L1, L5-L7 done; L2/L3 open) + Track 3 (B3 done; B1/B2/B4/B5 open) | 🔶 Partial |
| **M3: Performance & Accessibility** | Track 4 (T4-T7) + full Lighthouse pass | ⬜ Open |
| **M4: Catalog & Brand Assets** | Scent-canonical rename, 7 web exports, vector wordmark, OG raster | ✅ Shipped |
| **M5: Maintenance Go-Live** | Track 5 (M1-M9) | ❌ Cancelled — module retired in v2.3, owner inputs no longer needed |
| **M6: Lite Scarlett Storefront** | Track 6 (S1-S7) | 🔶 Partial — S1-S3 + S7 survive; grid requirements (S4-S6) retired in v2.3 |
| **M7: Odoo Storefront Migration** | Phase 12: `#produk` → `#shop` banner, Odoo CTAs, Shopee/backend/sticky deletion | ✅ Code complete, uncommitted; needs browser check + commit |

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

## 13. Risks & Open Questions

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| ~~GSAP CDN dependency (no self-hosted)~~ | Retired — GSAP removed (Phase 10), zero third-party JS | — |
| Odoo Shop dependency | Odoo outage/catalog change breaks all purchase paths; no on-page fallback | Monitor shop availability; keep WA support CTA as contact fallback |
| JSON-LD Product mismatch (NEW v2.3) | 4 Product nodes + prices with no on-page catalog; Google may flag or drop rich results | Follow-up: strip to Organization-only or point `offers.url` at Odoo (owner-deferred) |
| Odoo catalog parity (NEW v2.3) | Ritual copy names 4 scents; if Odoo renames/restocks differently, shoppers bounce | Verify Odoo slugs/names match Emerald Sweet, Blaine Floral, Feminine Blush, Bright Petal |
| ~~Shopee product URLs may change~~ | Retired — no Shopee links in shopper UI | — |
| CNAME/custom-domain drift | OG + JSON-LD absolute URLs 404 if domain detached (observed 2026-09-21) | Repoint to canonical host or reattach domain; verify with a link checker |
| ~~Open-write RLS abuse~~ | Retired with backend — no client writes remain | — |
| ~~Shopee API blocking sync~~ | Retired — `shopee-sync` deleted | — |
| ~~Provisional seed stock (100)~~ | Retired — stock display lives on Odoo | — |
| ~~Slot-carryover prices unconfirmed~~ | Retired — Odoo owns pricing; no prices on-page | — |

### Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| Q1 | Shopee primary vs WhatsApp chat for CTAs? | — | ✅ Superseded v2.3: Odoo Shop sole storefront, WA support-only |
| Q2 | Is i18n (ID/EN toggle) in scope for MVP? | Brand owner | Open — recommend: ID-only, EN as follow-up |
| Q3 | Split index.html into modules now or post-launch? | Developer | Open — single-file kept (560 lines static); revisit only if page grows |
| Q4 | Product photography mapping? | — | ✅ Resolved: scent-canonical, 4 SKUs mapped, reserve logged |
| Q5 | Same WA number for all products? | — | ✅ Resolved: single number 6282121262593, support-only role |
| Q6 | ~~Real per-scent price list?~~ | — | ❌ Closed v2.3: no prices on-page; Odoo owns pricing |
| Q7 | ~~Real per-product Shopee listing URLs (for sync)?~~ | — | ❌ Closed v2.3: sync module deleted |
| Q8 | ~~Edge-function deploy route (CLI vs dashboard)?~~ | — | ❌ Closed v2.3: function deleted |
| Q9 | Strip JSON-LD Products or point offers at Odoo? (NEW v2.3) | Brand owner | Open — Product-nodes-without-catalog mismatch is live SEO debt |
| Q10 | Odoo catalog names match ritual copy? (NEW v2.3) | Brand owner | Open — verify Emerald Sweet / Blaine Floral / Feminine Blush / Bright Petal exist on Odoo |

## 14. Out of Scope (Deferred)

| Item | Deferred To | Rationale |
|------|-------------|-----------|
| Shopping cart on-site | Post-MVP | Odoo Shop handles checkout |
| User accounts | Post-MVP | No loyalty program yet |
| Blog / content hub | Phase 2 | SEO content strategy is separate work |
| Multi-language | Phase 2 i18n track | ID-first launch |
| ~~Scheduled Shopee auto-sync~~ | Retired v2.3 | Sync module deleted with backend |
| A/B testing infrastructure | Post go-live | Need baseline metrics first |

## 15. Appendix: Current State Audit

| Component | Current | Target |
|-----------|---------|--------|
| Products | No on-page catalog — `#shop` banner links out to Odoo Shop | Verify Odoo names match ritual copy (Q10) |
| Images | Hero + ritual + promo/OG live; 4 card images unused on-page, kept on disk | Optional disk cleanup later |
| Analytics | gtag stub + `select_item` on all `[data-cta]` (odoo/whatsapp/social); GA ID unset | Set `ZV_GA_ID` to activate |
| SEO meta | Full OG + SVG favicon; JSON-LD Product nodes are owner-deferred debt | Q9: strip Products or point offers at Odoo |
| Accessibility | No skip-link, no page-wide focus-visible | M3 |
| Performance | Fully static, zero third-party JS; Supabase fetch gone | M3 Lighthouse pass |
| Social proof | None | Testimonials or IG embed |
| FAQ | Draft copy only (§7.3), no page block | Page section |
| CTA logic | Single Odoo intent everywhere (nav ×2, promo, banner, kontak); WA support-only; sticky deleted | None — verify Odoo shop is live |
| Maintenance | Module deleted; page static | None |

---

*This PRD is versioned in `PRD.md` at project root. Update after each milestone completion.*
