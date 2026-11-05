#!/bin/bash
# Round-10 E3-d: the round-9 within-tolerance candidate (not a mutant) through the current suite, seeds 0-9.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD10-E3-d
G=$ROOT/course/modules/E/E3/grader
P=$ROOT/.venv/bin/python
OUT=$ROOT/ledgers/E3/scripts/E3-d-r10/s3d_candidate_r9_04_0_9.out
: > $OUT
for seed in 0 1 2 3 4 5 6 7 8 9; do
  W=$(mktemp -d /tmp/E3d_r10_cand_XXXX)
  cp $G/test_project.py $G/instance.py $W/
  cp $ROOT/ledgers/E3/scripts/E3-d-r9/within_tolerance/r9_04_convergence_test_ignores_lambda.py $W/elicit.py
  (cd $W && QF_SEED=$seed env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 $P -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > $W/out.txt 2>&1)
  rc=$?
  echo "seed=$seed rc=$rc :: $(tail -1 $W/out.txt) :: $(grep -o 'FAILED test_project.py::[^ ]*' $W/out.txt | head -2 | tr '\n' ' ')" >> $OUT
  rm -rf $W
done
echo DONE >> $OUT
