#!/bin/bash
# Run the five round-8 float variants (altr8/) through the M7 suite on seeds 0-49.
CK=/Users/billyribeiro/.fanout/wt/verifyD8-M7-d
S=$CK/ledgers/M7/scripts/M7-d-r8
OUT=$S/altr8_run_0-49.log
: > $OUT
for f in $S/altr8/altV*.py; do
  for seed in $(seq 0 49); do
    res=$($S/grader_suite_r8.sh $f $seed /tmp/m7d-r8/v_$seed-$(basename $f .py) -q 2>&1 | tail -1)
    echo "$(basename $f) seed=$seed :: $res" >> $OUT
    if [[ "$res" != *" passed"* || "$res" == *failed* ]]; then
      $S/grader_suite_r8.sh $f $seed /tmp/m7d-r8/vf_$seed-$(basename $f .py) -rf 2>&1 | grep "^FAILED" | sed "s/^/$(basename $f) seed=$seed /" >> $S/altr8_failing_r8.log
    fi
  done
done
echo DONE >> $OUT
