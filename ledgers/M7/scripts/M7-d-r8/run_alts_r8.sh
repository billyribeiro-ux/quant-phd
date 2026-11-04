#!/bin/bash
# Run every alternative solver in alt/ through the M7 suite on seeds 0-49; one pytest summary line per (alt, seed).
CK=/Users/billyribeiro/.fanout/wt/verifyD8-M7-d
S=$CK/ledgers/M7/scripts/M7-d-r8
OUT=$S/alts_run_0-49.log
: > $OUT
for f in $S/alt/alt*.py; do
  for seed in $(seq 0 49); do
    res=$($S/grader_suite_r8.sh $f $seed /tmp/m7d-r8/alt_$seed-$(basename $f .py) 2>&1 | tail -1)
    echo "$(basename $f) seed=$seed :: $res" >> $OUT
  done
done
echo DONE >> $OUT
