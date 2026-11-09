#!/usr/bin/env bash
# Round-1 (closing delta, LX1-c) gate commands, run from the checkout root (pin 95f3f8cb). Exit code and output go to out/.
set -u
OUT=ledgers/LX1/scripts/LX1-c-r1/out
mkdir -p "$OUT"
PY=.venv/bin/python
run() { name="$1"; shift; { echo "\$ $*"; "$@"; echo "rc=$?"; } > "$OUT/$name.out" 2>&1; echo "$name: $(tail -1 "$OUT/$name.out")"; }
run check_projects_LX1 $PY tools/check_projects.py --unit LX1
run check_pages_LX1 $PY tools/check_pages.py --unit LX1
run check_dag_LX1 $PY tools/check_dag.py --unit LX1
run run_labs_LX1 $PY tools/run_labs.py --unit LX1
run run_labs_project $PY tools/run_labs.py --unit LX1 --page project
run page_smoke_project $PY tools/page_smoke.py --unit LX1 --pages project
run verify_refs_offline $PY tools/verify_refs.py --offline
run ruff_check $PY -m ruff check tests/labs/LX1 tests/test_lx1_project_lab3.py tools
run ruff_format $PY -m ruff format --check tests/labs/LX1 tests/test_lx1_project_lab3.py tools
run mypy_labs_LX1 $PY -m mypy --no-incremental tests/labs/LX1 tests/test_lx1_project_lab3.py
run pytest_lx1_lab3 $PY -m pytest -q tests/test_lx1_project_lab3.py
run pytest_labs $PY -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_page_checks.py
