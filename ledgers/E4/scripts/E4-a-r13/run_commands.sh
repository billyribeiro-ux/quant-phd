#!/bin/bash
# E4 slice a, round 13: gate commands on the pin, each with its exit code.
# Run from the checkout root: bash ledgers/E4/scripts/E4-a-r13/run_commands.sh
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT" || exit 1
OUT="$ROOT/ledgers/E4/scripts/E4-a-r13/outputs"
mkdir -p "$OUT"
PY=.venv/bin/python
run() {
  name="$1"; shift
  "$@" > "$OUT/$name.txt" 2>&1
  echo "$name EXIT=$?" >> "$OUT/exit_codes.txt"
}
: > "$OUT/exit_codes.txt"
run check_pages_E4 $PY tools/check_pages.py --unit E4
run check_dag_all $PY tools/check_dag.py --all
run check_projects_E4 $PY tools/check_projects.py --unit E4
run run_labs_E4 $PY tools/run_labs.py --unit E4
run run_labs_L01 $PY tools/run_labs.py --unit E4 --page L01
run run_labs_L02 $PY tools/run_labs.py --unit E4 --page L02
run run_labs_L03 $PY tools/run_labs.py --unit E4 --page L03
run lab_page_twin_check $PY ledgers/E4/scripts/E4-a-r13/lab_page_twin_check.py
run ruff_slice $PY -m ruff check tests/labs/E4 course/modules/E/E4/grader
run ruff_format $PY -m ruff format --check tests/labs/E4
run mypy_labs $PY -m mypy --no-incremental tests/labs/E4
run verify_refs_offline $PY tools/verify_refs.py --offline
run build_site_check $PY tools/build_site.py --check
run render_curriculum_check $PY tools/render_curriculum.py --check
run page_smoke_index $PY tools/page_smoke.py --unit E4 --pages index
run page_smoke_L01 $PY tools/page_smoke.py --unit E4 --pages L01
run page_smoke_L02 $PY tools/page_smoke.py --unit E4 --pages L02
run page_smoke_L03 $PY tools/page_smoke.py --unit E4 --pages L03
cat "$OUT/exit_codes.txt"
