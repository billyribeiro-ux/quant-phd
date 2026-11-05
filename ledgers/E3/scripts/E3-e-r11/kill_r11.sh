#!/bin/bash
# Kill check for the three round-11 mutants: seeds 0-9, stop at the first failing seed.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD11-E3-e
OUT=$ROOT/ledgers/E3/scripts/E3-e-r11/out/kill_r11.txt
: > $OUT
for m in r11_01_prospect_root_of_a_negative_value_raises_value_error r11_02_crra_certainty_equivalent_reported_as_final_wealth r11_03_gamma_hat_clamped_below_one_minus_1e3; do
  W=/tmp/e3e_r11/mut_$m
  cp $ROOT/ledgers/E3/mutants/$m.py $W/elicit.py
  killed="SURVIVED 0-9"
  for s in 0 1 2 3 4 5 6 7 8 9; do
    if ! (cd $W && QF_SEED=$s $ROOT/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > $W/seed$s.txt 2>&1); then
      killed="KILLED seed $s: $(grep '^FAILED' $W/seed$s.txt | head -1 | cut -c1-160)"; break
    fi
  done
  echo "$m: $killed" >> $OUT
done
echo DONE >> $OUT
