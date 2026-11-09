#!/bin/bash
# LX1-b round 17 gate runs on the pin 700bf33f (run from the checkout root; outputs in out/).
set -u
cd "$(dirname "$0")/../../../.." || exit 1
OUT=ledgers/LX1/scripts/LX1-b-r17/out
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "$name exit=$?" >> "$OUT/_exit_codes.txt"; }
rm -f "$OUT/_exit_codes.txt"
run check_pages_unit $PY tools/check_pages.py --unit LX1
run check_dag_unit $PY tools/check_dag.py --unit LX1
run check_projects_unit $PY tools/check_projects.py --unit LX1
run run_graders_unit $PY tools/run_graders.py --unit LX1
run run_labs_unit $PY tools/run_labs.py --unit LX1
run page_smoke_L03 $PY tools/page_smoke.py --unit LX1 --pages L03
run page_smoke_L04 $PY tools/page_smoke.py --unit LX1 --pages L04
run page_smoke_L01 $PY tools/page_smoke.py --unit LX1 --pages L01
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_unit $PY tools/verify_refs.py --unit LX1 --offline
run fetch_data_check $PY tools/fetch_data.py --check
run build_site_check $PY tools/build_site.py --check
run ruff_check_labs .venv/bin/ruff check tests/labs/LX1/
run ruff_format_labs .venv/bin/ruff format --check tests/labs/LX1/
run mypy_nocache .venv/bin/mypy --no-incremental tests/labs/LX1/lab-LX1-L01-1.py tests/labs/LX1/lab-LX1-L03-1.py tests/labs/LX1/lab-LX1-L04-1.py
run pytest_lx1 .venv/bin/pytest -q -k LX1
run pytest_lx1_collect .venv/bin/pytest --collect-only -q -k LX1
for t in L01 L03 L04; do
  d=$(mktemp -d /tmp/lx1b-r17-twin-XXXX)
  cp tests/labs/LX1/lab-LX1-$t-1.py "$d/"
  (cd "$d" && python3 -I -W error "lab-LX1-$t-1.py" > "$OLDPWD/$OUT/twin_$t.stdout" 2> "$OLDPWD/$OUT/twin_$t.stderr"; echo $? > "$OLDPWD/$OUT/twin_$t.exit")
  rm -rf "$d"
done
echo done >> "$OUT/_exit_codes.txt"
