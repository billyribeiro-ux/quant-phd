#!/bin/bash
# Round-6 gate runs for SC1 slice d, executed from the verifier checkout root.
set -u
cd /Users/billyribeiro/.fanout/wt/verifyE6-SC1-d || exit 1
O=ledgers/SC1/scripts/SC1-d-r6/out
PY=.venv/bin/python
$PY tools/run_labs.py --unit SC1 > $O/run_labs_SC1.txt 2>&1; echo "run_labs exit $?" >> $O/run_labs_SC1.txt
$PY tools/check_pages.py --unit SC1 > $O/check_pages_SC1.txt 2>&1; echo "check_pages exit $?" >> $O/check_pages_SC1.txt
$PY tools/check_dag.py --unit SC1 > $O/check_dag_SC1.txt 2>&1; echo "check_dag exit $?" >> $O/check_dag_SC1.txt
$PY tools/check_projects.py --unit SC1 > $O/check_projects_SC1.txt 2>&1; echo "check_projects exit $?" >> $O/check_projects_SC1.txt
$PY tools/run_graders.py --unit SC1 --seeds 0-49 > $O/run_graders_SC1_0-49.txt 2>&1; echo "run_graders exit $?" >> $O/run_graders_SC1_0-49.txt
$PY tools/verify_refs.py --offline --unit SC1 > $O/verify_refs_offline_SC1.txt 2>&1; echo "verify_refs exit $?" >> $O/verify_refs_offline_SC1.txt
echo done > $O/_done_fast.txt
