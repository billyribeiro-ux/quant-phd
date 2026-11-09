#!/bin/sh
# Runs each M2 slice twin alone under python -I -W error in a fresh scratch dir; prints exit code, stderr bytes and seconds.
ROOT="$1"
SCR=$(mktemp -d)
for n in 01 02 03 04 05 06; do
  f="$ROOT/tests/labs/M2/lab-M2-L$n-1.py"
  start=$(date +%s)
  ( cd "$SCR" && /usr/bin/env "$ROOT/.venv/bin/python" -I -W error "$f" > "$SCR/L$n.out" 2> "$SCR/L$n.err" )
  rc=$?
  end=$(date +%s)
  echo "L$n exit=$rc stderr_bytes=$(wc -c < "$SCR/L$n.err" | tr -d ' ') seconds=$((end-start)) stdout_lines=$(wc -l < "$SCR/L$n.out" | tr -d ' ')"
  cp "$SCR/L$n.out" "$SCR/L$n.stdout.saved" 2>/dev/null
done
echo "scratch=$SCR"
