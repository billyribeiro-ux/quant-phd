#!/bin/bash
# Collect-only counts for the PC3 grader suite on the reference solution, for several learner seeds.
# Usage: collect_counts.sh <workdir-with-market_maker.py> ; run from the quant-phd repo root.
set -u
REPO=/Users/billyribeiro/dev/quant-phd
GRADER=$REPO/course/modules/PC/PC3/grader
WORK=${1:?workdir}
rm -rf "$WORK" && mkdir -p "$WORK"
cp "$GRADER/engine.py" "$GRADER/instance.py" "$GRADER/test_project.py" "$WORK/"
cp "$GRADER/reference.py" "$WORK/market_maker.py"
cd "$WORK" || exit 1
for seed in 0 1 7 49 50 848197495; do
  printf 'QF_SEED=%s: ' "$seed"
  QF_SEED=$seed "$REPO/.venv/bin/pytest" --collect-only -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1
done
