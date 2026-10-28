#!/bin/bash
# usage: run_one.sh <engine.py> <label> <seeds_to>; runs the grader suite (run_graders flags) on seeds 0..seeds_to
PY=/tmp/verify12-M1-d/.venv/bin/python
G=/tmp/verify12-M1-d/course/modules/M/M1/grader
W=$(mktemp -d /tmp/m1-v12/d/work.XXXX)
cp $G/test_project.py $G/instance.py $W/ && cp "$1" $W/annuity_engine.py
pass=0; fail=0; failed=""
for s in $(seq 0 ${3:-9}); do
  if (cd $W && env -i PATH=/usr/bin:/bin QF_SEED=$s PYTHONHASHSEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >$W/last_$s.out 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); failed="$failed $s"; fi
done
echo "$2: seeds pass=$pass fail=$fail failed_seeds=[$failed]"
last=$(grep -h "FAILED\|passed\|failed" $W/last_*.out | sort | uniq -c | sort -rn | head -3)
echo "$last"
rm -rf $W
