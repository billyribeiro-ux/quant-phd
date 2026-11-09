#!/bin/bash
# BK4 slice c, round 17 (verifier E17): gate commands run on the pin 700bf33f. Each output goes to out/.
cd /Users/billyribeiro/.fanout/wt/verifyE17-BK4-c || exit 1
O=ledgers/BK4/scripts/BK4-c-r17/out
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$O/$name.txt" 2>&1; echo "$name exit=$?" >> "$O/_exit_codes.txt"; }
: > "$O/_exit_codes.txt"
run check_pages $PY tools/check_pages.py --unit BK4
run check_dag $PY tools/check_dag.py --unit BK4
run check_projects $PY tools/check_projects.py --unit BK4
run run_labs_project $PY tools/run_labs.py --unit BK4 --page project
run run_graders $PY tools/run_graders.py --unit BK4 --seeds 0-49
run page_smoke_project $PY tools/page_smoke.py --unit BK4 --pages project
run ruff_check .venv/bin/ruff check tests/labs/BK4 course/modules/BK/BK4/grader
run ruff_format .venv/bin/ruff format --check tests/labs/BK4 course/modules/BK/BK4/grader
run mypy_unit $PY -m mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader
run mypy_repo $PY -m mypy --no-incremental
run verify_refs_offline $PY tools/verify_refs.py --offline
run pytest_BK4 $PY -m pytest -q -k "BK4 or bk4" tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py
run mutate_graders $PY tools/mutate_graders.py --unit BK4 --seeds 0-9
echo DONE >> "$O/_exit_codes.txt"
