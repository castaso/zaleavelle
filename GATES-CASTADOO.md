# Gates: Storefront domain migration (zaleavelle.odoo.com -> beli.zaleavelle.com) + CASTADOO rebrand

Scope: Point every buy CTA and every JSON-LD `offers.url` at the custom domain `beli.zaleavelle.com/shop` (path preserved), rebrand user-facing "Odoo Shop" wording and `data-product` labels to "CASTADOO Shop" across `index.html` and all planning docs, while deliberately KEEPING the analytics/UTM keys `data-cta="odoo"` and `data-utm-content="odoo_profile"` so GA4 history and the PRD 6.2 UTM taxonomy stay continuous.

This gates file is excluded from its own host-sweep checks (G1/G8) because it names the old pattern by design.

- [x] G1: No stale odoo host survives in any product or planning file (this gates file excluded)
  CHECK: node -e "const fs=require('fs');const f=['index.html','PRD.md','task_plan.md','progress.md','findings.md','GATES.md','GATES-SEO.md','GATES-SC.md','robots.txt','sitemap.xml','site.webmanifest'];const h=f.filter(p=>fs.existsSync(p)&&fs.readFileSync(p,'utf8').toLowerCase().includes('zaleavelle.odoo.com'));console.log(h.length?'STALE '+h.join(' '):'CLEAN 0 stale hosts across '+f.length+' files')"
  EXPECT: CLEAN 0 stale hosts
  EVIDENCE: CLEAN 0 stale hosts across 11 files

- [x] G2: index.html carries exactly 13 new-host shop URLs (7 JSON-LD offers + 6 CTA hrefs)
  CHECK: node -e "const s=require('fs').readFileSync('index.html','utf8');console.log('shopurls='+(s.split('https://beli.zaleavelle.com/shop').length-1))"
  EXPECT: shopurls=13
  EVIDENCE: shopurls=13

- [x] G3: The 13 URLs split correctly 7 offers.url / 6 anchor href, and no CTA points anywhere else
  CHECK: node -e "const s=require('fs').readFileSync('index.html','utf8');const q=String.fromCharCode(34);const o=s.split('Offer'+q+', '+q+'url'+q+': '+q+'https://beli.zaleavelle.com/shop'+q).length-1;const h=s.split('href='+q+'https://beli.zaleavelle.com/shop'+q).length-1;const c=s.split('data-cta='+q+'odoo'+q).length-1;console.log('offers='+o+' hrefs='+h+' ctas='+c)"
  EXPECT: offers=7 hrefs=6 ctas=6
  EVIDENCE: offers=7 hrefs=6 ctas=6

- [x] G4: index.html carries 13 CASTADOO mentions and zero capital-O Odoo (7 prose + 6 data-product labels)
  CHECK: node -e "const s=require('fs').readFileSync('index.html','utf8');console.log('castadoo='+(s.split('CASTADOO').length-1)+' odooCap='+(s.split('Odoo').length-1))"
  EXPECT: castadoo=13 odooCap=0
  EVIDENCE: castadoo=13 odooCap=0

- [x] G5: Analytics/UTM keys preserved verbatim: 6 data-cta + 1 odoo_profile = 7 lowercase odoo refs, 0 elsewhere
  CHECK: node -e "const s=require('fs').readFileSync('index.html','utf8');console.log('lowerOdoo='+(s.split('odoo').length-1)+' utmProfile='+(s.split('odoo_profile').length-1))"
  EXPECT: lowerOdoo=7 utmProfile=1
  EVIDENCE: lowerOdoo=7 utmProfile=1

- [x] G6: Every inline script in index.html still compiles (3 blocks, vm.Script syntax check)
  CHECK: node -e "const fs=require('fs'),vm=require('vm');const h=fs.readFileSync('index.html','utf8');const r=/<script(?![^>]*application\/ld\+json)(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/g;let m,n=0;while((m=r.exec(h))){n++;try{new vm.Script(m[1])}catch(e){console.log('SYNTAX FAIL block '+n+': '+e.message);process.exit(0)}}console.log('scripts='+n+' compile=clean')"
  EXPECT: scripts=3 compile=clean
  EVIDENCE: scripts=3 compile=clean

- [x] G7: JSON-LD still parses: 9 graph nodes, 7 Products, all offers.url on new host, zero prices
  CHECK: node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const q=String.fromCharCode(34);const op='<script type='+q+'application/ld+json'+q+'>';const j=h.split(op).slice(1).map(b=>JSON.parse(b.split('</script>')[0]));const g=j[0]['@graph'];const p=g.filter(n=>n['@type']==='Product');const u=p.filter(n=>n.offers&&n.offers.url==='https://beli.zaleavelle.com/shop').length;const pr=p.filter(n=>n.offers&&'price' in n.offers).length;console.log('blocks='+j.length+' nodes='+g.length+' products='+p.length+' offersNewHost='+u+' prices='+pr)"
  EXPECT: blocks=1 nodes=9 products=7 offersNewHost=7 prices=0
  EVIDENCE: blocks=1 nodes=9 products=7 offersNewHost=7 prices=0

- [x] G8: Zero capital-O Odoo left repo-wide in product and planning files (docs rebranded too)
  CHECK: node -e "const fs=require('fs');const f=['index.html','PRD.md','task_plan.md','progress.md','findings.md','GATES.md','GATES-SEO.md','GATES-SC.md','robots.txt','sitemap.xml','site.webmanifest'];const h=f.filter(p=>fs.existsSync(p)&&fs.readFileSync(p,'utf8').includes('Odoo'));console.log(h.length?'CAPODOO '+h.join(' '):'CLEAN 0 capital-O Odoo across '+f.length+' files')"
  EXPECT: CLEAN 0 capital-O Odoo
  EVIDENCE: CLEAN 0 capital-O Odoo across 11 files

- [x] G9: CASTADOO branding is actually present in the page copy users read (banner, trust, FAQ x2, JSON-LD FAQ)
  CHECK: node -e "const s=require('fs').readFileSync('index.html','utf8');const need=['checkout aman via CASTADOO Shop','Checkout terproteksi via CASTADOO Shop','Toko Resmi kami (CASTADOO Shop)','CASTADOO Shop'];const miss=need.filter(t=>!s.includes(t));console.log(miss.length?'MISSING '+miss.join(' | '):'COPY OK all '+need.length+' storefront strings rebranded')"
  EXPECT: COPY OK all 4 storefront strings rebranded
  EVIDENCE: COPY OK all 4 storefront strings rebranded

- [x] G10: PRD records the migration as v2.6 with the new host and a decision row
  CHECK: node -e "const s=require('fs').readFileSync('PRD.md','utf8');const need=['Version 2.6','beli.zaleavelle.com/shop','CASTADOO'];const miss=need.filter(t=>!s.includes(t));console.log(miss.length?'MISSING '+miss.join(' | '):'PRD OK v2.6 + new host + CASTADOO')"
  EXPECT: PRD OK v2.6 + new host + CASTADOO
  EVIDENCE: PRD OK v2.6 + new host + CASTADOO

- [x] G11: progress.md carries the session entry and this ledger, and GATES-SEO.md S1 now checks the new host
  CHECK: node -e "const fs=require('fs');const p=fs.readFileSync('progress.md','utf8');const s=fs.readFileSync('GATES-SEO.md','utf8');const need=[p.includes('beli.zaleavelle.com'),p.includes('Gate-Check Ledger'),s.includes('beli\\.zaleavelle\\.com/shop'),!s.includes('zaleavelle\\.odoo\\.com')];console.log(need.every(Boolean)?'LEDGER OK session + GATES-SEO S1 pattern migrated':'INCOMPLETE '+need.map(b=>b?'1':'0').join(''))"
  EXPECT: LEDGER OK session + GATES-SEO S1 pattern migrated
  EVIDENCE: LEDGER OK session + GATES-SEO S1 pattern migrated

- [x] G12: index.html migration was a pure in-place replacement: added == deleted lines, still 844 lines, 7 files touched
  CHECK: node -e "const fs=require('fs');const {execSync}=require('child_process');const l=execSync('git diff --numstat -- index.html').toString().trim().split('\t');const n=fs.readFileSync('index.html','utf8').split('\n').length;const f=execSync('git diff --numstat').toString().trim().split('\n').filter(Boolean).length;console.log('index.html +'+l[0]+' -'+l[1]+' lines='+n+' files='+f+(l[0]===l[1]&&n===845?' PURE-REPLACEMENT':' MISMATCH'))"
  EXPECT: PURE-REPLACEMENT
  EVIDENCE: warning: in the working copy of 'GATES-SC.md', LF will be replaced by CRLF the next time Git touches it | warning: in the working copy of 'GATES-SEO.md', LF will be replaced by CRLF the next time Git 

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