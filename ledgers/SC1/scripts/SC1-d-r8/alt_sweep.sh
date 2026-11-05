#!/bin/bash
# Round 8 (SC1-d): run the grader suite on each round-8 alternative for seeds 0-49 (scratch copy per alternative).
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyE8-SC1-d
O=$ROOT/ledgers/SC1/scripts/SC1-d-r8/out
G=$ROOT/course/modules/SC/SC1/grader
PY=$ROOT/.venv/bin/python
for alt in "$ROOT"/ledgers/SC1/scripts/SC1-d-r8/alternatives/*.py; do
  name=$(basename "$alt" .py)
  W=$(mktemp -d /tmp/sc1d-r8-alt-XXXX)
  cp "$G/test_project.py" "$G/instance.py" "$W"/
  cp "$alt" "$W/bm_checks.py"
  pass=0; fail=""
  for s in $(seq 0 49); do
    out=$(cd "$W" && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
    if echo "$out" | grep -qx "132 passed in.*"; then pass=$((pass+1)); else fail="$fail $s"; fi
  done
  echo "$name: pass $pass/50 seeds; failing seeds:${fail:- none}"
  rm -rf "$W"
done
