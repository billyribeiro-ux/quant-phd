#!/bin/bash
# Round 18: run each LX1 slice-b lab twin alone, in an empty scratch dir, under the repo's CPython 3.14 with -I -W error.
# The L04 twin reads data/fx_monthly.csv relative to its working directory, so that file is copied in (as the page's data-files says).
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
PY="$ROOT/.venv/bin/python"
OUT="$ROOT/ledgers/LX1/scripts/LX1-b-r18/out"
mkdir -p "$OUT"
for t in L01 L03 L04; do
  d=$(mktemp -d /tmp/lx1b-r18-twin-XXXX)
  cp "$ROOT/tests/labs/LX1/lab-LX1-$t-1.py" "$d/"
  if [ "$t" = "L04" ]; then mkdir -p "$d/data" && cp "$ROOT/course/assets/data/market/fx_monthly.csv" "$d/data/"; fi
  (cd "$d" && "$PY" -I -W error "lab-LX1-$t-1.py" > "$OUT/twin_$t.stdout" 2> "$OUT/twin_$t.stderr"; echo $? > "$OUT/twin_$t.exit")
  echo "$t exit=$(cat "$OUT/twin_$t.exit")" 
  rm -rf "$d"
done
