#!/bin/sh
# Commands run by the round-34 verifier for slice AC4-b (L03, L04 and twins) in the pinned checkout.
# Outputs were written to /tmp/AC4-v/AC4-b/r34/. Run from the checkout root.
set -u
P=.venv/bin/python
git rev-parse HEAD
git diff --stat 5aeaaf0 455dd92 -- course/modules/AC/AC4 tests/labs/AC4
$P tools/check_pages.py --unit AC4 --page L03
$P tools/check_pages.py --unit AC4 --page L04
$P tools/check_dag.py --all
$P tools/run_labs.py --unit AC4 --page L03
$P tools/run_labs.py --unit AC4 --page L04
$P -I -W error tests/labs/AC4/lab-AC4-L03-1.py
$P -I -W error tests/labs/AC4/lab-AC4-L04-1.py
$P -I ledgers/AC4/scripts/AC4-b-r34/extract_expected.py course/modules/AC/AC4/L03.html /tmp/AC4-v/AC4-b/r34/expected_L03.txt
$P -I ledgers/AC4/scripts/AC4-b-r34/extract_expected.py course/modules/AC/AC4/L04.html /tmp/AC4-v/AC4-b/r34/expected_L04.txt
$P -m ruff check tests/labs/AC4/lab-AC4-L03-1.py tests/labs/AC4/lab-AC4-L04-1.py
$P -m ruff format --check tests/labs/AC4/lab-AC4-L03-1.py tests/labs/AC4/lab-AC4-L04-1.py
$P -m mypy --no-incremental tests/labs/AC4/lab-AC4-L03-1.py tests/labs/AC4/lab-AC4-L04-1.py
$P -m pytest tests/test_labs.py -k 'AC4 and (L03 or L04)' -q
$P tools/page_smoke.py --unit AC4 --pages L03 L04 --skip-sweep
$P tools/verify_refs.py --offline
$P tools/verify_refs.py --unit AC4
$P -I ledgers/AC4/scripts/AC4-b-r34/run_mutants.py /tmp/AC4-v/AC4-b/r34/expected_L03.txt ledgers/AC4/mutants/AC4-b-r30/m_L03_*.py ledgers/AC4/mutants/AC4-b-r32/m_L03_*.py ledgers/AC4/mutants/AC4-b-r34/m_L03_*.py
$P -I ledgers/AC4/scripts/AC4-b-r34/run_mutants.py /tmp/AC4-v/AC4-b/r34/expected_L04.txt ledgers/AC4/mutants/AC4-b-r30/m_L04_*.py ledgers/AC4/mutants/AC4-b-r32/m_L04_*.py ledgers/AC4/mutants/AC4-b-r34/m_L04_*.py
$P ledgers/AC4/scripts/AC4-b-r34/make_r34_mutants.py /tmp/verify34-AC4-b
