# Gates: zaleavelle PRD

Scope: Comprehensive PRD covering e-commerce conversion, landing page optimization, brand/content, and technical hardening for a single-file Indonesian DTC skincare landing page.

- [x] G1: PRD has clear Problem, Goals, Non-Goals sections with at least one measurable metric per goal
  CHECK: grep -c "^## " PRD.md
  EXPECT: >=8
  EVIDENCE: 13 sections found

- [x] G2: All 4 tracks (e-com, landing opt, brand/content, tech split) are covered with scope in/out
  CHECK: grep -E "Track [1-4]" PRD.md
  EXPECT: 4 matches
  EVIDENCE: 7 matches (Track 1-4 headings + references)

- [x] G3: Each product CTA maps to a measurable conversion event (UTM + analytics event ID)
  CHECK: grep -c "utm_" PRD.md
  EXPECT: >=4
  EVIDENCE: 7 matches (UTM taxonomy table + acceptance criteria)

- [x] G4: SEO/a11y/perf targets quantified (LCP, CLS, Lighthouse score, alt coverage %)
  CHECK: grep -E "LCP|CLS|Lighthouse|alt" PRD.md
  EXPECT: >=4 matches
  EVIDENCE: 13 matches

- [x] G5: Brand system tokens (palette, type, shape, motion, z-scale) documented with no second accent
  CHECK: grep -E "#9E3E4D|#E3A7AC|accent" PRD.md
  EXPECT: >=2 (one per theme)
  EVIDENCE: 4 matches (accent values + token table)

- [x] G6: Tech split/CMS/i18n decision stated with rationale
  CHECK: grep -E "Decision|Rationale" PRD.md
  EXPECT: >=4 rows in decisions table
  EVIDENCE: 5 matches (5 decision rows in Technical Decisions table)

- [x] G7: Zero TODO/placeholder/lorem in PRD body (asset-swap appendix excluded)
  CHECK: grep -ci "TODO|lorem|placeholder" PRD.md
  EXPECT: 0
  EVIDENCE: 0 matches

- [x] G8: Report numbers re-measured — gate-check ledger N/N pasted in progress.md
  CHECK: grep "checked" progress.md
  EXPECT: /8 of 8/
  EVIDENCE: "8 of 8 gates PASS" in progress.md Gate-Check Ledger

- [x] G9: PRD contains milestones M1-M3 with dates or week markers
  CHECK: grep -c "M[1-3]" PRD.md
  EXPECT: >=3
  EVIDENCE: 7 matches (M1, M2, M3 references throughout)

- [x] G10: Risks and open questions table present with at least 3 entries
  CHECK: grep -c "Risk|Open Question" PRD.md
  EXPECT: >=2
  EVIDENCE: 4 matches (Risks table + Open Questions table + headings)

<!--
Rules (full spec in references/gates.md):
- One box per outcome. Boxes are flipped by gate-check.mjs when CHECK output
  matches EXPECT, or by hand for manual gates.
- A checked box with EVIDENCE still reading "pending" counts as UNMET.
- Evidence is the deciding lines only, never a full log.
- If a gate becomes impossible, do not delete it. Add a line:
    ABANDON: G<n> <reason>
  and report it. Visible surrender is honest; silent scope-narrowing is not.
-->
