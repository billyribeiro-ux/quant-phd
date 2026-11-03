#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyD2-E3-d
D=ledgers/E3/scripts/E3-d-r2
for s in 0 1 2 3 4 5 6 7 8 9; do
  ( .venv/bin/python $D/alt_runner_r2.py alt4 $s > $D/alt4_seed$s.out 2>&1; echo "EXIT $?" >> $D/alt4_seed$s.out ) &
done
wait
