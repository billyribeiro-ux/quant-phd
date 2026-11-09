#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyD15-E3-f
S=ledgers/E3/scripts/E3-f-r15
O=$S/out
PY=.venv/bin/python
run(){ name=$1; shift; "$@" > $O/$name.out 2>&1; echo "$name rc=$?" >> $O/_rc.txt; }
run check_pages_unit $PY tools/check_pages.py --unit E3
run check_dag_unit $PY tools/check_dag.py --unit E3
run check_projects_unit $PY tools/check_projects.py --unit E3
run run_labs_L01 $PY tools/run_labs.py --unit E3 --page L01
run run_labs_L02 $PY tools/run_labs.py --unit E3 --page L02
run run_labs_L03 $PY tools/run_labs.py --unit E3 --page L03
run run_labs_L04 $PY tools/run_labs.py --unit E3 --page L04
run page_smoke $PY tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04
run ruff_check $PY -m ruff check tests/labs/E3 course/modules/E/E3/grader
run ruff_format $PY -m ruff format --check tests/labs/E3
run mypy $PY -m mypy --no-incremental
run pytest_e3 $PY -m pytest -q tests -k "E3 or lab"
run pytest_docs $PY -m pytest -q tests/test_docs_figures.py tests/test_refs.py
run verify_refs_offline $PY tools/verify_refs.py --offline
run build_site_check $PY tools/build_site.py --check
run render_curriculum $PY tools/render_curriculum.py
run render_diff git diff --stat -- CURRICULUM.md curriculum/curriculum.json
run fetch_data_check $PY tools/fetch_data.py --check
echo DONE >> $O/_rc.txt
