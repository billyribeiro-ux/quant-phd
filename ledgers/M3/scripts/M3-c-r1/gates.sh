#!/bin/bash
# Slice M3-c closing delta gates at pin 95f3f8cb. Each command's rc is recorded.
cd /Users/billyribeiro/.fanout/wt/verifyF21-M3-c || exit 1
OUT=ledgers/M3/scripts/M3-c-r1/out
PY=.venv/bin/python
run() { name="$1"; shift; echo "== $name" >> $OUT/gates.out; "$@" >> $OUT/$name.log 2>&1; rc=$?; echo "rc=$rc $name: $*" >> $OUT/gates.out; }
: > $OUT/gates.out
run check_pages_M3 $PY tools/check_pages.py --unit M3
run check_pages_L07 $PY tools/check_pages.py --unit M3 --page L07
run check_pages_L08 $PY tools/check_pages.py --unit M3 --page L08
run check_pages_L09 $PY tools/check_pages.py --unit M3 --page L09
run check_dag_M3 $PY tools/check_dag.py --unit M3
run check_projects_M3 $PY tools/check_projects.py --unit M3
run run_labs_M3 $PY tools/run_labs.py --unit M3
run run_labs_L07 $PY tools/run_labs.py --unit M3 --page L07
run run_labs_L08 $PY tools/run_labs.py --unit M3 --page L08
run run_labs_L09 $PY tools/run_labs.py --unit M3 --page L09
run ruff_check $PY -m ruff check tests/labs/M3 course/modules/M/M3/grader
run ruff_format $PY -m ruff format --check tests/labs/M3
run mypy $PY -m mypy --no-incremental
run pytest_M3 $PY -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k M3 -q
run build_site_check $PY tools/build_site.py --check
run render_curriculum $PY tools/render_curriculum.py
run render_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run verify_refs_offline $PY tools/verify_refs.py --offline
run fetch_data_check $PY tools/fetch_data.py --check
run page_smoke_L07 $PY tools/page_smoke.py --unit M3 --pages L07
run page_smoke_L08 $PY tools/page_smoke.py --unit M3 --pages L08
run page_smoke_L09 $PY tools/page_smoke.py --unit M3 --pages L09
echo DONE >> $OUT/gates.out
