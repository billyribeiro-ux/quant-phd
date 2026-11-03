#!/bin/bash
# FC1-c round 3 ad hoc checks (verifier D3), each output kept under out/. Run from the checkout root.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD3-FC1-c
cd "$ROOT"
S=ledgers/FC1/scripts/FC1-c-r3
O=$S/out
PY=$ROOT/.venv/bin/python
GR=course/modules/FC/FC1/grader
: > $O/checks_r3_exit.txt
# A. word-count scan of assert messages (short messages)
$PY -I $S/short_messages_r3.py $GR/test_project.py > $O/short_messages_r3.out 2>&1; echo "short_messages exit=$?" >> $O/checks_r3_exit.txt
# B. banned phrases, process words, long/short, hub and lesson hours, fixture use
grep -n -i -E "TODO|TBD|lorem|for brevity|beyond the scope|left as an exercise|it is important to note|studies show|experts agree|well known|obviously|clearly|builder|verifier|ledger|checkout|mutant|plan\b|architect|\blong\b|\bshort\b|\bround\b" course/modules/FC/FC1/project.html $GR/*.py course/modules/FC/FC1/cards.json > $O/banned_and_process_words_r3.out 2>&1; echo "banned_words exit=$?" >> $O/checks_r3_exit.txt
grep -n -E "data-hours" course/modules/FC/FC1/index.html course/modules/FC/FC1/L0*.html course/modules/FC/FC1/project.html > $O/hours_attributes_r3.out 2>&1; echo "hours exit=$?" >> $O/checks_r3_exit.txt
grep -n -E "10_001, 0, 1|10001, 0, 1|10_000, 500, 3|Bond\(10000, 500, 3\)|Bond\(1, 0, 1\)" $GR/test_project.py > $O/fixture_uses_r3.out 2>&1; echo "fixture_uses exit=$?" >> $O/checks_r3_exit.txt
# C. alternatives on sampled seeds: real pytest counts (the runner's text is fixed)
D=$(mktemp -d /tmp/fc1c_r3_sample_XXXX)
cp $GR/test_project.py $GR/instance.py $D/
for alt in ledgers/FC1/alternatives/a3_fraction_throughout.py $S/alt/alt_decimal.py $S/alt/alt_memo_per_yield.py; do
  cp "$alt" $D/instruments.py
  for s in 0 3 7 19; do
    (cd $D && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 | sed "s|^|$(basename $alt) seed $s: |") >> $O/sample_counts_r3.out
  done
done
rm -rf "$D"
# D. leak runs: a failing run shows the messages and no literal values
D=$(mktemp -d /tmp/fc1c_r3_leak_XXXX)
cp $GR/test_project.py $GR/instance.py $D/
for m in m03_principal_omitted_at_maturity v1c_trade_rounded_to_dollars; do
  cp ledgers/FC1/mutants/$m.py $D/instruments.py
  (cd $D && QF_SEED=0 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) > $O/leak_$m.out 2>&1
done
rm -rf "$D"
# E. the Decimal mutant at -9999 on the seed-0 bond: which exception
$PY -I $S/decimal_exception_r3.py $ROOT > $O/decimal_exception_r3.out 2>&1; echo "decimal_exception exit=$?" >> $O/checks_r3_exit.txt
echo DONE >> $O/checks_r3_exit.txt
