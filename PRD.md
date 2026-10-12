# PRD: zaleavelle — Product Requirements Document

> Version 2.7 · 2026-10-12
> Author: opencode (AI-assisted)
> Status: Phase 16 code complete (brand overhaul to the soft-luxury botanical palette; page moved to English; `tools/check.py` added as the verification harness)

---

## 1. Problem Statement

zaleavelle is an Indonesian DTC body care brand served by a single-file static landing page (`index.html`). Since v2.2 the on-page marketplace has been removed: no cart, no backend, no sticky CTA. Purchase happens exclusively on the official store (`https://beli.zaleavelle.com/shop`).

**Phase 16 (this version)** replaced the visual system rather than the commerce model. The page shipped a playful, sticker-and-tilt design built around a single deep-rose accent, which contradicted the owner's brand documentation: *elegant, graceful, empowering, fresh and minimalist*, with a palette of petal pink, warm nude, golden apricot, sage and champagne on an alabaster ground. Alongside the palette change the page moved from Indonesian to English (owner decision), and three real defects were fixed that predate this phase: an unparseable `site.webmanifest`, a wordmark whose SVG viewBox rendered it at roughly a third of its intended size, and figure images whose HTML `height` attribute silently defeated their `aspect-ratio`.

---

## 2. Goals

| # | Goal | Metric | Target |
|---|------|--------|--------|
| G1 | Increase landing-to-shop clicks | Click-through rate from CASTADOO CTAs (`data-cta="odoo"`) to `beli.zaleavelle.com/shop` | ≥ 8% of `#shop` banner views |
| G2 | Strengthen brand recall | Time on page + return visits (GA4) | ≥ 90s avg session, ≥ 15% return rate within 30 days |
| G3 | Improve SEO + mobile performance | Lighthouse Performance score (mobile), LCP, CLS | ≥ 90 score, LCP < 2.5s, CLS < 0.1 |
| G4 | Page matches the brand system | `python tools/check.py` | 41 of 41 checks pass |

---

## 3. Non-Goals

| # | Non-Goal | Rationale |
|---|----------|-----------|
| NG1 | Full e-commerce checkout on-site | The official store is the payment/logistics backbone; no cart on zaleavelle |
| NG2 | User accounts / login | Out of scope for MVP; community engagement via social only |
| NG3 | ~~Multi-language at launch~~ → English-only (v2.7) | Owner decision 2026-10-12: the page is now English throughout. Indonesian returns remain a possible follow-up, not a launch requirement |
| NG4 | Mobile app | Web-only |
| NG5 | Paid ad creative pipeline | PRD covers the owned landing page |
| NG6 | On-page pricing (v2.7) | Explicitly confirmed marketing-only. No price, no cart, no per-product buy button appears on the landing page |

---

## 4. Users & Journeys

### 4.1 Primary Persona: Body-Care Buyer (Indonesia, mobile-first)

- **Age:** 20–40, Indonesian, mobile-first. Broadened in v2.7 from the narrower Gen-Z framing, to match the brand documentation's stated audience.
- **Discovery:** TikTok / Instagram Reels → landing page → official store, or WhatsApp first.
- **Friction points:** prices and stock live off-page; no social proof on page; catalog names must match the scents named in the range section.

### 4.2 User Journey

```
Ad / Social Post → zaleavelle landing page
  → Hero: brand promise + Shop now
  → The range: four scents, described, no prices
  → #shop: where the transaction lives
  → CTA → official store (beli.zaleavelle.com/shop, new tab)
  → OR WhatsApp: "Hello zaleavelle!"
  → Purchase → Return visit: community section → IG/TikTok follow
```

---

## 5. Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Single-file HTML | No build step; the storefront is fully static |
| ~~ID-first language~~ → **English-only** (v2.7) | Owner decision. All copy, meta, JSON-LD and the webmanifest were rewritten |
| Official store as sole storefront | Marketplace removed in v2.3; all buy CTAs link to `beli.zaleavelle.com/shop` |
| GA4 gtag for analytics | Lightweight; stub queues events until `ZV_GA_ID` is set |
| WebP with JPG fallback | Modern format for perf, JPG fallback for older browsers |
| Self-hosted woff2 (v2.7) | The old display stack (`Bodoni MT`, `Didot`) does not exist on iOS or Android, so most visitors silently rendered Georgia. Cormorant Garamond (named in the brand docs) and Geist are now vendored as latin-subset woff2, 89 KB total, preloaded |
| Palette rebuilt on measured contrast (v2.7) | The documented accent (`#F6B78E`) fails as white-on-apricot (1.74:1). Buttons pair it with espresso text at 4.71:1 instead; borders use `#B4601F` at 3.92:1 because apricot-on-alabaster is only 1.50:1 |
| Contrast harness (v2.7) | Every colour pair is asserted by `tools/check.py`, so a future palette edit cannot silently regress WCAG AA |
| Light theme only (v2.7) | PRD S1 lite-only decision, retained and now explicit. The skill's dual-mode default is deliberately overridden |
| Product showcase is editorial, not commerce (v2.7) | Four scents shown with real photography. No prices, no per-tile buy buttons, so the marketing-only boundary holds |
| Image pipeline script | `tools/build-web-images.py` regenerates every web export from `assets/` with a single command. Crops are documented inline because the source art is AI-generated marketing creative with Indonesian copy baked into the frame |

---

## 6. Track 1: E-Commerce Conversion

### 6.1 Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| E1 | Every buy CTA links out to the official store in a new tab | `href="https://beli.zaleavelle.com/shop"` with `target="_blank" rel="noopener"` and `data-cta="odoo"`; WhatsApp CTAs are support-only |
| E2 | Shopee fully removed from shopper UI | Zero `data-cta="shopee"`, zero `s.shopee.co.id` links outside JSON-LD `sameAs` (known SEO debt, owner-deferred) |
| E3 | UTM taxonomy defined and documented | Table in PRD (§6.2) |
| E4 | Event tracking on CTA clicks | `select_item` queued on every `[data-cta]` click with product name + `utm_content` |
| E5 | Sticky CTA deleted | No floating buy button; nav + hero + `#shop` + footer carry purchase intent |
| E6 | No prices on-page | Confirmed marketing-only in v2.7 |
| E7 | One label per purchase intent (v2.7) | Every `data-cta="odoo"` link reads "Shop now"; every `data-cta="whatsapp"` link reads "WhatsApp". Asserted by `tools/check.py` |

### 6.2 UTM Taxonomy

| Placement | utm_source | utm_medium | utm_campaign | utm_content |
|-----------|------------|------------|--------------|-------------|
| Nav `Shop now` | zaleavelle | referral | landing_page | nav_cta |
| Hero `Shop now` | zaleavelle | referral | landing_page | hero_cta |
| `#shop` banner | zaleavelle | referral | landing_page | shop_banner |
| `#shop` WhatsApp | zaleavelle | referral | landing_page | shop_support |
| Community `Shop now` | zaleavelle | referral | landing_page | odoo_profile |
| Footer `Shop now` | zaleavelle | referral | landing_page | footer_cta |

> v2.7 changes: `nav_link` and `promo_cta` are **retired** (the nav link/button were merged into one CTA; the 3-slide promo carousel was deleted). `hero_cta` and `footer_cta` are **new**. The four surviving keys are unchanged, so GA4 history stays continuous.
> `data-cta="odoo"` is retained as the analytics key even though the visible brand is "CASTADOO Shop", for the same continuity reason recorded in v2.6.

---

## 7. Track 2: Landing Page Optimization

| ID | Requirement | Status |
|----|-------------|--------|
| L1 | Real brand photography, no placeholders | ✅ No `picsum.photos` anywhere |
| L2 | Social proof / UGC | ⬜ Still open. No testimonials or IG embed on page |
| L3 | FAQ section | ✅ `#faq` with 6 `<details>`, mirrored verbatim into `FAQPage` |
| L4 | Copy polish | ✅ Rewritten in English (v2.7) |
| L7 | Open Graph + Twitter Card | ✅ Absolute URLs on `zaleavelle.com` |
| L8 | Hamburger drawer under 1080px | ✅ Full-screen drawer, ESC / in-page / media-query close |
| L9 | Full-width stacked CTAs on phone | ✅ Under 780px |
| L11 | Product showcase | ✅ **New in v2.7.** Four scents, editorial, no prices |

---

## 8. Track 3: Brand & Content

### 8.1 Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| B1 | Ritual expanded into a real sequence | ✅ Vertical timeline: Cleanse, Treat, Seal (v2.7) |
| B2 | Strengthen the manifesto | ✅ Founder origin added to the About section (v2.7) |
| B3 | Community links all work | ✅ IG / TikTok / WhatsApp, new tab, tagged |
| B6 | Brand tokens match the documented palette | ✅ Rebuilt in v2.7, see §8.2 |
| B7 | Typography matches the documented direction | ✅ Cormorant Garamond display + Geist body, self-hosted (v2.7) |

### 8.2 Brand System (Locked, v2.7)

Replaces the v2.6 deep-rose system. Every pair below is asserted by `tools/check.py` with its measured ratio.

| Token | Value | Role | Measured contrast |
|-------|-------|------|-------------------|
| Alabaster | `#F2EEE6` | Page base, footer text | 7.08:1 with espresso |
| Petal Pink | `#F7D6DA` | Community panel surface | 4.75:1 with secondary ink |
| Warm Nude | `#FCE8D6` | Shop panel surface | 5.38:1 with secondary ink |
| Sage | `#D7E0D1` | Ritual band surface | 6.04:1 with espresso |
| Champagne | `#E6C9A3` | Reserved edge accent | 5.17:1 with espresso |
| Golden Apricot | `#F6B78E` | **Accent. Buttons only** | 4.71:1 with espresso text |
| Deep Apricot | `#B4601F` | Button hover, borders, focus ring | 3.92:1 on alabaster |
| Muted Warm Espresso | `#5E4B43` | All primary text, all borders | AAA on alabaster |
| Darkened Taupe | `#6B5C53` | All secondary text | 5.53:1 on alabaster |

**Rejections, both measured rather than assumed.** White on apricot is 1.74:1, so no white text ever sits on an apricot button. Apricot on alabaster is 1.50:1, so apricot is never used as a border or icon stroke. The documented `#8A786E` taupe was 3.64:1 on alabaster and fails AA for body text; it is darkened to `#6B5C53`.

**Palette note.** Sage is the load-bearing colour. Without it the page reads as generic cream, which is the default failure mode for this brand category.

| Token | Value |
|-------|-------|
| Display font | Cormorant Garamond (self-hosted, 400 + 400 italic) |
| Body font | Geist (self-hosted, variable 100–900) |
| Card radius | 14px |
| Media radius | 18px |
| Button radius | 999px |
| Motion spring | `cubic-bezier(0.16, 1, 0.3, 1)` |
| z-scale | nav 40 / drawer 41 / toggle 42 / wordmark 43 / grain 60 / skip 100 |

**Shape rule:** no tilt, no offset shadows, no rotated stickers. The v2.6 "tilt plus hard offset shadow" system is retired.

**Design dials:** `DESIGN_VARIANCE 7` / `MOTION_INTENSITY 5` / `VISUAL_DENSITY 3`, down from 9/8/3 in v2.6.

---

## 9. Track 4: Technical Hardening

| ID | Requirement | Status |
|----|-------------|--------|
| T1 | JSON-LD Product schema | ✅ 7 Products, BPOM + size per product, offers URL-only |
| T2 | Organization schema | ✅ |
| T3 | Favicon + manifest | ✅ **Fixed in v2.7:** `site.webmanifest` was invalid JSON (a corrupt byte in the `name` field) and PWA install was broken |
| T4 | Lighthouse Performance ≥ 90 | ⬜ Open, field run still needed |
| T5 | Lighthouse Accessibility ≥ 90 | ⬜ Open, field run still needed |
| T6 | Skip link | ✅ |
| T7 | `focus-visible` styles | ✅ 2px deep-apricot ring at 3.92:1 |
| T11 | Safe-area support | ✅ |
| T12 | 44px minimum tap targets | ✅ 48px on buttons, 44px on the toggle |
| T13 | No horizontal overflow on phone | ✅ Verified at a true 390px viewport |
| T14 | Deterministic verification (v2.7) | ✅ `python tools/check.py`, 41 mechanical checks |

### 9.2 Performance Budget

| Metric | Target | Current |
|--------|--------|---------|
| HTML + CSS + JS | < 500 KB | ~35 KB, zero third-party JS |
| Fonts | — | 89 KB, 3 woff2, preloaded |
| Images | — | 607 KB of WebP across 8 files; hero 147 KB is the LCP element |
| LCP | < 2.5s | Not field-measured |
| CLS | < 0.1 | Every image carries explicit `width`/`height` |

### 9.3 SEO Meta

```html
<title>zaleavelle | Body Care for a Naturally Confident Glow</title>   <!-- 53 chars -->
<meta name="description" content="Body wash, body lotion and body serum with niacinamide, swiftlet nest and calendula. Seven BPOM-registered variants, gentle enough for every morning.">  <!-- 149 chars -->
```

---

## 10. Verification

`python tools/check.py` runs every mechanical gate. Output is pasted into `GATES-BRAND.md` as evidence.

```
41 of 41 checks passed
```

---

## 11. Risks & Open Questions

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Official store dependency | An outage breaks every purchase path | Keep the WhatsApp CTA as the contact fallback |
| English-only copy (v2.7) | Indonesian search traffic may soften | `lang="en"` and `hreflang` set correctly; monitor Search Console after deploy |
| Source photography (v2.7) | Every raw asset in `assets/` is AI-generated marketing creative with Indonesian copy printed into the frame. Two crops in `build-web-images.py` work around this. A proper shoot removes the workaround | Documented per-job in the script |
| CNAME drift | OG and JSON-LD absolute URLs 404 if the domain detaches | Verify with a link checker post-deploy |
| `beli.zaleavelle.com` TLS | All 6 buy CTAs and 7 schema offers depend on it | Verify HTTPS 200 before deploy |
| Hero image weight | 147 KB WebP LCP | Preloaded; the square variant is unused and can be deleted if the hero ever becomes portrait |

### Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| Q2 | Bring Indonesian back as a second locale? | Brand owner | Open, deprioritised |
| Q10 | Official store catalog names match the four scents shown on-page? | Brand owner | 🔶 Unverified since v2.7 |
| Q11 | Visual QA on a physical iPhone SE / Android 360px? | Developer | Partly closed, verified headless at 390px |
| Q12 | Testimonials for the still-open social proof gap (L2)? | Brand owner | Open |

---

## 12. Out of Scope (Deferred)

| Item | Deferred To | Rationale |
|------|-------------|-----------|
| Shopping cart on-site | Never, for now | Official store handles checkout |
| Blog / content hub | Phase 2 | Separate SEO strategy |
| Multi-language | Phase 2 | English-only at launch (v2.7) |
| Dark mode | Not planned | Lite-only decision retained |
| A/B testing | Post go-live | Need baseline metrics first |

---

*This PRD is versioned in `PRD.md` at project root. Update after each milestone completion.*
