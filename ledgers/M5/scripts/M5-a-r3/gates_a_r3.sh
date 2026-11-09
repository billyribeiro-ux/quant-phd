#!/bin/sh
# Record of the commands run for M5 slice a, round 3 (pin 8196077d). Run from the checkout root.
# Each output file is in this directory. Scripts that back rows: cards_dump.py, recompute_a_r3.py.
set -u
O=ledgers/M5/scripts/M5-a-r3
PY=.venv/bin/python
$PY tools/check_pages.py --unit M5 > $O/check_pages_M5.out 2>&1; echo "exit $?" >> $O/check_pages_M5.out
$PY tools/check_dag.py --unit M5 > $O/check_dag_M5.out 2>&1; echo "exit $?" >> $O/check_dag_M5.out
$PY tools/check_projects.py --unit M5 > $O/check_projects_M5.out 2>&1; echo "exit $?" >> $O/check_projects_M5.out
$PY tools/run_labs.py --unit M5 --page index > $O/run_labs_M5_index.out 2>&1
for p in L01 L02 L03 L04; do $PY tools/run_labs.py --unit M5 --page $p > $O/run_labs_M5_$p.out 2>&1; done
for i in 1 2 3 4; do
  d=$(mktemp -d /tmp/m5a_r3_scratch/L0$i.XXXX); cp tests/labs/M5/lab-M5-L0$i-1.py "$d/"
  (cd "$d" && "$OLDPWD/$PY" -I -W error lab-M5-L0$i-1.py > "$OLDPWD/$O/twin_L0$i.out" 2> "$OLDPWD/$O/twin_L0$i.err")
done
ruff check . > $O/ruff_check.out 2>&1; ruff format --check . > $O/ruff_format.out 2>&1
$PY -m mypy --no-incremental > $O/mypy.out 2>&1
$PY tools/verify_refs.py --offline > $O/verify_refs_offline_all.out 2>&1
$PY tools/verify_refs.py --unit M5 > $O/verify_refs_M5_live.out 2>&1
$PY -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q > $O/pytest_M5_relevant.out 2>&1
$PY tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04 > $O/page_smoke_M5_a.out 2>&1
$PY tools/build_site.py --check > $O/build_site_check.out 2>&1
$PY $O/cards_dump.py course/modules/M/M5/cards.json L01,L02,L03,L04 > $O/cards_L01-L04_dump.out
$PY -I $O/recompute_a_r3.py > $O/recompute_a_r3.out 2>&1
