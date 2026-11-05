#!/bin/bash
# Round-11 M3 slice c: page_smoke for L07, L08, L09 run one at a time (each alone), then the pages' own tests.
cd /Users/billyribeiro/.fanout/wt/verifyD11-M3-c || exit 1
for p in L07 L08 L09; do
  echo "== page_smoke --unit M3 --pages $p"
  .venv/bin/python tools/page_smoke.py --unit M3 --pages $p
  echo "rc=$?"
done
