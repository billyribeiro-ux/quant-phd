#!/bin/bash
# usage: runalts.sh <engine.py> <label>  -- runs grader seeds 0-49 against that engine
PY=/tmp/verify7-M1-d/.venv/bin/python
G=/tmp/verify7-M1-d/course/modules/M/M1/grader
W=$(mktemp -d /tmp/m1-v7/d/work.XXXX)
cp $G/*.py $W/ && cp "$1" $W/annuity_engine.py
pass=0; fail=0; failed=""
for s in $(seq 0 49); do
  if QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error -c /dev/null --rootdir=$W $W/test_project.py >/tmp/m1-v7/d/last.out 2>&1; then pass=$((pass+1)); else fail=$((fail+1)); failed="$failed $s"; fi
done
echo "$2: seeds pass=$pass fail=$fail failed_seeds=[$failed]"
rm -rf $W
