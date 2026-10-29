#!/bin/bash
# Round 6, M7 slice a (hub index.html, L01-L03 and their twins). Run from the checkout root.
set -u
cd "$(dirname "$0")/../../../.." || exit 1
S=ledgers/M7/scripts/M7-a-r6
echo "== run_labs L01/L02/L03"; for p in L01 L02 L03; do .venv/bin/python tools/run_labs.py --unit M7 --page $p; echo "exit=$?"; done
echo "== independent lab check"; python3 -I $S/check_labs.py "$PWD"
echo "== independent number recomputation"; python3 -I $S/recompute_numbers.py
echo "== check_pages"; .venv/bin/python tools/check_pages.py --unit M7; echo "exit=$?"
echo "== check_dag"; .venv/bin/python tools/check_dag.py --unit M7; echo "exit=$?"
echo "== ruff/mypy twins"; .venv/bin/ruff check tests/labs/M7/lab-M7-L01-1.py tests/labs/M7/lab-M7-L02-1.py tests/labs/M7/lab-M7-L03-1.py; .venv/bin/ruff format --check tests/labs/M7/lab-M7-L01-1.py tests/labs/M7/lab-M7-L02-1.py tests/labs/M7/lab-M7-L03-1.py
.venv/bin/mypy --no-incremental --strict tests/labs/M7/lab-M7-L01-1.py tests/labs/M7/lab-M7-L02-1.py tests/labs/M7/lab-M7-L03-1.py; echo "exit=$?"
echo "== pytest lab twins"; .venv/bin/pytest tests/test_labs.py -q -k "M7 and (L01 or L02 or L03)"; echo "exit=$?"
echo "== verify_refs offline"; .venv/bin/python tools/verify_refs.py --offline; echo "exit=$?"
echo "== check_projects (unit-level, not this slice)"; .venv/bin/python tools/check_projects.py --unit M7 | tail -1
echo "== page_smoke index L01 L02 L03"; .venv/bin/python tools/page_smoke.py --unit M7 --pages index L01 L02 L03; echo "exit=$?"
