#!/bin/bash
# Run each round-4 alternative under the page's flags on seeds 0-49 (copies into scratch dirs; never runs in the repo).
ROOT=/Users/billyribeiro/.fanout/wt/verifyD4-M7-d
G=$ROOT/course/modules/M/M7/grader
PY=$ROOT/.venv/bin/python
S=$ROOT/ledgers/M7/scripts/M7-d-r4
OUT=$S/alts_run
mkdir -p $OUT
for alt in $S/alts/*.py; do
  name=$(basename $alt .py)
  log=$OUT/${name}_0-49.log
  : > $log
  for seed in $(seq 0 49); do
    D=/tmp/m7d-r4-run/$name/$seed
    rm -rf $D; mkdir -p $D
    cp $G/test_project.py $G/instance.py $D/
    cp $alt $D/constrained_allocator.py
    res=$(cd $D && QF_SEED=$seed PYTHONHASHSEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
    echo "seed $seed: $res" >> $log
  done
  echo "$name passing-seeds: $(grep -c ' passed' $log) of 50" >> $log
done
echo DONE >> $OUT/done.txt
