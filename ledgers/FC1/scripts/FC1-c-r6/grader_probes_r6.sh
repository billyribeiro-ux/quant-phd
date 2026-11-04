#!/bin/bash
# Round 6 verifier probes for FC1-c, run from the checkout root. Writes outputs to ledgers/FC1/scripts/FC1-c-r6/out/.
set -u
R=$(pwd)
PY=$R/.venv/bin/python
G=$R/course/modules/FC/FC1/grader
S=$R/ledgers/FC1/scripts/FC1-c-r6
O=$S/out
W=$(mktemp -d /tmp/fc1c_r6_probe.XXXXXX)
run_seed() { # dir seed
  (cd "$1" && QF_SEED=$2 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >"$1/log_$2.txt" 2>&1)
}
# 1. starter file: the suite must fail and name the property
mkdir -p $W/starter && cp $G/test_project.py $G/instance.py $G/starter.py $W/starter/ && cp $G/starter.py $W/starter/instruments.py
(cd $W/starter && QF_SEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error -rA test_project.py > $O/starter_probe_r6.out 2>&1); tail -1 $O/starter_probe_r6.out
# 2. leak check: failing outputs under the documented flags must not print expected values
mkdir -p $W/leak && cp $G/test_project.py $G/instance.py $W/leak/ && cp $S/../../mutants/r6c_coupon_cumulative_rounding.py $W/leak/instruments.py 2>/dev/null || cp $R/ledgers/FC1/mutants/r6c_coupon_cumulative_rounding.py $W/leak/instruments.py
(cd $W/leak && QF_SEED=3 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > $O/leak_probe_r6.out 2>&1); tail -1 $O/leak_probe_r6.out
# 3. the proposed grader fix (scripts/proposed_grader_fix_r6.py) on every mutant, seeds 0-19
mkdir -p $W/fix && cp $S/proposed_grader_fix_r6.py $W/fix/test_project.py && cp $G/instance.py $W/fix/
: > $O/proposed_fix_mutants_r6.out
for f in $R/ledgers/FC1/mutants/*.py; do
  cp "$f" $W/fix/instruments.py; killed=0
  for s in $(seq 0 19); do run_seed $W/fix $s || { killed=1; break; }; done
  echo "$(basename $f) killed_with_proposed_fix=$killed" >> $O/proposed_fix_mutants_r6.out
done
# 4. the proposed fix on the reference (seeds 0-49) and on the nine correct alternatives (seeds 0-19)
mkdir -p $W/ref && cp $G/reference.py $W/ref/instruments.py && cp $S/proposed_grader_fix_r6.py $W/ref/test_project.py && cp $G/instance.py $W/ref/
fails=0; for s in $(seq 0 49); do run_seed $W/ref $s || fails=$((fails+1)); done; echo "reference with proposed fix: failing seeds 0-49 = $fails" > $O/proposed_fix_reference_r6.out
for A in $R/ledgers/FC1/alternatives/*.py $R/ledgers/FC1/scripts/FC1-c-r4/alt/*.py $S/alt/*.py; do
  mkdir -p $W/alt && cp "$A" $W/alt/instruments.py && cp $S/proposed_grader_fix_r6.py $W/alt/test_project.py && cp $G/instance.py $W/alt/
  k=0; for s in $(seq 0 19); do run_seed $W/alt $s || k=$((k+1)); done; echo "$(basename $A) failing_seeds_with_proposed_fix=$k"
done >> $O/proposed_fix_reference_r6.out
rm -rf $W
echo probes-done
