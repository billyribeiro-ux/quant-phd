#!/bin/bash
V=/Users/billyribeiro/.fanout/wt/verifyB7-M4-d/.venv/bin/python
S=/tmp/M4-d-r7-scratch
for m in "$@"; do
  n=$(basename $m .py); d=$S/m_$n; rm -rf $d; mkdir -p $d
  cp /Users/billyribeiro/.fanout/wt/verifyB7-M4-d/course/modules/M/M4/grader/*.py $d/
  cp $m $d/tail_risk.py; cd $d; killed=""
  for s in $(seq 0 9); do
    if ! QF_SEED=$s $V -I -W error -m pytest -p no:cacheprovider -q test_project.py > out.txt 2>&1; then
      killed="$(grep -o 'FAILED test_project.py::[^ ]*' out.txt | head -1) (seed $s)"; break; fi
  done
  echo "$n: ${killed:-SURVIVED}"
done
