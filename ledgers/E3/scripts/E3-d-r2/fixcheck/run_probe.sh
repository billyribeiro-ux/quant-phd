#!/bin/bash
# Runs the gap-probe test (test_zz_gain_of_zero_probability_does_not_make_a_mix) against the reference and against mutant e3d2_01.
cd "$(dirname "$0")"
PY=/Users/billyribeiro/.fanout/wt/verifyD2-E3-d/.venv/bin/python
for impl in reference_elicit mutant_elicit; do
  rm -rf work_$impl && mkdir work_$impl && cp test_project_with_gap_probe.py work_$impl/test_project.py && cp instance.py work_$impl/ && cp $impl.py work_$impl/elicit.py
  (cd work_$impl && QF_SEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py -k zz 2>&1 | tail -1 | sed "s/^/$impl: /")
done
