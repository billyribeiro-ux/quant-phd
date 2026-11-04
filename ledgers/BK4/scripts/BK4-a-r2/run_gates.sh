#!/bin/bash
# BK4-a round-2 verifier: the commands run on the pin 67c4768 (repo root = this checkout).
# Outputs are archived under ledgers/BK4/scripts/BK4-a-r2/out/.
set -u
cd "$(dirname "$0")/../../../.." || exit 1
P=.venv/bin/python
$P tools/check_pages.py --unit BK4; echo "exit $?"
for pg in L01 L02 L03; do $P tools/check_pages.py --unit BK4 --page $pg; echo "exit $?"; done
$P tools/check_dag.py --unit BK4; echo "exit $?"
$P tools/check_projects.py --unit BK4; echo "exit $?"
$P tools/run_labs.py --unit BK4; echo "exit $?"
for t in L01 L02 L03; do python3 -I -W error tests/labs/BK4/lab-BK4-$t-1.py >/dev/null; echo "twin $t exit $?"; done
.venv/bin/ruff check tests/labs/BK4/lab-BK4-L01-1.py tests/labs/BK4/lab-BK4-L02-1.py tests/labs/BK4/lab-BK4-L03-1.py
.venv/bin/ruff format --check tests/labs/BK4/lab-BK4-L01-1.py tests/labs/BK4/lab-BK4-L02-1.py tests/labs/BK4/lab-BK4-L03-1.py
.venv/bin/mypy --no-incremental tests/labs/BK4/lab-BK4-L01-1.py tests/labs/BK4/lab-BK4-L02-1.py tests/labs/BK4/lab-BK4-L03-1.py
.venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py
$P tools/verify_refs.py --unit BK4; echo "exit $?"
$P tools/page_smoke.py --unit BK4 --pages index L01 L02 L03
$P ledgers/BK4/scripts/BK4-a-r2/rederive_slice_a.py
$P ledgers/BK4/scripts/BK4-a-r2/banned_process_scan.py
$P ledgers/BK4/scripts/BK4-a-r2/link_check.py
