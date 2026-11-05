#!/bin/sh
# LX1-b round 12 gate commands, run from the checkout root on pin 5db69a9 (outputs in out/).
# Usage: sh ledgers/LX1/scripts/LX1-b-r12/gates_r12.sh <checkout>
cd "$1" || exit 1
PY=.venv/bin/python
O=ledgers/LX1/scripts/LX1-b-r12/out
mkdir -p "$O"
$PY tools/check_pages.py --unit LX1 > "$O/check_pages.out" 2>&1; echo "exit=$?" >> "$O/check_pages.out"
$PY tools/check_dag.py --unit LX1 > "$O/check_dag.out" 2>&1; echo "exit=$?" >> "$O/check_dag.out"
$PY tools/check_projects.py --unit LX1 > "$O/check_projects.out" 2>&1; echo "exit=$?" >> "$O/check_projects.out"
$PY tools/run_labs.py --unit LX1 > "$O/run_labs.out" 2>&1; echo "exit=$?" >> "$O/run_labs.out"
$PY tools/run_graders.py --unit LX1 > "$O/run_graders.out" 2>&1; echo "exit=$?" >> "$O/run_graders.out"
$PY tools/verify_refs.py --offline > "$O/verify_refs_offline.out" 2>&1; echo "exit=$?" >> "$O/verify_refs_offline.out"
$PY tools/verify_refs.py --unit LX1 > "$O/verify_refs_unit_LX1.out" 2>&1; echo "exit=$?" >> "$O/verify_refs_unit_LX1.out"
$PY tools/fetch_data.py --check > "$O/fetch_check.out" 2>&1; echo "exit=$?" >> "$O/fetch_check.out"
$PY tools/page_smoke.py --unit LX1 --pages L03 > "$O/page_smoke_L03.out" 2>&1; echo "exit=$?" >> "$O/page_smoke_L03.out"
$PY tools/page_smoke.py --unit LX1 --pages L04 > "$O/page_smoke_L04.out" 2>&1; echo "exit=$?" >> "$O/page_smoke_L04.out"
.venv/bin/ruff check tests/labs/LX1 > "$O/ruff_check.out" 2>&1; echo "exit=$?" >> "$O/ruff_check.out"
.venv/bin/ruff format --check tests/labs/LX1 > "$O/ruff_format.out" 2>&1; echo "exit=$?" >> "$O/ruff_format.out"
.venv/bin/mypy --no-incremental tests/labs/LX1/lab-LX1-L03-1.py tests/labs/LX1/lab-LX1-L04-1.py > "$O/mypy_L03_L04.out" 2>&1; echo "exit=$?" >> "$O/mypy_L03_L04.out"
$PY -m pytest tests/test_labs.py tests/test_page_checks.py -q -k LX1 > "$O/pytest_LX1.out" 2>&1; echo "exit=$?" >> "$O/pytest_LX1.out"
$PY -m pytest --collect-only -q tests/test_labs.py tests/test_page_checks.py -k LX1 > "$O/pytest_collect_LX1.out" 2>&1; echo "exit=$?" >> "$O/pytest_collect_LX1.out"
S=/tmp/lx1b-r12
rm -rf "$S" && mkdir -p "$S/L03" "$S/L04/data"
cp tests/labs/LX1/lab-LX1-L03-1.py "$S/L03/"
cp tests/labs/LX1/lab-LX1-L04-1.py "$S/L04/"
cp course/assets/data/market/fx_monthly.csv "$S/L04/data/"
R=$(pwd)
(cd "$S/L03" && "$R/$PY" -I -W error lab-LX1-L03-1.py > "$R/$O/twin_L03.out" 2> "$R/$O/twin_L03.err"; echo "exit=$?" >> "$R/$O/twin_L03.err")
(cd "$S/L04" && "$R/$PY" -I -W error lab-LX1-L04-1.py > "$R/$O/twin_L04.out" 2> "$R/$O/twin_L04.err"; echo "exit=$?" >> "$R/$O/twin_L04.err")
echo DONE > "$O/DONE"
