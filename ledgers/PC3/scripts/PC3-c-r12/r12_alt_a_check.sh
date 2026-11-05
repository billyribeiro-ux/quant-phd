#!/bin/bash
# Round 12 verifier: runs the turn-indexed alternative (alt_r12_a) through the checkout's grader on seed 0 and records the failing test.
ROOT=/Users/billyribeiro/.fanout/wt/verifyE12-PC3-c
S=$ROOT/ledgers/PC3/scripts/PC3-c-r12
W=$(mktemp -d /tmp/pc3c-r12-altA.XXXX)
cp $ROOT/course/modules/PC/PC3/grader/engine.py $ROOT/course/modules/PC/PC3/grader/instance.py $ROOT/course/modules/PC/PC3/grader/test_project.py $W/
cp $S/alts/alt_r12_a_turn_indexed_history.py $W/market_maker.py
(cd $W && QF_SEED=0 PYTHONDONTWRITEBYTECODE=1 $ROOT/.venv/bin/python -I -B -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py -rf 2>&1 | grep -E "^FAILED|^E |passed|failed")
rm -rf $W
