#!/bin/bash
# Round-5 command record for M2 slice b (pin dde0486b). Every command below was run in the verifier checkout.
# Outputs are kept next to this file in ledgers/M2/scripts/M2-b-r5/.
cd /Users/billyribeiro/.fanout/wt/verifyS5-M2-b || exit 1
S=ledgers/M2/scripts/M2-b-r5
PY=.venv/bin/python
$S/run_gates_r5.sh                                   # g01-g04, g04b-d, g07, g07b, g08, g10
for n in L07 L08 L09 L10 L11 L12; do                 # g05: twins alone under python -I -W error, from a scratch dir
  (cd /tmp/m2b-r5-iso && /Users/billyribeiro/.fanout/wt/verifyS5-M2-b/.venv/bin/python -I -W error \
     /Users/billyribeiro/.fanout/wt/verifyS5-M2-b/tests/labs/M2/lab-M2-$n-1.py > $S/twin_$n.stdout 2> $S/twin_$n.stderr; echo "$n exit=$?")
done
$PY tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12 > $S/g06_page_smoke_L07_L12.out 2>&1; echo "exit=$?" >> $S/g06_page_smoke_L07_L12.out
$PY -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_refs.py -k 'M2 or lab or page' -q > $S/g09_pytest_labs_pagechecks.out 2>&1; echo "exit=$?" >> $S/g09_pytest_labs_pagechecks.out
$PY tools/verify_refs.py --unit M2 > $S/g15_verify_refs_live_M2.out 2>&1; echo "exit=$?" >> $S/g15_verify_refs_live_M2.out
$PY $S/cards_r5_checks.py > $S/cards_r5_checks.out
$PY -I $S/numbers_r5.py > $S/numbers_r5.out
$PY -I $S/c126_check_r5.py > $S/c126_check_r5.out
$S/carry_identity_r5.sh > $S/carry_identity_r5.out
