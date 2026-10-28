#!/bin/bash
# usage: run_engine.sh <engine.py> <label> -- grader seeds 0-49 for that engine, pytest flags as tools/run_graders.py (PYTEST_FLAGS, QF_SEED, PYTHONHASHSEED=0)
PY=/tmp/verify11-M1-d/.venv/bin/python
G=/tmp/verify11-M1-d/course/modules/M/M1/grader
mkdir -p /tmp/m1-v11/d
W=$(mktemp -d /tmp/m1-v11/d/work.XXXX)
cp $G/test_project.py $G/instance.py $W/ && cp "$1" $W/annuity_engine.py
pass=0; fail=0; failed=""
for s in $(seq 0 ${SEEDS_TO:-49}); do
  if (cd $W && env -i PATH=/usr/bin:/bin QF_SEED=$s PYTHONHASHSEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error $W/test_project.py >/tmp/m1-v11/d/last.out 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); failed="$failed $s"; fi
done
echo "$2: seeds pass=$pass fail=$fail failed_seeds=[$failed]"
rm -rf $W
