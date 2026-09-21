# Gates: Supabase maintenance module (M8)

Scope: Hover-reveal cog + Supabase-backed full-CRUD product maintenance on a static single-file page. No gate by owner decision; open-write RLS accepted with JSON backup path.

- [x] M8.1: Cog fixed bottom-left, transparent, opacity 0 → hover/focus reveal
  CHECK: grep -c "maintCog" index.html
  EXPECT: >=8
  EVIDENCE: 9 maintCog refs (button, CSS, JS open/close)

- [x] M8.2: Panel CRUD (list/edit/add/delete/active-toggle) wired to `products` table
  CHECK: grep -c "from(\"products\")\|from('products')" index.html
  EXPECT: >=5
  EVIDENCE: 6 from("products") queries (fetch, list, delete, save, backup, refresh)

- [ ] M8.3: `public.products` exists with seed rows (owner runs SETUP-SQL)
  CHECK: curl REST products?select=*&limit=1 with publishable key
  EXPECT: 200 + 4 rows
  EVIDENCE: pending (live probe)

- [ ] M8.4: Page renders DB cards on load; static HTML intact as fallback
  CHECK: load page with network, count .p-card; block backend, count .p-card
  EXPECT: 4 and 4
  EVIDENCE: pending (browser test by owner or next session)

- [ ] M8.5: E2E CRUD round-trip from panel (add → shows in stack → delete → gone)
  CHECK: manual panel test against live project
  EXPECT: round-trip clean, JSON backup downloads
  EVIDENCE: pending

- [x] M8.6: All inline scripts parse
  CHECK: node --check on extracted blocks
  EXPECT: clean
  EVIDENCE: ALL JS SYNTAX OK (5 blocks)

- [x] M8.7: Panel clicks don't pollute analytics (no data-cta in panel)
  CHECK: grep panel block for data-cta
  EXPECT: 0 in maint HTML (page-level hooks unchanged)
  EVIDENCE: 0 data-cta in panel lines 575-619 (sole hit was the stickyCta line itself)

<!--
- A checked box with EVIDENCE still "pending" counts as UNMET.
- M8.3–M8.5 require the live table; flip when the owner confirms SETUP-SQL.
-->
