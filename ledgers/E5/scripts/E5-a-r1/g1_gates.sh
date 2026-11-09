#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyG1-E5-a
D=ledgers/E5/scripts/E5-a-r1
P=.venv/bin/python
run(){ name=$1; shift; "$@" > $D/g1_$name.out 2>&1; echo "$name rc=$?" >> $D/g1_gates.summary; }
rm -f $D/g1_gates.summary
run check_pages_unit $P tools/check_pages.py --unit E5
run check_pages_L01 $P tools/check_pages.py --unit E5 --page L01
run check_pages_L02 $P tools/check_pages.py --unit E5 --page L02
run check_pages_L03 $P tools/check_pages.py --unit E5 --page L03
run check_dag_E5 $P tools/check_dag.py --unit E5
run check_projects_E5 $P tools/check_projects.py --unit E5
run run_labs_L01 $P tools/run_labs.py --unit E5 --page L01
run run_labs_L02 $P tools/run_labs.py --unit E5 --page L02
run run_labs_L03 $P tools/run_labs.py --unit E5 --page L03
run run_labs_unit $P tools/run_labs.py --unit E5
run page_smoke_E5 $P tools/page_smoke.py --unit E5 --pages index L01 L02 L03
run verify_refs_offline $P tools/verify_refs.py --offline
run ruff_check_E5 $P -m ruff check tests/labs/E5
run ruff_format_E5 $P -m ruff format --check tests/labs/E5
run mypy_E5 $P -m mypy --no-incremental tests/labs/E5
run pytest_E5 $P -m pytest -q -k E5
run twin_L01 $P -I -W error tests/labs/E5/lab-E5-L01-1.py
run twin_L02 $P -I -W error tests/labs/E5/lab-E5-L02-1.py
run twin_L03 $P -I -W error tests/labs/E5/lab-E5-L03-1.py
run build_site_check $P tools/build_site.py --check
echo DONE >> $D/g1_gates.summary
