#!/bin/sh
cd /Users/billyribeiro/dev/quant-phd
for i in 1 2 3; do
  .venv/bin/python tools/page_smoke.py --unit E3 --pages project > ledgers/E3/scripts/fixer-d-r13/out/page_smoke_project_run$i.out 2>&1
  echo "EXIT $?" >> ledgers/E3/scripts/fixer-d-r13/out/page_smoke_project_run$i.out
done
echo done > ledgers/E3/scripts/fixer-d-r13/out/page_smoke_done.flag
