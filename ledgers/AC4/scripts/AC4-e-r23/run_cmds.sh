#!/bin/bash
cd /tmp/verify23-AC4-e
O=ledgers/AC4/scripts/AC4-e-r23/out
.venv/bin/python tools/check_pages.py --all > $O/check_pages.out 2>&1; echo "exit $?" >> $O/check_pages.out
.venv/bin/python tools/check_dag.py --all > $O/check_dag.out 2>&1; echo "exit $?" >> $O/check_dag.out
.venv/bin/python tools/check_projects.py --all > $O/check_projects.out 2>&1; echo "exit $?" >> $O/check_projects.out
.venv/bin/python tools/run_labs.py --unit AC4 > $O/run_labs.out 2>&1; echo "exit $?" >> $O/run_labs.out
.venv/bin/python tools/run_graders.py --unit AC4 --seeds 0-49 > $O/run_graders.out 2>&1; echo "exit $?" >> $O/run_graders.out
.venv/bin/python tools/page_smoke.py --unit AC4 > $O/page_smoke.out 2>&1; echo "exit $?" >> $O/page_smoke.out
.venv/bin/python tools/build_site.py --check > $O/build_site_check.out 2>&1; echo "exit $?" >> $O/build_site_check.out
.venv/bin/ruff check . > $O/ruff_check.out 2>&1; echo "exit $?" >> $O/ruff_check.out
.venv/bin/mypy --no-incremental > $O/mypy.out 2>&1; echo "exit $?" >> $O/mypy.out
.venv/bin/python -m pytest --collect-only -q tests/ -k "AC4 or ac4 or project" > $O/collect_ac4.out 2>&1; echo "exit $?" >> $O/collect_ac4.out
echo done > $O/ALLDONE
