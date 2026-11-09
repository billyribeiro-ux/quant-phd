#!/bin/bash
# Closing-delta gate commands (d9de2fe5). Run from the checkout root; outputs in out/ with *_E3 / *_L0x names.
cd /Users/billyribeiro/.fanout/wt/verifyH1-E3-g
O=ledgers/E3/scripts/E3-g-r1/out
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "$name rc=$?"; }
run check_pages_E3 .venv/bin/python tools/check_pages.py --unit E3
run check_dag_E3 .venv/bin/python tools/check_dag.py --unit E3
run check_projects_E3 .venv/bin/python tools/check_projects.py --unit E3
run run_labs_L05 .venv/bin/python tools/run_labs.py --unit E3 --page L05
run run_labs_L06 .venv/bin/python tools/run_labs.py --unit E3 --page L06
run run_labs_L07 .venv/bin/python tools/run_labs.py --unit E3 --page L07
run run_labs_L08 .venv/bin/python tools/run_labs.py --unit E3 --page L08
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run build_site_check .venv/bin/python tools/build_site.py --check
run render_curriculum .venv/bin/python tools/render_curriculum.py
run curriculum_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run ruff_check_delta .venv/bin/ruff check .
run ruff_format_delta .venv/bin/ruff format --check .
run mypy_delta .venv/bin/mypy --no-incremental
run pytest_docs_refs .venv/bin/pytest -q tests/test_docs_figures.py tests/test_refs.py
