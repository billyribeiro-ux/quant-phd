#!/bin/bash
# Round-7 gates for PC3 slice a (hub index, L01-L03, lab twins). Run from the checkout root.
set -u
OUT=ledgers/PC3/scripts/PC3-a-r7/outputs
PY=.venv/bin/python
{
echo "== check_pages --unit PC3"; $PY tools/check_pages.py --unit PC3; echo "exit=$?"
for p in L01 L02 L03; do echo "== check_pages --unit PC3 --page $p"; $PY tools/check_pages.py --unit PC3 --page $p; echo "exit=$?"; done
echo "== check_dag --unit PC3"; $PY tools/check_dag.py --unit PC3; echo "exit=$?"
echo "== check_projects --unit PC3"; $PY tools/check_projects.py --unit PC3; echo "exit=$?"
echo "== run_labs --unit PC3"; $PY tools/run_labs.py --unit PC3; echo "exit=$?"
for p in L01 L02 L03; do echo "== run_labs --unit PC3 --page $p"; $PY tools/run_labs.py --unit PC3 --page $p; echo "exit=$?"; done
for t in L01 L02 L03; do echo "== twin $t alone: python -I -W error"; $PY -I -W error tests/labs/PC3/lab-PC3-$t-1.py > /dev/null; echo "exit=$?"; done
echo "== ruff check twins"; .venv/bin/ruff check tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py; echo "exit=$?"
echo "== ruff format --check twins"; .venv/bin/ruff format --check tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py; echo "exit=$?"
echo "== mypy --no-incremental twins"; .venv/bin/mypy --no-incremental tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py; echo "exit=$?"
echo "== pytest tests/test_labs.py -k PC3"; .venv/bin/pytest tests/test_labs.py -k PC3 -q; echo "exit=$?"
echo "== pytest collect-only -k PC3"; .venv/bin/pytest tests/test_labs.py -k PC3 --collect-only -q | tail -3; echo "exit=$?"
echo "== verify_refs --offline"; $PY tools/verify_refs.py --offline; echo "exit=$?"
echo "== run_graders --unit PC3 --seeds 0-49"; $PY tools/run_graders.py --unit PC3 --seeds 0-49; echo "exit=$?"
} > $OUT/gates.out 2>&1
echo done
