#!/bin/bash
# Round 16: alternatives and equivalent variants against the E4 suite, seeds 0-49, plus collect-only on the reference.
R=/Users/billyribeiro/.fanout/wt/verifyE16-E4-d
cd $R || exit 1
D=ledgers/E4/scripts/E4-d-r16
O=$D/out/cand
PY=$R/.venv/bin/python
$PY -I $D/run_candidate_r16.py course/modules/E/E4/grader/reference.py 0-49 --collect > $O/collect_reference.txt 2>&1
$PY -I $D/run_candidate_r16.py course/modules/E/E4/grader/reference.py 0-49 > $O/reference_0_49.txt 2>&1
for f in ledgers/E4/alternatives/alt_*.py; do n=$(basename $f .py); $PY -I $D/run_candidate_r16.py $f 0-49 > $O/$n.txt 2>&1; done
for f in ledgers/E4/equivalent/*.py; do n=equiv_$(basename $f .py); $PY -I $D/run_candidate_r16.py $f 0-49 > $O/$n.txt 2>&1; done
echo CANDDONE > $O/done.txt
