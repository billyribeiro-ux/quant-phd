#!/bin/bash
# Round 1 closing delta gates, pin d9de2fe5. Run sequentially.
cd /Users/billyribeiro/.fanout/wt/verifyH1-E3-f
S=ledgers/E3/scripts/E3-f-r1
O=$S/out2
PY=.venv/bin/python
rm -f $O/_rc.txt
run(){ name=$1; shift; "$@" > $O/$name.out 2>&1; echo "$name rc=$?" >> $O/_rc.txt; }
run check_pages_unit $PY tools/check_pages.py --unit E3
run check_dag_unit $PY tools/check_dag.py --unit E3
run check_projects_unit $PY tools/check_projects.py --unit E3
run run_labs_L01 $PY tools/run_labs.py --unit E3 --page L01
run run_labs_L02 $PY tools/run_labs.py --unit E3 --page L02
run run_labs_L03 $PY tools/run_labs.py --unit E3 --page L03
run run_labs_L04 $PY tools/run_labs.py --unit E3 --page L04
run ruff_labs $PY -m ruff check tests/labs/E3 course/modules/E/E3/grader
run ruff_format_labs $PY -m ruff format --check tests/labs/E3
run ruff_repo $PY -m ruff check .
run ruff_format_repo $PY -m ruff format --check .
run build_site_check $PY tools/build_site.py --check
run render_curriculum $PY tools/render_curriculum.py
run render_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run fetch_data_check $PY tools/fetch_data.py --check
run verify_refs_offline $PY tools/verify_refs.py --offline
echo DONE >> $O/_rc.txt
