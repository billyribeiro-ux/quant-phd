#!/bin/bash
# Round-5 gate runner for M4 slice a. Run from the checkout root. Each gate writes its log and exit code.
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT" || exit 1
OUT="$ROOT/ledgers/M4/scripts/M4-a-r5/gates"
PY="$ROOT/.venv/bin/python"
run() {
  name="$1"; shift
  "$@" > "$OUT/$name.log" 2>&1
  echo "$? $name :: $*" >> "$OUT/exit_codes.txt"
}
run check_pages "$PY" tools/check_pages.py --unit M4
run check_dag "$PY" tools/check_dag.py --unit M4
run check_projects "$PY" tools/check_projects.py --unit M4
run run_labs "$PY" tools/run_labs.py --unit M4
run page_smoke_slice "$PY" tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04
run ruff_check "$ROOT/.venv/bin/ruff" check .
run ruff_format_check "$ROOT/.venv/bin/ruff" format --check .
run mypy "$ROOT/.venv/bin/mypy" --no-incremental
run pytest_relevant "$ROOT/.venv/bin/pytest" -q -p no:cacheprovider tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_docs_figures.py tests/test_page_smoke.py tests/test_curriculum.py
run verify_refs_offline "$PY" tools/verify_refs.py --offline
run build_site_check "$PY" tools/build_site.py --check
echo done >> "$OUT/exit_codes.txt"
