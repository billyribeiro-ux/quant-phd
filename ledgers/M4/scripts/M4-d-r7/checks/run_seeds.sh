#!/bin/bash
# usage: run_seeds.sh <variant>  -> prints PASS/FAIL per seed 0..49 for the chi-square lag test
V=$1
G=/Users/billyribeiro/.fanout/wt/verifyD7-M4-d/course/modules/M/M4/grader
W=/tmp/M4-d-r7-chk/work-$V
rm -rf $W; mkdir -p $W; cp $G/test_project.py $G/instance.py $W/; cp /tmp/M4-d-r7-chk/$V.py $W/tail_risk.py
cd $W
fails=0
for s in $(seq 0 49); do
  if QF_SEED=$s PYTHONHASHSEED=0 /Users/billyribeiro/.fanout/wt/verifyD7-M4-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py -k test_student_t_draws_do_not_share_chi_square >/dev/null 2>&1; then :; else fails=$((fails+1)); fi
done
echo "$V failing_seeds=$fails of 50"
