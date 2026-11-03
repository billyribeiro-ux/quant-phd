#!/bin/bash
# FC1-c round 3 command rows, run on pin a007712 (verifier D3). Each command's exact output is kept.
cd /Users/billyribeiro/.fanout/wt/verifyD3-FC1-c
O=ledgers/FC1/scripts/FC1-c-r3/out
rm -f "$O/_exit_codes.txt"
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "$name exit=$?" >> "$O/_exit_codes.txt"; }
run check_pages .venv/bin/python tools/check_pages.py --unit FC1
run check_dag .venv/bin/python tools/check_dag.py --unit FC1
run check_projects .venv/bin/python tools/check_projects.py --unit FC1
run run_labs_project .venv/bin/python tools/run_labs.py --unit FC1 --page project
run run_labs_all_pages .venv/bin/python tools/run_labs.py --unit FC1
run run_graders_0_19 .venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-19
run mutate_graders_0_9 .venv/bin/python tools/mutate_graders.py --unit FC1 --seeds 0-9
run page_smoke_project .venv/bin/python tools/page_smoke.py --unit FC1 --pages project
run ruff_check_grader_labs .venv/bin/ruff check course/modules/FC/FC1/grader tests/labs/FC1
run ruff_format_grader_labs .venv/bin/ruff format --check course/modules/FC/FC1/grader tests/labs/FC1
run ruff_repo .venv/bin/ruff check .
run ruff_format_repo .venv/bin/ruff format --check .
run mypy_no_incremental .venv/bin/mypy --no-incremental
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run render_curriculum_check .venv/bin/python tools/render_curriculum.py
run render_curriculum_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run build_site_check .venv/bin/python tools/build_site.py --check
echo DONE >> "$O/_exit_codes.txt"
