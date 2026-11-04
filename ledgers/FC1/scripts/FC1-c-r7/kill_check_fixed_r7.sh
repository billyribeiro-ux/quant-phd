#!/bin/bash
# Round 7 verifier: run every grader mutant and every alternative against a candidate test_project.py (seeds 0-19).
# Usage: kill_check_fixed_r7.sh <dir containing candidate test_project.py and instance.py>
R=/Users/billyribeiro/.fanout/wt/verifyD7-FC1-c
CAND=$1
W=$(mktemp -d /tmp/fc1c_r7_kill.XXXXXX)
cp $CAND/test_project.py $CAND/instance.py $W/
killed=0; survived=0
for M in $R/ledgers/FC1/mutants/*.py; do
  cp "$M" $W/instruments.py
  k=0
  for s in $(seq 0 19); do
    if ! (cd $W && QF_SEED=$s $R/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then k=1; break; fi
  done
  if [ $k = 1 ]; then killed=$((killed+1)); else survived=$((survived+1)); echo "SURVIVED $(basename $M)"; fi
done
echo "mutants killed=$killed survived=$survived"
for A in $R/ledgers/FC1/alternatives/*.py $R/ledgers/FC1/scripts/FC1-c-r7/alt/*.py; do
  cp "$A" $W/instruments.py; p=0; f=0
  for s in $(seq 0 19); do
    if (cd $W && QF_SEED=$s $R/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then p=$((p+1)); else f=$((f+1)); fi
  done
  echo "alt $(basename $A): pass=$p fail=$f"
done
rm -rf $W
