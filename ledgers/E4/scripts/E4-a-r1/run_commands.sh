#!/bin/sh
# E4 slice a (hub, L01 to L03, lab twins) verifier round 1: the command rows, run from the checkout root.
# Each command is the one cited in ledgers/E4/E4-a.json; outputs were observed at pin 1c1645f.
set -u
cd "$(dirname "$0")/../../../.." || exit 1
.venv/bin/python tools/check_pages.py --unit E4
.venv/bin/python tools/check_pages.py --unit E4 --page L01
.venv/bin/python tools/check_pages.py --unit E4 --page L02
.venv/bin/python tools/check_pages.py --unit E4 --page L03
.venv/bin/python tools/check_dag.py --unit E4
.venv/bin/python tools/check_projects.py --unit E4
.venv/bin/python tools/run_labs.py --unit E4
for t in L01-1 L02-1 L03-1; do env -i HOME="$HOME" PATH=/usr/bin:/bin .venv/bin/python -I -W error "tests/labs/E4/lab-E4-$t.py" >/dev/null; echo "twin $t exit $?"; done
.venv/bin/python -I ledgers/E4/scripts/E4-a-r1/check_embeds.py
.venv/bin/ruff check tests/labs/E4/lab-E4-L01-1.py tests/labs/E4/lab-E4-L02-1.py tests/labs/E4/lab-E4-L03-1.py
.venv/bin/ruff format --check tests/labs/E4/lab-E4-L01-1.py tests/labs/E4/lab-E4-L02-1.py tests/labs/E4/lab-E4-L03-1.py
.venv/bin/mypy --no-incremental tests/labs/E4/lab-E4-L01-1.py tests/labs/E4/lab-E4-L02-1.py tests/labs/E4/lab-E4-L03-1.py
.venv/bin/python tools/page_smoke.py --unit E4 --pages index L01 L02 L03
.venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py
.venv/bin/python tools/verify_refs.py --offline
.venv/bin/python -I ledgers/E4/scripts/E4-a-r1/rederive_numbers.py
