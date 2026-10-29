#!/bin/bash
# Round-21 command rows for slice AC1-b (L04, L05, L06 and twins). Run from the checkout root.
set -u
P=.venv/bin/python
O=ledgers/AC1/scripts/AC1-b-r21/out
echo "pin: $(git rev-parse --short HEAD) $(git status --short | grep -v '^?? .venv' | wc -l) modified" > $O/pin.txt
$P tools/check_pages.py --unit AC1 > $O/check_pages.txt 2>&1; echo "exit $?" >> $O/check_pages.txt
$P tools/check_dag.py --unit AC1 > $O/check_dag.txt 2>&1; echo "exit $?" >> $O/check_dag.txt
$P tools/check_projects.py --unit AC1 > $O/check_projects.txt 2>&1; echo "exit $?" >> $O/check_projects.txt
for p in L04 L05 L06; do
  $P tools/run_labs.py --unit AC1 --page $p > $O/run_labs_$p.txt 2>&1; echo "exit $?" >> $O/run_labs_$p.txt
done
for l in L04 L05 L06; do
  $P -I -W error tests/labs/AC1/lab-AC1-$l-1.py > $O/twin_$l.txt 2>&1; echo "exit $?" >> $O/twin_$l.txt
done
$P tools/page_smoke.py --unit AC1 --pages L04 L05 L06 > $O/page_smoke.txt 2>&1; echo "exit $?" >> $O/page_smoke.txt
$P -m ruff check tests/labs/AC1 > $O/ruff_check.txt 2>&1; echo "exit $?" >> $O/ruff_check.txt
$P -m ruff format --check tests/labs/AC1 > $O/ruff_format.txt 2>&1; echo "exit $?" >> $O/ruff_format.txt
$P -m mypy --no-incremental tests/labs/AC1 > $O/mypy.txt 2>&1; echo "exit $?" >> $O/mypy.txt
$P -m pytest -q -k 'AC1 or lab' > $O/pytest.txt 2>&1; echo "exit $?" >> $O/pytest.txt
$P -m pytest --collect-only -q -k 'AC1 or lab' > $O/collect.txt 2>&1; echo "exit $?" >> $O/collect.txt
$P tools/verify_refs.py --offline > $O/verify_refs_offline.txt 2>&1; echo "exit $?" >> $O/verify_refs_offline.txt
$P tools/verify_refs.py --unit AC1 > $O/verify_refs_live.txt 2>&1; echo "exit $?" >> $O/verify_refs_live.txt
