#!/bin/bash
# Round 10 gate commands for BK4 slice b, run from the verifier checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyE10-BK4-b || exit 1
OUT=ledgers/BK4/scripts/BK4-b-r10
run() { name="$1"; shift; "$@" > "$OUT/$name.txt" 2>&1; echo "$name exit=$?" >> "$OUT/gates_exit.txt"; }
rm -f "$OUT/gates_exit.txt"
run check_pages .venv/bin/python tools/check_pages.py --unit BK4
run check_dag .venv/bin/python tools/check_dag.py --unit BK4
run check_projects .venv/bin/python tools/check_projects.py --unit BK4
run run_labs .venv/bin/python tools/run_labs.py --unit BK4
run ruff_check .venv/bin/ruff check tests/labs/BK4
run ruff_format .venv/bin/ruff format --check tests/labs/BK4
run mypy_labs .venv/bin/mypy --no-incremental tests/labs/BK4
run pytest_labs .venv/bin/pytest tests/test_labs.py -k "BK4 and (L04 or L05)" -v
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run verify_refs_unit .venv/bin/python tools/verify_refs.py --unit BK4
run build_site_check .venv/bin/python tools/build_site.py --check
echo DONE >> "$OUT/gates_exit.txt"
