#!/bin/bash
# Verifier E4-c round 5: mechanical gates on the pin, each run alone, output to out/.
# Usage: run_gates.sh <checkout-root>
set -u
R="$1"
cd "$R" || exit 2
O="$R/ledgers/E4/scripts/E4-c-r5/out"
mkdir -p "$O"
PY="$R/.venv/bin/python"
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "exit=$?" >> "$O/$name.out"; }
run check_pages_L07 $PY tools/check_pages.py --unit E4 --page L07
run check_pages_L08 $PY tools/check_pages.py --unit E4 --page L08
run check_pages_L09 $PY tools/check_pages.py --unit E4 --page L09
run check_dag_E4 $PY tools/check_dag.py --unit E4
run check_projects_E4 $PY tools/check_projects.py --unit E4
run run_labs_L07 $PY tools/run_labs.py --unit E4 --page L07
run run_labs_L08 $PY tools/run_labs.py --unit E4 --page L08
run run_labs_L09 $PY tools/run_labs.py --unit E4 --page L09
run page_smoke_L07_L08_L09 $PY tools/page_smoke.py --unit E4 --pages L07 L08 L09
run ruff_check $PY -m ruff check tests/labs/E4/lab-E4-L07-1.py tests/labs/E4/lab-E4-L08-1.py tests/labs/E4/lab-E4-L09-1.py
run ruff_format $PY -m ruff format --check tests/labs/E4/lab-E4-L07-1.py tests/labs/E4/lab-E4-L08-1.py tests/labs/E4/lab-E4-L09-1.py
run mypy_twins $PY -m mypy --no-incremental tests/labs/E4/lab-E4-L07-1.py tests/labs/E4/lab-E4-L08-1.py tests/labs/E4/lab-E4-L09-1.py
run pytest_labs_E4 $PY -m pytest tests/test_labs.py -q -k E4
run verify_refs_offline $PY tools/verify_refs.py --offline
for t in L07 L08 L09; do
  f="tests/labs/E4/lab-E4-$t-1.py"
  tmp=$(mktemp -d /tmp/e4c-r5-XXXX)
  (cd "$tmp" && env -i PATH=/usr/bin:/bin "$PY" -I -W error "$R/$f" > "$O/twin-$t.stdout" 2> "$O/twin-$t.stderr"; echo "exit=$?" > "$O/twin-$t.exit")
  rm -rf "$tmp"
done
echo DONE > "$O/done.txt"
