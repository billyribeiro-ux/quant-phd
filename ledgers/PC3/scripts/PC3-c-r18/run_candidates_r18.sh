#!/bin/bash
# Round 18, PC3 slice c. Runs the grader suite (copied to a scratch dir) against each candidate module.
# Usage: run_candidates_r18.sh <seed> <module.py> ...   (seed 0 covers the fixed seeds 0-49 and 7919)
REPO=/Users/billyribeiro/.fanout/wt/verifyE18-PC3-c
G="$REPO/course/modules/PC/PC3/grader"
SEED_VAL="$1"; shift
for M in "$@"; do
  D=$(mktemp -d /tmp/pc3c_r18_cand.XXXXXX)
  cp "$G/engine.py" "$G/instance.py" "$G/test_project.py" "$D/"
  cp "$M" "$D/market_maker.py"
  ( cd "$D" && QF_SEED="$SEED_VAL" "$REPO/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error -rf test_project.py > "$D/log.txt" 2>&1; echo "exit=$?" > "$D/exit.txt" )
  echo "== seed=$SEED_VAL $(basename "$M"): $(cat "$D/exit.txt") $(tail -1 "$D/log.txt")"
  grep "^FAILED" "$D/log.txt" | head -3
  rm -rf "$D"
done
