#!/bin/sh
# Verifier gate commands, M3 slice a, round 1 (closing delta, pin 95f3f8cb). Run from the checkout root.
O=ledgers/M3/scripts/M3-a-r1/out
mkdir -p $O
.venv/bin/python tools/check_pages.py --unit M3 > $O/check_pages_M3.out 2>&1; echo "exit $?" >> $O/check_pages_M3.out
.venv/bin/python tools/check_dag.py --unit M3 > $O/check_dag_M3.out 2>&1; echo "exit $?" >> $O/check_dag_M3.out
.venv/bin/python tools/check_projects.py --unit M3 > $O/check_projects_M3.out 2>&1; echo "exit $?" >> $O/check_projects_M3.out
.venv/bin/python tools/run_labs.py --unit M3 > $O/run_labs_M3.out 2>&1; echo "exit $?" >> $O/run_labs_M3.out
.venv/bin/python tools/page_smoke.py --unit M3 --pages index L01 L02 L03 > $O/page_smoke_slice_a.out 2>&1; echo "exit $?" >> $O/page_smoke_slice_a.out
.venv/bin/python tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1; echo "exit $?" >> $O/verify_refs_offline.out
.venv/bin/python tools/build_site.py --check > $O/build_site_check.out 2>&1; echo "exit $?" >> $O/build_site_check.out
.venv/bin/ruff check . > $O/ruff_check.out 2>&1; echo "exit $?" >> $O/ruff_check.out
.venv/bin/ruff format --check . > $O/ruff_format.out 2>&1; echo "exit $?" >> $O/ruff_format.out
.venv/bin/mypy --no-incremental > $O/mypy.out 2>&1; echo "exit $?" >> $O/mypy.out
.venv/bin/python -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q > $O/pytest_relevant.out 2>&1; echo "exit $?" >> $O/pytest_relevant.out
