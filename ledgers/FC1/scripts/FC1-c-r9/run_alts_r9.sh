#!/bin/bash
# Round 9 verifier (FC1-c): run every alternative correct implementation against the FC1 grader suite, seeds 0-19.
R=/Users/billyribeiro/.fanout/wt/verifyD9-FC1-c
G=$R/course/modules/FC/FC1/grader
ALTS="$R/ledgers/FC1/alternatives/a1_list_comprehension_events.py $R/ledgers/FC1/alternatives/a2_generator_methods.py $R/ledgers/FC1/alternatives/a3_fraction_throughout.py $R/ledgers/FC1/alternatives/a4_integer_division_half_up.py $R/ledgers/FC1/alternatives/a5_frozen_dataclass_reduce.py $R/ledgers/FC1/scripts/FC1-c-r4/alt/alt6_r4_pow_fraction_floor.py $R/ledgers/FC1/scripts/FC1-c-r6/alt/alt7_r6_decimal_prec60_half_up.py $R/ledgers/FC1/scripts/FC1-c-r6/alt/alt8_r6_integer_common_denominator.py $R/ledgers/FC1/scripts/FC1-c-r6/alt/alt9_r6_running_discount_factor.py $R/ledgers/FC1/scripts/FC1-c-r7/alt/alt10_r7_pow_of_reciprocal_ratio.py $R/ledgers/FC1/scripts/FC1-c-r7/alt/alt11_r7_decimal_prec200_half_up.py $R/ledgers/FC1/scripts/FC1-c-r7/alt/alt12_r7_running_division_floor_half.py $R/ledgers/FC1/scripts/FC1-c-r8/alt/alt13_r8_floor_half_fraction.py $R/ledgers/FC1/scripts/FC1-c-r8/alt/alt14_r8_common_scale_integers.py $R/ledgers/FC1/scripts/FC1-c-r8/alt/alt15_r8_decimal_prec60_quantize.py"
for A in $ALTS; do
  D=$(mktemp -d /tmp/fc1c_r9_alt.XXXXXX)
  cp $G/test_project.py $G/instance.py $D/
  cp "$A" $D/instruments.py
  pass=0; fail=0; failed=""
  for s in $(seq 0 19); do
    if (cd $D && QF_SEED=$s $R/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >$D/log_$s.txt 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); failed="$failed $s"; fi
  done
  echo "$(basename $A): pass=$pass fail=$fail failed_seeds=[$failed ]"
  rm -rf "$D"
done
