#!/bin/sh
# Round 7 CS2 slice a: gate commands run from the checkout root (pin 7aa909e).
set -u
P=.venv/bin/python
for f in tests/labs/CS2/lab-CS2-L01-1.py tests/labs/CS2/lab-CS2-L02-1.py tests/labs/CS2/lab-CS2-L03-1.py tests/labs/CS2/lab-CS2-L04-1.py; do
  $P -I -W error "$f" >/dev/null; echo "twin $f exit $?"; done
$P tools/check_pages.py --unit CS2; echo "check_pages $?"
$P tools/check_dag.py --unit CS2; echo "check_dag $?"
$P tools/check_projects.py --unit CS2; echo "check_projects $?"
for p in L01 L02 L03 L04 index.html; do $P tools/run_labs.py --unit CS2 --page $p; echo "run_labs $p $?"; done
$P tools/page_smoke.py --unit CS2 --pages index.html L01.html L02.html L03.html L04.html; echo "page_smoke $?"
.venv/bin/ruff check tests/labs/CS2/lab-CS2-L0[1-4]-1.py && .venv/bin/ruff format --check tests/labs/CS2/lab-CS2-L0[1-4]-1.py
.venv/bin/mypy --no-incremental tests/labs/CS2/lab-CS2-L01-1.py tests/labs/CS2/lab-CS2-L02-1.py tests/labs/CS2/lab-CS2-L03-1.py tests/labs/CS2/lab-CS2-L04-1.py
.venv/bin/pytest -q -k CS2
