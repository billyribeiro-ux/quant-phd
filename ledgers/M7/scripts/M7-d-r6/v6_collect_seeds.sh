#!/bin/bash
# Round 6 (M7-d): collect-only count of test_project.py per seed 0-49, with the reference as the learner module.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD6-M7-d
G=$ROOT/course/modules/M/M7/grader
PY=$ROOT/.venv/bin/python
for seed in $(seq 0 49); do
  D=/tmp/m7d-r6-c$seed; rm -rf $D; mkdir -p $D
  cp $G/test_project.py $G/instance.py $D/
  cp $G/reference.py $D/constrained_allocator.py
  n=$(cd $D && QF_SEED=$seed PYTHONDONTWRITEBYTECODE=1 $PY -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1)
  echo "seed $seed: $n"
done
