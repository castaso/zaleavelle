# Gates: Odoo + SEO storefront (SEO)

Scope: Phase 12 marketplace removal (Odoo sole storefront, static page, backend deleted) + Phase 13 BPOM-doc SEO content (7-product + FAQPage schema, #faq section, keyword meta, crawl files). Verified 2026-09-24.

- [x] S1: All buy CTAs point at the Odoo Shop
  CHECK: grep -c "zaleavelle\.odoo\.com/shop" index.html
  EXPECT: >=10
  EVIDENCE: 12 refs (5 page CTAs + 7 schema offers)

- [x] S2: Shopee purged from shopper UI (JSON-LD sameAs debt excepted)
  CHECK: grep -ci "shopee" index.html
  EXPECT: 1
  EVIDENCE: 1 ref — Organization sameAs only (owner-deferred, PRD Q9 context)

- [x] S3: Meta within bounds + canonical present
  CHECK: title/description lengths, rel="canonical"
  EXPECT: title <=60, description <=155, canonical present
  EVIDENCE: title 58, description 134, canonical https://zaleavelle.com/

- [x] S4: JSON-LD parses — Org + 7 Products + FAQPage, Odoo offers, no stale prices
  CHECK: python json.loads on ld+json block; inspect offers
  EXPECT: 9 nodes, offers url-only, 0 slot-carryover prices
  EVIDENCE: 9 nodes; offers {url, priceCurrency, availability}; 0 stale prices; BPOM + volume per product; images for 4 photographed scents only

- [x] S5: All inline scripts parse
  CHECK: node --check on extracted blocks
  EXPECT: clean
  EVIDENCE: ALL JS SYNTAX OK (3 blocks)

- [x] S6: Visible FAQ matches schema verbatim (FAQPage eligibility)
  CHECK: 6 <details> answers each present in FAQPage mainEntity
  EXPECT: 6/6 match
  EVIDENCE: 6/6 verbatim match (script-verified)

- [x] S7: Crawl files exist and validate
  CHECK: robots.txt + sitemap.xml present; sitemap XML parses
  EXPECT: present + valid
  EVIDENCE: robots (allow + sitemap ref); sitemap single-URL, parses OK

- [x] S8: No broken in-page anchors
  CHECK: every href="#x" has a matching id
  EXPECT: all resolve
  EVIDENCE: #ritual, #shop, #tentang, #top all OK

<!--
- A checked box with EVIDENCE still "pending" counts as UNMET.
- S2's single sameAs hit is accepted debt, not failure — see PRD Q9.
-->
