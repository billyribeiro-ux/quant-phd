#!/bin/bash
# Round-7 command rows for SC1-c (L07, L08 and their lab twins). Run from the checkout root.
set -u
OUT=ledgers/SC1/scripts/SC1-c-r7/out
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "exit=$?" >> "$OUT/$name.out"; }
run check_pages_unit $PY tools/check_pages.py --unit SC1
run check_pages_L07 $PY tools/check_pages.py --unit SC1 --page L07
run check_pages_L08 $PY tools/check_pages.py --unit SC1 --page L08
run check_dag $PY tools/check_dag.py --unit SC1
run check_projects $PY tools/check_projects.py --unit SC1
run run_labs_L07 $PY tools/run_labs.py --unit SC1 --page L07
run run_labs_L08 $PY tools/run_labs.py --unit SC1 --page L08
run run_labs_unit $PY tools/run_labs.py --unit SC1
run ruff_check_twins .venv/bin/ruff check tests/labs/SC1/lab-SC1-L07-1.py tests/labs/SC1/lab-SC1-L08-1.py
run ruff_format_twins .venv/bin/ruff format --check tests/labs/SC1/lab-SC1-L07-1.py tests/labs/SC1/lab-SC1-L08-1.py
run mypy_twins .venv/bin/mypy --no-incremental tests/labs/SC1/lab-SC1-L07-1.py tests/labs/SC1/lab-SC1-L08-1.py
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_unit_SC1 $PY tools/verify_refs.py --unit SC1
run pytest_labs_pages .venv/bin/pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k "SC1 or sc1 or lab" -q
