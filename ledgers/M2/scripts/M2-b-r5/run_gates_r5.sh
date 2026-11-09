#!/bin/bash
# Round-5 delta gates for M2 slice b, run from the verifier checkout (pin dde0486b).
cd /Users/billyribeiro/.fanout/wt/verifyS5-M2-b || exit 1
S=ledgers/M2/scripts/M2-b-r5
PY=.venv/bin/python
echo "pin: $(git rev-parse HEAD)"
$PY tools/check_pages.py --unit M2 > $S/g01_check_pages_M2.out 2>&1; echo "exit=$?" >> $S/g01_check_pages_M2.out
$PY tools/check_dag.py --unit M2 > $S/g02_check_dag_M2.out 2>&1; echo "exit=$?" >> $S/g02_check_dag_M2.out
$PY tools/check_projects.py --unit M2 > $S/g03_check_projects_M2.out 2>&1; echo "exit=$?" >> $S/g03_check_projects_M2.out
$PY tools/run_labs.py --unit M2 > $S/g04_run_labs_M2.out 2>&1; echo "exit=$?" >> $S/g04_run_labs_M2.out
$PY tools/check_pages.py --all > $S/g04b_check_pages_all.out 2>&1; echo "exit=$?" >> $S/g04b_check_pages_all.out
$PY tools/check_dag.py --all > $S/g04c_check_dag_all.out 2>&1; echo "exit=$?" >> $S/g04c_check_dag_all.out
$PY tools/check_projects.py --all > $S/g04d_check_projects_all.out 2>&1; echo "exit=$?" >> $S/g04d_check_projects_all.out
$PY tools/verify_refs.py --offline > $S/g10_verify_refs_offline.out 2>&1; echo "exit=$?" >> $S/g10_verify_refs_offline.out
$PY -m ruff check tests/labs/M2 > $S/g07_ruff_check_M2_twins.out 2>&1; echo "exit=$?" >> $S/g07_ruff_check_M2_twins.out
$PY -m ruff format --check tests/labs/M2 > $S/g07b_ruff_format_M2_twins.out 2>&1; echo "exit=$?" >> $S/g07b_ruff_format_M2_twins.out
$PY -m mypy --no-incremental tests/labs/M2 > $S/g08_mypy_M2_twins.out 2>&1; echo "exit=$?" >> $S/g08_mypy_M2_twins.out
echo done
