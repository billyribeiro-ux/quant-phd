#!/bin/bash
# Round 11 gate runner for E4 slice e (run from the checkout root). Each step writes its own .out file.
cd "$(dirname "$0")/../../../.." || exit 1
S=ledgers/E4/scripts/E4-e-r11
run() { name=$1; shift; { "$@" 2>&1; echo "EXIT $?"; } > "$S/$name.out"; }
run check_pages .venv/bin/python tools/check_pages.py --all
run check_dag .venv/bin/python tools/check_dag.py --all
run check_projects .venv/bin/python tools/check_projects.py --all
run build_site_check .venv/bin/python tools/build_site.py --check
run run_labs_E4 .venv/bin/python tools/run_labs.py --unit E4
run run_graders_E4 .venv/bin/python tools/run_graders.py --unit E4 --seeds 0-49
run mutate_E4 .venv/bin/python tools/mutate_graders.py --unit E4
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run ruff_check .venv/bin/ruff check tests/labs/E4 course/modules/E/E4/grader
run ruff_format .venv/bin/ruff format --check tests/labs/E4 course/modules/E/E4/grader
run mypy_strict .venv/bin/mypy --no-incremental
run collect_grader_E4 .venv/bin/python -m pytest --collect-only -q course/modules/E/E4/grader/test_project.py
run page_smoke_E4 .venv/bin/python tools/page_smoke.py --unit E4
echo done > "$S/ALL_DONE"
