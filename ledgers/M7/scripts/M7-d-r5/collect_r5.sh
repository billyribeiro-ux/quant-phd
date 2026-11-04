#!/bin/bash
# Collect-only count of the suite for each seed 0-49, with the reference as the learner module (copied to scratch).
for seed in $(seq 0 49); do
  D=/tmp/m7d-r5-c$seed; rm -rf $D; mkdir -p $D
  cp /Users/billyribeiro/.fanout/wt/verifyD5-M7-d/course/modules/M/M7/grader/test_project.py /Users/billyribeiro/.fanout/wt/verifyD5-M7-d/course/modules/M/M7/grader/instance.py $D/
  cp /Users/billyribeiro/.fanout/wt/verifyD5-M7-d/course/modules/M/M7/grader/reference.py $D/constrained_allocator.py
  n=$(cd $D && QF_SEED=$seed /Users/billyribeiro/.fanout/wt/verifyD5-M7-d/.venv/bin/python -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1)
  echo "seed $seed: $n"
done
