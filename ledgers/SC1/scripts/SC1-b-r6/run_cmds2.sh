#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyE6-SC1-b
O=ledgers/SC1/scripts/SC1-b-r6/out
PY=.venv/bin/python
for t in L04 L05 L06; do
  { echo "\$ run_labs --unit SC1 --page $t"; $PY tools/run_labs.py --unit SC1 --page $t; echo "exit=$?"; } > $O/run_labs_$t.out 2>&1
done
{ echo "\$ page_smoke --unit SC1 --pages L04 L05 L06 --skip-sweep"; $PY tools/page_smoke.py --unit SC1 --pages L04 L05 L06; echo "exit=$?"; } > $O/page_smoke.out 2>&1
{ echo "\$ pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q"; $PY -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q; echo "exit=$?"; } > $O/pytest_tooling.out 2>&1
{ echo "\$ verify_refs --offline"; $PY tools/verify_refs.py --offline; echo "exit=$?"; } > $O/verify_refs_offline.out 2>&1
{ echo "\$ verify_refs --unit SC1 (live)"; $PY tools/verify_refs.py --unit SC1; echo "exit=$?"; } > $O/verify_refs_live.out 2>&1
echo DONE > $O/cmds2.done
