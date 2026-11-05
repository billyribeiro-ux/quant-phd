#!/bin/bash
# Round 12 slice b gates, run from the checkout root (pin 5db69a9). Output in out/.
cd /Users/billyribeiro/.fanout/wt/verifyE12-SC1-b || exit 1
O=ledgers/SC1/scripts/SC1-b-r12/out
: > $O/exit_codes.txt
run() { name=$1; shift; "$@" > $O/$name.txt 2>&1; echo "$name exit=$?" >> $O/exit_codes.txt; }
run check_pages_unit .venv/bin/python tools/check_pages.py --unit SC1
run check_pages_L04 .venv/bin/python tools/check_pages.py --unit SC1 --page L04
run check_pages_L05 .venv/bin/python tools/check_pages.py --unit SC1 --page L05
run check_pages_L06 .venv/bin/python tools/check_pages.py --unit SC1 --page L06
run check_dag_unit .venv/bin/python tools/check_dag.py --unit SC1
run check_dag_all .venv/bin/python tools/check_dag.py --all
run check_projects_unit .venv/bin/python tools/check_projects.py --unit SC1
run run_labs_unit .venv/bin/python tools/run_labs.py --unit SC1
run run_labs_L04 .venv/bin/python tools/run_labs.py --unit SC1 --page L04
run run_labs_L05 .venv/bin/python tools/run_labs.py --unit SC1 --page L05
run run_labs_L06 .venv/bin/python tools/run_labs.py --unit SC1 --page L06
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run verify_refs_unit_offline .venv/bin/python tools/verify_refs.py --offline --unit SC1
run ruff_labs .venv/bin/ruff check tests/labs/SC1
run ruff_format_labs .venv/bin/ruff format --check tests/labs/SC1
run mypy_twins .venv/bin/mypy --no-incremental tests/labs/SC1/lab-SC1-L04-1.py tests/labs/SC1/lab-SC1-L05-1.py tests/labs/SC1/lab-SC1-L06-1.py
run pytest_labs_SC1 .venv/bin/pytest tests/test_labs.py -q -k SC1
