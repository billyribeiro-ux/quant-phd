#!/bin/bash
# Round 9 slice a gates; run from checkout root. Logs to gates/.
cd "$(dirname "$0")/../../../.." || exit 1
G=ledgers/M4/scripts/M4-a-r9/gates
run() { name=$1; shift; "$@" > "$G/$name.log" 2>&1; echo "$name exit=$?" >> "$G/_exit_codes.log"; }
rm -f "$G/_exit_codes.log"
run check_pages .venv/bin/python tools/check_pages.py --unit M4
run check_dag .venv/bin/python tools/check_dag.py --unit M4
run check_projects .venv/bin/python tools/check_projects.py --unit M4
run run_labs_M4 .venv/bin/python tools/run_labs.py --unit M4
run ruff_check .venv/bin/ruff check tests/labs/M4 course/modules/M/M4
run ruff_format .venv/bin/ruff format --check tests/labs/M4 course/modules/M/M4
run mypy .venv/bin/mypy --no-incremental
run pytest_relevant .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_docs_figures.py tests/test_page_smoke.py tests/test_curriculum.py
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run verify_refs_unit_M4 .venv/bin/python tools/verify_refs.py --unit M4
run render_curriculum_diff .venv/bin/python tools/render_curriculum.py
run build_site_check .venv/bin/python tools/build_site.py --check
echo done >> "$G/_exit_codes.log"
