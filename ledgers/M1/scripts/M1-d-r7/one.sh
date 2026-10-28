#!/bin/bash
# usage: one.sh <engine.py> ; runs seed 0 of the grader against that engine, prints summary
W=$(mktemp -d /tmp/m1-v7/d/one.XXXX)
cp /tmp/verify7-M1-d/course/modules/M/M1/grader/*.py $W/
cp "$1" $W/annuity_engine.py
cd $W && QF_SEED=${SEED:-0} /tmp/verify7-M1-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error -c /dev/null --rootdir=$W test_project.py 2>&1 | grep -E "^FAILED|passed|failed" | head -6
rm -rf $W
