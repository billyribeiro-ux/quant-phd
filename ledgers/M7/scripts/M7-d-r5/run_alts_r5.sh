#!/bin/bash
# Run one alternative (arg 1) on seeds 0-49 under the page's flags, in scratch dirs only.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD5-M7-d
G=$ROOT/course/modules/M/M7/grader
PY=$ROOT/.venv/bin/python
S=$ROOT/ledgers/M7/scripts/M7-d-r5
alt=$1
name=$(basename $alt .py)
log=$S/alts_run/${name}_0-49.log
: > $log
for seed in $(seq 0 49); do
  D=/tmp/m7d-r5-run/$name/$seed
  rm -rf $D; mkdir -p $D
  cp $G/test_project.py $G/instance.py $D/
  cp $alt $D/constrained_allocator.py
  res=$(cd $D && QF_SEED=$seed PYTHONHASHSEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  echo "seed $seed: $res" >> $log
done
echo "$name passing-seeds: $(grep -c ' passed' $log | head -1) lines; full-pass: $(grep -c 'seed [0-9]*: 363 passed' $log) of 50" >> $log
