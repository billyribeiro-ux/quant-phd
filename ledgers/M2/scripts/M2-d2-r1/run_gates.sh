#!/bin/bash
# Slice M2-d2 round 1 gates, run from the checkout root at pin 95f3f8cb.
cd /Users/billyribeiro/.fanout/wt/verifyF21-M2-d2 || exit 1
O=ledgers/M2/scripts/M2-d2-r1/out
P=.venv/bin/python
run() { name=$1; shift; "$@" > "$O/$name.txt" 2>&1; echo "$name exit=$?"; }
run check_pages_L22 $P tools/check_pages.py --unit M2 --page L22
run check_pages_L23 $P tools/check_pages.py --unit M2 --page L23
run check_pages_L24 $P tools/check_pages.py --unit M2 --page L24
run check_pages_unit $P tools/check_pages.py --unit M2
run check_pages_all $P tools/check_pages.py --all
run check_dag_M2 $P tools/check_dag.py --unit M2
run check_dag_all $P tools/check_dag.py --all
run check_projects_all $P tools/check_projects.py --all
run run_labs_L22 $P tools/run_labs.py --unit M2 --page L22
run run_labs_L23 $P tools/run_labs.py --unit M2 --page L23
run run_labs_L24 $P tools/run_labs.py --unit M2 --page L24
run page_smoke_L22 $P tools/page_smoke.py --unit M2 --pages L22
run page_smoke_L23 $P tools/page_smoke.py --unit M2 --pages L23
run page_smoke_L24 $P tools/page_smoke.py --unit M2 --pages L24
run ruff_check $P -m ruff check .
run ruff_format $P -m ruff format --check .
run mypy $P -m mypy --no-incremental
run pytest_labs_M2 $P -m pytest tests/test_labs.py -k M2 -q
run verify_refs_offline $P tools/verify_refs.py --offline
run verify_refs_live_M2 $P tools/verify_refs.py --unit M2
run render_curriculum $P tools/render_curriculum.py
run curriculum_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run build_site_check $P tools/build_site.py --check
run fetch_data_check $P tools/fetch_data.py --check
