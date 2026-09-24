# Gates: Supabase maintenance module (M8) — RETIRED in Phase 12

Scope: Hover-reveal cog + Supabase-backed full-CRUD product maintenance on a static single-file page. No gate by owner decision; open-write RLS accepted with JSON backup path.
Phase 12 deleted the entire module (cog/panel, data layer, `shopee-sync`, `supabase/` dir). All gates below are ABANDONed per repo rule (visible surrender, not silent narrowing). Verified 2026-09-24: 0 maintCog, 0 from("products"), 0 mfSku/mfBpom/mfVolume/mfStock/oos-badge refs in index.html.

- [ ] M8.1: Cog fixed bottom-left, transparent, opacity 0 → hover/focus reveal
  CHECK: grep -c "maintCog" index.html
  EXPECT: >=8
  EVIDENCE: 0 refs — cog deleted
  ABANDON: M8.1 — maintenance cog deleted in Phase 12

- [ ] M8.2: Panel CRUD (list/edit/add/delete/active-toggle) wired to `products` table
  CHECK: grep -c "from(\"products\")\|from('products')" index.html
  EXPECT: >=5
  EVIDENCE: 0 refs — data layer deleted
  ABANDON: M8.2 — panel + data layer deleted in Phase 12

- [ ] M8.3: `public.products` exists with seed rows (owner runs SETUP-SQL)
  CHECK: curl REST products?select=*&limit=1 with publishable key
  EXPECT: 200 + 4 rows
  EVIDENCE: pending (live probe)
  ABANDON: M8.3 — go-live cancelled; page reads no table

- [ ] M8.4: Page renders DB cards on load; static HTML intact as fallback
  CHECK: load page with network, count .p-card; block backend, count .p-card
  EXPECT: 4 and 4
  EVIDENCE: pending (browser test by owner or next session)
  ABANDON: M8.4 — no cards; page is fully static

- [ ] M8.5: E2E CRUD round-trip from panel (add → shows in stack → delete → gone)
  CHECK: manual panel test against live project
  EXPECT: round-trip clean, JSON backup downloads
  EVIDENCE: pending
  ABANDON: M8.5 — panel deleted

- [ ] M8.6: All inline scripts parse
  CHECK: node --check on extracted blocks
  EXPECT: clean
  EVIDENCE: surviving scripts parse (see GATES-SEO S5); this gate's module is gone
  ABANDON: M8.6 — superseded by GATES-SEO S5 for the surviving scripts

- [ ] M8.7: Panel clicks don't pollute analytics (no data-cta in panel)
  CHECK: grep panel block for data-cta
  EXPECT: 0 in maint HTML (page-level hooks unchanged)
  EVIDENCE: panel deleted — vacuously true, gate meaningless
  ABANDON: M8.7 — panel deleted in Phase 12

- [ ] M8.8: Settings fields v2 present (SKU/BPOM/volume/stock) + OOS rendering
  CHECK: grep -c "mfSku|mfBpom|mfVolume|mfStock|oos-badge|form.(sku|bpom|volume|stock)" index.html
  EXPECT: >=10
  EVIDENCE: 0 refs — form deleted (BPOM data now lives in schema + FAQ, see GATES-SEO)
  ABANDON: M8.8 — maintenance form deleted in Phase 12

- [ ] M8.9: Shopee sync fills form from live listing (needs deployed function + listing URLs)
  CHECK: panel sync test against one real listing
  EXPECT: name/price/image/stock filled, last_synced_at stamped on save
  EVIDENCE: pending
  ABANDON: M8.9 — `shopee-sync` function deleted in Phase 12

<!--
- A checked box with EVIDENCE still "pending" counts as UNMET.
- M8.3–M8.5 require the live table; flip when the owner confirms SETUP-SQL.
-->
