#!/bin/bash
# Round-28 part C gate re-runs (verifier checkout, pin c9beb92). Each command's exit code and tail are logged.
R=/tmp/verify-s7-r2-C
L=$R/ledgers/S7/scripts/data-tooling-r28-C/logs
PY=$R/.venv/bin/python
cd $R || exit 1
run() { name=$1; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > $L/$name.log 2>&1; echo "$name: $(tail -1 $L/$name.log)"; }
run ruff_check $R/.venv/bin/ruff check .
run ruff_format $R/.venv/bin/ruff format --check .
run mypy $R/.venv/bin/mypy --no-incremental
run pytest_full $R/.venv/bin/pytest -p no:cacheprovider -q
run run_labs_all $PY tools/run_labs.py --all
run check_pages_all $PY tools/check_pages.py --all
run check_dag_all $PY tools/check_dag.py --all
run check_projects_all $PY tools/check_projects.py --all
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_unit_S7_live $PY tools/verify_refs.py --unit S7
run build_site_check $PY tools/build_site.py --check
run fetch_data_check $PY tools/fetch_data.py --check
run fetch_vendor_check $PY tools/fetch_vendor.py --check
run render_curriculum $PY tools/render_curriculum.py
run curriculum_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run run_graders_all $PY tools/run_graders.py --all --seeds 0-49
run mutate_graders_all $PY tools/mutate_graders.py --all --seeds 0-9
run page_smoke_S7 $PY tools/page_smoke.py --unit S7 --pages L01 L02 L03 L05 L06 L07 L08 project
run git_status git status --short
