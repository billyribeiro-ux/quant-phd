#!/bin/sh
# Verifier E3-e round 3: the five alternatives run as parallel processes (one per alternative or seed window).
cd /Users/billyribeiro/.fanout/wt/verifyD3-E3-e || exit 1
S=ledgers/E3/scripts/E3-e-r3
R2=ledgers/E3/scripts/E3-e-r2
for a in alt1 alt2 alt3 alt5; do
  ( .venv/bin/python -I $R2/run_alt_one_r2.py $a 0-49 > $S/alt_${a}_0_49.out 2>&1; echo "exit=$?" >> $S/alt_${a}_0_49.out ) &
done
for w in 0-9 10-19 20-29 30-39 40-49; do
  ( .venv/bin/python -I $R2/run_alt_one_r2.py alt4 $w > $S/alt4_$w.out 2>&1; echo "exit=$?" >> $S/alt4_$w.out ) &
done
wait
echo done > $S/ALTS_DONE
