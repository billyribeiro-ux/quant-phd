#!/bin/bash
# Round 9 verifier gate run for PC3 slice c, pin c93dd52 (checkout /Users/billyribeiro/.fanout/wt/verifyE9-PC3-c).
cd /Users/billyribeiro/.fanout/wt/verifyE9-PC3-c || exit 1
S=ledgers/PC3/scripts/PC3-c-r9
P=.venv/bin/python
run() { name=$1; shift; { "$@"; echo "exit $?"; } > $S/r9v_$name.out 2>&1; }
run check_pages $P tools/check_pages.py --all
run check_dag $P tools/check_dag.py --all
run check_projects $P tools/check_projects.py --all
run run_labs_project $P tools/run_labs.py --unit PC3 --page project
run run_graders $P tools/run_graders.py --unit PC3 --seeds 0-49
run page_smoke_project $P tools/page_smoke.py --unit PC3 --pages project
run ruff_check .venv/bin/ruff check course/modules/PC/PC3/grader tests/labs/PC3
run ruff_format .venv/bin/ruff format --check course/modules/PC/PC3/grader tests/labs/PC3
run mypy_repo .venv/bin/mypy --no-incremental
run verify_refs $P tools/verify_refs.py --offline
run pytest_collect .venv/bin/pytest --collect-only -q -k PC3
run pytest_pc3 .venv/bin/pytest -q -k PC3
echo ALLDONE > $S/r9v_done.flag
