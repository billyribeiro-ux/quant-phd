#!/bin/bash
# Collect-only count of the FC2 project suite per seed, on the reference solution as scanner.py.
# usage: collect_count.sh <repo-root> <scratch-dir> <seed-from> <seed-to>
set -u
ROOT="$1"; SCR="$2"; A="$3"; B="$4"
G="$ROOT/course/modules/FC/FC2/grader"
rm -rf "$SCR"; mkdir -p "$SCR"
cp "$G/test_project.py" "$G/instance.py" "$SCR/"
cp "$G/reference.py" "$SCR/scanner.py"
cd "$SCR" || exit 1
PY="$ROOT/.venv/bin/python"
counts=""
for s in $(seq "$A" "$B"); do
  n=$(QF_SEED=$s "$PY" -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>/dev/null | grep -c '::')
  counts="$counts $s:$n"
done
echo "$counts"
