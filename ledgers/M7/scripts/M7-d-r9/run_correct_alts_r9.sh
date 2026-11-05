#!/bin/bash
# Round 9: the five correct alternatives (exact altA, altB; float relative-cutoff altV1, altV2, altV4 from round 8) on seeds 0-49.
CK=/Users/billyribeiro/.fanout/wt/verifyD9-M7-d
S=$CK/ledgers/M7/scripts/M7-d-r9
R8=$CK/ledgers/M7/scripts/M7-d-r8
OUT=$S/correct_alts_run_0-49.log
: > $OUT
for f in $R8/alt/altA_exact_tight_last_tie.py $R8/alt/altB_exact_empty_most_negative.py $R8/altr8/altV1_rel_plain.py $R8/altr8/altV2_rel_gamma_scaled.py $R8/altr8/altV4_rel_gamma_scaled_mostneg.py; do
  clean=0
  for seed in $(seq 0 49); do
    res=$($S/grader_suite_r9.sh $f $seed /tmp/m7d-r9/alt_$seed-$(basename $f .py) 2>&1 | grep -E " passed| failed|error" | tail -1)
    echo "$(basename $f) seed=$seed :: $res" >> $OUT
    if [[ "$res" == *" passed"* && "$res" != *failed* && "$res" != *error* ]]; then clean=$((clean+1)); fi
  done
  echo "SUMMARY $(basename $f) clean $clean/50" >> $OUT
done
echo DONE >> $OUT
