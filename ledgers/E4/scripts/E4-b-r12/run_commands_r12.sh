#!/bin/bash
# Round-12 command battery for E4 slice b (L04-L06 and lab twins). Run from the checkout root.
set -u
cd /Users/billyribeiro/.fanout/wt/verifyE12-E4-b || exit 1
PY=.venv/bin/python
O=ledgers/E4/scripts/E4-b-r12/outputs
run() { name="$1"; shift; "$@" > "$O/$name.txt" 2>&1; echo "$name exit=$?" >> "$O/_exit_codes.txt"; }
rm -f "$O/_exit_codes.txt"
run check_pages_E4 $PY tools/check_pages.py --unit E4
run check_pages_L04 $PY tools/check_pages.py --unit E4 --page L04
run check_pages_L05 $PY tools/check_pages.py --unit E4 --page L05
run check_pages_L06 $PY tools/check_pages.py --unit E4 --page L06
run check_pages_all $PY tools/check_pages.py --all
run check_dag_E4 $PY tools/check_dag.py --unit E4
run check_dag_all $PY tools/check_dag.py --all
run check_projects_E4 $PY tools/check_projects.py --unit E4
run run_labs_E4 $PY tools/run_labs.py --unit E4
run ruff_twins .venv/bin/ruff check tests/labs/E4/lab-E4-L04-1.py tests/labs/E4/lab-E4-L05-1.py tests/labs/E4/lab-E4-L06-1.py
run ruff_format_twins .venv/bin/ruff format --check tests/labs/E4/lab-E4-L04-1.py tests/labs/E4/lab-E4-L05-1.py tests/labs/E4/lab-E4-L06-1.py
run ruff_repo .venv/bin/ruff check .
run ruff_format_repo .venv/bin/ruff format --check .
run mypy_full .venv/bin/mypy --no-incremental
run mypy_twins .venv/bin/mypy --no-incremental tests/labs/E4/lab-E4-L04-1.py tests/labs/E4/lab-E4-L05-1.py tests/labs/E4/lab-E4-L06-1.py
run pytest_labs $PY -m pytest tests/test_labs.py tests/test_run_labs.py -rA -q
run pytest_page $PY -m pytest tests/test_page_checks.py tests/test_page_smoke.py -rA -q
run page_smoke_E4 $PY tools/page_smoke.py --unit E4 --pages L04 L05 L06
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_unit_E4_live $PY tools/verify_refs.py --unit E4
run render_curriculum $PY tools/render_curriculum.py
run render_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run fetch_data_check $PY tools/fetch_data.py --check
run build_site_check $PY tools/build_site.py --check
echo DONE >> "$O/_exit_codes.txt"
