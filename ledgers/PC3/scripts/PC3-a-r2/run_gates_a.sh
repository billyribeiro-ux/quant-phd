#!/bin/bash
# Round-2 gate run for PC3 slice a (hub, L01-L03, lab twins). Run from the checkout root.
set -u
PY=.venv/bin/python
OUT=/tmp/pc3-v/a-r2
mkdir -p "$OUT"
echo "== check_pages PC3 L01/L02/L03"
for p in L01 L02 L03; do $PY tools/check_pages.py --unit PC3 --page $p; echo "exit=$?"; done
echo "== check_pages PC3 (unit)"; $PY tools/check_pages.py --unit PC3; echo "exit=$?"
echo "== check_dag PC3"; $PY tools/check_dag.py --unit PC3; echo "exit=$?"
echo "== check_projects PC3"; $PY tools/check_projects.py --unit PC3; echo "exit=$?"
echo "== run_labs PC3 page L01"; $PY tools/run_labs.py --unit PC3 --page L01; echo "exit=$?"
echo "== run_labs PC3 page L02"; $PY tools/run_labs.py --unit PC3 --page L02; echo "exit=$?"
echo "== run_labs PC3 page L03"; $PY tools/run_labs.py --unit PC3 --page L03; echo "exit=$?"
echo "== ruff PC3 twins"; $PY -m ruff check tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py; echo "exit=$?"
$PY -m ruff format --check tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py; echo "exit=$?"
echo "== mypy twins"; $PY -m mypy --no-incremental tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py; echo "exit=$?"
echo "== verify_refs offline"; $PY tools/verify_refs.py --offline; echo "exit=$?"
