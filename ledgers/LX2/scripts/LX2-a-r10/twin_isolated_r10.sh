#!/bin/sh
# Run each slice-a lab twin alone under python -I -W error from an empty scratch dir.
# usage: twin_isolated_r10.sh <checkout>
CO="$1"
PY="$CO/.venv/bin/python"
for t in L01-1 L02-1; do
  d=$(mktemp -d /tmp/lx2a_r10_twin_XXXX)
  cd "$d" || exit 1
  "$PY" -I -W error "$CO/tests/labs/LX2/lab-LX2-$t.py" > "$d/stdout.txt" 2> "$d/stderr.txt"
  rc=$?
  echo "== lab-LX2-$t exit=$rc stderr_bytes=$(wc -c < "$d/stderr.txt") stdout_lines=$(wc -l < "$d/stdout.txt")"
  sha256sum "$d/stdout.txt" | cut -c1-64
done
