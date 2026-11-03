#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyD2-E3-d
D=ledgers/E3/scripts/E3-d-r2
for a in alt1 alt2 alt3 alt4 alt5; do
  ( .venv/bin/python $D/alt_runner_r2.py $a 0-9 > $D/alt_$a.out 2>&1; echo "EXIT $?" >> $D/alt_$a.out ) &
done
wait
