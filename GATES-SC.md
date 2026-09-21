# Gates: Lite Scarlett rebuild (SC)

Scope: Lite-only teardown, marquee deletion, Scarlett-style tabs+grid replacing the sticky stack, promo carousel, real-only discount badges. All Phase 8/9 functionality preserved.

- [x] SC1: Zero dark-mode remnants
  CHECK: grep -c "data-theme|themeBtn|zv-theme|prefers-color-scheme|theme-toggle" index.html
  EXPECT: 0
  EVIDENCE: 0 matches

- [x] SC2: Zero marquee remnants
  CHECK: grep -c "marquee|scrollx" index.html
  EXPECT: 0
  EVIDENCE: 0 matches

- [x] SC3: Tabs + grid present, stack pin logic gone
  CHECK: grep -c "promo-slide|data-tab|disc-badge|was-price" index.html
  EXPECT: >=10
  EVIDENCE: 23 refs (carousel, tabs, badge, was-price)

- [x] SC4: Functionality contract kept (.p-card + data-* + panel hooks)
  CHECK: grep -c "p-card|data-cta|zvRenderProducts|maintCog" index.html
  EXPECT: >=20
  EVIDENCE: 48 refs (cards, tracking hooks, renderer, cog)

- [x] SC5: JS parses + eyebrow budget (2 eyebrows, 7 sections)
  CHECK: node --check on extracted blocks
  EXPECT: clean
  EVIDENCE: ALL JS SYNTAX OK (5 blocks)

- [x] SC6: No invented discounts (badge gated on compare_at_price)
  CHECK: grep "cmp > price" guard in zvCompare
  EXPECT: present
  EVIDENCE: zvCompare returns empty badge/was unless compare_at_price > price

- [x] SC7: Square tiles + serum zoom hook
  CHECK: grep -c "aspect-ratio: 1/1|zoom-out" index.html
  EXPECT: >=3
  EVIDENCE: 6 refs (square rule, zoom rules, static class, renderer flag)

- [x] SC8: WA-only purchase CTAs (no Keranjang/Shopee purchase links)
  CHECK: grep -c "Keranjang" index.html + shopee data-cta scope
  EXPECT: 0 and social-only
  EVIDENCE: 0 Keranjang; single shopee data-cta is the social-grid channel link

<!--
- A checked box with EVIDENCE still "pending" counts as UNMET.
-->
