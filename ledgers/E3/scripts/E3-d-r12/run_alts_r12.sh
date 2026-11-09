#!/bin/bash
# Run every alternative correct implementation (r10 and r11 alts) against the round-12 suite, seeds given in $SEEDS.
# usage: run_alts_r12.sh <checkout> <outdir>
CK="$1"; OUT="$2"; mkdir -p "$OUT"
G="$CK/course/modules/E/E3/grader"
SEEDS="${SEEDS:-0 1 2 3 4 5 6 7 8 9}"
S=/Users/billyribeiro/.fanout/wt/verifyD12-E3-d/ledgers/E3/scripts
for f in $S/E3-d-r10/alts/*/elicit.py $S/E3-d-r11/alts/*/elicit.py; do
  name=$(basename $(dirname $f))
  for seed in $SEEDS; do
    res=$(TAILN=400 /Users/billyribeiro/.fanout/scratch/E3-d-r12/run_suite.sh "$f" "$seed" "$G" 2>&1)
    code=$(echo "$res" | grep '^EXIT=' | cut -d= -f2)
    summ=$(echo "$res" | grep -E 'passed|failed' | tail -1)
    fails=$(echo "$res" | grep -E '^FAILED' | sed 's/ - .*//' | tr '\n' ' ')
    echo "$name seed=$seed EXIT=$code | $summ | $fails" >> "$OUT/alts_summary.txt"
  done
done
echo DONE >> "$OUT/alts_summary.txt"
