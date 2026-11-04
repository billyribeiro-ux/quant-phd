#!/bin/sh
# SC1-a round 1 gate re-run (verifier). Run from the checkout root: sh ledgers/SC1/scripts/SC1-a-r1/gates.sh
set -u
PY=.venv/bin/python
echo "== check_pages";   $PY tools/check_pages.py --unit SC1; echo "exit $?"
echo "== check_dag";     $PY tools/check_dag.py --unit SC1; echo "exit $?"
echo "== run_labs unit"; $PY tools/run_labs.py --unit SC1; echo "exit $?"
for p in L01 L02 L03; do echo "== run_labs $p"; $PY tools/run_labs.py --unit SC1 --page $p; echo "exit $?"; done
PYREAL=$(readlink -f .venv/bin/python)
for f in L01-1 L02-1 L03-1; do
  echo "== twin lab-SC1-$f under python -I -W error"
  d=$(mktemp -d); (cd "$d" && "$PYREAL" -I -W error "$OLDPWD/tests/labs/SC1/lab-SC1-$f.py" > out.txt 2> err.txt; echo "exit $? stderr_bytes $(wc -c < err.txt)")
done
echo "== page_smoke index L01 L02 L03"; $PY tools/page_smoke.py --unit SC1 --pages index L01 L02 L03; echo "exit $?"
echo "== ruff check/format twins"; .venv/bin/ruff check tests/labs/SC1/lab-SC1-L0[123]-1.py; .venv/bin/ruff format --check tests/labs/SC1/lab-SC1-L0[123]-1.py
echo "== mypy strict twins"; .venv/bin/mypy --no-incremental tests/labs/SC1/lab-SC1-L01-1.py tests/labs/SC1/lab-SC1-L02-1.py tests/labs/SC1/lab-SC1-L03-1.py; echo "exit $?"
echo "== pytest lab tests for L01-L03"; $PY -m pytest -q tests/test_labs.py -k "SC1 and (L01 or L02 or L03)"; echo "exit $?"
echo "== verify_refs offline"; $PY tools/verify_refs.py --offline | tail -1
echo "== verify_refs live SC1"; $PY tools/verify_refs.py --unit SC1 | tail -1
echo "== independent recomputation"; $PY -I ledgers/SC1/scripts/SC1-a-r1/recompute_numbers.py > /dev/null; echo "exit $?"
$PY -I ledgers/SC1/scripts/SC1-a-r1/recompute_lab_L02_L03.py > /dev/null; echo "exit $?"
