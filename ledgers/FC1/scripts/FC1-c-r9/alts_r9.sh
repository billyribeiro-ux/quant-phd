#!/bin/bash
ROOT=/Users/billyribeiro/.fanout/wt/verifyC9-FC1-c
PY=$ROOT/.venv/bin/python
for alt in $ROOT/ledgers/FC1/alternatives/*.py; do
  name=$(basename $alt .py)
  d=/tmp/fc1c9_alts/$name; rm -rf $d; mkdir -p $d
  cp $ROOT/course/modules/FC/FC1/grader/test_project.py $ROOT/course/modules/FC/FC1/grader/instance.py $d/
  cp $alt $d/instruments.py
  fails=0
  for s in $(seq 0 49); do
    out=$(cd $d && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
    case "$out" in *failed*|*error*) fails=$((fails+1));; esac
  done
  echo "$name seeds=50 failing_seeds=$fails"
done
