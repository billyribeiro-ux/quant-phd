#!/bin/bash
# Run each candidate solver as solver.py against the E4 suite for seeds 0-49 (scratch copies only).
ROOT=/Users/billyribeiro/.fanout/wt/verifyE7-E4-d
PY=$ROOT/.venv/bin/python
G=$ROOT/course/modules/E/E4/grader
for cand in "$@"; do
  D=$(mktemp -d /tmp/e4r7-alt-XXXXXX)
  cp $G/test_project.py $G/instance.py $G/starter.py $G/reference.py $D/
  cp "$cand" $D/solver.py
  pass=0; fail=0; failed=""
  for s in $(seq 0 49); do
    out=$(cd $D && QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
    if echo "$out" | tail -1 | grep -q " passed" && ! echo "$out" | tail -1 | grep -q failed; then pass=$((pass+1)); else fail=$((fail+1)); failed="$failed $s"; fi
  done
  echo "$(basename $cand): pass_seeds=$pass fail_seeds=$fail failing=[$failed ]"
  rm -rf $D
done
