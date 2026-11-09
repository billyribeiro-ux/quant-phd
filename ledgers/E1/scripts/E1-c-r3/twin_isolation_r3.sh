#!/bin/sh
# Round-3: run each E1 L07-L09 lab twin alone under python -I -W error, empty environment, from a fresh temp dir.
ROOT="$1"
PY="$ROOT/.venv/bin/python"
for f in L07 L08 L09; do
  T=$(mktemp -d)
  (cd "$T" && env -i PATH=/usr/bin:/bin "$PY" -I -W error "$ROOT/tests/labs/E1/lab-E1-$f-1.py" > "$ROOT/ledgers/E1/scripts/E1-c-r3/twin_$f.stdout" 2> "$ROOT/ledgers/E1/scripts/E1-c-r3/twin_$f.stderr")
  echo "$f exit=$? stderr_bytes=$(wc -c < "$ROOT/ledgers/E1/scripts/E1-c-r3/twin_$f.stderr" | tr -d ' ') stdout_lines=$(wc -l < "$ROOT/ledgers/E1/scripts/E1-c-r3/twin_$f.stdout" | tr -d ' ')"
  rm -rf "$T"
done
