#!/bin/bash
# Round 9: collect-only count of the M7 suite on seeds 0-49, reference copied to a scratch dir.
CK=/Users/billyribeiro/.fanout/wt/verifyD9-M7-d
SRC=$CK/course/modules/M/M7/grader
OUT=$CK/ledgers/M7/scripts/M7-d-r9/collect_all_seeds_r9.log
: > $OUT
for seed in $(seq 0 49); do
  WD=$(mktemp -d /tmp/m7d-r9-collect-XXXX)
  cp $SRC/instance.py $SRC/test_project.py $WD/
  cp $SRC/reference.py $WD/constrained_allocator.py
  n=$(cd $WD && QF_SEED=$seed $CK/.venv/bin/python -I -m pytest -p no:cacheprovider --assert=plain -W error --collect-only test_project.py 2>&1 | grep -E "tests? collected" | tail -1)
  echo "seed=$seed :: $n" >> $OUT
  rm -rf $WD
done
echo DONE >> $OUT
