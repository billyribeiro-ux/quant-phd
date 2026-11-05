#!/bin/bash
# Round-10 E3-d: run the three new verifier mutants (d10_*) through the suite, seeds 0-9, stop at first failure.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD10-E3-d
G=$ROOT/course/modules/E/E3/grader
P=$ROOT/.venv/bin/python
OUT=$ROOT/ledgers/E3/scripts/E3-d-r10/s3d_new_mutants_0_9.out
: > $OUT
for m in $ROOT/ledgers/E3/mutants/d10_*.py; do
  name=$(basename $m)
  killed=""
  for seed in 0 1 2 3 4 5 6 7 8 9; do
    W=$(mktemp -d /tmp/E3d_r10_mut_XXXX)
    cp $G/test_project.py $G/instance.py $W/
    cp $m $W/elicit.py
    (cd $W && QF_SEED=$seed env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 $P -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > $W/out.txt 2>&1)
    rc=$?
    if [ $rc -ne 0 ]; then
      killed=$(grep -o "FAILED test_project.py::[^ ]*" $W/out.txt | head -1 | sed 's/FAILED test_project.py:://')
      echo "KILLED $name seed=$seed by $killed" >> $OUT
      rm -rf $W; break
    fi
    rm -rf $W
  done
  if [ -z "$killed" ]; then echo "SURVIVED $name (seeds 0-9)" >> $OUT; fi
done
echo DONE >> $OUT
