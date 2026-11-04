#!/bin/bash
# Round 5 verifier: run each alternative correct implementation against the FC1 grader on seeds 0-19.
R=/Users/billyribeiro/.fanout/wt/verifyD5-FC1-c
G=$R/course/modules/FC/FC1/grader
ALTS="$R/ledgers/FC1/alternatives/a1_list_comprehension_events.py $R/ledgers/FC1/alternatives/a2_generator_methods.py $R/ledgers/FC1/alternatives/a3_fraction_throughout.py $R/ledgers/FC1/alternatives/a4_integer_division_half_up.py $R/ledgers/FC1/alternatives/a5_frozen_dataclass_reduce.py $R/ledgers/FC1/scripts/FC1-c-r4/alt/alt6_r4_pow_fraction_floor.py"
for A in $ALTS; do
  D=$(mktemp -d /tmp/fc1c_r5_alt.XXXXXX)
  cp $G/test_project.py $G/instance.py $D/
  cp "$A" $D/instruments.py
  pass=0; fail=0; failed=""
  for s in $(seq 0 19); do
    if (cd $D && QF_SEED=$s $R/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >$D/log_$s.txt 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); failed="$failed $s"; fi
  done
  echo "$(basename $A): pass=$pass fail=$fail failed_seeds=[$failed ]"
done
