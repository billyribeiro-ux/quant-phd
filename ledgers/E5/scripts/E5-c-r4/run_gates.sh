#!/bin/bash
# E5-c round 4 gate runs on pin b276325 (run from the checkout root)
cd "$(dirname "$0")/../../../.." || exit 1
set -u
run() { echo "### $*"; .venv/bin/python "$@" 2>&1 | tail -4; echo "exit=${PIPESTATUS[0]}"; }
run tools/check_pages.py --unit E5
run tools/check_dag.py --unit E5
run tools/check_projects.py --unit E5
run tools/run_labs.py --unit E5 --page L07
run tools/run_labs.py --unit E5 --page L08
run tools/page_smoke.py --unit E5 --pages L07 L08
run tools/verify_refs.py --offline
run tools/run_graders.py --unit E5
echo "### ruff (twins)"; .venv/bin/python -m ruff check tests/labs/E5/lab-E5-L07-1.py tests/labs/E5/lab-E5-L08-1.py; .venv/bin/python -m ruff format --check tests/labs/E5/lab-E5-L07-1.py tests/labs/E5/lab-E5-L08-1.py
echo "### mypy (twins)"; .venv/bin/python -m mypy --no-incremental tests/labs/E5/lab-E5-L07-1.py tests/labs/E5/lab-E5-L08-1.py
echo "### pytest"; .venv/bin/python -m pytest -q tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py 2>&1 | tail -2
echo "### twin vs page"; python3 -I ledgers/E5/scripts/E5-c-r4/twin_check.py "$PWD"
echo "### recompute"; python3 -I ledgers/E5/scripts/E5-c-r4/recompute.py | tail -1
echo "### cards"; python3 -I ledgers/E5/scripts/E5-c-r4/cards_check.py "$PWD" | head -2
