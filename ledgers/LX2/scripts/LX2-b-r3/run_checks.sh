#!/bin/sh
# LX2-b round 3 command rows, run from the verifier checkout (pin 67a2d13e). Outputs written beside this script.
cd "$(dirname "$0")/../../../.." || exit 1
D=ledgers/LX2/scripts/LX2-b-r3
.venv/bin/python tools/check_pages.py --unit LX2 > $D/check_pages.out 2>&1; echo "check_pages rc=$?" >> $D/check_pages.out
.venv/bin/python tools/check_dag.py --unit LX2 > $D/check_dag.out 2>&1; echo "check_dag rc=$?" >> $D/check_dag.out
.venv/bin/python tools/check_projects.py --unit LX2 > $D/check_projects.out 2>&1; echo "check_projects rc=$?" >> $D/check_projects.out
.venv/bin/python tools/run_labs.py --unit LX2 > $D/run_labs.out 2>&1; echo "run_labs rc=$?" >> $D/run_labs.out
.venv/bin/python -m ruff check tests/labs/LX2 > $D/ruff_check.out 2>&1; echo "rc=$?" >> $D/ruff_check.out
.venv/bin/python -m ruff format --check tests/labs/LX2 > $D/ruff_format.out 2>&1; echo "rc=$?" >> $D/ruff_format.out
.venv/bin/python -m mypy --no-incremental tests/labs/LX2 > $D/mypy.out 2>&1; echo "rc=$?" >> $D/mypy.out
.venv/bin/python -m pytest tests/test_labs.py -k 'LX2-L03 or LX2-L04' -q > $D/pytest_labs.out 2>&1; echo "rc=$?" >> $D/pytest_labs.out
.venv/bin/python tools/verify_refs.py --unit LX2 > $D/verify_refs.out 2>&1; echo "rc=$?" >> $D/verify_refs.out
.venv/bin/python tools/page_smoke.py --unit LX2 --pages L03 L04 > $D/page_smoke_L03_L04.out 2>&1; echo "rc=$?" >> $D/page_smoke_L03_L04.out
