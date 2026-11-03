#!/bin/bash
# FC1-c round 3 extra command rows (verifier D3). Run from the checkout root; outputs under out/.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD3-FC1-c
cd "$ROOT"
S=ledgers/FC1/scripts/FC1-c-r3
O=$S/out
PY=$ROOT/.venv/bin/python
GR=course/modules/FC/FC1/grader
W=$(mktemp -d /tmp/fc1c_r3_extra_XXXX)
cp $GR/test_project.py $GR/instance.py $W/
# 1. collect-only on the reference (68 -> 69 check)
cp $GR/reference.py $W/instruments.py
(cd $W && $PY -I -m pytest --collect-only -q -p no:cacheprovider --assert=plain -W error test_project.py) > $O/collect_only_r3.out 2>&1
# 2. starter under the browser flags
cp $GR/starter.py $W/instruments.py
(cd $W && QF_SEED=0 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) > $O/starter_local_r3.out 2>&1
# 3. float-discount mutant: the two exact-half docstring tests
cp ledgers/FC1/mutants/r3c_discount_factor_float_times_amount.py $W/instruments.py
for t in test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield test_bond_price_exact_half_cent_at_496_bps_is_exact_not_float; do
  (cd $W && QF_SEED=0 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error "test_project.py::$t") 2>&1 | tail -1 >> $O/float_mutant_single_tests_r3.out
done
# 4. mutant probes (cap at twenty periods, ten-digit Decimal) against the reference fixtures
$PY -I $S/mutant_probes_r3.py $ROOT > $O/mutant_probes_r3.out 2>&1
# 5. verify the twins alone under -I -W error
$PY -I -W error tests/labs/FC1/lab-FC1-project-1.py > $O/twin_p1.out 2>&1; echo "twin1 exit=$?" >> $O/_extra_exit.txt
$PY -I -W error tests/labs/FC1/lab-FC1-project-3.py > $O/twin_p3.out 2>&1; echo "twin3 exit=$?" >> $O/_extra_exit.txt
# 6. independent numbers and instance checks
$PY -I $S/numbers_instances_r3.py $ROOT > $O/numbers_instances_r3.out 2>&1
# 7. assert scans and leak scans of the round-3 test file
$PY -I $S/scan_asserts.py $GR/test_project.py > $O/scan_asserts.out 2>&1
$PY -I $S/scan_leak.py $GR/test_project.py > $O/scan_leak.out 2>&1
# 8. card check over all 124 cards
$PY -I $S/cards_check.py $ROOT > $O/cards_check.out 2>&1
# 9. alternatives on seeds 0-19 (exit codes decide; the runner's success text is a fixed string)
$PY -I $S/run_alts_r3.py $ROOT /tmp/fc1c_r3_alts_extra ledgers/FC1/alternatives/*.py $S/alt/*.py > $O/alternatives_0_19_r3.out 2>&1
rm -rf "$W"
echo DONE >> $O/_extra_exit.txt
