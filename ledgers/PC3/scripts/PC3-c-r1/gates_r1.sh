#!/bin/bash
# PC3 slice c, closing delta round 1 (pin 95f3f8cb). Run from checkout root; each output under out/.
cd /Users/billyribeiro/.fanout/wt/verifyF31-PC3-c || exit 1
O=ledgers/PC3/scripts/PC3-c-r1/out
PY=.venv/bin/python
run() { name="$1"; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > "$O/$name.out" 2>&1; echo "$name $(tail -1 "$O/$name.out")"; }
run check_pages_project $PY tools/check_pages.py --unit PC3 --page project
run check_pages_unit $PY tools/check_pages.py --unit PC3
run check_dag_unit $PY tools/check_dag.py --unit PC3
run check_projects_unit $PY tools/check_projects.py --unit PC3
run run_labs_project $PY tools/run_labs.py --unit PC3 --page project
run run_graders_0_49 $PY tools/run_graders.py --unit PC3 --seeds 0-49
run page_smoke_project $PY tools/page_smoke.py --unit PC3 --pages project
run ruff_check_slice .venv/bin/ruff check course/modules/PC/PC3 tests/labs/PC3 ledgers/PC3
run ruff_format_slice .venv/bin/ruff format --check course/modules/PC/PC3 tests/labs/PC3 ledgers/PC3
run mypy_repo .venv/bin/mypy --no-incremental
run pytest_pc3 .venv/bin/pytest tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py tests/test_page_smoke.py -k PC3 -q -p no:cacheprovider
run verify_refs_offline_pc3 $PY tools/verify_refs.py --offline --unit PC3
run mutate_pc3_0_49 $PY tools/mutate_graders.py --unit PC3 --seeds 0-49
echo ALL_DONE
