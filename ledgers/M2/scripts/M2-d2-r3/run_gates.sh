#!/bin/bash
# Gate runner for M2 slice d2 (L22, L23, L24 and twins), round 3. Run from the checkout root.
# Each gate writes <name>.out (stdout+stderr) and <name>.rc (exit code).
R=ledgers/M2/scripts/M2-d2-r3
PY=.venv/bin/python
run() { name=$1; shift; "$@" > "$R/$name.out" 2>&1; echo $? > "$R/$name.rc"; echo "$name rc=$(cat $R/$name.rc)"; }
run check_pages $PY tools/check_pages.py --unit M2
run check_dag_M2 $PY tools/check_dag.py --unit M2
run check_dag_all $PY tools/check_dag.py --all
run check_projects $PY tools/check_projects.py --unit M2
run run_labs_L22 $PY tools/run_labs.py --unit M2 --page L22
run run_labs_L23 $PY tools/run_labs.py --unit M2 --page L23
run run_labs_L24 $PY tools/run_labs.py --unit M2 --page L24
run run_labs_M2 $PY tools/run_labs.py --unit M2
run ruff_check .venv/bin/ruff check tests/labs/M2/lab-M2-L22-1.py tests/labs/M2/lab-M2-L23-1.py tests/labs/M2/lab-M2-L24-1.py
run ruff_format .venv/bin/ruff format --check tests/labs/M2/lab-M2-L22-1.py tests/labs/M2/lab-M2-L23-1.py tests/labs/M2/lab-M2-L24-1.py
run mypy .venv/bin/mypy tests/labs/M2/lab-M2-L22-1.py tests/labs/M2/lab-M2-L23-1.py tests/labs/M2/lab-M2-L24-1.py --no-incremental
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_live_M2 $PY tools/verify_refs.py --unit M2
run page_smoke_slice $PY tools/page_smoke.py --unit M2 --pages L22 L23 L24
run pytest_labs $PY -m pytest tests/test_labs.py -q
run pytest_checks $PY -m pytest tests/test_page_checks.py tests/test_run_labs.py -q
