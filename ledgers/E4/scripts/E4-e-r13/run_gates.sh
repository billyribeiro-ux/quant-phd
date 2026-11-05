#!/bin/bash
# Verifier r13 (E4 cards slice): deterministic gates run on pin e919577, outputs under outputs/.
cd /Users/billyribeiro/.fanout/wt/verifyE13-E4-e || exit 1
O=ledgers/E4/scripts/E4-e-r13/outputs
PY=.venv/bin/python
$PY tools/check_pages.py --unit E4 > $O/check_pages_E4.txt 2>&1; echo "rc=$?" >> $O/check_pages_E4.txt
$PY tools/check_dag.py --unit E4 > $O/check_dag_E4.txt 2>&1; echo "rc=$?" >> $O/check_dag_E4.txt
$PY tools/check_projects.py --unit E4 > $O/check_projects_E4.txt 2>&1; echo "rc=$?" >> $O/check_projects_E4.txt
$PY tools/verify_refs.py --offline > $O/verify_refs_offline.txt 2>&1; echo "rc=$?" >> $O/verify_refs_offline.txt
$PY -m ruff check course/modules/E/E4 tests/labs/E4 > $O/ruff_check.txt 2>&1; echo "rc=$?" >> $O/ruff_check.txt
$PY -m mypy --no-incremental > $O/mypy.txt 2>&1; echo "rc=$?" >> $O/mypy.txt
$PY tools/run_labs.py --unit E4 > $O/run_labs_E4.txt 2>&1; echo "rc=$?" >> $O/run_labs_E4.txt
for f in tests/labs/E4/*.py; do b=$(basename $f .py); $PY -I -W error $f > $O/twin_$b.out 2>$O/twin_$b.err; echo "rc=$?" >> $O/twin_$b.out; done
echo DONE > $O/gates_done.txt
