#!/bin/bash
# FC1-c round 2 command rows, run on pin c737272 (verifier D2). Each command's exact output is kept.
cd /Users/billyribeiro/.fanout/wt/verifyD2-FC1-c
O=ledgers/FC1/scripts/FC1-c-r2/out
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "$name exit=$?" >> "$O/_exit_codes.txt"; }
run check_pages .venv/bin/python tools/check_pages.py --unit FC1
run check_dag .venv/bin/python tools/check_dag.py --unit FC1
run check_projects .venv/bin/python tools/check_projects.py --unit FC1
run run_labs_project .venv/bin/python tools/run_labs.py --unit FC1 --page project
run run_graders_0_19 .venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-19
run mutate_graders_0_9 .venv/bin/python tools/mutate_graders.py --unit FC1 --seeds 0-9
run page_smoke_project .venv/bin/python tools/page_smoke.py --unit FC1 --pages project
run ruff_check .venv/bin/ruff check course/modules/FC/FC1/grader tests/labs/FC1
run ruff_format .venv/bin/ruff format --check course/modules/FC/FC1/grader tests/labs/FC1
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
echo DONE >> "$O/_exit_codes.txt"
