#!/bin/bash
# usage: run_alts.sh <WORKDIR> <solution.py> <label> <seeds...>; fresh scratch dir per seed; grader copied from WORKDIR
WD=$1; SOL=$2; LABEL=$3; shift 3
G=$WD/course/modules/M/M7/grader
for seed in "$@"; do
  W=/tmp/m7d_r11_${LABEL}_$seed; rm -rf $W; mkdir -p $W
  cp $G/test_project.py $G/instance.py $W/
  cp "$SOL" $W/constrained_allocator.py
  out=$(cd $W && QF_SEED=$seed $WD/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  echo "$LABEL seed $seed: $out"
done
