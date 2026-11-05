#!/bin/bash
# Round-10 E3-d: run one alternative elicit.py through the page suite for seeds 0-9 (arg: alt directory name).
ROOT=/Users/billyribeiro/.fanout/wt/verifyD10-E3-d
G=$ROOT/course/modules/E/E3/grader
P=$ROOT/.venv/bin/python
name=$1
alt=$ROOT/ledgers/E3/scripts/E3-d-r10/alts/$name/
OUT=$ROOT/ledgers/E3/scripts/E3-d-r10/alts_out/$name.out
mkdir -p $ROOT/ledgers/E3/scripts/E3-d-r10/alts_out
: > $OUT
for seed in 0 1 2 3 4 5 6 7 8 9; do
  W=$(mktemp -d /tmp/E3d_r10_alt_XXXX)
  cp $G/test_project.py $G/instance.py $W/
  cp ${alt}elicit.py $W/elicit.py
  (cd $W && QF_SEED=$seed env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 $P -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > $W/out.txt 2>&1; rc=$?;
   summary=$(tail -1 $W/out.txt); fails=$(grep -o "FAILED test_project.py::[^ ]*" $W/out.txt | sed 's/FAILED test_project.py:://' | tr '\n' ' ');
   echo "$name seed=$seed rc=$rc :: $summary :: $fails" >> $OUT)
  rm -rf $W
done
echo DONE >> $OUT
