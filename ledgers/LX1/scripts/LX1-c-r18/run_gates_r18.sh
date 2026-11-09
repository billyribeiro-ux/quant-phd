#!/usr/bin/env bash
# Round-17 gate commands for LX1-c, run from the checkout root. Each command's exit code and output go to out/.
set -u
OUT=ledgers/LX1/scripts/LX1-c-r18/out
PY=.venv/bin/python
run() { name="$1"; shift; { echo "\$ $*"; "$@"; echo "rc=$?"; } > "$OUT/$name.out" 2>&1; echo "$name: $(tail -1 "$OUT/$name.out")"; }
run check_pages_LX1 $PY tools/check_pages.py --unit LX1
run check_pages_project $PY tools/check_pages.py --unit LX1 --page project
run check_dag_LX1 $PY tools/check_dag.py --unit LX1
run check_projects_LX1 $PY tools/check_projects.py --unit LX1
run run_labs_LX1 $PY tools/run_labs.py --unit LX1
run run_labs_project $PY tools/run_labs.py --unit LX1 --page project
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_LX1_online $PY tools/verify_refs.py --unit LX1
run fetch_data_check $PY tools/fetch_data.py --check
run build_site_check $PY tools/build_site.py --check
run mutate_graders_LX1 $PY tools/mutate_graders.py --unit LX1 --seeds 0-9
run ruff_check $PY -m ruff check tests/labs/LX1 tools
run ruff_format $PY -m ruff format --check tests/labs/LX1 tools
run mypy_full $PY -m mypy --no-incremental
run pytest_labs $PY -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_page_checks.py tests/test_curriculum.py
run pytest_refs $PY -m pytest -q tests/test_refs.py
