#!/bin/bash
# usage: run_seeds.sh <engine.py> <label>  -- seeds 0-49 against the repo's current M1 grader, browser pytest flags
PY=/Users/billyribeiro/dev/quant-phd/.venv/bin/python
G=/Users/billyribeiro/dev/quant-phd/course/modules/M/M1/grader
W=$(mktemp -d /tmp/m1-fix-r10/seeds.XXXX)
cp $G/instance.py $G/test_project.py $W/ && cp "$1" $W/annuity_engine.py
pass=0; fail=0; failed=""
for s in $(seq 0 49); do
  if (cd $W && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error -c /dev/null --rootdir=$W $W/test_project.py >$W/last.out 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); failed="$failed $s"; fi
done
echo "$2: seeds pass=$pass fail=$fail failed_seeds=[$failed]"
rm -rf $W
