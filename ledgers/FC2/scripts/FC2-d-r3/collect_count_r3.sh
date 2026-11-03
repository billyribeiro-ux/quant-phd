#!/bin/bash
# collect-only count of the FC2 suite on the reference as scanner.py, per seed. usage: collect_count_r3.sh <root> <scratch> <from> <to>
ROOT="$1"; SCR="$2"; A="$3"; B="$4"
G="$ROOT/course/modules/FC/FC2/grader"
rm -rf "$SCR"; mkdir -p "$SCR"; cp "$G/test_project.py" "$G/instance.py" "$SCR/"; cp "$G/reference.py" "$SCR/scanner.py"
cd "$SCR" || exit 1
counts=""
for s in $(seq "$A" "$B"); do
  n=$(QF_SEED=$s "$ROOT/.venv/bin/python" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>/dev/null | grep -c '::')
  counts="$counts $s:$n"
done
echo "$counts"
