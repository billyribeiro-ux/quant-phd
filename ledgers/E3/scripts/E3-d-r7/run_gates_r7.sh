#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyC7-E3-d
S=ledgers/E3/scripts/E3-d-r7
P=.venv/bin/python
$P tools/check_projects.py --all > $S/check_projects.out 2>&1; echo "rc=$?" >> $S/check_projects.out
$P tools/check_pages.py --all > $S/check_pages.out 2>&1; echo "rc=$?" >> $S/check_pages.out
$P tools/check_dag.py --all > $S/check_dag.out 2>&1; echo "rc=$?" >> $S/check_dag.out
$P tools/run_labs.py --unit E3 --page project > $S/run_labs_project.out 2>&1; echo "rc=$?" >> $S/run_labs_project.out
for i in 1 2 3; do (cd /tmp && /Users/billyribeiro/.fanout/wt/verifyC7-E3-d/$P -I -W error /Users/billyribeiro/.fanout/wt/verifyC7-E3-d/tests/labs/E3/lab-E3-project-$i.py > $S/twin_project_$i.out 2>$S/twin_project_$i.err; echo "rc=$?" >> $S/twin_project_$i.out); done
$P tools/page_smoke.py --unit E3 --pages project > $S/page_smoke.out 2>&1; echo "rc=$?" >> $S/page_smoke.out
$P tools/run_graders.py --unit E3 --seeds 0-49 > $S/run_graders_0_49.out 2>&1; echo "rc=$?" >> $S/run_graders_0_49.out
$P tools/mutate_graders.py --unit E3 --seeds 0-9 > $S/mutate_E3_0_9.out 2>&1; echo "rc=$?" >> $S/mutate_E3_0_9.out
$P ledgers/E3/scripts/run_alternatives.py > $S/alternatives.out 2>&1; echo "rc=$?" >> $S/alternatives.out
$P -m pytest --collect-only -q course/modules/E/E3/grader/test_project.py > $S/collect_only.out 2>&1; echo "rc=$?" >> $S/collect_only.out
.venv/bin/ruff check course/modules/E/E3/grader tests/labs/E3/lab-E3-project-*.py > $S/ruff_check.out 2>&1; echo "rc=$?" >> $S/ruff_check.out
.venv/bin/ruff format --check course/modules/E/E3/grader tests/labs/E3/lab-E3-project-*.py > $S/ruff_format.out 2>&1; echo "rc=$?" >> $S/ruff_format.out
.venv/bin/mypy --no-incremental tests/labs/E3/lab-E3-project-1.py tests/labs/E3/lab-E3-project-2.py tests/labs/E3/lab-E3-project-3.py > $S/mypy.out 2>&1; echo "rc=$?" >> $S/mypy.out
$P tools/verify_refs.py --offline > $S/verify_refs.out 2>&1; echo "rc=$?" >> $S/verify_refs.out
echo DONE > $S/done.flag
