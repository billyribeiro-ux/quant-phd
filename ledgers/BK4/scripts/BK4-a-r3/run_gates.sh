#!/bin/bash
# BK4-a round-3 verifier: commands run on the pin 67a2d13 (repo root = this checkout).
# Outputs are archived under ledgers/BK4/scripts/BK4-a-r3/out/.
set -u
cd "$(dirname "$0")/../../../.." || exit 1
P=.venv/bin/python
O=ledgers/BK4/scripts/BK4-a-r3/out
{ $P tools/check_pages.py --unit BK4; echo "exit $?"; } > $O/check_pages_unit.txt 2>&1
for pg in L01 L02 L03; do { $P tools/check_pages.py --unit BK4 --page $pg; echo "exit $?"; } > $O/check_pages_$pg.txt 2>&1; done
{ $P tools/check_dag.py --unit BK4; echo "exit $?"; } > $O/check_dag.txt 2>&1
{ $P tools/check_projects.py --unit BK4; echo "exit $?"; } > $O/check_projects.txt 2>&1
{ $P tools/run_labs.py --unit BK4; echo "exit $?"; } > $O/run_labs.txt 2>&1
for t in L01 L02 L03; do { python3 -I -W error tests/labs/BK4/lab-BK4-$t-1.py > $O/twin_$t.stdout; echo "exit $?"; } > $O/twin_$t.exit 2>&1; done
{ .venv/bin/ruff check tests/labs/BK4/lab-BK4-L01-1.py tests/labs/BK4/lab-BK4-L02-1.py tests/labs/BK4/lab-BK4-L03-1.py; echo "exit $?"; } > $O/ruff_check.txt 2>&1
{ .venv/bin/ruff format --check tests/labs/BK4/lab-BK4-L01-1.py tests/labs/BK4/lab-BK4-L02-1.py tests/labs/BK4/lab-BK4-L03-1.py; echo "exit $?"; } > $O/ruff_format.txt 2>&1
{ .venv/bin/mypy --no-incremental tests/labs/BK4/lab-BK4-L01-1.py tests/labs/BK4/lab-BK4-L02-1.py tests/labs/BK4/lab-BK4-L03-1.py; echo "exit $?"; } > $O/mypy.txt 2>&1
{ .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -p no:cacheprovider; echo "exit $?"; } > $O/pytest.txt 2>&1
{ $P tools/verify_refs.py --unit BK4; echo "exit $?"; } > $O/verify_refs_unit.txt 2>&1
{ $P tools/page_smoke.py --unit BK4 --pages index L01 L02 L03; echo "exit $?"; } > $O/page_smoke.txt 2>&1
echo done > $O/DONE
