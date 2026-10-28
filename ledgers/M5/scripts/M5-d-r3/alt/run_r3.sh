#!/bin/bash
cd /tmp/M5-v/d3/alt
W=w_$1; rm -rf $W; mkdir -p $W && cp instance.py test_project.py reference_r3.py $W/ && cp $1.py $W/contraction_solver.py && cd $W
fail=0
for s in $(seq 0 49); do
  out=$(QF_SEED=$s /tmp/verifyB3-M5-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  case "$out" in *failed*|*error*) fail=$((fail+1)); echo "seed $s: $out";; esac
done
echo "$1 failing seeds: $fail / 50"
