#!/bin/bash
# Verifier r4 scratch checks for FC1-c (run from anywhere; writes only under /tmp and out/).
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c
G=$ROOT/course/modules/FC/FC1/grader
PY=$ROOT/.venv/bin/python
OUT=$ROOT/ledgers/FC1/scripts/FC1-c-r4/out
# 1. collect-only count of the suite against the reference (the suite imports instruments)
rm -rf /tmp/fc1c_r4_collect && mkdir -p /tmp/fc1c_r4_collect && cp $G/reference.py /tmp/fc1c_r4_collect/instruments.py && cp $G/test_project.py $G/instance.py /tmp/fc1c_r4_collect/
(cd /tmp/fc1c_r4_collect && $PY -m pytest --collect-only -q -p no:cacheprovider test_project.py) > $OUT/collect_only_r4.out 2>&1; echo "collect exit=$?"
(cd /tmp/fc1c_r4_collect && QF_SEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) > $OUT/reference_seed0_r4.out 2>&1; echo "reference seed0 exit=$?"
# 2. the starter must fail the suite
rm -rf /tmp/fc1c_r4_starter && mkdir -p /tmp/fc1c_r4_starter && cp $G/starter.py /tmp/fc1c_r4_starter/instruments.py && cp $G/test_project.py $G/instance.py /tmp/fc1c_r4_starter/
(cd /tmp/fc1c_r4_starter && QF_SEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) > $OUT/starter_seed0_r4.out 2>&1; echo "starter exit=$? (nonzero expected)"
# 3. a 40-period test (scratch only, not in the repo) must kill both thirty-period survivors and pass the reference
rm -rf /tmp/fc1c_r4_fix && mkdir -p /tmp/fc1c_r4_fix/{ref40,m30,m30x} && cp $G/test_project.py $G/instance.py /tmp/fc1c_r4_fix/
cat >> /tmp/fc1c_r4_fix/test_project.py <<'PYEOF'


def test_scratch_forty_periods() -> None:
    __tracebackhide__ = True
    bond = sol.Bond(10_000, 500, 40)
    rows = checked_events(bond.events(), "Bond.events")
    assert rows == oracle_events(10_000, 500, 40), "every period 1..40"
    got = checked_int(sol.bond_price_cents(bond, 400), "bond_price_cents")
    assert got == oracle_price(oracle_events(10_000, 500, 40), 400), "all 40 events discounted by their own period"
PYEOF
for d in ref40 m30 m30x; do cp /tmp/fc1c_r4_fix/test_project.py /tmp/fc1c_r4_fix/instance.py /tmp/fc1c_r4_fix/$d/; done
cp $G/reference.py /tmp/fc1c_r4_fix/ref40/instruments.py
cp $ROOT/ledgers/FC1/mutants/r4c_schedule_stops_at_thirty_periods.py /tmp/fc1c_r4_fix/m30/instruments.py
cp $ROOT/ledgers/FC1/mutants/r4c_discount_exponent_capped_at_thirty.py /tmp/fc1c_r4_fix/m30x/instruments.py
for d in ref40 m30 m30x; do (cd /tmp/fc1c_r4_fix/$d && QF_SEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) > $OUT/fix40_$d.out 2>&1; echo "fix40 $d exit=$? (ref40 0 expected, m30 and m30x nonzero expected)"; done
