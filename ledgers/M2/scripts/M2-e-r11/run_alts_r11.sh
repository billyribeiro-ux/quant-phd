#!/bin/bash
# Round-11 verifier: run each alternative correct engine on the M2 grader (r11 checkout), seeds 0-49, -W error.
R=/Users/billyribeiro/.fanout/wt/verifyB11-M2-e
P=$R/.venv/bin/python
G=$R/course/modules/M/M2/grader
ALTS=$R/ledgers/M2/scripts/M2-e-r11/alts
for a in altA altB altC altD; do
  W=/tmp/m2e_r11/$a; rm -rf $W; mkdir -p $W
  cp $G/test_project.py $G/instance.py $W/; cp $ALTS/$a.py $W/sensitivity_engine.py
  pass=0; fail=0
  for s in $(seq 0 49); do
    if (cd $W && QF_SEED=$s $P -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); echo "  $a seed $s FAIL"; fi
  done
  echo "$a.py: $pass/50 seeds pass (fail=$fail)"
done
