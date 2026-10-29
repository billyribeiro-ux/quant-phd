#!/bin/sh
# Round 20, slice AC1-b. Run from the checkout root. Output in out/.
P=.venv/bin/python
O=ledgers/AC1/scripts/AC1-b-r20/out
git rev-parse --short HEAD > $O/pin.txt
$P tools/check_pages.py --unit AC1 > $O/check_pages.txt 2>&1; echo "rc=$?" >> $O/check_pages.txt
$P tools/check_dag.py --unit AC1 > $O/check_dag.txt 2>&1; echo "rc=$?" >> $O/check_dag.txt
$P tools/check_projects.py --unit AC1 > $O/check_projects.txt 2>&1; echo "rc=$?" >> $O/check_projects.txt
for L in L04 L05 L06; do $P tools/run_labs.py --unit AC1 --page $L > $O/run_labs_$L.txt 2>&1; echo "rc=$?" >> $O/run_labs_$L.txt; done
for L in L04 L05 L06; do $P -I -W error tests/labs/AC1/lab-AC1-$L-1.py > $O/twin_$L.txt 2>&1; echo "rc=$?" >> $O/twin_$L.txt; done
$P -I ledgers/AC1/scripts/AC1-b-r20/embed_cmp.py > $O/embed_cmp.txt 2>&1
$P -I ledgers/AC1/scripts/AC1-b-r20/expcmp.py > $O/expcmp.txt 2>&1
$P -m ruff check tests/labs/AC1 > $O/ruff_check.txt 2>&1; $P -m ruff format --check tests/labs/AC1 > $O/ruff_format.txt 2>&1
$P -m mypy --no-incremental tests/labs/AC1/lab-AC1-L04-1.py tests/labs/AC1/lab-AC1-L05-1.py tests/labs/AC1/lab-AC1-L06-1.py > $O/mypy.txt 2>&1
$P -m pytest -q -k 'AC1 or lab' -p no:cacheprovider > $O/pytest.txt 2>&1; echo "rc=$?" >> $O/pytest.txt
$P tools/verify_refs.py --offline > $O/verify_refs_offline.txt 2>&1
$P tools/verify_refs.py --unit AC1 > $O/verify_refs_live.txt 2>&1
$P tools/page_smoke.py --unit AC1 --pages L04 L05 L06 > $O/page_smoke.txt 2>&1; echo "rc=$?" >> $O/page_smoke.txt
