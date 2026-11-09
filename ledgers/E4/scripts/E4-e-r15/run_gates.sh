#!/bin/bash
# Verifier r15 (E4 cards slice, pin d1e65a02): deterministic gates, outputs under outputs/.
cd /Users/billyribeiro/.fanout/wt/verifyE15-E4-e || exit 1
O=ledgers/E4/scripts/E4-e-r15/outputs
PY=.venv/bin/python
$PY tools/check_pages.py --unit E4 > $O/check_pages_E4.txt 2>&1; echo "rc=$?" >> $O/check_pages_E4.txt
$PY tools/check_dag.py --unit E4 > $O/check_dag_E4.txt 2>&1; echo "rc=$?" >> $O/check_dag_E4.txt
$PY tools/check_projects.py --unit E4 > $O/check_projects_E4.txt 2>&1; echo "rc=$?" >> $O/check_projects_E4.txt
$PY tools/verify_refs.py --offline > $O/verify_refs_offline.txt 2>&1; echo "rc=$?" >> $O/verify_refs_offline.txt
$PY -m ruff check course/modules/E/E4 tests/labs/E4 > $O/ruff_check.txt 2>&1; echo "rc=$?" >> $O/ruff_check.txt
$PY -m ruff format --check course/modules/E/E4 tests/labs/E4 > $O/ruff_format_check.txt 2>&1; echo "rc=$?" >> $O/ruff_format_check.txt
$PY tools/run_labs.py --unit E4 > $O/run_labs_E4.txt 2>&1; echo "rc=$?" >> $O/run_labs_E4.txt
for f in tests/labs/E4/*.py; do b=$(basename $f .py); $PY -I -W error $f > $O/twin_$b.out 2>$O/twin_$b.err; echo "rc=$?" >> $O/twin_$b.out; done
$PY tools/page_smoke.py --unit E4 --skip-sweep --pages L03.html L06.html > $O/page_smoke_L03_L06.txt 2>&1; echo "rc=$?" >> $O/page_smoke_L03_L06.txt
$PY -m pytest tests/test_page_checks.py tests/test_run_labs.py -q > $O/pytest_subset.txt 2>&1; echo "rc=$?" >> $O/pytest_subset.txt
echo DONE > $O/gates_done.txt
