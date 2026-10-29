#!/bin/bash
# Round-6 E1-d: collect count, alternative correct implementations over seeds 0-49, and the float-kill probe.
R=/Users/billyribeiro/.fanout/wt/verifyB6-E1-d
S=$R/ledgers/E1/scripts/E1-d-r6
cd /tmp
W=$(mktemp -d /tmp/e1d-col-XXXX)
cp $R/course/modules/E/E1/grader/{instance.py,test_project.py} $W/
cp $R/course/modules/E/E1/grader/reference.py $W/market_structure.py
(cd $W && $R/.venv/bin/python -m pytest --collect-only -q -p no:cacheprovider test_project.py | tail -1)
rm -rf $W
for f in alt1_integer_pairs alt2_decimal_half_up alt3_cramer alt4_trapezoid_consumer; do
  fails=0; for s in $(seq 0 49); do $S/run_candidate.sh $S/$f.py $s > /dev/null 2>&1 || fails=$((fails+1)); done
  echo "$f: failing seeds of 50 = $fails"
done
$S/run_candidate.sh $S/alt1_integer_pairs.py 0 | grep FAILED
