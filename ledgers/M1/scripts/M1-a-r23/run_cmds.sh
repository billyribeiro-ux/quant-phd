#!/bin/bash
# Round 23 M1-a command rows; run from the checkout root; outputs to /tmp/M1-v/M1-a/r23
cd /tmp/verify23-M1-a || exit 1
O=/tmp/M1-v/M1-a/r23
PY=.venv/bin/python
$PY tools/check_pages.py --all > $O/check_pages.txt 2>&1; echo "check_pages rc=$?" >> $O/rc.txt
$PY tools/check_dag.py --all > $O/check_dag.txt 2>&1; echo "check_dag rc=$?" >> $O/rc.txt
$PY tools/check_projects.py --all > $O/check_projects.txt 2>&1; echo "check_projects rc=$?" >> $O/rc.txt
$PY tools/run_labs.py --unit M1 > $O/run_labs.txt 2>&1; echo "run_labs rc=$?" >> $O/rc.txt
for L in L01 L02 L03; do
  $PY -I -W error tests/labs/M1/lab-M1-$L-1.py > $O/twin_$L.stdout 2> $O/twin_$L.err; echo "twin $L rc=$?" >> $O/rc.txt
done
$PY tools/page_smoke.py --unit M1 --pages index.html L01.html L02.html L03.html > $O/page_smoke.txt 2>&1; echo "page_smoke rc=$?" >> $O/rc.txt
$PY -m ruff check . > $O/ruff_check.txt 2>&1; echo "ruff check rc=$?" >> $O/rc.txt
$PY -m ruff format --check . > $O/ruff_format.txt 2>&1; echo "ruff format rc=$?" >> $O/rc.txt
$PY -m mypy --no-incremental > $O/mypy.txt 2>&1; echo "mypy rc=$?" >> $O/rc.txt
$PY tools/verify_refs.py --offline > $O/vr_offline.txt 2>&1; echo "verify_refs offline rc=$?" >> $O/rc.txt
$PY tools/verify_refs.py --unit M1 > $O/vr_live_M1.txt 2>&1; echo "verify_refs live M1 rc=$?" >> $O/rc.txt
$PY -m pytest tests/test_labs.py tests/test_run_labs.py -q > $O/pytest.txt 2>&1; echo "pytest rc=$?" >> $O/rc.txt
