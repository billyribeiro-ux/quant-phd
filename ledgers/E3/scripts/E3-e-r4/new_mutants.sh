#!/bin/sh
# Round 4, slice e: run each new student-error mutant (ledgers/E3/mutants/g4_*.py) against the E3 suite on seeds 0-2.
# Usage: sh new_mutants.sh <checkout> <python>
CHECK="$1"; PY="$2"
for m in "$CHECK"/ledgers/E3/mutants/g4_0*.py; do
  d=$(mktemp -d /tmp/e3e_r4_mut.XXXXXX)
  cp "$CHECK/course/modules/E/E3/grader/test_project.py" "$CHECK/course/modules/E/E3/grader/instance.py" "$d/"
  cp "$m" "$d/elicit.py"
  for s in 0 1 2; do
    (cd "$d" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 | sed "s|^|seed $s $(basename "$m"): |")
  done
  rm -rf "$d"
done
