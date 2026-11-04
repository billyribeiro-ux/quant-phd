#!/bin/sh
# LX1-c round 1: command rows, run from the checkout root. Prints each command and its exit code.
# Usage: sh ledgers/LX1/scripts/LX1-c-r1/gates_r1.sh
V=.venv/bin/python
run() { echo "\$ $*"; "$@"; echo "exit=$?"; }
run $V tools/check_pages.py --unit LX1
run $V tools/check_dag.py --unit LX1
run $V tools/check_projects.py --unit LX1
run $V tools/run_labs.py --unit LX1
run $V tools/page_smoke.py --unit LX1 --pages project
run $V tools/fetch_data.py --check
run $V tools/verify_refs.py --unit LX1
run .venv/bin/ruff check tests/labs/LX1
run .venv/bin/ruff format --check tests/labs/LX1
run .venv/bin/mypy --no-incremental tests/labs/LX1
run .venv/bin/pytest -q tests/test_labs.py -k LX1
