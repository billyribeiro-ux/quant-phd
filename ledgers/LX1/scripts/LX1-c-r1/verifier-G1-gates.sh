#!/usr/bin/env bash
# Verifier G1, LX1-c closing delta round 1, pin 2a805c83. Run from the checkout root. Output to out/G1_*.out.
set -u
OUT=ledgers/LX1/scripts/LX1-c-r1/out
mkdir -p "$OUT"
PY=.venv/bin/python
run() { name="$1"; shift; { echo "\$ $*"; "$@"; echo "rc=$?"; } > "$OUT/$name.out" 2>&1; echo "$name: $(tail -1 "$OUT/$name.out")"; }
run G1_check_projects $PY tools/check_projects.py --unit LX1
run G1_check_pages $PY tools/check_pages.py --unit LX1
run G1_check_dag $PY tools/check_dag.py --unit LX1
run G1_run_labs_unit $PY tools/run_labs.py --unit LX1
run G1_run_labs_project $PY tools/run_labs.py --unit LX1 --page project
run G1_page_smoke_project $PY tools/page_smoke.py --unit LX1 --pages project
run G1_verify_refs_offline $PY tools/verify_refs.py --offline
run G1_ruff_check $PY -m ruff check tests/labs/LX1 tests/test_lx1_project_lab3.py tools
run G1_ruff_format $PY -m ruff format --check tests/labs/LX1 tests/test_lx1_project_lab3.py tools
run G1_mypy $PY -m mypy --no-incremental tests/labs/LX1 tests/test_lx1_project_lab3.py
run G1_pytest_lab3 $PY -m pytest -q tests/test_lx1_project_lab3.py
run G1_pytest_labs $PY -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_page_checks.py
