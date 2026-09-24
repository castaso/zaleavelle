# Gates: Lite Scarlett rebuild (SC) — PARTLY RETIRED in Phase 12

Scope: Lite-only teardown, marquee deletion, Scarlett-style tabs+grid replacing the sticky stack, promo carousel, real-only discount badges. All Phase 8/9 functionality preserved.
Phase 12 removed the tabbed grid, cards, sticky CTA, and backend: grid-era gates below are ABANDONed per repo rule (visible surrender, not silent narrowing). SC1/SC2/SC5 still hold.

- [x] SC1: Zero dark-mode remnants
  CHECK: grep -c "data-theme|themeBtn|zv-theme|prefers-color-scheme|theme-toggle" index.html
  EXPECT: 0
  EVIDENCE: 0 matches (re-verified 2026-09-24)

- [x] SC2: Zero marquee remnants
  CHECK: grep -c "marquee|scrollx" index.html
  EXPECT: 0
  EVIDENCE: 0 matches (re-verified 2026-09-24)

- [ ] SC3: Tabs + grid present, stack pin logic gone
  CHECK: grep -c "promo-slide|data-tab|disc-badge|was-price" index.html
  EXPECT: >=10
  EVIDENCE: 13 refs but tabs/grid gone — survivors are promo carousel + brand-card CSS only
  ABANDON: SC3 — tabbed BEST SELLER grid deleted in Phase 12 (replaced by #shop Odoo banner)

- [ ] SC4: Functionality contract kept (.p-card + data-* + panel hooks)
  CHECK: grep -c "p-card|data-cta|zvRenderProducts|maintCog" index.html
  EXPECT: >=20
  EVIDENCE: 12 refs, all data-cta tracking hooks — cards, renderer, and cog deleted
  ABANDON: SC4 — contract retired with grid + backend in Phase 12; tracking hooks live on in GATES-SEO S4

- [x] SC5: JS parses + eyebrow budget (2 eyebrows, 7 sections)
  CHECK: node --check on extracted blocks
  EXPECT: clean
  EVIDENCE: ALL JS SYNTAX OK (3 blocks post-Phase 12/13; was 5)

- [ ] SC6: No invented discounts (badge gated on compare_at_price)
  CHECK: grep "cmp > price" guard in zvCompare
  EXPECT: present
  EVIDENCE: zvCompare deleted with the data layer — no discounts renderable at all
  ABANDON: SC6 — discount machinery deleted in Phase 12; no prices on-page (Odoo owns pricing)

- [ ] SC7: Square tiles + serum zoom hook
  CHECK: grep -c "aspect-ratio: 1/1|zoom-out" index.html
  EXPECT: >=3
  EVIDENCE: 1 ref — brand-card logo only, product tiles gone
  ABANDON: SC7 — tiles deleted in Phase 12

- [ ] SC8: WA-only purchase CTAs (no Keranjang/Shopee purchase links)
  CHECK: grep -c "Keranjang" index.html + shopee data-cta scope
  EXPECT: 0 and social-only
  EVIDENCE: 0 Keranjang still true, but purchase CTAs are now Odoo (data-cta="odoo" x5), WA support-only
  ABANDON: SC8 — WA-only flow superseded by Odoo-primary in Phase 12

<!--
- A checked box with EVIDENCE still "pending" counts as UNMET.
-->
