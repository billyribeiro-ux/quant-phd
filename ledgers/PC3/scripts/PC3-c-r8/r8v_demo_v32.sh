#!/bin/bash
# Demonstrate v32 (module-global quote) and v33 (no-fill print) survive the suite, and that a fresh process and a second game in the same process differ.
REPO=/Users/billyribeiro/.fanout/wt/verifyE8-PC3-c
W=/tmp/pc3c-r8/demo-v32
rm -rf $W && mkdir -p $W && cp $REPO/course/modules/PC/PC3/grader/{engine.py,instance.py,test_project.py} $W/
cp $REPO/ledgers/PC3/mutants/v32_quote_keeps_last_fill_in_a_module_global.py $W/market_maker.py
cd $W
echo "== same process: play seed 7 first, then seed 0; turn-1 quote of seed 0 game"
$REPO/.venv/bin/python -c "
import engine, market_maker as m
engine.play(m.quote, 7)
log = engine.play(m.quote, 0)
print('seed0 after seed7 turn1 (bid,ask,size):', (log['turns'][0]['bid_cents'], log['turns'][0]['ask_cents'], log['turns'][0]['size']))
"
echo "== fresh process: seed 0 turn-1 quote"
$REPO/.venv/bin/python -c "
import engine, market_maker as m
log = engine.play(m.quote, 0)
print('seed0 fresh turn1 (bid,ask,size):', (log['turns'][0]['bid_cents'], log['turns'][0]['ask_cents'], log['turns'][0]['size']))
"
echo "== suite with QF_SEED=0 on v32"
for s in 0 7 1712259056; do printf "QF_SEED=$s: "; QF_SEED=$s $REPO/.venv/bin/pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1; done
