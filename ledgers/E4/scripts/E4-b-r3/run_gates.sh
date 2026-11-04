#!/bin/bash
# E4-b round 3 command gates. Run from the checkout root.
set -u
cd "$(dirname "$0")/../../../.." || exit 1
O=ledgers/E4/scripts/E4-b-r3/outputs
PY=.venv/bin/python
run() { name=$1; shift; "$@" > $O/$name.txt 2>&1; echo "$name exit=$?"; }
run check_pages_E4 $PY tools/check_pages.py --unit E4
run check_dag_E4 $PY tools/check_dag.py --unit E4
run check_projects_E4 $PY tools/check_projects.py --unit E4
run run_labs_E4 $PY tools/run_labs.py --unit E4
run run_labs_L04 $PY tools/run_labs.py --unit E4 --page L04
run run_labs_L05 $PY tools/run_labs.py --unit E4 --page L05
run run_labs_L06 $PY tools/run_labs.py --unit E4 --page L06
for t in lab-E4-L04-1 lab-E4-L05-1 lab-E4-L06-1; do run twin_$t $PY -I -W error tests/labs/E4/$t.py; done
run ruff_check $PY -m ruff check tests/labs/E4/lab-E4-L04-1.py tests/labs/E4/lab-E4-L05-1.py tests/labs/E4/lab-E4-L06-1.py
run ruff_format $PY -m ruff format --check tests/labs/E4/lab-E4-L04-1.py tests/labs/E4/lab-E4-L05-1.py tests/labs/E4/lab-E4-L06-1.py
run mypy_twins $PY -m mypy --no-incremental tests/labs/E4/lab-E4-L04-1.py tests/labs/E4/lab-E4-L05-1.py tests/labs/E4/lab-E4-L06-1.py
run verify_refs_offline $PY tools/verify_refs.py --offline
run page_smoke_L04_06 $PY tools/page_smoke.py --unit E4 --pages L04 L05 L06
run pytest_labs $PY -m pytest tests/test_labs.py tests/test_run_labs.py -q -k "E4 or L04 or L05 or L06"
