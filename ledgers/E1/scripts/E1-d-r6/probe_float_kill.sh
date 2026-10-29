#!/bin/bash
# Round-6 E1-d: adds a large-exact-input test to a scratch copy of the grader and runs it on the float mutant,
# the reference and two alternatives. Output: failures for the float mutant, passes for the others.
R=/Users/billyribeiro/.fanout/wt/verifyB6-E1-d
S=$R/ledgers/E1/scripts/E1-d-r6
W=$(mktemp -d /tmp/e1d-fix-XXXX)
cp $R/course/modules/E/E1/grader/{instance.py,test_project.py} $W/
cat >> $W/test_project.py <<'PY'


@pytest.mark.parametrize("structure", STRUCTURES)
def test_large_exact_inputs_round_once(structure: str) -> None:
    a, b, c = 15000000000000002, 1, 1
    check(sol.outcome(structure, a, b, c) == expected(structure, a, b, c), "large exact inputs must round from exact values")
PY
for impl in $R/ledgers/E1/mutants/r6d_m01_half_up_in_float_wrong_for_large_inputs.py $R/course/modules/E/E1/grader/reference.py $S/alt3_cramer.py $S/alt2_decimal_half_up.py; do
  cp "$impl" $W/market_structure.py
  echo "== $(basename $impl)"; (cd $W && QF_SEED=0 $R/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py | tail -1)
done
rm -rf $W
