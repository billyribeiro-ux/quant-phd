#!/bin/bash
# Round-6 verifier gates for E3-d, run from the checkout root. Each step writes <name>.out and <name>.rc.
cd /Users/billyribeiro/.fanout/wt/verifyD6-E3-d || exit 1
S=ledgers/E3/scripts/E3-d-r6
run() { name=$1; shift; "$@" > $S/$name.out 2>&1; echo $? > $S/$name.rc; }
run check_pages .venv/bin/python tools/check_pages.py --all
run check_dag .venv/bin/python tools/check_dag.py --all
run check_projects .venv/bin/python tools/check_projects.py --all
run run_labs_project .venv/bin/python tools/run_labs.py --unit E3 --page project
run run_graders_0_49 .venv/bin/python tools/run_graders.py --unit E3 --seeds 0-49
run ruff_check .venv/bin/ruff check course/modules/E/E3 tests/labs/E3 ledgers/E3/mutants ledgers/E3/scripts/E3-d-r6
run ruff_format .venv/bin/ruff format --check course/modules/E/E3/grader tests/labs/E3
run mypy .venv/bin/mypy --no-incremental
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run check_docs_figures .venv/bin/pytest -q tests/test_docs_figures.py tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py
run page_smoke_project .venv/bin/python tools/page_smoke.py --unit E3 --pages project
echo done > $S/gates_done.flag
