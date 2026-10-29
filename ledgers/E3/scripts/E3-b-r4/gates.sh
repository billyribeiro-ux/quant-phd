#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyC4-E3-b
P=.venv/bin/python
O=ledgers/E3/scripts/E3-b-r4
for L in L04 L05 L06; do $P tools/check_pages.py --unit E3 --page $L > $O/check_pages_$L.out 2>&1; echo "exit $?" >> $O/check_pages_$L.out; done
$P tools/check_dag.py --unit E3 > $O/check_dag.out 2>&1; echo "exit $?" >> $O/check_dag.out
$P tools/run_labs.py --unit E3 > $O/run_labs_E3.out 2>&1; echo "exit $?" >> $O/run_labs_E3.out
$P tools/build_site.py --check > $O/build_site.out 2>&1; echo "exit $?" >> $O/build_site.out
$P tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1; echo "exit $?" >> $O/verify_refs_offline.out
$P tools/page_smoke.py --unit E3 --pages L04 L05 L06 > $O/page_smoke_L04-L06.out 2>&1; echo "exit $?" >> $O/page_smoke_L04-L06.out
for L in 04 05 06; do $P -I -W error tests/labs/E3/lab-E3-L$L-1.py > $O/twin_L$L.out 2>&1; echo "exit $?" >> $O/twin_L$L.out; done
.venv/bin/ruff check . > $O/ruff_check.out 2>&1; echo "exit $?" >> $O/ruff_check.out
.venv/bin/ruff format --check . > $O/ruff_format.out 2>&1; echo "exit $?" >> $O/ruff_format.out
.venv/bin/mypy --no-incremental > $O/mypy.out 2>&1; echo "exit $?" >> $O/mypy.out
.venv/bin/pytest tests/test_labs.py tests/test_page_checks.py -q -k 'E3 or lab' > $O/pytest_labs.out 2>&1; echo "exit $?" >> $O/pytest_labs.out
echo done
