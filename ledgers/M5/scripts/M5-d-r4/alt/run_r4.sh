#!/bin/bash
# usage: run_r4.sh <solver-module-name>  (file <name>.py in this directory); runs test_project.py on seeds 0-49
PY=/tmp/verifyB4-M5-d/.venv/bin/python
SRC=/tmp/verifyB4-M5-d/course/modules/M/M5/grader
HERE=/tmp/verifyB4-M5-d/ledgers/M5/scripts/M5-d-r4/alt
W=/tmp/M5-v/d4/alt/w_$1; rm -rf $W; mkdir -p $W && cp $SRC/instance.py $SRC/test_project.py $HERE/reference_r3.py $W/ && cp $HERE/$1.py $W/contraction_solver.py && cd $W
fail=0
for s in $(seq 0 49); do
  out=$(QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  case "$out" in *failed*|*error*) fail=$((fail+1)); echo "seed $s: $out";; esac
done
echo "$1 failing seeds: $fail / 50"
