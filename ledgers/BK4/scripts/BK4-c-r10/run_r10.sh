#!/bin/bash
# Round-10 gate runs for BK4-c. Usage: run_r10.sh <checkout-root>
cd "$1" || exit 2
O=ledgers/BK4/scripts/BK4-c-r10/out
mkdir -p "$O"
P=.venv/bin/python
rm -f "$O/_exit_codes.txt"
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "$name exit=$?" >> "$O/_exit_codes.txt"; }
run check_projects_bk4 $P tools/check_projects.py --unit BK4
run check_pages_all $P tools/check_pages.py --all
run check_dag_all $P tools/check_dag.py --all
run run_labs_bk4 $P tools/run_labs.py --unit BK4
run run_graders_bk4 $P tools/run_graders.py --unit BK4 --seeds 0-49
run mutate_graders_bk4 $P tools/mutate_graders.py --unit BK4 --seeds 0-9
run ruff_check .venv/bin/ruff check tests/labs/BK4 course/modules/BK/BK4/grader ledgers/BK4
run ruff_format .venv/bin/ruff format --check tests/labs/BK4 course/modules/BK/BK4/grader ledgers/BK4
run mypy_repo .venv/bin/mypy --no-incremental
run pytest_labs .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py
run verify_refs_offline $P tools/verify_refs.py --unit BK4 --offline
run page_smoke_bk4_project $P tools/page_smoke.py --unit BK4 --pages project
echo done >> "$O/_exit_codes.txt"
