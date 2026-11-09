#!/bin/sh
# Verifier M7-d round 12: targeted command rows, run on the pin 329c1d7 (checkout root is the cwd).
cd /Users/billyribeiro/.fanout/wt/verifyD12-M7-d || exit 1
G=ledgers/M7/scripts/M7-d-r12/gates
PY=.venv/bin/python
run() { name="$1"; shift; echo "### $name: $*" > "$G/$name.log"; "$@" >> "$G/$name.log" 2>&1; echo "EXIT $?" >> "$G/$name.log"; }
run check_pages_M7 $PY tools/check_pages.py --unit M7
run check_dag_all $PY tools/check_dag.py --all
run check_projects_M7 $PY tools/check_projects.py --unit M7
run run_labs_M7 $PY tools/run_labs.py --unit M7
run run_graders_M7_0_49 $PY tools/run_graders.py --unit M7 --seeds 0-49
run mutate_M7_0_9 $PY tools/mutate_graders.py --unit M7 --seeds 0-9
run page_smoke_M7_project $PY tools/page_smoke.py --unit M7 --pages project
run verify_refs_offline_M7 $PY tools/verify_refs.py --offline --unit M7
run ruff_check $PY -m ruff check tests/labs/M7 course/modules/M/M7/grader
run ruff_format $PY -m ruff format --check tests/labs/M7 course/modules/M/M7/grader
run mypy_nocache $PY -m mypy --no-incremental
echo done > "$G/DONE"
