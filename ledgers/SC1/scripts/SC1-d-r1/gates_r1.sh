#!/bin/bash
# Round 1 gate run for SC1-d (delta verification at pin 95f3f8cb), from the verifier checkout root.
R=/Users/billyribeiro/.fanout/wt/verifyF31-SC1-d
cd "$R" || exit 1
O=$R/ledgers/SC1/scripts/SC1-d-r1/out
PY=$R/.venv/bin/python
run() { name=$1; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > "$O/$name.txt" 2>&1; }
run check_pages_unit_r1 $PY tools/check_pages.py --unit SC1
run check_dag_unit_r1 $PY tools/check_dag.py --unit SC1
run check_projects_unit_r1 $PY tools/check_projects.py --unit SC1
run run_labs_unit_r1 $PY tools/run_labs.py --unit SC1
run run_labs_project_r1 $PY tools/run_labs.py --unit SC1 --page project
run run_graders_0_49_r1 $PY tools/run_graders.py --unit SC1 --seeds 0-49
run page_smoke_project_r1 $PY tools/page_smoke.py --unit SC1 --pages project
run page_smoke_L02_L03_r1 $PY tools/page_smoke.py --unit SC1 --pages L02 L03
run mutate_graders_unit_r1 $PY tools/mutate_graders.py --unit SC1 --seeds 0-9
run mypy_r1 .venv/bin/mypy --no-incremental
run ruff_check_repo_r1 .venv/bin/ruff check .
run ruff_format_repo_r1 .venv/bin/ruff format --check .
run collect_count_r1 $PY -m pytest --collect-only -q -p no:cacheprovider course/modules/SC/SC1/grader/test_project.py
run verify_refs_offline_r1 $PY tools/verify_refs.py --offline
run pytest_labs_r1 $PY -m pytest -q -p no:cacheprovider tests/labs
echo done > "$O/GATES_DONE"
