#!/bin/bash
# Round-8 SC1 slice b gates. Run from the checkout root. Each gate writes out/<name>.txt and its exit code.
cd "$(dirname "$0")/../../../.." || exit 1
O=ledgers/SC1/scripts/SC1-b-r9/out
run() { name=$1; shift; "$@" > "$O/$name.txt" 2>&1; echo "exit=$?" >> "$O/$name.txt"; echo "$name: $(tail -1 $O/$name.txt)"; }
run check_pages .venv/bin/python tools/check_pages.py --unit SC1
run check_dag .venv/bin/python tools/check_dag.py --unit SC1
run check_projects_sc1 .venv/bin/python tools/check_projects.py --unit SC1
run run_labs_L04 .venv/bin/python tools/run_labs.py --unit SC1 --page L04
run run_labs_L05 .venv/bin/python tools/run_labs.py --unit SC1 --page L05
run run_labs_L06 .venv/bin/python tools/run_labs.py --unit SC1 --page L06
run page_smoke .venv/bin/python tools/page_smoke.py --unit SC1 --pages L04 L05 L06
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run verify_refs_unit .venv/bin/python tools/verify_refs.py --unit SC1
run ruff_check .venv/bin/ruff check tests/labs/SC1
run ruff_format .venv/bin/ruff format --check tests/labs/SC1
run mypy_labs .venv/bin/mypy --no-incremental tests/labs/SC1/lab-SC1-L04-1.py tests/labs/SC1/lab-SC1-L05-1.py tests/labs/SC1/lab-SC1-L06-1.py
run pytest_tooling .venv/bin/pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q
