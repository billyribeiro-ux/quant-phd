#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyE5-PC3-c
S=ledgers/PC3/scripts/PC3-c-r5
P=.venv/bin/python
run() { name=$1; shift; { "$@"; echo "exit $?"; } > $S/$name.out 2>&1; }
run check_pages $P tools/check_pages.py --unit PC3
run check_dag $P tools/check_dag.py --unit PC3
run check_projects $P tools/check_projects.py --unit PC3
run run_labs_project $P tools/run_labs.py --unit PC3 --page project
run run_graders $P tools/run_graders.py --unit PC3 --seeds 0-49
run mutate_all $P tools/mutate_graders.py --unit PC3 --seeds 0-49
run page_smoke_project $P tools/page_smoke.py --unit PC3 --pages project
run ruff_check .venv/bin/ruff check course/modules/PC/PC3/grader tests/labs/PC3
run ruff_format .venv/bin/ruff format --check course/modules/PC/PC3/grader tests/labs/PC3
run mypy_repo .venv/bin/mypy --no-incremental
run verify_refs $P tools/verify_refs.py --offline
run pytest_pc3 .venv/bin/pytest -q -k PC3
run collect_only .venv/bin/pytest --collect-only -q course/modules/PC/PC3/grader/test_project.py
echo ALLDONE > $S/done.flag
