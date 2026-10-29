#!/bin/bash
# Round-22 command rows for M1 slice b. Run from the checkout root.
C=/tmp/verify22-M1-b
O=$C/ledgers/M1/scripts/M1-b-r22/out
P=$C/.venv/bin/python
cd $C
git rev-parse HEAD > $O/pin.txt
git diff --stat f95243f d160ac3 -- course/modules/M/M1 tests/labs/M1 tools references >> $O/pin.txt
$P tools/run_labs.py --unit M1 > $O/run_labs.txt 2>&1; echo "exit $?" >> $O/run_labs.txt
for t in L04 L05; do
  (cd /tmp && $C/.venv/bin/python -I -W error $C/tests/labs/M1/lab-M1-$t-1.py > $O/twin_$t.out 2> $O/twin_$t.err; echo "exit $?" >> $O/twin_$t.out)
done
$P tools/page_smoke.py --unit M1 --pages L04 L05 > $O/page_smoke.txt 2>&1; echo "exit $?" >> $O/page_smoke.txt
$P tools/check_pages.py --unit M1 > $O/check_pages.txt 2>&1; echo "exit $?" >> $O/check_pages.txt
$P tools/check_dag.py --unit M1 > $O/check_dag.txt 2>&1; echo "exit $?" >> $O/check_dag.txt
$P -m ruff check tests/labs/M1/lab-M1-L04-1.py tests/labs/M1/lab-M1-L05-1.py > $O/ruff_check.txt 2>&1; echo "exit $?" >> $O/ruff_check.txt
$P -m ruff format --check tests/labs/M1/lab-M1-L04-1.py tests/labs/M1/lab-M1-L05-1.py > $O/ruff_format.txt 2>&1; echo "exit $?" >> $O/ruff_format.txt
$P -m mypy --no-incremental tests/labs/M1/lab-M1-L04-1.py tests/labs/M1/lab-M1-L05-1.py > $O/mypy.txt 2>&1; echo "exit $?" >> $O/mypy.txt
$P tools/verify_refs.py --offline > $O/vr_offline.txt 2>&1; echo "exit $?" >> $O/vr_offline.txt
$P tools/verify_refs.py --unit M1 > $O/vr_live.txt 2>&1; echo "exit $?" >> $O/vr_live.txt
$P -m pytest -q tests/test_run_labs.py tests/test_page_checks.py tests/test_labs.py > $O/pytest.txt 2>&1; echo "exit $?" >> $O/pytest.txt
