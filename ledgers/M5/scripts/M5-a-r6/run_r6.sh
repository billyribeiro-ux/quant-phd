#!/bin/sh
# Round-6 M5-a verifier commands (run from the checkout root, pin 44f1eb6). Output recorded alongside.
set -u
PY=.venv/bin/python
$PY tools/check_pages.py --unit M5
$PY tools/check_dag.py --unit M5
$PY tools/check_projects.py --unit M5
$PY tools/run_labs.py --unit M5 --page L01
$PY tools/run_labs.py --unit M5 --page L02
$PY tools/run_labs.py --unit M5 --page L03
$PY tools/run_labs.py --unit M5 --page L04
for n in 1 2 3 4; do $PY -I -W error "$PWD/tests/labs/M5/lab-M5-L0$n-1.py" >/dev/null; echo "twin L0$n rc=$?"; done
$PY tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04
ruff_bin=.venv/bin/ruff
$ruff_bin check tests/labs/M5/lab-M5-L01-1.py tests/labs/M5/lab-M5-L02-1.py tests/labs/M5/lab-M5-L03-1.py tests/labs/M5/lab-M5-L04-1.py
$ruff_bin format --check tests/labs/M5/lab-M5-L01-1.py tests/labs/M5/lab-M5-L02-1.py tests/labs/M5/lab-M5-L03-1.py tests/labs/M5/lab-M5-L04-1.py
$PY -m mypy --no-incremental tests/labs/M5/lab-M5-L01-1.py tests/labs/M5/lab-M5-L02-1.py tests/labs/M5/lab-M5-L03-1.py tests/labs/M5/lab-M5-L04-1.py
$PY -m pytest -q tests/test_labs.py -k M5
$PY tools/verify_refs.py --offline
$PY -I ledgers/M5/scripts/M5-a-r6/numcheck_r6.py
