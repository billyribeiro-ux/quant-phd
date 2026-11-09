#!/bin/sh
# Re-run the verifier's command rows for M5 slice c (L08-L10) on the checkout root given as $1.
set -u
R="$1"
cd "$R" || exit 1
O="$R/ledgers/M5/scripts/M5-c-r1/out"
mkdir -p "$O"
.venv/bin/python tools/check_pages.py --unit M5 > "$O/check_pages.out" 2>&1; echo "check_pages exit $?" >> "$O/check_pages.out"
.venv/bin/python tools/check_dag.py --unit M5 > "$O/check_dag.out" 2>&1; echo "check_dag exit $?" >> "$O/check_dag.out"
.venv/bin/python tools/check_projects.py --unit M5 > "$O/check_projects.out" 2>&1; echo "check_projects exit $?" >> "$O/check_projects.out"
.venv/bin/python tools/run_labs.py --unit M5 > "$O/run_labs.out" 2>&1; echo "run_labs exit $?" >> "$O/run_labs.out"
for f in L08 L09 L10; do
  .venv/bin/python -I -W error tests/labs/M5/lab-M5-$f-1.py > "$O/twin-$f.stdout" 2> "$O/twin-$f.stderr"; echo "twin $f exit $?" >> "$O/twin-$f.stdout"
  .venv/bin/python tools/page_smoke.py --unit M5 --pages $f > "$O/page_smoke-$f.out" 2>&1; echo "page_smoke $f exit $?" >> "$O/page_smoke-$f.out"
done
.venv/bin/ruff check tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L10-1.py > "$O/ruff.out" 2>&1; echo "ruff check exit $?" >> "$O/ruff.out"
.venv/bin/ruff format --check tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L10-1.py >> "$O/ruff.out" 2>&1; echo "ruff format exit $?" >> "$O/ruff.out"
.venv/bin/mypy --no-incremental tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L10-1.py > "$O/mypy.out" 2>&1; echo "mypy exit $?" >> "$O/mypy.out"
.venv/bin/python tools/verify_refs.py --offline > "$O/verify_refs_offline.out" 2>&1; echo "verify_refs exit $?" >> "$O/verify_refs_offline.out"
.venv/bin/pytest tests/test_labs.py -q -k M5 > "$O/pytest_labs_M5.out" 2>&1; echo "pytest exit $?" >> "$O/pytest_labs_M5.out"
