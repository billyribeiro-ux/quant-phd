#!/bin/bash
# Round 9 collect-only and reference-solution pass counts for the PC3 grader at pin c93dd52.
REPO=/Users/billyribeiro/.fanout/wt/verifyE9-PC3-c
GRADER=$REPO/course/modules/PC/PC3/grader
W=/tmp/pc3c-r9/work-ref
rm -rf "$W" && mkdir -p "$W"
cp "$GRADER/engine.py" "$GRADER/instance.py" "$GRADER/test_project.py" "$W/"
cp "$GRADER/reference.py" "$W/market_maker.py"
cd "$W" || exit 1
for seed in 0 1 7 49 50 848197495 1712259056; do
  printf 'collect QF_SEED=%s: ' "$seed"
  QF_SEED=$seed "$REPO/.venv/bin/pytest" --collect-only -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1
  printf 'reference run QF_SEED=%s: ' "$seed"
  QF_SEED=$seed "$REPO/.venv/bin/pytest" -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1
done
