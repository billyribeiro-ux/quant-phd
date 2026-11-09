#!/bin/bash
# Round-3 gate runs for M5 slice c (L08-L10, twins, cards). Run from the checkout root.
set -u
cd "$(dirname "$0")/../../../.." || exit 1
OUT=ledgers/M5/scripts/M5-c-r3/out
PY=.venv/bin/python
run() { name=$1; shift; "$@" > "$OUT/$name.out" 2>&1; echo "$name exit=$?" >> "$OUT/summary.txt"; }
: > "$OUT/summary.txt"
run check_pages $PY tools/check_pages.py --unit M5
run check_dag $PY tools/check_dag.py --unit M5
run check_projects $PY tools/check_projects.py --unit M5
run run_labs $PY tools/run_labs.py --unit M5
run run_labs_L08 $PY tools/run_labs.py --unit M5 --page L08
run run_labs_L09 $PY tools/run_labs.py --unit M5 --page L09
run run_labs_L10 $PY tools/run_labs.py --unit M5 --page L10
run ruff_check .venv/bin/ruff check tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L10-1.py
run ruff_format .venv/bin/ruff format --check tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L10-1.py
run mypy .venv/bin/mypy --no-incremental
run pytest_labs_M5 $PY -m pytest tests/test_labs.py -q -k M5
run verify_refs_offline $PY tools/verify_refs.py --offline
run ps_L08 $PY tools/page_smoke.py --unit M5 --pages L08
run ps_L09 $PY tools/page_smoke.py --unit M5 --pages L09
run ps_L10 $PY tools/page_smoke.py --unit M5 --pages L10
for t in L08 L09 L10; do
  $PY -I -W error tests/labs/M5/lab-M5-$t-1.py > "$OUT/twin-$t.stdout" 2> "$OUT/twin-$t.stderr"; echo "twin-$t exit=$?" >> "$OUT/summary.txt"
done
echo DONE >> "$OUT/summary.txt"
