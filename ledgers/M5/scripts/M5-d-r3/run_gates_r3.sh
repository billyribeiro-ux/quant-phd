#!/bin/bash
# Round 3, slice d (M5 project page, grader, project labs, mutants, alternatives). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyS3-M5-d || exit 1
O=ledgers/M5/scripts/M5-d-r3/out
run() { name=$1; shift; "$@" > "$O/$name.out" 2>&1; echo "rc=$?" >> "$O/$name.out"; }
run run_graders_M5_0-49 .venv/bin/python tools/run_graders.py --unit M5 --seeds 0-49
run mutate_M5_0-9 .venv/bin/python tools/mutate_graders.py --unit M5 --seeds 0-9
run check_pages_M5 .venv/bin/python tools/check_pages.py --unit M5
run check_dag_M5 .venv/bin/python tools/check_dag.py --unit M5
run check_projects_M5 .venv/bin/python tools/check_projects.py --unit M5
run run_labs_M5_project .venv/bin/python tools/run_labs.py --unit M5 --page project
run run_labs_M5_all .venv/bin/python tools/run_labs.py --unit M5
run page_smoke_project .venv/bin/python tools/page_smoke.py --unit M5 --pages project
run ruff_check_scope .venv/bin/ruff check course/modules/M/M5/grader tests/labs/M5 ledgers/M5/alternatives ledgers/M5/mutants
run ruff_format_scope .venv/bin/ruff format --check course/modules/M/M5/grader tests/labs/M5 ledgers/M5/alternatives ledgers/M5/mutants
run mypy_no_incremental .venv/bin/mypy --no-incremental
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run collect_only_suite sh -c 'cd /Users/billyribeiro/.fanout/wt/verifyS3-M5-d/course/modules/M/M5/grader && QF_SEED=0 /Users/billyribeiro/.fanout/wt/verifyS3-M5-d/.venv/bin/python -m pytest -q -p no:cacheprovider --collect-only test_project.py'
echo GATES_DONE > "$O/GATES_DONE"
