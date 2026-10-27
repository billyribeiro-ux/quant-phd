#!/bin/sh
# Round-34 timing of the solution snippets (python -I -W error, scratch directory, 3 runs each; wall seconds).
# Usage: sh ledgers/S7/scripts/L05-L06-r34/time_snippets.sh <repo-root> <scratch-dir>
ROOT="$1"; SCR="$2"; mkdir -p "$SCR"
for f in sol-S7-L05-E2 sol-S7-L05-E3 sol-S7-L06-E3; do
  for i in 1 2 3; do
    d=$(mktemp -d "$SCR/t.XXXX")
    s=$(python3 -c 'import time;print(time.time())')
    (cd "$d" && "$ROOT/.venv/bin/python" -I -W error "$ROOT/tests/labs/S7/$f.py" > /dev/null 2>&1; echo "rc=$?" > "$d/rc")
    e=$(python3 -c 'import time;print(time.time())')
    echo "$f run $i: $(cat "$d/rc") wall $(python3 -c "print(round($e-$s,2))") s"
    rm -rf "$d"
  done
done
