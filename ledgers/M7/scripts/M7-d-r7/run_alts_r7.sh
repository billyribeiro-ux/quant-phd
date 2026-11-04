#!/bin/bash
# Run every alternative solver through the M7 suite on seeds 0-49 (pytest summary per seed).
cd /Users/billyribeiro/.fanout/wt/verifyD7-M7-d || exit 1
S=ledgers/M7/scripts/M7-d-r7
OUT=$S/alts_run_0-49.log
: > $OUT
for f in $S/alt/alt[A-E]*.py; do
  for seed in $(seq 0 49); do
    res=$($S/grader_suite.sh $PWD/$f $seed /tmp/m7d-r7/alt_$seed-$(basename $f .py) 2>&1 | tail -1)
    echo "$(basename $f) seed=$seed :: $res" >> $OUT
  done
done
echo DONE >> $OUT
