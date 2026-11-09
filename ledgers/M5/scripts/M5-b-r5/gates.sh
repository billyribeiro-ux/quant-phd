#!/bin/bash
# M5-b round 5 gate runs on pin dde0486b. Run from the checkout root. Output in out/.
cd /Users/billyribeiro/.fanout/wt/verifyS5-M5-b || exit 1
O=ledgers/M5/scripts/M5-b-r5/out
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "$name rc=$?" >> "$O/_rc.txt"; }
rm -f "$O/_rc.txt"
run check_pages_M5 $PY tools/check_pages.py --unit M5
run check_pages_L05 $PY tools/check_pages.py --unit M5 --page L05
run check_pages_L06 $PY tools/check_pages.py --unit M5 --page L06
run check_pages_L07 $PY tools/check_pages.py --unit M5 --page L07
run check_dag_M5 $PY tools/check_dag.py --unit M5
run check_projects_M5 $PY tools/check_projects.py --unit M5
run run_labs_L05 $PY tools/run_labs.py --unit M5 --page L05
run run_labs_L06 $PY tools/run_labs.py --unit M5 --page L06
run run_labs_L07 $PY tools/run_labs.py --unit M5 --page L07
run page_smoke_L05 $PY tools/page_smoke.py --unit M5 --pages L05
run page_smoke_L06 $PY tools/page_smoke.py --unit M5 --pages L06
run page_smoke_L07 $PY tools/page_smoke.py --unit M5 --pages L07
run ruff_check_twins $PY -m ruff check tests/labs/M5/lab-M5-L05-1.py tests/labs/M5/lab-M5-L06-1.py tests/labs/M5/lab-M5-L07-1.py
run ruff_format_twins $PY -m ruff format --check tests/labs/M5/lab-M5-L05-1.py tests/labs/M5/lab-M5-L06-1.py tests/labs/M5/lab-M5-L07-1.py
run mypy_full $PY -m mypy --no-incremental
run pytest_labs_M5 $PY -m pytest tests/test_labs.py -k M5 -q
run pytest_collect_M5 $PY -m pytest tests/test_labs.py -k M5 --collect-only -q
run verify_refs_offline $PY tools/verify_refs.py --offline
run build_site_check $PY tools/build_site.py --check
echo DONE >> "$O/_rc.txt"
