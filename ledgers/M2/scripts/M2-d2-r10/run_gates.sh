#!/bin/bash
# M2-d2 round 10 gate runner. Run from the checkout root. Records exit code and output per gate.
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT" || exit 1
OUT="$ROOT/ledgers/M2/scripts/M2-d2-r10/out"
mkdir -p "$OUT"
PY=.venv/bin/python
run() { # name, command...
  local name="$1"; shift
  "$@" > "$OUT/$name.txt" 2>&1
  echo "$name exit=$?" >> "$OUT/_exit_codes.txt"
}
rm -f "$OUT/_exit_codes.txt"
run check_pages_L22 $PY tools/check_pages.py --unit M2 --page L22
run check_pages_L23 $PY tools/check_pages.py --unit M2 --page L23
run check_pages_L24 $PY tools/check_pages.py --unit M2 --page L24
run check_pages_unit $PY tools/check_pages.py --unit M2
run check_dag_M2 $PY tools/check_dag.py --unit M2
run check_projects_M2 $PY tools/check_projects.py --unit M2
run run_labs_L22 $PY tools/run_labs.py --unit M2 --page L22
run run_labs_L23 $PY tools/run_labs.py --unit M2 --page L23
run run_labs_L24 $PY tools/run_labs.py --unit M2 --page L24
run page_smoke_L22 $PY tools/page_smoke.py --unit M2 --pages L22
run page_smoke_L23 $PY tools/page_smoke.py --unit M2 --pages L23
run page_smoke_L24 $PY tools/page_smoke.py --unit M2 --pages L24
run ruff_check $PY -m ruff check tests/labs/M2/lab-M2-L22-1.py tests/labs/M2/lab-M2-L23-1.py tests/labs/M2/lab-M2-L24-1.py
run ruff_format $PY -m ruff format --check tests/labs/M2/lab-M2-L22-1.py tests/labs/M2/lab-M2-L23-1.py tests/labs/M2/lab-M2-L24-1.py
run mypy_twins $PY -m mypy --no-incremental tests/labs/M2/lab-M2-L22-1.py tests/labs/M2/lab-M2-L23-1.py tests/labs/M2/lab-M2-L24-1.py
run pytest_labs_M2 $PY -m pytest tests/test_labs.py -q -k M2
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_unit_M2 $PY tools/verify_refs.py --unit M2 --offline
run fetch_data_check $PY tools/fetch_data.py --check
run build_site_check $PY tools/build_site.py --check
run check_pages_all $PY tools/check_pages.py --all
run check_dag_all $PY tools/check_dag.py --all
echo done >> "$OUT/_exit_codes.txt"
