#!/bin/bash
# Round-4 slice-a gates at pin edbb7aa8. Usage: run_gates_a_r4.sh <checkout-root>
cd "$1" || exit 1
O=ledgers/M2/scripts/M2-a-r4
PY=.venv/bin/python
run() { name=$1; shift; "$@" > "$O/$name.out" 2>&1; echo "EXIT $?" >> "$O/$name.out"; }
run g01_check_pages $PY tools/check_pages.py --unit M2
run g02_check_dag $PY tools/check_dag.py --unit M2
run g03_run_labs $PY tools/run_labs.py --unit M2
run g05_pytest_labs $PY -m pytest -q tests/test_labs.py -k "M2 and (L01 or L02 or L03 or L04 or L05 or L06)"
run g08_page_smoke $PY tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06 --skip-sweep
run g06_ruff bash -c "$PY -m ruff check tests/labs/M2/lab-M2-L0[1-6]-1.py && $PY -m ruff format --check tests/labs/M2/lab-M2-L0[1-6]-1.py"
run g07_mypy $PY -m mypy --no-incremental tests/labs/M2/lab-M2-L01-1.py tests/labs/M2/lab-M2-L02-1.py tests/labs/M2/lab-M2-L03-1.py tests/labs/M2/lab-M2-L04-1.py tests/labs/M2/lab-M2-L05-1.py tests/labs/M2/lab-M2-L06-1.py
run g10_verify_refs_offline $PY tools/verify_refs.py --offline
run g09_check_projects $PY tools/check_projects.py --unit M2
$PY ledgers/M2/scripts/M2-a-r4/lab_slice_a_r4.py "$1" > "$O/g04_twins_isolated.out" 2>&1; echo "EXIT $?" >> "$O/g04_twins_isolated.out"
echo DONE > "$O/gates_done.flag"
