# PRD: zaleavelle — Product Requirements Document

> Version 1.3 · 2026-09-21
> Author: opencode (AI-assisted)
> Status: Phase 8 code complete — awaiting SETUP-SQL run for live verify

---

## 1. Problem Statement

zaleavelle is an Indonesian DTC skincare brand with a single-file landing page (`index.html`, 519 lines) that showcases 4 products. The current page is a polished Awwwards-style showcase but lacks the conversion infrastructure, analytics, SEO foundations, and content depth needed to drive measurable business outcomes. Every CTA links to an on-page anchor — none drive directly to Shopee or WhatsApp purchase flows.

**Core problem:** The landing page is a beautiful brand statement that does not convert.

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
- **Friction points:** Unclear which product to buy first, no social proof on page, no direct purchase links

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
| L1 | Replace all picsum sample images with real brand photography | Zero `picsum.photos` URLs in production HTML |
| L2 | Add social proof / UGC section | ≥ 3 customer testimonials with names, or IG embed grid |
| L3 | Add FAQ section | ≥ 5 questions covering shipping, returns, ingredients, routine, suitability |
| L4 | Polish Indonesian copy | Tone: warm, casual, Gen-Z ID. No formal/baku register. Review all `class="sub"`, `class="why"`, step descriptions |
| L5 | Improve sticky CTA logic | Show only after hero scroll AND not in contact section. Show product-specific text. Handle mobile safe area insets |
| L6 | Add favicon | 32x32 + 180x180 Apple Touch Icon using brand wordmark or rose mark |
| L7 | Add Open Graph + Twitter Card meta tags | `og:title`, `og:description`, `og:image`, `twitter:card` with real brand image |

### 7.2 Image Pipeline

| Image | Dimensions | Source | Format | Fallback |
|-------|-----------|--------|--------|----------|
| Hero | 1200×1400 | Brand shoot | WebP + JPG | Gradient radial (existing) |
| Confidence Set | 900×1100 | Product photo | WebP + JPG | Gradient radial |
| Glow Elixir | 800×900 | Product photo | WebP + JPG | Gradient radial |
| Soft Skin Lotion | 800×900 | Product photo | WebP + JPG | Gradient radial |
| Calm Ritual Scrub | 800×900 | Product photo | WebP + JPG | Gradient radial |
| Ritual lifestyle | 1600×800 | Lifestyle photo | WebP + JPG | Gradient radial |
| Favicon | 32×32 / 180×180 | Vector wordmark | PNG | — |
| OG image | 1200×630 | Brand composite | JPG | — |

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
| T1 | Add JSON-LD Product schema for all 4 products | `ld+json` script tag with `@type: Product`, `name`, `price`, `priceCurrency`, `image`, `brand` |
| T2 | Add JSON-LD Organization schema | `@type: Organization`, `name`, `url`, `sameAs` (social links) |
| T3 | Add favicon + manifest.json | Browser tab shows brand mark; `manifest.json` with name, icons, theme_color |
| T4 | Lighthouse Performance ≥ 90 (mobile) | Run Lighthouse, paste score in progress.md |
| T5 | Lighthouse Accessibility ≥ 90 | Run Lighthouse, paste score in progress.md |
| T6 | Add skip-link for keyboard navigation | Visible on Tab, jumps to `<main>` |
| T7 | Add `focus-visible` styles | Visible focus ring on all interactive elements |
| T8 | Consider CSS/JS split (decision deferred) | Document decision in Decisions table — MVP keeps single-file |
| T9 | Image optimization pipeline | WebP variants with `<picture>` fallback to JPG |
| T10 | Meta description + title optimized | `<title>` ≤ 60 chars, `<meta name="description">` ≤ 155 chars, primary keyword: "skincare Indonesia" |

### 9.2 Performance Budget

| Metric | Target | Current (estimated) |
|--------|--------|---------------------|
| Lighthouse Performance | ≥ 90 | ~75-85 (picsum + GSAP CDN) |
| Lighthouse Accessibility | ≥ 90 | ~70-80 (no skip-link, no focus-visible) |
| Lighthouse SEO | ≥ 95 | ~60-70 (no OG, no JSON-LD, no favicon) |
| Lighthouse Best Practices | ≥ 90 | ~80 (no HTTPS image optimization) |
| LCP | < 2.5s | Unknown (picsum CDN dependent) |
| CLS | < 0.1 | Likely ~0 (no dynamic layout shifts) |
| Total page weight | < 500KB (excl. images) | ~45KB (HTML+CSS+JS, GSAP from CDN) |

### 9.3 SEO Meta (Target State)

```html
<title>zaleavelle — Skincare Sederhana, Percaya Diri yang Alami</title>
<meta name="description" content="Rutinitas tiga langkah yang lembut untuk kulit lembap dan tenang. Confidence Set, Glow Elixir, Soft Skin Lotion, Calm Ritual Scrub.">
<meta property="og:title" content="zaleavelle — Naturally Confident">
<meta property="og:description" content="Rutinitas kulit sederhana, autentik, dan penuh perhatian.">
<meta property="og:image" content="https://zaleavelle.com/og-image.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
```

## 10. Track 5: Maintenance Module (Supabase)

Owner decisions: Supabase backend, no access gate (obscurity only), full CRUD, open-write RLS accepted with JSON backup path.

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| M1 | `products` table holds the catalog (slug, name, category, price_idr, description, image_webp/jpg/alt, img_focus, shopee_url, wa_number, sort_order, active) | Live probe returns 4 seeded scent rows |
| M2 | Page renders cards from DB, auto-numbered, static HTML stays as fallback | 4 cards with DB data on success; 4 static cards with backend blocked |
| M3 | Hover-reveal cog bottom-left opens CRUD panel | opacity 0 → visible on hover/focus; faint on touch; ESC closes |
| M4 | Panel edits/adds/deletes/toggles products with live page refresh | Round-trip clean; validation mirrors DB CHECKs |
| M5 | Image upload to `product-images` Storage bucket or paste-URL | Public URL lands in both image fields |
| M6 | JSON backup download of all rows | File downloads with 4+ rows |

## 11. Milestones

| Milestone | Scope | Target |
|-----------|-------|--------|
| **M1: Conversion Foundation** | Track 1 (E1-E6) + Track 4 (T1-T3, T10) | Week 1 |
| **M2: Content & Polish** | Track 2 (L1-L7) + Track 3 (B1-B5) | Week 2 |
| **M3: Performance & Accessibility** | Track 4 (T4-T9) + full Lighthouse pass | Week 3 |

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
| Product images not available from brand owner | Blocks L1, degrades conversion | Use gradient fallbacks with real product names; image pipeline ready for swap |
| GSAP CDN dependency (no self-hosted) | CDN outage breaks sticky-stack | Acceptable for MVP; add fallback: stack cards collapse to static layout |
| Shopee product URLs may change | Broken CTAs | Use Shopee store link as single redirect; update per-product links in one place |
| Indonesian copy quality | Brand perception | Flag for brand owner review before M2 launch |

### Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| Q1 | Should product CTAs link to Shopee product pages or WhatsApp chat? | Brand owner | Open — recommend: Shopee primary, WhatsApp secondary |
| Q2 | Is i18n (ID/EN toggle) in scope for MVP? | Brand owner | Open — recommend: ID-only, EN as follow-up |
| Q3 | Should we split index.html into modular files now or post-launch? | Developer | Open — recommend: defer to post-M3 |
| Q4 | What is the brand's photography status? When will real images be available? | Brand owner | Open — blocks L1 |
| Q5 | Should the WhatsApp number be the same for all products, or per-product agents? | Brand owner | Open — recommend: single number, pre-filled message |

## 13. Out of Scope (Deferred)

| Item | Deferred To | Rationale |
|------|-------------|-----------|
| Shopping cart on-site | Post-MVP | Shopee handles checkout |
| User accounts | Post-MVP | No loyalty program yet |
| Blog / content hub | Phase 2 | SEO content strategy is separate work |
| Multi-language | Phase 2 i18n track | ID-first launch |
| A/B testing infrastructure | Post-M1 | Need baseline metrics first |

## 14. Appendix: Current State Audit

| Component | Current | Target |
|-----------|---------|--------|
| Products | 4 scent-named cards with Shopee + WA links | Same (prices by slot until price list arrives) |
| Images | 6 local web assets (WebP + JPG, ~40–190KB) + OG raster | Same (reserve: Classic Pink, Flavia Floral, alternates) |
| Analytics | None | GA4 gtag with item-level events |
| SEO meta | Basic title + description | Full OG + JSON-LD + favicon |
| Accessibility | Basic aria labels | Skip-link, focus-visible, Lighthouse ≥90 |
| Performance | ~75-85 Lighthouse | ≥90 Lighthouse, LCP <2.5s |
| Social proof | None | Testimonials or IG embed |
| FAQ | None | ≥5 questions |
| CTA logic | All link to `#produk` | Product-specific Shopee/WA links |

---

*This PRD is versioned in `PRD.md` at project root. Update after each milestone completion.*
