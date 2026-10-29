#!/bin/bash
# usage: run_alts_r10.sh <solution.py> <label> <seeds...>; fresh scratch dir per seed, grader copied from this checkout
SOL=$1; LABEL=$2; shift 2
ROOT=/Users/billyribeiro/.fanout/wt/verifyB10-M7-d
G=$ROOT/course/modules/M/M7/grader
for seed in "$@"; do
  W=/tmp/m7d_r10_${LABEL}_$seed; rm -rf $W; mkdir -p $W
  cp $G/test_project.py $G/instance.py $W/
  cp "$SOL" $W/constrained_allocator.py
  out=$(cd $W && QF_SEED=$seed $ROOT/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  echo "$LABEL seed $seed: $out"
done
