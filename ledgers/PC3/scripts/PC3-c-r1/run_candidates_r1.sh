#!/bin/bash
# PC3 slice c, closing delta round 1. Runs the grader suite (copied to a scratch dir) against each candidate module.
# Usage: run_candidates_r1.sh <seed> <module.py> ...
REPO=/Users/billyribeiro/.fanout/wt/verifyF31-PC3-c
G="$REPO/course/modules/PC/PC3/grader"
SEED_VAL="$1"; shift
for M in "$@"; do
  D=$(mktemp -d /tmp/pc3c_r1_cand.XXXXXX)
  cp "$G/engine.py" "$G/instance.py" "$G/test_project.py" "$D/"
  cp "$M" "$D/market_maker.py"
  ( cd "$D" && QF_SEED="$SEED_VAL" "$REPO/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error -rf test_project.py > "$D/log.txt" 2>&1; echo "exit=$?" > "$D/exit.txt" )
  echo "== seed=$SEED_VAL $(basename "$M"): $(cat "$D/exit.txt") $(tail -1 "$D/log.txt")"
  grep "^FAILED" "$D/log.txt" | head -3
  rm -rf "$D"
done
