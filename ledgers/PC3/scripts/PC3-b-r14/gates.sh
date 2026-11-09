#!/bin/bash
# Round-14 gate commands for PC3 slice b, run in the verifier checkout (pin 8e5751c).
cd /Users/billyribeiro/.fanout/wt/verifyE14-PC3-b || exit 1
O=ledgers/PC3/scripts/PC3-b-r14/out
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "$name exit=$?" >> "$O/ALL_EXIT.txt"; }
rm -f "$O/ALL_EXIT.txt"
run run_labs_unit .venv/bin/python tools/run_labs.py --unit PC3
run check_pages .venv/bin/python tools/check_pages.py --unit PC3
run check_dag .venv/bin/python tools/check_dag.py --unit PC3
run check_projects .venv/bin/python tools/check_projects.py --unit PC3
run ruff_check .venv/bin/ruff check tests/labs/PC3
run ruff_format .venv/bin/ruff format --check tests/labs/PC3
run mypy .venv/bin/mypy --no-incremental
run pytest_lab_tooling .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run fetch_data_check .venv/bin/python tools/fetch_data.py --check
run render_curriculum_diff sh -c '.venv/bin/python tools/render_curriculum.py && git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json'
run build_site_check .venv/bin/python tools/build_site.py --check
echo DONE >> "$O/ALL_EXIT.txt"
