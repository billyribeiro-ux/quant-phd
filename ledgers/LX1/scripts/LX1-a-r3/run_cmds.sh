#!/bin/bash
# Round 3 verifier commands for LX1 slice a (hub index.html, L01, L02, twins L01-1 and L02-1). Run from the checkout root.
set -u
OUT=ledgers/LX1/scripts/LX1-a-r3/out
PY=.venv/bin/python
run() { name="$1"; shift; { "$@"; echo "EXIT=$?"; } > "$OUT/$name.txt" 2>&1; echo "$name: $(tail -n1 $OUT/$name.txt)"; }
run check_pages $PY tools/check_pages.py --unit LX1
run check_dag $PY tools/check_dag.py --unit LX1
run check_projects $PY tools/check_projects.py --unit LX1
run run_labs_unit $PY tools/run_labs.py --unit LX1
run twin_L01 env PYTHONDONTWRITEBYTECODE=1 $PY -I -W error tests/labs/LX1/lab-LX1-L01-1.py
run twin_L02 env PYTHONDONTWRITEBYTECODE=1 $PY -I -W error tests/labs/LX1/lab-LX1-L02-1.py
run ruff_labs .venv/bin/ruff check tests/labs/LX1
run ruff_format_labs .venv/bin/ruff format --check tests/labs/LX1
run mypy_labs .venv/bin/mypy --no-incremental tests/labs/LX1
run verify_refs_unit $PY tools/verify_refs.py --unit LX1
run verify_refs_offline $PY tools/verify_refs.py --offline
run fetch_data_check $PY tools/fetch_data.py --check
run pytest_relevant .venv/bin/pytest -q -k 'lab or page or LX1 or dag or project or embed or refs' tests
run page_smoke_index $PY tools/page_smoke.py --unit LX1 --pages index
run page_smoke_L01 $PY tools/page_smoke.py --unit LX1 --pages L01
run page_smoke_L02 $PY tools/page_smoke.py --unit LX1 --pages L02
run mutate_graders_unit $PY tools/mutate_graders.py --unit LX1 --seeds 0-9
echo DONE
