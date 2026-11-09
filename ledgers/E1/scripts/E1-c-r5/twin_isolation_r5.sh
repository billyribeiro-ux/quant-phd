#!/bin/sh
# Run each slice twin alone: python -I -W error, empty environment, fresh temp dir (verifier round 5, E1 slice c).
# Usage (repository root): sh ledgers/E1/scripts/E1-c-r4/twin_isolation_r4.sh
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
PY="$ROOT/.venv/bin/python"
for L in L07 L08 L09; do
  D=$(mktemp -d)
  cp "$ROOT/tests/labs/E1/lab-E1-$L-1.py" "$D/twin.py"
  (cd "$D" && env -i PATH=/usr/bin:/bin "$PY" -I -W error twin.py > out.txt 2> err.txt)
  rc=$?
  echo "$L exit=$rc stderr_bytes=$(wc -c < "$D/err.txt" | tr -d ' ') stdout_lines=$(wc -l < "$D/out.txt" | tr -d ' ')"
  rm -rf "$D"
done
