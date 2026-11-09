#!/bin/bash
# BK4 slice d, round 1 (verifier F31): cards-slice gates on pin 95f3f8cb. Each output goes to out/.
cd /Users/billyribeiro/.fanout/wt/verifyF31-BK4-d || exit 1
O=ledgers/BK4/scripts/BK4-d-r1/out
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$O/$name.txt" 2>&1; echo "$name exit=$?" >> "$O/_exit_codes.txt"; }
: > "$O/_exit_codes.txt"
run check_pages $PY tools/check_pages.py --unit BK4
run check_dag $PY tools/check_dag.py --unit BK4
run run_labs_unit $PY tools/run_labs.py --unit BK4
run page_smoke_unit $PY tools/page_smoke.py --unit BK4
run pytest_page_checks $PY -m pytest -q tests/test_page_checks.py
run verify_refs_live $PY tools/verify_refs.py --unit BK4
run verify_refs_offline $PY tools/verify_refs.py --offline
run collect_grader $PY -m pytest --collect-only -q course/modules/BK/BK4/grader/test_project.py
echo DONE >> "$O/_exit_codes.txt"
