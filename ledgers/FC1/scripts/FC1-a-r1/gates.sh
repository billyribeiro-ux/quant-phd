#!/bin/bash
# Round-1 verifier gate runner for FC1-a. Run from the checkout root.
cd "$(dirname "$0")/../../../.." || exit 1
PY=.venv/bin/python
run() { echo "== $*"; "$@" 2>&1 | tail -40; echo "exit=${PIPESTATUS[0]}"; }
run $PY tools/check_pages.py --unit FC1
run $PY tools/check_dag.py --unit FC1
run $PY tools/check_projects.py --unit FC1
run $PY tools/run_labs.py --unit FC1 --page L01
run $PY tools/run_labs.py --unit FC1 --page L02
run $PY tools/run_labs.py --unit FC1 --page L03
run $PY tools/check_pages.py --unit FC1 --page index
run $PY tools/check_pages.py --unit FC1 --page L01
run $PY tools/check_pages.py --unit FC1 --page L02
run $PY tools/check_pages.py --unit FC1 --page L03
