#!/bin/bash
# Round-10 PC3 slice a: mechanical gates, run from the checkout root. Output in outputs/.
cd /Users/billyribeiro/.fanout/wt/verifyE10-PC3-a || exit 1
O=ledgers/PC3/scripts/PC3-a-r10/outputs
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "$name exit=$?" >> "$O/exit_codes.txt"; }
rm -f "$O/exit_codes.txt"
run check_pages .venv/bin/python tools/check_pages.py --unit PC3
run check_dag .venv/bin/python tools/check_dag.py --unit PC3
run check_projects .venv/bin/python tools/check_projects.py --unit PC3
run run_labs .venv/bin/python tools/run_labs.py --unit PC3
run run_graders .venv/bin/python tools/run_graders.py --unit PC3 --seeds 0-49
run ruff_check .venv/bin/ruff check tests/labs/PC3
run ruff_format .venv/bin/ruff format --check tests/labs/PC3
run mypy .venv/bin/mypy --no-incremental tests/labs/PC3
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
