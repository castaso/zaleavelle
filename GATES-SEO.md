# Gates: CASTADOO + SEO storefront (SEO)

Scope: Phase 12 marketplace removal (CASTADOO sole storefront, static page, backend deleted) + Phase 13 BPOM-doc SEO content (7-product + FAQPage schema, #faq section, keyword meta, crawl files). Verified 2026-09-24; storefront host + copy re-verified 2026-10-05 after the Phase 15 custom-domain migration. **Re-verified 2026-10-12 after the Phase 16 brand overhaul (PRD v2.7), which rewrote every user-facing string into English.**

- [x] S1: All buy CTAs point at the CASTADOO Shop
  CHECK: grep -c "beli\.zaleavelle\.com/shop" index.html
  EXPECT: >=10
  EVIDENCE: 13 refs (6 page CTAs + 7 schema offers) — re-verified 2026-10-05 on the custom domain

- [x] S2: Shopee purged from shopper UI (JSON-LD sameAs debt excepted)
  CHECK: grep -ci "shopee" index.html
  EXPECT: 1
  EVIDENCE: 1 ref — Organization sameAs only (owner-deferred, PRD Q9 context)

- [x] S3: Meta within bounds + canonical present
  CHECK: python tools/check.py
  EXPECT: title <=60, description <=155, canonical present
  EVIDENCE: title 53, description 149, canonical https://zaleavelle.com/ (English as of v2.7; was 58/134 in Indonesian)

- [x] S4: JSON-LD parses — Org + 7 Products + FAQPage, CASTADOO offers, no stale prices
  CHECK: python tools/check.py
  EXPECT: 9 nodes, offers url-only, 0 slot-carryover prices
  EVIDENCE: 9 nodes; offers {url, priceCurrency, availability}; 0 prices; BPOM + size per product; images for the 4 photographed scents only

- [x] S5: All inline scripts parse
  CHECK: python tools/check.py
  EXPECT: clean
  EVIDENCE: 2 inline blocks (was 3; v2.7 deleted the promo carousel's rotation script)

- [x] S6: Visible FAQ matches schema verbatim (FAQPage eligibility)
  CHECK: python tools/check.py
  EXPECT: 6/6 match
  EVIDENCE: 6/6 verbatim match, English both sides. Rewriting the FAQ in v2.7 would have silently broken rich-result eligibility had the schema and the visible answers been edited separately, so the harness diffs them rather than trusting review

- [x] S7: Crawl files exist and validate
  CHECK: robots.txt + sitemap.xml present; sitemap XML parses
  EXPECT: present + valid
  EVIDENCE: robots (allow + sitemap ref); sitemap single-URL, parses OK

- [x] S8: No broken in-page anchors
  CHECK: python tools/check.py
  EXPECT: all resolve
  EVIDENCE: 7 anchors resolve (#main, #range, #ritual, #ingredients, #tentang, #faq, #kontak). v2.7 added #range and #ingredients, and repointed the skip link at #main. **#tentang and #kontak kept their Indonesian IDs on purpose:** renaming them would break any inbound anchor, and an ID is not visible to a visitor

<!--
- A checked box with EVIDENCE still "pending" counts as UNMET.
- S2's single sameAs hit is accepted debt, not failure — see PRD Q9.
-->
