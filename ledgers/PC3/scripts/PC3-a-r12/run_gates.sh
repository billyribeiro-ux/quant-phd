#!/bin/bash
# Round-12 PC3 slice a: mechanical gates, run from the checkout root (pin 5db69a9). Output in outputs/.
cd /Users/billyribeiro/.fanout/wt/verifyE12-PC3-a || exit 1
O=ledgers/PC3/scripts/PC3-a-r12/outputs
mkdir -p "$O"
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "$name exit=$?" >> "$O/exit_codes.txt"; }
rm -f "$O/exit_codes.txt"
run check_pages .venv/bin/python tools/check_pages.py --unit PC3
run check_dag .venv/bin/python tools/check_dag.py --unit PC3
run check_projects .venv/bin/python tools/check_projects.py --unit PC3
run run_labs .venv/bin/python tools/run_labs.py --unit PC3
run run_labs_L01 .venv/bin/python tools/run_labs.py --unit PC3 --page L01
run run_labs_L02 .venv/bin/python tools/run_labs.py --unit PC3 --page L02
run run_labs_L03 .venv/bin/python tools/run_labs.py --unit PC3 --page L03
run ruff_check .venv/bin/ruff check tests/labs/PC3
run ruff_format .venv/bin/ruff format --check tests/labs/PC3
run mypy .venv/bin/mypy --no-incremental tests/labs/PC3
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run pytest_pc3 .venv/bin/pytest -q -k PC3
run page_smoke_index .venv/bin/python tools/page_smoke.py --unit PC3 --pages index
run page_smoke_L01 .venv/bin/python tools/page_smoke.py --unit PC3 --pages L01
run page_smoke_L02 .venv/bin/python tools/page_smoke.py --unit PC3 --pages L02
run page_smoke_L03 .venv/bin/python tools/page_smoke.py --unit PC3 --pages L03
