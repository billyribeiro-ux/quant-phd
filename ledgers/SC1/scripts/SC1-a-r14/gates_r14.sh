#!/bin/bash
# Round-14 gate run for SC1-a at pin 8e5751c. Run from the checkout root (absolute path).
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyE14-SC1-a
cd "$ROOT" || exit 1
O=ledgers/SC1/scripts/SC1-a-r14/out
PY=.venv/bin/python
rm -f $O/rc.txt
$PY tools/check_pages.py --unit SC1 > $O/check_pages_SC1.out 2>&1; echo "check_pages rc=$?" >> $O/rc.txt
$PY tools/check_dag.py --all > $O/check_dag_all.out 2>&1; echo "check_dag --all rc=$?" >> $O/rc.txt
$PY tools/check_projects.py --unit SC1 > $O/check_projects_SC1.out 2>&1; echo "check_projects rc=$?" >> $O/rc.txt
$PY tools/run_labs.py --unit SC1 > $O/run_labs_SC1.out 2>&1; echo "run_labs rc=$?" >> $O/rc.txt
for p in index L01 L02 L03; do
  $PY tools/page_smoke.py --unit SC1 --pages $p > $O/page_smoke_$p.out 2>&1; echo "page_smoke $p rc=$?" >> $O/rc.txt
done
$PY -m ruff check . > $O/ruff_check.out 2>&1; echo "ruff check rc=$?" >> $O/rc.txt
$PY -m ruff format --check . > $O/ruff_format.out 2>&1; echo "ruff format rc=$?" >> $O/rc.txt
$PY tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1; echo "verify_refs offline rc=$?" >> $O/rc.txt
$PY tools/verify_refs.py --unit SC1 > $O/verify_refs_unit_SC1.out 2>&1; echo "verify_refs unit SC1 rc=$?" >> $O/rc.txt
$PY tools/fetch_data.py --check > $O/fetch_data_check.out 2>&1; echo "fetch_data check rc=$?" >> $O/rc.txt
$PY -m pytest -q -p no:cacheprovider -k SC1 tests > $O/pytest_SC1.out 2>&1; echo "pytest -k SC1 rc=$?" >> $O/rc.txt
$PY -m pytest --collect-only -q -p no:cacheprovider -k SC1 tests > $O/pytest_SC1_collect.out 2>&1; echo "pytest collect rc=$?" >> $O/rc.txt
$PY -m mypy --no-incremental > $O/mypy_full.out 2>&1; echo "mypy full rc=$?" >> $O/rc.txt
echo done >> $O/rc.txt
