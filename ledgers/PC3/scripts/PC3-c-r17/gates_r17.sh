#!/bin/bash
# Round 17, PC3 slice c (project.html, grader, project labs, mutants). Run from the pinned checkout root.
# Each command's exit code is appended to out/ALL_EXIT_r17.txt.
cd /Users/billyribeiro/.fanout/wt/verifyE17-PC3-c || exit 1
OUT=ledgers/PC3/scripts/PC3-c-r17/out
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "$name exit=$?" >> "$OUT/ALL_EXIT_r17.txt"; }
run check_projects_unit $PY tools/check_projects.py --unit PC3
run check_pages_unit $PY tools/check_pages.py --unit PC3
run check_dag_unit $PY tools/check_dag.py --unit PC3
run run_labs_project $PY tools/run_labs.py --unit PC3 --page project
run run_graders_0_49 $PY tools/run_graders.py --unit PC3 --seeds 0-49
run ruff_check .venv/bin/ruff check tests/labs/PC3 course/modules/PC/PC3/grader
run ruff_format .venv/bin/ruff format --check tests/labs/PC3 course/modules/PC/PC3/grader
run mypy_grader_labs .venv/bin/mypy --no-incremental tests/labs/PC3 course/modules/PC/PC3/grader
run page_smoke_project $PY tools/page_smoke.py --unit PC3 --pages project
run mutate_pc3_0_49 $PY tools/mutate_graders.py --unit PC3 --seeds 0-49
echo DONE >> "$OUT/ALL_EXIT_r17.txt"
