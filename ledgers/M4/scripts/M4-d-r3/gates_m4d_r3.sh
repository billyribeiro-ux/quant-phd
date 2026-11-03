#!/bin/bash
# Round-3 gate runs for M4 slice d (verifier D3). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyD3-M4-d || exit 1
OUT=ledgers/M4/scripts/M4-d-r3
PY=.venv/bin/python
run() { name=$1; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > "$OUT/$name.out" 2>&1; }
run check_pages_M4 $PY tools/check_pages.py --unit M4
run check_dag_M4 $PY tools/check_dag.py --unit M4
run check_projects_M4 $PY tools/check_projects.py --unit M4
run run_labs_M4 $PY tools/run_labs.py --unit M4
run run_graders_M4_0-49 $PY tools/run_graders.py --unit M4 --seeds 0-49
run mutate_M4_0-9 $PY tools/mutate_graders.py --unit M4 --seeds 0-9
run ruff_check $PY -m ruff check .
run ruff_format $PY -m ruff format --check .
run mypy_nocache $PY -m mypy --no-incremental
run verify_refs_offline $PY tools/verify_refs.py --offline --unit M4
run pytest_m4_labs $PY -m pytest -q tests/test_labs.py -k M4 
run pytest_project_grader $PY -m pytest -q course/modules/M/M4/grader/test_project.py 2>&1 | tail -3
echo done > "$OUT/DONE"
