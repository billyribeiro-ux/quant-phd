#!/bin/sh
# CF8-a round 3 gate commands, run from the checkout root (python from .venv).
set -u
cd "$(dirname "$0")/../../../.." || exit 1
PY=.venv/bin/python
echo "== check_pages"; $PY tools/check_pages.py --unit CF8; echo "exit=$?"
echo "== check_dag"; $PY tools/check_dag.py --unit CF8; echo "exit=$?"
echo "== check_projects"; $PY tools/check_projects.py --unit CF8; echo "exit=$?"
echo "== run_labs L01"; $PY tools/run_labs.py --unit CF8 --page L01; echo "exit=$?"
echo "== run_labs L02"; $PY tools/run_labs.py --unit CF8 --page L02; echo "exit=$?"
echo "== page_smoke (stems index L01 L02)"; $PY tools/page_smoke.py --unit CF8 --pages index L01 L02; echo "exit=$?"
echo "== verify_refs --offline (registry-wide; --unit needs live run)"; $PY tools/verify_refs.py --offline; echo "exit=$?"
echo "== ruff twins"; .venv/bin/ruff check tests/labs/CF8/lab-CF8-L01-1.py tests/labs/CF8/lab-CF8-L02-1.py; echo "exit=$?"
echo "== mypy twins"; .venv/bin/mypy --no-incremental tests/labs/CF8/lab-CF8-L01-1.py tests/labs/CF8/lab-CF8-L02-1.py; echo "exit=$?"
echo "== lab twin vs page"; $PY -I ledgers/CF8/scripts/CF8-a-r3/lab_check.py | head -6; echo "exit=$?"
echo "== numbers"; $PY -I ledgers/CF8/scripts/CF8-a-r3/recheck_numbers.py | head -3; echo "exit=$?"
