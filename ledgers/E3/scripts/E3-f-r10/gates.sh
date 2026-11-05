#!/bin/bash
# Round 10 gate runner for E3 slice f (lessons L01-L04 and their cards). Run from the checkout root.
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyD10-E3-f
cd "$ROOT" || exit 2
PY=.venv/bin/python
OUT="$ROOT/ledgers/E3/scripts/E3-f-r10"
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; rc=$?; echo "exit $rc" >> "$OUT/$name.out"; echo "$name rc=$rc"; }
run check_pages $PY tools/check_pages.py --unit E3
run check_dag $PY tools/check_dag.py --unit E3
run check_projects $PY tools/check_projects.py --unit E3
run run_labs_L01 $PY tools/run_labs.py --unit E3 --page L01
run run_labs_L02 $PY tools/run_labs.py --unit E3 --page L02
run run_labs_L03 $PY tools/run_labs.py --unit E3 --page L03
run run_labs_L04 $PY tools/run_labs.py --unit E3 --page L04
run page_smoke $PY tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04
run ruff_labs bash -c ".venv/bin/ruff check tests/labs/E3 && .venv/bin/ruff format --check tests/labs/E3"
run mypy_twins $PY -m mypy --no-incremental tests/labs/E3/lab-E3-L01-1.py tests/labs/E3/lab-E3-L02-1.py tests/labs/E3/lab-E3-L03-1.py tests/labs/E3/lab-E3-L04-1.py
run pytest_labs_E3 $PY -m pytest tests/test_labs.py -k E3 -q
run verify_refs_offline $PY tools/verify_refs.py --offline
