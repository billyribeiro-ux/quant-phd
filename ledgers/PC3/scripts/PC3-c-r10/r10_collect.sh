#!/bin/bash
# Round 10 verifier: collect-only counts of the PC3 grader for several seeds, with the page's flags, in a scratch copy.
ROOT=/Users/billyribeiro/.fanout/wt/verifyE10-PC3-c
G=$ROOT/course/modules/PC/PC3/grader
for seed in 0 1 7 49 50 848197495 1712259056; do
  W=$(mktemp -d /tmp/pc3c-r10-collect.XXXX)
  cp $G/engine.py $G/instance.py $G/test_project.py $W/
  cp $G/reference.py $W/market_maker.py
  (cd $W && QF_SEED=$seed PYTHONHASHSEED=0 $ROOT/.venv/bin/python -m pytest --collect-only -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 | sed "s/^/seed $seed: /")
  rm -rf $W
done
