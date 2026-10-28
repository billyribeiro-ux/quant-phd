#!/bin/bash
# usage: run_variants.sh <variant.py> <seeds-from> <seeds-to>
PY=/tmp/verifyC1-E3-d/.venv/bin/python
G=/tmp/verifyC1-E3-d/course/modules/E/E3/grader
v=$1; a=$2; b=$3
fails=0; first=""
for s in $(seq $a $b); do
  w=$(mktemp -d /tmp/e3d-v/d/work-XXXX)
  cp $G/test_project.py $G/instance.py $w/
  cp "$v" $w/elicit.py
  out=$(cd $w && QF_SEED=$s PYTHONDONTWRITEBYTECODE=1 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  rc=$?
  if [ $rc -ne 0 ]; then fails=$((fails+1)); [ -z "$first" ] && first="seed $s: $(echo "$out" | grep -E '^FAILED' | head -1)"; fi
  rm -rf $w
done
echo "$(basename $v): failing seeds $fails of $((b-a+1)) ; first: ${first:-none}"
