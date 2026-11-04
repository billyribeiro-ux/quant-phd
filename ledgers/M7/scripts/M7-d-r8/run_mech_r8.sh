#!/bin/bash
# Round 8 mechanical gates for M7-d, run from the verifier checkout (pin 2d75559).
cd /Users/billyribeiro/.fanout/wt/verifyD8-M7-d || exit 1
S=ledgers/M7/scripts/M7-d-r8
V=.venv/bin/python
{ $V tools/check_pages.py --unit M7; echo "exit $?"; } > $S/check_pages_M7.log 2>&1
{ $V tools/check_projects.py --unit M7; echo "exit $?"; } > $S/check_projects_M7.log 2>&1
{ $V tools/check_dag.py --all; echo "exit $?"; } > $S/check_dag_all.log 2>&1
{ $V tools/run_labs.py --unit M7; echo "exit $?"; } > $S/run_labs_M7.log 2>&1
{ $V tools/page_smoke.py --unit M7 --pages project; echo "exit $?"; } > $S/page_smoke_project.log 2>&1
{ $V tools/verify_refs.py --offline; echo "exit $?"; } > $S/verify_refs_offline.log 2>&1
echo done > $S/MECH_DONE_r8
