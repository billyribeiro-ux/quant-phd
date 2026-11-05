#!/bin/bash
# Round 9 mechanical gates for M7-d, run from the verifier checkout (pin 1e272e5).
cd /Users/billyribeiro/.fanout/wt/verifyD9-M7-d || exit 1
S=ledgers/M7/scripts/M7-d-r9
V=.venv/bin/python
{ $V tools/check_pages.py --unit M7; echo "exit $?"; } > $S/check_pages_M7.log 2>&1
{ $V tools/check_projects.py --unit M7; echo "exit $?"; } > $S/check_projects_M7.log 2>&1
{ $V tools/check_dag.py --all; echo "exit $?"; } > $S/check_dag_all.log 2>&1
{ $V tools/run_labs.py --unit M7; echo "exit $?"; } > $S/run_labs_M7.log 2>&1
{ $V tools/page_smoke.py --unit M7 --pages project; echo "exit $?"; } > $S/page_smoke_project.log 2>&1
{ $V tools/verify_refs.py --offline; echo "exit $?"; } > $S/verify_refs_offline.log 2>&1
{ $V tools/run_graders.py --unit M7 --seeds 0-49; echo "exit $?"; } > $S/run_graders_M7_0-49.log 2>&1
{ .venv/bin/ruff check course/modules/M/M7 tests/labs/M7 tools 2>&1; .venv/bin/ruff format --check course/modules/M/M7 tests/labs/M7 2>&1; echo "exit $?"; } > $S/ruff_M7_r9.log 2>&1
{ $V -m mypy --no-incremental 2>&1; echo "exit $?"; } > $S/mypy_r9.log 2>&1
{ $V -m pytest -q tests/test_labs.py -k M7 2>&1 | tail -5; echo "exit ${PIPESTATUS[0]}"; } > $S/pytest_M7_r9.log 2>&1
{ $V tools/mutate_graders.py --unit M7 --seeds 0-9; echo "exit $?"; } > $S/mutate_M7_0-9_r9.log 2>&1
echo done > $S/MECH_DONE_r9
