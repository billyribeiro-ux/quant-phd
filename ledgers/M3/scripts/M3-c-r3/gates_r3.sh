#!/bin/bash
# Round 3 gate runner for M3 slice c (L07-L09 and lab twins). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyD3-M3-c
D=ledgers/M3/scripts/M3-c-r3
PY=.venv/bin/python
run(){ name=$1; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > $D/$name.log 2>&1; }
run check_pages_L07-L09 $PY tools/check_pages.py --unit M3 --page L07
$PY tools/check_pages.py --unit M3 --page L08 > $D/check_pages_L08.log 2>&1; echo "EXIT=$?" >> $D/check_pages_L08.log
$PY tools/check_pages.py --unit M3 --page L09 > $D/check_pages_L09.log 2>&1; echo "EXIT=$?" >> $D/check_pages_L09.log
$PY tools/check_pages.py --unit M3 > $D/check_pages_M3_unit.log 2>&1; echo "EXIT=$?" >> $D/check_pages_M3_unit.log
$PY tools/check_dag.py --unit M3 > $D/check_dag_M3.log 2>&1; echo "EXIT=$?" >> $D/check_dag_M3.log
$PY tools/run_labs.py --unit M3 --page L07 > $D/run_labs_L07.log 2>&1; echo "EXIT=$?" >> $D/run_labs_L07.log
$PY tools/run_labs.py --unit M3 --page L08 > $D/run_labs_L08.log 2>&1; echo "EXIT=$?" >> $D/run_labs_L08.log
$PY tools/run_labs.py --unit M3 --page L09 > $D/run_labs_L09.log 2>&1; echo "EXIT=$?" >> $D/run_labs_L09.log
$PY tools/run_labs.py --unit M3 > $D/run_labs_M3_all.log 2>&1; echo "EXIT=$?" >> $D/run_labs_M3_all.log
$PY tools/page_smoke.py --unit M3 --pages L07 > $D/page_smoke_L07.log 2>&1; echo "EXIT=$?" >> $D/page_smoke_L07.log
$PY tools/page_smoke.py --unit M3 --pages L08 > $D/page_smoke_L08.log 2>&1; echo "EXIT=$?" >> $D/page_smoke_L08.log
$PY tools/page_smoke.py --unit M3 --pages L09 > $D/page_smoke_L09.log 2>&1; echo "EXIT=$?" >> $D/page_smoke_L09.log
$PY -m ruff check tests/labs/M3/lab-M3-L07-1.py tests/labs/M3/lab-M3-L08-1.py tests/labs/M3/lab-M3-L09-1.py > $D/ruff_check_r3.log 2>&1; echo "EXIT=$?" >> $D/ruff_check_r3.log
$PY -m ruff format --check tests/labs/M3/lab-M3-L07-1.py tests/labs/M3/lab-M3-L08-1.py tests/labs/M3/lab-M3-L09-1.py > $D/ruff_format_r3.log 2>&1; echo "EXIT=$?" >> $D/ruff_format_r3.log
$PY -m mypy --no-incremental > $D/mypy_r3.log 2>&1; echo "EXIT=$?" >> $D/mypy_r3.log
$PY tools/verify_refs.py --offline > $D/verify_refs_offline_r3.log 2>&1; echo "EXIT=$?" >> $D/verify_refs_offline_r3.log
echo DONE > $D/gates_done.flag
