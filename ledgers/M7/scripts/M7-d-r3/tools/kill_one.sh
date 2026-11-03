#!/bin/bash
# usage: kill_one.sh <mutant.py> <checkout-root> ; runs seeds 0-9, stops at first failing seed
M="$1"; R="$2"; G="$R/course/modules/M/M7/grader"
W=$(mktemp -d /tmp/m7d-kill-XXXX)
cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$M" "$W/constrained_allocator.py"
for s in 0 1 2 3 4 5 6 7 8 9; do
  out=$(cd "$W" && QF_SEED=$s "$R/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  rc=$?
  if [ $rc -ne 0 ]; then echo "KILLED $(basename "$M") seed $s: $(echo "$out" | grep -o 'FAILED [^ ]*' | head -1) ($(echo "$out" | tail -1))"; rm -rf "$W"; exit 0; fi
done
echo "SURVIVED $(basename "$M") seeds 0-9"; rm -rf "$W"
