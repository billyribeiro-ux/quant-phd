#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyC7-E3-d
S=ledgers/E3/scripts/E3-d-r7
.venv/bin/python tools/mutate_graders.py --unit E3 --seeds 0-9 > $S/mutate_E3_0_9_r7.out 2>&1; echo "rc=$?" >> $S/mutate_E3_0_9_r7.out
.venv/bin/python ledgers/E3/scripts/run_alternatives.py --seeds 0-49 > $S/alternatives_0_49.out 2>&1; echo "rc=$?" >> $S/alternatives_0_49.out
for i in 1 2 3; do (cd /tmp && /Users/billyribeiro/.fanout/wt/verifyC7-E3-d/.venv/bin/python -I -W error /Users/billyribeiro/.fanout/wt/verifyC7-E3-d/tests/labs/E3/lab-E3-project-$i.py > /Users/billyribeiro/.fanout/wt/verifyC7-E3-d/$S/twin_project_$i.out 2>/Users/billyribeiro/.fanout/wt/verifyC7-E3-d/$S/twin_project_$i.err; echo "rc=$?" >> /Users/billyribeiro/.fanout/wt/verifyC7-E3-d/$S/twin_project_$i.out); done
.venv/bin/python -m pytest -q -p no:cacheprovider --collect-only course/modules/E/E3/grader/test_project.py > $S/collect_only_r7.out 2>&1; echo "rc=$?" >> $S/collect_only_r7.out
echo DONE > $S/done2.flag
