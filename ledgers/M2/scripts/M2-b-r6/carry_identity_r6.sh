#!/bin/bash
# Round-6: byte-identity of M2 slice-b subjects between the previous pin (dde0486b) and HEAD (e896b7a4).
cd /Users/billyribeiro/.fanout/wt/verifyS6-M2-b || exit 1
for f in course/modules/M/M2/L07.html course/modules/M/M2/L08.html course/modules/M/M2/L09.html course/modules/M/M2/L10.html \
         course/modules/M/M2/L11.html course/modules/M/M2/L12.html course/modules/M/M2/cards.json course/modules/M/M2/index.html \
         course/modules/M/M2/project.html \
         tests/labs/M2/lab-M2-L07-1.py tests/labs/M2/lab-M2-L08-1.py tests/labs/M2/lab-M2-L09-1.py tests/labs/M2/lab-M2-L10-1.py \
         tests/labs/M2/lab-M2-L11-1.py tests/labs/M2/lab-M2-L12-1.py \
         notation/notation.json references/references.json BUILDER_RULES.md VERIFIER_RULES.md CLAUDE.md plans/M2-build-plan.md \
         plans/FINAL-ARCHITECT-RULINGS.md plans/KNOWN-ISSUES.md \
         tools/check_pages.py tools/check_dag.py tools/run_labs.py tools/page_smoke.py tools/labs.py tools/ledger.py tools/verify_refs.py \
         tools/refs/match.py course/assets/js/site.js course/assets/js/chart.js course/assets/data/market/MANIFEST.json; do
  if git diff --quiet dde0486b e896b7a4 -- "$f" 2>/dev/null; then echo "IDENTICAL $f"; else echo "CHANGED   $f"; fi
done
