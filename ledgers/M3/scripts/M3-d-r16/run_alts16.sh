#!/bin/bash
PY=$1; G=$2; C=$3
W=$(mktemp -d /tmp/m3d16_run.XXXX)
cp $G/test_project.py $G/instance.py $W/
cp $C/covariance_doctor.py $W/
pass=0; fail=0
cd $W
for s in $(seq 0 49); do
  if QF_SEED=$s $PY -I -W error -m pytest -q -p no:cacheprovider --assert=plain test_project.py >/dev/null 2>&1; then pass=$((pass+1)); else fail=$((fail+1)); fi
done
echo "$(basename $C): pass=$pass fail=$fail"
