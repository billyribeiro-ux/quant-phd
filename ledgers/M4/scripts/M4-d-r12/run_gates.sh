#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyD12-M4-d
G=ledgers/M4/scripts/M4-d-r12/gates
PY=.venv/bin/python
$PY tools/check_pages.py --all > $G/check_pages_all.out 2>&1; echo "exit $?" >> $G/check_pages_all.out
$PY tools/check_dag.py --all > $G/check_dag_all.out 2>&1; echo "exit $?" >> $G/check_dag_all.out
$PY tools/check_projects.py --all > $G/check_projects_all.out 2>&1; echo "exit $?" >> $G/check_projects_all.out
$PY tools/run_labs.py --help > $G/run_labs_help.out 2>&1
$PY tools/run_labs.py --unit M4 > $G/run_labs_M4.out 2>&1; echo "exit $?" >> $G/run_labs_M4.out
$PY tools/run_graders.py --unit M4 --seeds 0-49 > $G/run_graders_M4_0-49.out 2>&1; echo "exit $?" >> $G/run_graders_M4_0-49.out
$PY tools/mutate_graders.py --unit M4 --seeds 0-9 > $G/mutate_M4_0-9.out 2>&1; echo "exit $?" >> $G/mutate_M4_0-9.out
$PY tools/page_smoke.py --unit M4 > $G/page_smoke_M4.out 2>&1; echo "exit $?" >> $G/page_smoke_M4.out
$PY tools/verify_refs.py --offline > $G/verify_refs_offline.out 2>&1; echo "exit $?" >> $G/verify_refs_offline.out
echo done > $G/ALL_DONE
