#!/bin/bash
# usage: run_mutant.sh <mutant file> <seed-from> <seed-to>; prints first failing seed and test, or PASSALL
M=$1; A=$2; B=$3
G=/Users/billyribeiro/.fanout/wt/verifyB6-M5-d/course/modules/M/M5/grader
PY=/Users/billyribeiro/.fanout/wt/verifyB6-M5-d/.venv/bin/python
W=$(mktemp -d /tmp/m5d_r6_XXXXXX)
cp "$G/test_project.py" "$G/instance.py" "$W/"
cp "$M" "$W/contraction_solver.py"
for s in $(seq $A $B); do
  out=$(cd "$W" && QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  if [ $? -ne 0 ]; then
    echo "KILLED seed=$s: $(echo "$out" | grep -o 'FAILED [^ ]*' | head -1)"; rm -rf "$W"; exit 0
  fi
done
echo "PASSALL seeds $A-$B"; rm -rf "$W"
