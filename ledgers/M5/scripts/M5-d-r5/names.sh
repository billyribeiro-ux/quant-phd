#!/bin/bash
# usage: names.sh <solver.py> <seed>
W=$(mktemp -d /tmp/M5-v/d5/w.XXXX)
cp /tmp/verifyB5-M5-d/course/modules/M/M5/grader/test_project.py /tmp/verifyB5-M5-d/course/modules/M/M5/grader/instance.py $W/
cp "$1" $W/contraction_solver.py
cd $W && QF_SEED=$2 PYTHONHASHSEED=0 /tmp/verifyB5-M5-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error -rf test_project.py 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-400
