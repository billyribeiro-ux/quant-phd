#!/bin/bash
# Collect-only count of the M7 suite on seeds 0-49 (pytest --collect-only -q), reference copied to a scratch dir.
CK=/Users/billyribeiro/.fanout/wt/verifyD8-M7-d
SRC=$CK/course/modules/M/M7/grader
OUT=$CK/ledgers/M7/scripts/M7-d-r8/collect_all_seeds.log
: > $OUT
for seed in $(seq 0 49); do
  WD=$(mktemp -d /tmp/m7d-r8-collect-XXXX)
  cp $SRC/instance.py $SRC/test_project.py $WD/
  cp $SRC/reference.py $WD/constrained_allocator.py
  n=$(cd $WD && QF_SEED=$seed $CK/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py 2>&1 | tail -1)
  echo "seed=$seed :: $n" >> $OUT
  rm -rf $WD
done
echo DONE >> $OUT
