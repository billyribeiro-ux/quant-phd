#!/bin/bash
# FC2-d r2: run every alternative implementation (alt/*.py) as scanner.py against the FC2 suite, seeds A..B.
# usage: alt_run.sh <repo-root> <seed-from> <seed-to>
ROOT="$1"; A="$2"; B="$3"
HERE="$ROOT/ledgers/FC2/scripts/FC2-d-r2"
G="$ROOT/course/modules/FC/FC2/grader"
PY="$ROOT/.venv/bin/python"
for alt in "$HERE"/alt/*.py; do
  name=$(basename "$alt" .py)
  W=/tmp/fc2d-r2-$name
  rm -rf "$W"; mkdir -p "$W"
  cp "$G/test_project.py" "$G/instance.py" "$W/"
  cp "$alt" "$W/scanner.py"
  cd "$W" || exit 1
  fails=0; failed_tests=""
  for s in $(seq "$A" "$B"); do
    out=$(QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
    rc=$?
    if [ $rc -ne 0 ]; then
      fails=$((fails+1))
      t=$(echo "$out" | grep -o 'FAILED test_project.py::[^ ]*' | sed 's/FAILED test_project.py:://' | sort -u | tr '\n' ' ')
      failed_tests="$failed_tests seed$s:[$t]"
    fi
  done
  echo "$name: seeds-failed=$fails/$((B-A+1)) $failed_tests" | cut -c1-900
done
