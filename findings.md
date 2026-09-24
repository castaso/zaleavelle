# Findings & Decisions

Durable knowledge base for discoveries, evidence, and decisions during zaleavelle PRD work.

## Requirements

- Cover 4 tracks: e-commerce conversion, landing optimization, brand/content, tech split
- Success metrics: (1) increase clicks to Shopee/WA, (2) strengthen brand recall, (3) SEO + mobile perf
- Target audience: Gen-Z Indonesian skincare buyers, mobile-first
- Keep existing design language: Didone wordmark, single rose accent, playful Awwwards aesthetic

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
- **Mobile:** responsive at 968px and 600px breakpoints; nav links hidden on mobile; sticky CTA appears after hero scroll; stickers hidden on <600px
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
| Odoo Shop (`https://zaleavelle.odoo.com/shop`) is the sole purchase channel (2026-09-24) | Owner interview: marketplace section removed altogether; `#shop` banner + nav/promo/kontak CTAs link out with `data-cta="odoo"` |
| Static storefront, no backend | Supabase products fetch, maintenance panel, and `shopee-sync` edge function deleted; page is static HTML again (560 lines) |
| JSON-LD Product nodes retained as known debt | `sameAs` Shopee URL + 4 Product offers kept per owner "leave SEO untouched"; mismatch vs no-catalog page flagged for follow-up |
| Keep single-file for MVP | Simplicity; no build step required; GSAP CDN approach works |
| ID-first, EN as appendix | Primary audience is Indonesian; EN can be added later |
| Analytics via inline script | Avoids external dependencies; GA4 gtag snippet is lightweight |
| ~~Shopee as primary CTA~~ (superseded Phase 12) | ~~Existing Shopee store link~~ → Odoo Shop is now the only purchase channel |

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

*Updated during Phase 1 discovery sweep.*
