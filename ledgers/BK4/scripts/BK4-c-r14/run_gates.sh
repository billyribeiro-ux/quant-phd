#!/bin/bash
# Round-14 BK4-c mechanical gates on the verifier pin (8e5751c).
set -u
cd /Users/billyribeiro/.fanout/wt/verifyE14-BK4-c
O=ledgers/BK4/scripts/BK4-c-r14/out
P=.venv/bin/python
$P tools/check_projects.py --unit BK4 > $O/check_projects.txt 2>&1; echo "exit=$?" >> $O/check_projects.txt
$P tools/check_pages.py --unit BK4 > $O/check_pages.txt 2>&1; echo "exit=$?" >> $O/check_pages.txt
$P tools/check_dag.py --unit BK4 > $O/check_dag.txt 2>&1; echo "exit=$?" >> $O/check_dag.txt
$P tools/run_labs.py --unit BK4 > $O/run_labs.txt 2>&1; echo "exit=$?" >> $O/run_labs.txt
$P tools/run_graders.py --unit BK4 --seeds 0-49 > $O/run_graders_0-49.txt 2>&1; echo "exit=$?" >> $O/run_graders_0-49.txt
$P tools/mutate_graders.py --unit BK4 > $O/mutate_graders.txt 2>&1; echo "exit=$?" >> $O/mutate_graders.txt
$P -m ruff check course/modules/BK/BK4/grader tests/labs/BK4 > $O/ruff_check.txt 2>&1; echo "exit=$?" >> $O/ruff_check.txt
$P -m ruff format --check course/modules/BK/BK4/grader tests/labs/BK4 > $O/ruff_format.txt 2>&1; echo "exit=$?" >> $O/ruff_format.txt
$P -m mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader > $O/mypy_unit.txt 2>&1; echo "exit=$?" >> $O/mypy_unit.txt
$P -m mypy --no-incremental > $O/mypy_repo.txt 2>&1; echo "exit=$?" >> $O/mypy_repo.txt
$P -m pytest --collect-only -q course/modules/BK/BK4/grader/test_project.py > $O/collect.txt 2>&1; echo "exit=$?" >> $O/collect.txt
$P tools/verify_refs.py --unit BK4 --offline > $O/verify_refs_offline.txt 2>&1; echo "exit=$?" >> $O/verify_refs_offline.txt
$P tools/page_smoke.py --unit BK4 --pages project.html > $O/page_smoke_project.txt 2>&1; echo "exit=$?" >> $O/page_smoke_project.txt
echo done > $O/DONE
