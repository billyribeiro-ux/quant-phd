#!/bin/bash
# Round-10 slice-d gate runner for unit M4 (verifier D). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyD10-M4-d || exit 1
G=ledgers/M4/scripts/M4-d-r10/gates
run() { name="$1"; shift; "$@" > "$G/$name.out" 2>&1; echo "EXIT $?" >> "$G/$name.out"; tail -3 "$G/$name.out"; }
run check_pages_M4 .venv/bin/python tools/check_pages.py --unit M4
run check_dag_M4 .venv/bin/python tools/check_dag.py --unit M4
run check_projects_M4 .venv/bin/python tools/check_projects.py --unit M4
run run_labs_M4 .venv/bin/python tools/run_labs.py --unit M4
run run_graders_M4_0-49 .venv/bin/python tools/run_graders.py --unit M4 --seeds 0-49
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run ruff_check .venv/bin/ruff check tests/labs/M4 course/modules/M/M4 ledgers/M4/mutants ledgers/M4/scripts/M4-d-r10
run ruff_format .venv/bin/ruff format --check tests/labs/M4 course/modules/M/M4/grader
run mypy .venv/bin/mypy --no-incremental
