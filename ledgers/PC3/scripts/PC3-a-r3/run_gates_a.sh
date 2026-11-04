#!/bin/bash
# Round-3 gate run for PC3 slice a (hub index.html, L01-L03, lab twins L01-L03). Run from the checkout root.
set -u
PY=.venv/bin/python
OUT=ledgers/PC3/scripts/PC3-a-r3/outputs
mkdir -p "$OUT"
{
echo "== check_pages PC3 L01/L02/L03"
for p in L01 L02 L03; do $PY tools/check_pages.py --unit PC3 --page $p; echo "exit=$?"; done
echo "== check_pages PC3 (unit)"; $PY tools/check_pages.py --unit PC3; echo "exit=$?"
echo "== check_dag PC3"; $PY tools/check_dag.py --unit PC3; echo "exit=$?"
echo "== check_dag --all"; $PY tools/check_dag.py --all; echo "exit=$?"
echo "== check_projects PC3"; $PY tools/check_projects.py --unit PC3; echo "exit=$?"
echo "== run_labs PC3 L01"; $PY tools/run_labs.py --unit PC3 --page L01; echo "exit=$?"
echo "== run_labs PC3 L02"; $PY tools/run_labs.py --unit PC3 --page L02; echo "exit=$?"
echo "== run_labs PC3 L03"; $PY tools/run_labs.py --unit PC3 --page L03; echo "exit=$?"
echo "== ruff check twins"; $PY -m ruff check tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py; echo "exit=$?"
echo "== ruff format twins"; $PY -m ruff format --check tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py; echo "exit=$?"
echo "== mypy twins"; $PY -m mypy --no-incremental tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py; echo "exit=$?"
echo "== verify_refs offline"; $PY tools/verify_refs.py --offline; echo "exit=$?"
echo "== verify_refs unit PC3"; $PY tools/verify_refs.py --unit PC3; echo "exit=$?"
echo "== pytest labs PC3 collect-only"; $PY -m pytest tests/test_labs.py -k PC3 --collect-only -q; echo "exit=$?"
echo "== pytest labs PC3"; $PY -m pytest tests/test_labs.py -k PC3 -q; echo "exit=$?"
echo "== page_smoke PC3 index L01 L02 L03"; $PY tools/page_smoke.py --unit PC3 --pages index L01 L02 L03; echo "exit=$?"
} > "$OUT/gates.out" 2>&1
echo "gates done"
