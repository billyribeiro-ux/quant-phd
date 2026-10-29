#!/bin/bash
# usage: alts_r5.sh <python> <workdir> <grader dir> <alt file>...
PY=$1; W=$2; G=$3; shift 3
for alt in "$@"; do
  cp "$alt" "$W/instruments.py"
  fails=0; tot=0
  for s in $(seq 0 49); do
    out=$(cd $W && QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
    tot=$((tot+1))
    case "$out" in *failed*|*error*) fails=$((fails+1)); echo "  seed $s: $out";; esac
  done
  echo "$(basename $alt): seeds=$tot failing_seeds=$fails"
done
