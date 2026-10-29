#!/bin/sh
# Commands run by the round-1 verifier for M5 slice a (hub, L01-L04 and twins). Run from the checkout root.
set -u
PY=.venv/bin/python
$PY tools/check_pages.py --all            # M5: PASS (AC1 L08 'why it matters' 130 words is outside this slice)
$PY tools/check_dag.py --all              # M5: PASS
$PY tools/run_labs.py --unit M5           # run_labs M5: PASS (13/13)
$PY tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04   # page_smoke M5: PASS
for f in lab-M5-L01-1 lab-M5-L02-1 lab-M5-L03-1 lab-M5-L04-1; do
  $PY -I -W error tests/labs/M5/$f.py    # exit 0 each
done
.venv/bin/ruff check tests/labs/M5/lab-M5-L0[1-4]-1.py
.venv/bin/ruff format --check tests/labs/M5/lab-M5-L0[1-4]-1.py
.venv/bin/mypy tests/labs/M5/lab-M5-L0[1-4]-1.py
$PY tools/verify_refs.py --offline        # offline integrity: 560 entries, 0 problems
$PY tools/verify_refs.py --unit M5        # live re-verification of M5: 2 of 560 entries, 0 problems
$PY -I ledgers/M5/scripts/M5-a-r1/recompute_a.py   # 37 of 37 PASS
