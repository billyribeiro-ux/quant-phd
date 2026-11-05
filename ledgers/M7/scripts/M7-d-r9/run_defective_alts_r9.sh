#!/bin/bash
# Round 9: the defective alternatives (round 8) through the round-9 suite on seeds 0-49; count seeds where each passes.
CK=/Users/billyribeiro/.fanout/wt/verifyD9-M7-d
S=$CK/ledgers/M7/scripts/M7-d-r9
R8=$CK/ledgers/M7/scripts/M7-d-r8
OUT=$S/defective_alts_run_0-49.log
: > $OUT
for f in $R8/alt/alt_empty_start.py $R8/alt/alt_float.py $R8/alt/alt_nullspace.py $R8/alt/alt_reverse_order.py $R8/alt/altC_float_tight_1e-12.py $R8/alt/altD_float_empty_last_added_1e-10.py $R8/alt/altE_float_search_exact_polish.py $R8/alt/altG_float_empty_gamma_scaled_1e-10.py $R8/alt/altH_float_empty_last_added_budget_refined.py $R8/altr8/altV3_abs_last_tie.py $R8/altr8/altV5_abs_gamma_scaled.py; do
  clean=0
  for seed in $(seq 0 49); do
    res=$($S/grader_suite_r9.sh $f $seed /tmp/m7d-r9/dalt_$seed-$(basename $f .py) -rf 2>&1)
    line=$(echo "$res" | tail -1)
    fails=$(echo "$res" | grep '^FAILED' | head -2 | cut -c1-160 | tr '\n' ' ')
    echo "$(basename $f) seed=$seed :: $line $fails" >> $OUT
    if echo "$line" | grep -qE "^364 passed in"; then clean=$((clean+1)); fi
  done
  echo "SUMMARY $(basename $f) passing $clean/50" >> $OUT
done
echo DONE >> $OUT
