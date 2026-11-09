#!/bin/bash
# Run the grader suite (QF_SEED=0 covers fixed seeds 0-49, seed 0 and 7919) against each mutant given as an argument.
REPO=/Users/billyribeiro/.fanout/wt/verifyE16-PC3-c
G="$REPO/course/modules/PC/PC3/grader"
for M in "$@"; do
  D=$(mktemp -d /tmp/pc3c_r16_mut.XXXXXX)
  cp "$G/engine.py" "$G/instance.py" "$G/test_project.py" "$D/"
  cp "$M" "$D/market_maker.py"
  ( cd "$D" && QF_SEED=0 "$REPO/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$D/log.txt" 2>&1; echo "exit=$?" )
  echo "== $(basename "$M"): $(tail -1 "$D/log.txt")"
  grep "^FAILED" "$D/log.txt" | head -4
  rm -rf "$D"
done
