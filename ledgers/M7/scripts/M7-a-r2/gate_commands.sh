#!/bin/sh
# Verifier round 2, M7 slice a. Run from the checkout root (/Users/billyribeiro/.fanout/wt/verifyS2-M7-a), at pin 9294b914.
set -e
.venv/bin/python tools/check_pages.py --unit M7
.venv/bin/python tools/check_pages.py --unit M7 --page L01
.venv/bin/python tools/check_pages.py --unit M7 --page L02
.venv/bin/python tools/check_pages.py --unit M7 --page L03
.venv/bin/python tools/check_dag.py --unit M7
.venv/bin/python tools/check_projects.py --unit M7
.venv/bin/python tools/run_labs.py --unit M7 --page L01
.venv/bin/python tools/run_labs.py --unit M7 --page L02
.venv/bin/python tools/run_labs.py --unit M7 --page L03
for n in L01 L02 L03; do .venv/bin/python -I -W error tests/labs/M7/lab-M7-$n-1.py; done
.venv/bin/python -I -W error ledgers/M7/scripts/M7-a-r2/lab_check.py
.venv/bin/python -I -W error ledgers/M7/scripts/M7-a-r2/recompute_L01_L03.py
.venv/bin/python -I -W error ledgers/M7/scripts/M7-a-r2/cards_check.py
.venv/bin/python tools/page_smoke.py --unit M7 --pages index L01 L02 L03
.venv/bin/ruff check tests/labs/M7/lab-M7-L01-1.py tests/labs/M7/lab-M7-L02-1.py tests/labs/M7/lab-M7-L03-1.py
.venv/bin/ruff format --check tests/labs/M7/lab-M7-L01-1.py tests/labs/M7/lab-M7-L02-1.py tests/labs/M7/lab-M7-L03-1.py
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy --no-incremental --strict tests/labs/M7/lab-M7-L01-1.py tests/labs/M7/lab-M7-L02-1.py tests/labs/M7/lab-M7-L03-1.py
.venv/bin/mypy --no-incremental
.venv/bin/pytest tests/test_labs.py -k M7 -q
.venv/bin/python tools/verify_refs.py --offline
.venv/bin/python tools/verify_refs.py --unit M7
