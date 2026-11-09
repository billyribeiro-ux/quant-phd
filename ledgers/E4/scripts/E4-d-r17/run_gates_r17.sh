#!/bin/bash
# Round 17 gate runs for E4 slice d (verifier). Each command's output and exit code go to out/.
cd "$(dirname "$0")/../../../.." || exit 1
O=ledgers/E4/scripts/E4-d-r17/out
run() { name=$1; shift; { "$@" 2>&1; echo "exit $?"; } > "$O/$name.txt"; tail -2 "$O/$name.txt" | sed "s/^/$name: /"; }
run check_pages .venv/bin/python tools/check_pages.py --unit E4
run check_dag .venv/bin/python tools/check_dag.py --unit E4
run check_projects .venv/bin/python tools/check_projects.py --unit E4
run run_labs .venv/bin/python tools/run_labs.py --unit E4
run run_graders_0_49 .venv/bin/python tools/run_graders.py --unit E4 --seeds 0-49
run page_smoke_project .venv/bin/python tools/page_smoke.py --unit E4 --pages modules/E/E4/project.html
run mutate_graders_0_9 .venv/bin/python tools/mutate_graders.py --unit E4 --seeds 0-9
run collect_only .venv/bin/python -m pytest --collect-only -q course/modules/E/E4/grader/test_project.py
run ruff_check .venv/bin/ruff check course/modules/E/E4 tests/labs/E4
run ruff_format .venv/bin/ruff format --check course/modules/E/E4 tests/labs/E4
run mypy_e4 .venv/bin/mypy --no-incremental tests/labs/E4 course/modules/E/E4/grader
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run verify_refs_E4_live .venv/bin/python tools/verify_refs.py --unit E4
echo ALLDONE
