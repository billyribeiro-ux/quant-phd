#!/bin/sh
# Run every alternative in $1 against the M2 suite for seeds 0-49; print pass/fail per alternative.
PY="$2"
GRADER="$3"
for d in "$1"/*/; do
  name=$(basename "$d")
  cp "$GRADER/test_project.py" "$GRADER/instance.py" "$d"
  fails=0; passes=0
  for s in $(seq 0 49); do
    if (cd "$d" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > /tmp/m2e_r10_alt_last.out 2>&1); then
      passes=$((passes+1))
    else
      fails=$((fails+1)); echo "  $name seed $s FAILED: $(tail -1 /tmp/m2e_r10_alt_last.out)"
    fi
  done
  echo "$name: seeds passed $passes/50, failed $fails"
done
