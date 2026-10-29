#!/bin/bash
# Round-10 verifier: run each alternative correct engine on the M2 grader, seeds 0-49, with -W error.
P=/Users/billyribeiro/.fanout/wt/verifyB10-M2-e/.venv/bin/python
G=/Users/billyribeiro/.fanout/wt/verifyB10-M2-e/course/modules/M/M2/grader
ALTS=/Users/billyribeiro/.fanout/wt/verifyB10-M2-e/ledgers/M2/scripts/M2-e-r10/alts
for a in altA altB altC; do
  W=/tmp/m2e_r10/$a; rm -rf $W; mkdir -p $W
  cp $G/test_project.py $G/instance.py $W/; cp $ALTS/$a.py $W/sensitivity_engine.py
  pass=0; fail=0
  for s in $(seq 0 49); do
    if (cd $W && QF_SEED=$s $P -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); echo "  $a seed $s FAIL"; fi
  done
  echo "$a.py: $pass/50 seeds pass (fail=$fail)"
done
