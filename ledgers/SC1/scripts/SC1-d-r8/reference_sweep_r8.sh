#!/bin/bash
# Round 8 (SC1-d): reference suite over seeds 1000-1199 (browser seeds are arbitrary, e.g. 1566136316) and the
# five round-8 alternatives are already swept over 0-49 by alt_sweep.sh.
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyE8-SC1-d
G=$ROOT/course/modules/SC/SC1/grader
PY=$ROOT/.venv/bin/python
W=$(mktemp -d /tmp/sc1d-r8-sweep-XXXX)
cp "$G/test_project.py" "$G/instance.py" "$W"/
cp "$G/reference.py" "$W/bm_checks.py"
pass=0; fail=""
for s in $(seq 1000 1199); do
  out=$(cd "$W" && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  if echo "$out" | grep -qx "132 passed in.*"; then pass=$((pass+1)); else fail="$fail $s"; fi
done
echo "reference seeds 1000-1199: pass $pass/200; failing:${fail:- none}"
rm -rf "$W"
