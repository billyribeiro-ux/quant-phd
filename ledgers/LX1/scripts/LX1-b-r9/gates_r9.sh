#!/bin/sh
# LX1-b round 9 gate commands, run from the checkout root on pin c93dd526 (outputs in out/).
# Usage: sh ledgers/LX1/scripts/LX1-b-r9/gates_r9.sh <checkout>
cd "$1" || exit 1
PY=.venv/bin/python
O=ledgers/LX1/scripts/LX1-b-r9/out
mkdir -p "$O"
$PY tools/check_pages.py --unit LX1 > "$O/check_pages.out" 2>&1; echo "exit=$?" >> "$O/check_pages.out"
$PY tools/check_dag.py --unit LX1 > "$O/check_dag.out" 2>&1; echo "exit=$?" >> "$O/check_dag.out"
$PY tools/check_projects.py --unit LX1 > "$O/check_projects.out" 2>&1; echo "exit=$?" >> "$O/check_projects.out"
$PY tools/run_labs.py --unit LX1 > "$O/run_labs.out" 2>&1; echo "exit=$?" >> "$O/run_labs.out"
$PY tools/run_graders.py --unit LX1 > "$O/run_graders.out" 2>&1; echo "exit=$?" >> "$O/run_graders.out"
$PY tools/verify_refs.py --offline > "$O/verify_refs_offline.out" 2>&1; echo "exit=$?" >> "$O/verify_refs_offline.out"
$PY tools/verify_refs.py --unit LX1 > "$O/verify_refs_unit_LX1.out" 2>&1; echo "exit=$?" >> "$O/verify_refs_unit_LX1.out"
$PY tools/fetch_data.py --check > "$O/fetch_check.out" 2>&1; echo "exit=$?" >> "$O/fetch_check.out"
$PY tools/build_site.py --check > "$O/build_site_check.out" 2>&1; echo "exit=$?" >> "$O/build_site_check.out"
# Twins alone, under python -I -W error, from scratch directories holding only the twin and (for L04) data/fx_monthly.csv.
S=/tmp/lx1b-r9
rm -rf "$S" && mkdir -p "$S/L03" "$S/L04/data"
cp tests/labs/LX1/lab-LX1-L03-1.py "$S/L03/"
cp tests/labs/LX1/lab-LX1-L04-1.py "$S/L04/"
cp course/assets/data/market/fx_monthly.csv "$S/L04/data/"
(cd "$S/L03" && "$OLDPWD/$PY" -I -W error lab-LX1-L03-1.py > "$OLDPWD/$O/twin_L03.out" 2> "$OLDPWD/$O/twin_L03.err")
(cd "$S/L04" && "$OLDPWD/$PY" -I -W error lab-LX1-L04-1.py > "$OLDPWD/$O/twin_L04.out" 2> "$OLDPWD/$O/twin_L04.err")
python3 -I ledgers/LX1/scripts/LX1-b-r9/compare_pages_twins.py "$PWD" "$O" > "$O/compare_pages_twins.out"
python3 -I ledgers/LX1/scripts/LX1-b-r9/recompute_LX1b.py "$PWD" > "$O/recompute_LX1b.out" 2>&1
python3 -I ledgers/LX1/scripts/LX1-b-r9/delta_check_r9.py "$PWD" > "$O/delta_check_r9.out" 2>&1
python3 -I ledgers/LX1/scripts/LX1-b-r9/cards_dump.py "$PWD" > "$O/cards_dump.out" 2>&1
sh ledgers/LX1/scripts/LX1-b-r9/prose_scan.sh "$PWD" > "$O/prose_scan.out" 2>&1
mkdir -p /tmp/lx1b-r9/guard && python3 -I ledgers/LX1/scripts/LX1-b-r9/guard_L04.py "$PWD" /tmp/lx1b-r9/guard > "$O/guard_L04.out" 2>&1; echo "exit=$?" >> "$O/guard_L04.out"
$PY tools/page_smoke.py --unit LX1 --pages L03 L04 > "$O/page_smoke_L03_L04.out" 2>&1; echo "exit=$?" >> "$O/page_smoke_L03_L04.out"
.venv/bin/ruff check tests/labs/LX1 > "$O/ruff_check.out" 2>&1; echo "exit=$?" >> "$O/ruff_check.out"
.venv/bin/ruff format --check tests/labs/LX1 > "$O/ruff_format.out" 2>&1; echo "exit=$?" >> "$O/ruff_format.out"
.venv/bin/mypy --no-incremental tests/labs/LX1/lab-LX1-L03-1.py tests/labs/LX1/lab-LX1-L04-1.py > "$O/mypy_L03_L04.out" 2>&1; echo "exit=$?" >> "$O/mypy_L03_L04.out"
$PY -m pytest tests/test_labs.py tests/test_page_checks.py -q -k LX1 > "$O/pytest_LX1.out" 2>&1; echo "exit=$?" >> "$O/pytest_LX1.out"
curl -sS -L --max-time 30 -o "$O/fed_disclaimer.html" -w "%{http_code}\n" https://www.federalreserve.gov/disclaimer.htm > "$O/curl_fed_code.out" 2>&1
