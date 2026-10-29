#!/bin/sh
# Command rows for E3 slice a (hub index.html, L01-L03 and twins), run from the verifier checkout root.
set -u
P=.venv/bin/python
$P tools/check_pages.py --unit E3
$P tools/check_dag.py --all | grep E3
$P tools/run_labs.py --unit E3 --page L01
$P tools/run_labs.py --unit E3 --page L02
$P tools/run_labs.py --unit E3 --page L03
for f in 01 02 03; do $P -I -W error tests/labs/E3/lab-E3-L$f-1.py >/dev/null; echo "twin L$f exit $?"; done
.venv/bin/ruff check tests/labs/E3 && .venv/bin/ruff format --check tests/labs/E3
.venv/bin/mypy --no-incremental tests/labs/E3/lab-E3-L01-1.py tests/labs/E3/lab-E3-L02-1.py tests/labs/E3/lab-E3-L03-1.py
$P -m pytest tests/test_labs.py -k E3 -q
$P tools/verify_refs.py --offline
