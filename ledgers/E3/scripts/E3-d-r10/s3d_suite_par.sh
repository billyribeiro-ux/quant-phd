#!/bin/bash
# Round-10 E3-d: run one candidate elicit.py through the page suite for seeds 0-9, one process per seed (in parallel).
# usage: s3d_suite_par.sh <label> <path/to/elicit.py>
# NOTE: the seed is passed inside `env -i` (the earlier runners dropped QF_SEED there and ran every seed as seed 0).
ROOT=/Users/billyribeiro/.fanout/wt/verifyD10-E3-d
G=$ROOT/course/modules/E/E3/grader
P=$ROOT/.venv/bin/python
LABEL=$1
SRC=$2
OUT=$ROOT/ledgers/E3/scripts/E3-d-r10/suite_out/$LABEL.out
mkdir -p $ROOT/ledgers/E3/scripts/E3-d-r10/suite_out
: > $OUT.tmp
run_seed() {
  seed=$1
  W=$(mktemp -d /tmp/E3d_r10_suite_XXXX)
  cp $G/test_project.py $G/instance.py $W/
  cp "$SRC" $W/elicit.py
  (cd $W && env -i PATH=/usr/bin:/bin QF_SEED=$seed PYTHONHASHSEED=0 $P -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > $W/out.txt 2>&1)
  rc=$?
  echo "$LABEL seed=$seed rc=$rc :: $(tail -1 $W/out.txt) :: $(grep -o 'FAILED test_project.py::[^ ]*' $W/out.txt | sed 's/FAILED test_project.py:://' | tr '\n' ' ')" >> $OUT.tmp.$seed
  rm -rf $W
}
for seed in 0 1 2 3 4 5 6 7 8 9; do run_seed $seed & done
wait
cat $OUT.tmp.* 2>/dev/null | sort -t= -k2 -n > $OUT
rm -f $OUT.tmp $OUT.tmp.*
echo "DONE" >> $OUT
