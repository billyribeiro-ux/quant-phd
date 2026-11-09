#!/bin/bash
# Round-5 gates for M5 slice c (L08-L10 twins, pages, cards). Run from the checkout root.
cd "$(dirname "$0")/../../../.." || exit 1
O=ledgers/M5/scripts/M5-c-r5/out
PY=.venv/bin/python
run() { name=$1; shift; "$@" > "$O/$name.out" 2>&1; echo "$name exit=$?" >> "$O/summary.txt"; }
: > "$O/summary.txt"
run check_pages $PY tools/check_pages.py --unit M5
run check_dag $PY tools/check_dag.py --unit M5
run check_projects $PY tools/check_projects.py --unit M5
run run_labs_L08 $PY tools/run_labs.py --unit M5 --page L08
run run_labs_L09 $PY tools/run_labs.py --unit M5 --page L09
run run_labs_L10 $PY tools/run_labs.py --unit M5 --page L10
for p in L08 L09 L10; do
  run "twin_$p" $PY -I -W error tests/labs/M5/lab-M5-$p-1.py
done
run page_smoke_L08 $PY tools/page_smoke.py --unit M5 --pages L08
run page_smoke_L09 $PY tools/page_smoke.py --unit M5 --pages L09
run page_smoke_L10 $PY tools/page_smoke.py --unit M5 --pages L10
run ruff_check_twins $PY -m ruff check tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L10-1.py
run ruff_format_twins $PY -m ruff format --check tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L10-1.py
run mypy_no_incremental $PY -m mypy --no-incremental
run pytest_labs_M5 $PY -m pytest tests/test_labs.py -q -k M5
run verify_refs_offline $PY tools/verify_refs.py --offline
echo DONE >> "$O/summary.txt"
