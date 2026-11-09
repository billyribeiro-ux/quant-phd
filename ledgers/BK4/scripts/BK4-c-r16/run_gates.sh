#!/bin/bash
# BK4 slice c, round 16: gate commands run on the pin (56cc575a). Each output goes to out/.
cd /Users/billyribeiro/.fanout/wt/verifyE16-BK4-c || exit 1
O=ledgers/BK4/scripts/BK4-c-r16/out
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$O/$name.txt" 2>&1; echo "$name exit=$?" >> "$O/_exit_codes.txt"; }
: > "$O/_exit_codes.txt"
run check_pages $PY tools/check_pages.py --unit BK4
run check_dag $PY tools/check_dag.py --unit BK4
run check_projects $PY tools/check_projects.py --unit BK4
run run_labs_project $PY tools/run_labs.py --unit BK4 --page project
run run_graders $PY tools/run_graders.py --unit BK4 --seeds 0-49
run page_smoke_project $PY tools/page_smoke.py --unit BK4 --pages project
run ruff_check .venv/bin/ruff check tests/labs/BK4 course/modules/BK/BK4/grader
run ruff_format .venv/bin/ruff format --check tests/labs/BK4 course/modules/BK/BK4/grader
run mypy_unit $PY -m mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader
run mypy_repo $PY -m mypy --no-incremental
run verify_refs_offline $PY tools/verify_refs.py --offline
run verify_refs_BK4 $PY tools/verify_refs.py --unit BK4
run pytest_BK4 $PY -m pytest -q -k "BK4 or bk4" tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py
# collect_only: run by collect_and_local_run_r16.sh (the suite needs clearing_house.py beside it)
run mutate_graders_87 $PY tools/mutate_graders.py --unit BK4 --seeds 0-9  # 87 mutants before the five round-16 mutants; later run wrote out/mutate_graders_r16.txt (92)
echo DONE >> "$O/_exit_codes.txt"
