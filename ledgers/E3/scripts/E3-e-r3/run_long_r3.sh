#!/bin/sh
# Verifier E3-e round 3 (fresh runs at pin a007712): long gates and alternatives, run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyD3-E3-e || exit 1
S=ledgers/E3/scripts/E3-e-r3
.venv/bin/python tools/run_graders.py --unit E3 --seeds 0-49 > $S/r3_run_graders_0_49.out 2>&1; echo "exit=$?" >> $S/r3_run_graders_0_49.out &
.venv/bin/python tools/mutate_graders.py --unit E3 --seeds 0-9 > $S/r3_mutate_E3_0_9.out 2>&1; echo "exit=$?" >> $S/r3_mutate_E3_0_9.out &
for a in alt1 alt2 alt3 alt5; do
  ( .venv/bin/python -I ledgers/E3/scripts/E3-e-r2/run_alt_one_r2.py $a 0-49 > $S/r3_alt_${a}_0_49.out 2>&1; echo "exit=$?" >> $S/r3_alt_${a}_0_49.out ) &
done
for w in 0-9 10-19 20-29 30-39 40-49; do
  ( .venv/bin/python -I ledgers/E3/scripts/E3-e-r2/run_alt_one_r2.py alt4 $w > $S/r3_alt4_$w.out 2>&1; echo "exit=$?" >> $S/r3_alt4_$w.out ) &
done
wait
echo done > $S/r3_LONG_DONE
