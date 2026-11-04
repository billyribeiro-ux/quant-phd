#!/bin/bash
# Round-6 gate runs for BK4 slice a, from the checkout root. Each output goes to ledgers/BK4/scripts/BK4-a-r6/.
S=ledgers/BK4/scripts/BK4-a-r6
PY=.venv/bin/python
run() { name=$1; shift; "$@" > $S/$name.out 2>&1; echo "$name exit=$?" >> $S/gates_exit.txt; }
rm -f $S/gates_exit.txt
run check_pages_unit $PY tools/check_pages.py --unit BK4
run check_pages_L01 $PY tools/check_pages.py --unit BK4 --page L01
run check_pages_L02 $PY tools/check_pages.py --unit BK4 --page L02
run check_pages_L03 $PY tools/check_pages.py --unit BK4 --page L03
run check_pages_index $PY tools/check_pages.py --unit BK4 --page index
run check_dag $PY tools/check_dag.py --unit BK4
run run_labs $PY tools/run_labs.py --unit BK4
run verify_refs_offline $PY tools/verify_refs.py --offline
run ruff_check_labs .venv/bin/ruff check tests/labs/BK4
run ruff_format_labs .venv/bin/ruff format --check tests/labs/BK4
run mypy_labs .venv/bin/mypy --no-incremental tests/labs/BK4
echo done >> $S/gates_exit.txt
