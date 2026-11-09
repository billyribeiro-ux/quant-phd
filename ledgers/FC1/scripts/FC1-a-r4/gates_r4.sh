#!/bin/bash
# FC1-a round 4 gate runs (slice: hub index, L01-L03, twins, cards for L01-L03). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyS4-FC1-a || exit 1
OUT=ledgers/FC1/scripts/FC1-a-r4/out
mkdir -p "$OUT"
PY=.venv/bin/python
run() { name="$1"; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > "$OUT/$name.out" 2>&1; echo "$name: $(tail -1 "$OUT/$name.out")"; }
run check_pages_unit $PY tools/check_pages.py --unit FC1
run check_pages_all $PY tools/check_pages.py --all
run check_dag_unit $PY tools/check_dag.py --unit FC1
run check_dag_all $PY tools/check_dag.py --all
run check_projects_unit $PY tools/check_projects.py --unit FC1
run run_labs_L01 $PY tools/run_labs.py --unit FC1 --page L01
run run_labs_L02 $PY tools/run_labs.py --unit FC1 --page L02
run run_labs_L03 $PY tools/run_labs.py --unit FC1 --page L03
run twin_L01 $PY -I -W error tests/labs/FC1/lab-FC1-L01-1.py
run twin_L02 $PY -I -W error tests/labs/FC1/lab-FC1-L02-1.py
run twin_L03 $PY -I -W error tests/labs/FC1/lab-FC1-L03-1.py
run page_smoke $PY tools/page_smoke.py --unit FC1 --pages index L01 L02 L03
run ruff_check .venv/bin/ruff check .
run ruff_format .venv/bin/ruff format --check .
run mypy_full .venv/bin/mypy --no-incremental
run pytest_labs_fc1 .venv/bin/pytest tests/test_labs.py -k FC1 -q
run pytest_page_checks .venv/bin/pytest tests/test_page_checks.py tests/test_page_smoke.py tests/test_refs.py tests/test_run_labs.py -q
run pytest_docs_figures .venv/bin/pytest tests/test_docs_figures.py -q
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_unit_live $PY tools/verify_refs.py --unit FC1
run fetch_data_check $PY tools/fetch_data.py --check
run build_site_check $PY tools/build_site.py --check
run collect_fc1 .venv/bin/pytest --collect-only -q tests/test_labs.py -k FC1
echo DONE
