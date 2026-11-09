#!/bin/bash
# Round 18, PC3 slice c. Collect-only counts of grader/test_project.py for two seeds, using reference.py as market_maker.py.
REPO=/Users/billyribeiro/.fanout/wt/verifyE18-PC3-c
G="$REPO/course/modules/PC/PC3/grader"
for SEED_VAL in 0 77314143; do
  D=$(mktemp -d /tmp/pc3c_r18_collect.XXXXXX)
  cp "$G/engine.py" "$G/instance.py" "$G/test_project.py" "$G/reference.py" "$D/"
  mv "$D/reference.py" "$D/market_maker.py"
  ( cd "$D" && QF_SEED="$SEED_VAL" "$REPO/.venv/bin/python" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py > "$D/collect.txt" 2>&1; echo "exit=$?" >> "$D/collect.txt" )
  echo "== seed=$SEED_VAL"; tail -2 "$D/collect.txt"
  grep '::' "$D/collect.txt" | sed -E 's/\[.*//' | sort | uniq -c
  rm -rf "$D"
done
