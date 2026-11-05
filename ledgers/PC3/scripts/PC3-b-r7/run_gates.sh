#!/bin/bash
# Round-7 gate runs for PC3-b on pin 06994db1. Writes outputs to ledgers/PC3/scripts/PC3-b-r7/out/.
cd "$(dirname "$0")/../../../.." || exit 1
O=ledgers/PC3/scripts/PC3-b-r7/out
run() { name=$1; shift; "$@" > "$O/$name.out" 2>&1; echo "$name rc=$?" >> "$O/rc.txt"; }
rm -f "$O/rc.txt"
run run_labs .venv/bin/python tools/run_labs.py --unit PC3
run check_pages .venv/bin/python tools/check_pages.py --unit PC3
run check_dag .venv/bin/python tools/check_dag.py --unit PC3
run check_projects .venv/bin/python tools/check_projects.py --unit PC3
run page_smoke_L04_L06 .venv/bin/python tools/page_smoke.py --unit PC3 --pages L04 L05 L06
run ruff_check .venv/bin/ruff check tests/labs/PC3/lab-PC3-L04-1.py tests/labs/PC3/lab-PC3-L05-1.py tests/labs/PC3/lab-PC3-L06-1.py
run ruff_format .venv/bin/ruff format --check tests/labs/PC3/lab-PC3-L04-1.py tests/labs/PC3/lab-PC3-L05-1.py tests/labs/PC3/lab-PC3-L06-1.py
run mypy_nocache .venv/bin/mypy --no-incremental
run pytest_labs .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
echo DONE >> "$O/rc.txt"
