#!/bin/bash
# FC2-d r3: run one alternative (or reference) as scanner.py against the FC2 suite over seeds A..B.
# usage: alt_run_r3.sh <repo-root> <impl-path> <seed-from> <seed-to>
ROOT="$1"; IMPL="$2"; A="$3"; B="$4"
G="$ROOT/course/modules/FC/FC2/grader"
PY="$ROOT/.venv/bin/python"
name=$(basename "$IMPL" .py)
W=/tmp/fc2d-r3-$name
rm -rf "$W"; mkdir -p "$W"
cp "$G/test_project.py" "$G/instance.py" "$W/"
cp "$IMPL" "$W/scanner.py"
cd "$W" || exit 1
fails=0; detail=""
for s in $(seq "$A" "$B"); do
  out=$(QF_SEED=$s "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  rc=$?
  if [ $rc -ne 0 ]; then
    fails=$((fails+1))
    t=$(echo "$out" | grep -o 'FAILED test_project.py::[^ ]*' | sed 's/FAILED test_project.py:://' | sort -u | tr '\n' ' ')
    detail="$detail seed$s:[$t]"
  fi
done
echo "$name: failing_seeds=$fails/$((B-A+1)) $(echo "$detail" | cut -c1-600)"
