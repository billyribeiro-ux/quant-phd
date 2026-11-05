#!/bin/bash
# Round 7 (SC1-d): collect count, starter failure, and reference pass for seed 0, all run from a scratch copy of the grader.
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyE7-SC1-d
O=$ROOT/ledgers/SC1/scripts/SC1-d-r7/out
PY=$ROOT/.venv/bin/python
W=$(mktemp -d /tmp/sc1d-r7-suite-XXXX)
cp $ROOT/course/modules/SC/SC1/grader/test_project.py $ROOT/course/modules/SC/SC1/grader/instance.py "$W"/
cp $ROOT/course/modules/SC/SC1/grader/reference.py "$W"/bm_checks.py
cd "$W" || exit 1
$PY -I -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -2 > $O/collect_test_project_r7.txt
QF_SEED=0 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 > $O/suite_reference_seed0_r7.txt
QF_SEED=7 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 > $O/suite_reference_seed7_r7.txt
cp $ROOT/course/modules/SC/SC1/grader/starter.py bm_checks.py
QF_SEED=0 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 > $O/suite_starter_seed0_r7.txt
cd /; rm -rf "$W"
echo done
