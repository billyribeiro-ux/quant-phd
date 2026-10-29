#!/bin/bash
# usage: run_alts.sh <solution.py> <label> <seeds...>; copies grader + solution into a fresh scratch dir per seed
SOL=$1; LABEL=$2; shift 2
ROOT=/Users/billyribeiro/.fanout/wt/verifyB8-M7-d
G=$ROOT/course/modules/M/M7/grader
for seed in "$@"; do
  W=/tmp/m7d_r8_alt_${LABEL}_$seed; rm -rf $W; mkdir -p $W
  cp $G/test_project.py $G/instance.py $W/
  cp "$SOL" $W/constrained_allocator.py
  out=$(cd $W && QF_SEED=$seed $ROOT/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  fails=$(cd $W && QF_SEED=$seed $ROOT/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | grep -E '^FAILED' | sed 's/ - .*//' | head -8)
  echo "$LABEL seed $seed: $out"
  [ -n "$fails" ] && echo "$fails"
done
