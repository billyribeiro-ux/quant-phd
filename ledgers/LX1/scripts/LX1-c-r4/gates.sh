#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyE4-LX1-c || exit 1
for c in "tools/check_projects.py --unit LX1" "tools/check_pages.py --unit LX1" "tools/check_dag.py --unit LX1" "tools/run_labs.py --unit LX1" "tools/fetch_data.py --check" "tools/verify_refs.py --offline"; do
  echo "== $c"
  .venv/bin/python $c > /tmp/lx1c-r4-gate.txt 2>&1
  rc=$?
  tail -8 /tmp/lx1c-r4-gate.txt
  echo "exit=$rc"
done
