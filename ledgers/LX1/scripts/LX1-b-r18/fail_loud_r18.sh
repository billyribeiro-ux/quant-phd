#!/bin/bash
# Round 18: the L04 twin must raise ValueError on a blank GBP cell, a non-decimal GBP cell, a skipped month and a missing column.
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
PY="$ROOT/.venv/bin/python"
SRC="$ROOT/course/assets/data/market/fx_monthly.csv"
for case in blank nondecimal skipped nocolumn; do
  d=$(mktemp -d /tmp/lx1b-r18-fail-XXXX)
  cp "$ROOT/tests/labs/LX1/lab-LX1-L04-1.py" "$d/"
  mkdir -p "$d/data"
  "$PY" -I -c "
import sys
src, dst, case = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(src, encoding='utf-8').read().splitlines()
hdr = lines[0].split(',')
g = hdr.index('GBP')
out = [lines[0]]
for i, line in enumerate(lines[1:], start=1):
    parts = line.split(',')
    if i == 300 and case == 'blank': parts[g] = ''
    if i == 300 and case == 'nondecimal': parts[g] = 'n/a'
    if i == 300 and case == 'skipped': continue
    if case == 'nocolumn': parts[g] = parts[g]
    out.append(','.join(parts))
if case == 'nocolumn': out[0] = out[0].replace('GBP', 'GBX')
open(dst, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
" "$SRC" "$d/data/fx_monthly.csv" "$case"
  (cd "$d" && "$PY" -I -W error lab-LX1-L04-1.py > out.txt 2> err.txt; echo "$case exit=$?")
  tail -1 "$d/err.txt"
  rm -rf "$d"
done
