#!/bin/bash
# Round 15 verifier gate runner for PC3 slice c. Each command's exit code is recorded.
cd /Users/billyribeiro/.fanout/wt/verifyE15-PC3-c
O=ledgers/PC3/scripts/PC3-c-r15/out
run() { name="$1"; shift; ( "$@" ) > "$O/$name.out" 2>&1; echo "$name exit=$?" >> "$O/ALL_EXIT.txt"; }
rm -f "$O/ALL_EXIT.txt"
run check_pages_unit .venv/bin/python tools/check_pages.py --unit PC3
run check_dag_unit .venv/bin/python tools/check_dag.py --unit PC3
run check_projects_unit .venv/bin/python tools/check_projects.py --unit PC3
run page_smoke_project .venv/bin/python tools/page_smoke.py --unit PC3 --pages project.html
run run_labs_project .venv/bin/python tools/run_labs.py --unit PC3 --page project
run run_graders_0_49 .venv/bin/python tools/run_graders.py --unit PC3 --seeds 0-49
run ruff_check .venv/bin/ruff check course/modules/PC/PC3 tests/labs/PC3 tests/test_*.py
run ruff_format .venv/bin/ruff format --check course/modules/PC/PC3 tests/labs/PC3
run mypy_repo .venv/bin/mypy --no-incremental
run pytest_pc3 .venv/bin/pytest -k PC3 -q
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run fetch_data_check .venv/bin/python tools/fetch_data.py --check
run build_site_check .venv/bin/python tools/build_site.py --check
run mutate_pc3_0_49 .venv/bin/python tools/mutate_graders.py --unit PC3 --seeds 0-49
echo DONE >> "$O/ALL_EXIT.txt"
