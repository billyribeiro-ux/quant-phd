#!/bin/sh
# E3 slice b (L04-L06) verifier round 2: commands behind the ledger rows. Run from the checkout root.
set -e
PY=.venv/bin/python
$PY tools/run_labs.py --unit E3 --page L04
$PY tools/run_labs.py --unit E3 --page L05
$PY tools/run_labs.py --unit E3 --page L06
for L in L04 L05 L06; do
  $PY -I -W error tests/labs/E3/lab-E3-$L-1.py > /tmp/E3-b-$L.run.txt
  /usr/bin/python3 -I ledgers/E3/scripts/E3-b-r2/cmp_outputs.py course/modules/E/E3/$L.html /tmp/E3-b-$L.run.txt
  /usr/bin/python3 -I ledgers/E3/scripts/E3-b-r2/cmp_code.py course/modules/E/E3/$L.html tests/labs/E3/lab-E3-$L-1.py
  /usr/bin/python3 -I ledgers/E3/scripts/E3-b-r2/totext.py course/modules/E/E3/$L.html > /tmp/E3-b-$L.txt
done
$PY tools/check_dag.py --unit E3
$PY tools/check_pages.py --unit E3
$PY tools/page_smoke.py --unit E3 --pages L04 L05 L06
.venv/bin/ruff check tests/labs/E3/lab-E3-L04-1.py tests/labs/E3/lab-E3-L05-1.py tests/labs/E3/lab-E3-L06-1.py
.venv/bin/ruff format --check tests/labs/E3/lab-E3-L04-1.py tests/labs/E3/lab-E3-L05-1.py tests/labs/E3/lab-E3-L06-1.py
.venv/bin/mypy --no-incremental tests/labs/E3/lab-E3-L04-1.py tests/labs/E3/lab-E3-L05-1.py tests/labs/E3/lab-E3-L06-1.py
$PY tools/verify_refs.py --unit E3
$PY tools/verify_refs.py --offline
$PY -I ledgers/E3/scripts/E3-b-r2/recheck_E3b.py
