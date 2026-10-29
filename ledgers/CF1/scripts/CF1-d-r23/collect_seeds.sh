#!/bin/bash
# Collect-only count of the CF1 project suite against the reference engine, for seeds given as arguments.
G=/tmp/verify23-CF1-d/course/modules/CF/CF1/grader
PY=/tmp/verify23-CF1-d/.venv/bin/python
for s in "$@"; do
  W=$(mktemp -d /tmp/CF1-v/d23/collect.XXXX)
  cp $G/test_project.py $G/instance.py $W/ && cp $G/reference.py $W/capbudget.py
  echo -n "seed $s: "
  (cd $W && QF_SEED=$s PYTHONHASHSEED=0 $PY -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1)
  rm -rf $W
done
