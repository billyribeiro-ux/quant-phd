#!/bin/bash
cd /tmp/verify36-AC4-e
O=ledgers/AC4/scripts/AC4-e-r36/out
.venv/bin/python tools/check_pages.py --all > $O/check_pages.out 2>&1; echo "exit $?" >> $O/check_pages.out
.venv/bin/python tools/check_dag.py --all > $O/check_dag.out 2>&1; echo "exit $?" >> $O/check_dag.out
.venv/bin/python tools/check_projects.py --all > $O/check_projects.out 2>&1; echo "exit $?" >> $O/check_projects.out
.venv/bin/python tools/run_labs.py --unit AC4 > $O/run_labs.out 2>&1; echo "exit $?" >> $O/run_labs.out
.venv/bin/python tools/page_smoke.py --unit AC4 --pages project.html > $O/page_smoke_project.out 2>&1; echo "exit $?" >> $O/page_smoke_project.out
.venv/bin/ruff check . > $O/ruff_check.out 2>&1; echo "exit $?" >> $O/ruff_check.out
.venv/bin/ruff format --check . > $O/ruff_format.out 2>&1; echo "exit $?" >> $O/ruff_format.out
.venv/bin/mypy --no-incremental > $O/mypy.out 2>&1; echo "exit $?" >> $O/mypy.out
.venv/bin/python -m pytest --collect-only -q course/modules/AC/AC4 tests/labs/AC4 > $O/collect_ac4.out 2>&1; echo "exit $?" >> $O/collect_ac4.out
.venv/bin/python tools/verify_refs.py --unit AC4 > $O/verify_refs_live_AC4.out 2>&1; echo "exit $?" >> $O/verify_refs_live_AC4.out
.venv/bin/python tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1; echo "exit $?" >> $O/verify_refs_offline.out
.venv/bin/python -I -W error tests/labs/AC4/lab-AC4-project-1.py > $O/twin_project1.out 2>&1; echo "exit $?" >> $O/twin_project1.out
.venv/bin/python -I -W error tests/labs/AC4/lab-AC4-project-2.py > $O/twin_project2.out 2>&1; echo "exit $?" >> $O/twin_project2.out
.venv/bin/python tools/run_graders.py --unit AC4 --seeds 0-49 > $O/run_graders.out 2>&1; echo "exit $?" >> $O/run_graders.out
.venv/bin/python tools/mutate_graders.py --unit AC4 --seeds 0-49 > $O/mutate_ac4.out 2>&1; echo "exit $?" >> $O/mutate_ac4.out
echo done > $O/ALLDONE
