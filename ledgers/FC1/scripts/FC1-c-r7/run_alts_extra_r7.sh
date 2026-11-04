#!/bin/bash
# Round 7 verifier: the round-4 and round-6 alternatives (alt6-alt9), against the current suite on seeds 0-19.
R=/Users/billyribeiro/.fanout/wt/verifyD7-FC1-c
G=$R/course/modules/FC/FC1/grader
for A in $R/ledgers/FC1/scripts/FC1-c-r4/alt/alt6_r4_pow_fraction_floor.py $R/ledgers/FC1/scripts/FC1-c-r6/alt/alt7_r6_decimal_prec60_half_up.py $R/ledgers/FC1/scripts/FC1-c-r6/alt/alt8_r6_integer_common_denominator.py $R/ledgers/FC1/scripts/FC1-c-r6/alt/alt9_r6_running_discount_factor.py; do
  D=$(mktemp -d /tmp/fc1c_r7_xalt.XXXXXX); cp $G/test_project.py $G/instance.py $D/; cp "$A" $D/instruments.py
  p=0; f=0
  for s in $(seq 0 19); do
    if (cd $D && QF_SEED=$s $R/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then p=$((p+1)); else f=$((f+1)); fi
  done
  echo "$(basename $A): pass=$p fail=$f"
done
