#!/bin/bash
# M3 slice b round 4 gate runs on the pinned checkout (edbb7aa8). Each output in out/.
cd /Users/billyribeiro/.fanout/wt/verifyS4-M3-b || exit 1
O=ledgers/M3/scripts/M3-b-r4/out
PY=.venv/bin/python
run() { name=$1; shift; { "$@"; echo "EXIT=$?"; } > "$O/$name.out" 2>&1; }
run check_pages_M3 $PY tools/check_pages.py --unit M3
run check_pages_L04 $PY tools/check_pages.py --unit M3 --page L04
run check_pages_L05 $PY tools/check_pages.py --unit M3 --page L05
run check_pages_L06 $PY tools/check_pages.py --unit M3 --page L06
run check_dag_M3 $PY tools/check_dag.py --unit M3
run check_projects_M3 $PY tools/check_projects.py --unit M3
run run_labs_L04 $PY tools/run_labs.py --unit M3 --page L04
run run_labs_L05 $PY tools/run_labs.py --unit M3 --page L05
run run_labs_L06 $PY tools/run_labs.py --unit M3 --page L06
run ruff_check_labs .venv/bin/ruff check tests/labs/M3
run ruff_format_labs .venv/bin/ruff format --check tests/labs/M3
run mypy .venv/bin/mypy --no-incremental
run verify_refs_offline $PY tools/verify_refs.py --offline
run pytest_relevant $PY -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_docs_figures.py
run page_smoke_L04_L06 $PY tools/page_smoke.py --unit M3 --pages L04 L05 L06
echo ALL_DONE > "$O/done"
