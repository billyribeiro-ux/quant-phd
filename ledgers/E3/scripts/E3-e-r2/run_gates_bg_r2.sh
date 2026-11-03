#!/bin/sh
# Verifier E3-e round 2: long gates, run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyD2-E3-e || exit 1
S=ledgers/E3/scripts/E3-e-r2
.venv/bin/python tools/run_graders.py --unit E3 --seeds 0-49 > $S/run_graders_E3_0_49.out 2>&1; echo "exit=$?" >> $S/run_graders_E3_0_49.out
.venv/bin/python tools/mutate_graders.py --unit E3 --seeds 0-9 > $S/mutate_E3_0_9.out 2>&1; echo "exit=$?" >> $S/mutate_E3_0_9.out
