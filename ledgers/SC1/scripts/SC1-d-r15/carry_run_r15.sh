#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyE15-SC1-d
R=/Users/billyribeiro/.fanout/wt/verifyE15-SC1-d
O=$R/ledgers/SC1/scripts/SC1-d-r15/out
for d in ledgers/SC1/scripts/SC1-d-r14/alternatives ledgers/SC1/scripts/SC1-d-r13/alternatives ledgers/SC1/scripts/SC1-d-r12/alternatives ledgers/SC1/scripts/SC1-d-r10/alternatives_r8_repathed_r10 ledgers/SC1/scripts/SC1-d-r10/alternatives ledgers/SC1/scripts/SC1-d-r11/alternatives ledgers/SC1/scripts/SC1-d-r9/alternatives_r8_repathed; do
  n=$(echo $d | tr '/' '_')
  /Users/billyribeiro/.fanout/wt/verifyE15-SC1-d/.venv/bin/python -I $R/ledgers/SC1/scripts/SC1-d-r15/run_alternatives_r15.py $R $R/$d /tmp/sc1d-r15/carried/$n > $O/carried_$n.txt 2>&1
  echo "EXIT=$?" >> $O/carried_$n.txt
done
echo done > $O/CARRIED_DONE
