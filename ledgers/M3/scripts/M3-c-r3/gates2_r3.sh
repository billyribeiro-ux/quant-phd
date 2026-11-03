#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyD3-M3-c
D=ledgers/M3/scripts/M3-c-r3
PY=.venv/bin/python
$PY tools/check_projects.py --unit M3 > $D/check_projects_M3_r3.log 2>&1; echo "EXIT=$?" >> $D/check_projects_M3_r3.log
$PY tools/run_graders.py --unit M3 --seeds 0-49 > $D/run_graders_M3_r3.log 2>&1; echo "EXIT=$?" >> $D/run_graders_M3_r3.log
$PY -m pytest -q tests/test_labs.py -k "M3" > $D/pytest_labs_M3_r3.log 2>&1; echo "EXIT=$?" >> $D/pytest_labs_M3_r3.log
echo DONE > $D/gates2_done.flag
