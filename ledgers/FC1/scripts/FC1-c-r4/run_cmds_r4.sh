#!/bin/bash
# FC1-c round 4 command runner: every command row, run from the verifier checkout.
set -u
cd /Users/billyribeiro/.fanout/wt/verifyD4-FC1-c
OUT=ledgers/FC1/scripts/FC1-c-r4/out
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "$name exit=$?" >> "$OUT/_exit_codes.txt"; }
rm -f "$OUT/_exit_codes.txt"
run check_pages $PY tools/check_pages.py --unit FC1
run check_dag $PY tools/check_dag.py --unit FC1
run check_projects $PY tools/check_projects.py --unit FC1
run run_labs_project $PY tools/run_labs.py --unit FC1 --page project
run run_labs_fc1 $PY tools/run_labs.py --unit FC1
run run_graders_0_49 $PY tools/run_graders.py --unit FC1 --seeds 0-49
run page_smoke_project $PY tools/page_smoke.py --unit FC1 --pages project
run ruff_check_repo .venv/bin/ruff check .
run ruff_format_repo .venv/bin/ruff format --check .
run mypy_no_incremental .venv/bin/mypy --no-incremental
run verify_refs_offline $PY tools/verify_refs.py --offline
run collect_only .venv/bin/pytest --collect-only -q course/modules/FC/FC1/grader/test_project.py
run mutate_graders_0_9 $PY tools/mutate_graders.py --unit FC1 --seeds 0-9
run mutate_graders_0_19 $PY tools/mutate_graders.py --unit FC1 --seeds 0-19
echo DONE >> "$OUT/_exit_codes.txt"
