#!/bin/bash
# Round 10: run each L01-L04 lab twin alone under CPython -I -W error (no page, no harness).
ROOT=/Users/billyribeiro/.fanout/wt/verifyD10-E3-f
cd "$ROOT/tests/labs/E3" || exit 2
for f in lab-E3-L01-1.py lab-E3-L02-1.py lab-E3-L03-1.py lab-E3-L04-1.py; do
  echo "== $f"
  "$ROOT/.venv/bin/python" -I -W error "$f" 2>&1
  echo "exit $?"
done
