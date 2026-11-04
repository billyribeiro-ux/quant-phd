#!/bin/sh
# SC1 slice b (L04-L06 and lab twins), round 1. Run from the checkout root.
set -u
PY=.venv/bin/python
D=ledgers/SC1/scripts/SC1-b-r1
OUT=ledgers/SC1/scripts/SC1-b-r1/out
mkdir -p $OUT
$PY tools/check_pages.py --unit SC1 > $OUT/check_pages.txt 2>&1; echo "check_pages exit=$?" >> $OUT/check_pages.txt
$PY tools/check_dag.py --unit SC1 > $OUT/check_dag.txt 2>&1; echo "check_dag exit=$?" >> $OUT/check_dag.txt
$PY tools/run_labs.py --unit SC1 > $OUT/run_labs.txt 2>&1; echo "run_labs exit=$?" >> $OUT/run_labs.txt
$PY -I $D/twin_match.py > $OUT/twin_match.txt 2>&1; echo "twin_match exit=$?" >> $OUT/twin_match.txt
$PY tools/page_smoke.py --unit SC1 --pages L04 L05 L06 > $OUT/page_smoke.txt 2>&1; echo "page_smoke exit=$?" >> $OUT/page_smoke.txt
$PY -m ruff check tests/labs/SC1/lab-SC1-L04-1.py tests/labs/SC1/lab-SC1-L05-1.py tests/labs/SC1/lab-SC1-L06-1.py > $OUT/ruff.txt 2>&1; echo "ruff_check exit=$?" >> $OUT/ruff.txt
$PY -m ruff format --check tests/labs/SC1/lab-SC1-L04-1.py tests/labs/SC1/lab-SC1-L05-1.py tests/labs/SC1/lab-SC1-L06-1.py >> $OUT/ruff.txt 2>&1; echo "ruff_format exit=$?" >> $OUT/ruff.txt
$PY -m mypy --no-incremental tests/labs/SC1/lab-SC1-L04-1.py tests/labs/SC1/lab-SC1-L05-1.py tests/labs/SC1/lab-SC1-L06-1.py > $OUT/mypy.txt 2>&1; echo "mypy exit=$?" >> $OUT/mypy.txt
$PY tools/verify_refs.py --unit SC1 > $OUT/verify_refs.txt 2>&1; echo "verify_refs exit=$?" >> $OUT/verify_refs.txt
$PY -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py > $OUT/pytest.txt 2>&1; echo "pytest exit=$?" >> $OUT/pytest.txt
$PY -I $D/recompute.py > $OUT/recompute.txt 2>&1; echo "recompute exit=$?" >> $OUT/recompute.txt
