#!/bin/bash
# LX1-b round 18 gate runs on the pin 50559266 (run from the checkout root; outputs in out/).
set -u
cd "$(dirname "$0")/../../../.." || exit 1
OUT=ledgers/LX1/scripts/LX1-b-r18/out
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "$name exit=$?" >> "$OUT/_exit_codes.txt"; }
rm -f "$OUT/_exit_codes.txt"
run check_pages_unit $PY tools/check_pages.py --unit LX1
run check_dag_unit $PY tools/check_dag.py --unit LX1
run check_projects_unit $PY tools/check_projects.py --unit LX1
run run_graders_unit $PY tools/run_graders.py --unit LX1
run run_labs_unit $PY tools/run_labs.py --unit LX1
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_unit $PY tools/verify_refs.py --unit LX1 --offline
run fetch_data_check $PY tools/fetch_data.py --check
run build_site_check $PY tools/build_site.py --check
run ruff_check_labs .venv/bin/ruff check tests/labs/LX1/
run ruff_format_labs .venv/bin/ruff format --check tests/labs/LX1/
run mypy_nocache .venv/bin/mypy --no-incremental tests/labs/LX1/lab-LX1-L01-1.py tests/labs/LX1/lab-LX1-L03-1.py tests/labs/LX1/lab-LX1-L04-1.py
run pytest_lx1 .venv/bin/pytest -q -k LX1
run pytest_lx1_collect .venv/bin/pytest --collect-only -q -k LX1
# twin runs are in run_twins_r18.sh (repo CPython 3.14, -I -W error, each twin alone)
echo done >> "$OUT/_exit_codes.txt"
