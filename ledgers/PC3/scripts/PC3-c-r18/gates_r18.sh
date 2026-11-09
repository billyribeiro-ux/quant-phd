#!/bin/bash
# Round 18, PC3 slice c. Run from the checkout root. Each command's output is kept under out/.
cd /Users/billyribeiro/.fanout/wt/verifyE18-PC3-c || exit 1
O=ledgers/PC3/scripts/PC3-c-r18/out
PY=.venv/bin/python
run() { name="$1"; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > "$O/$name.out" 2>&1; echo "$name $(tail -1 "$O/$name.out")"; }
run check_pages_project $PY tools/check_pages.py --unit PC3 --page project
run check_dag_unit $PY tools/check_dag.py --unit PC3
run check_projects_unit $PY tools/check_projects.py --unit PC3
run run_labs_project $PY tools/run_labs.py --unit PC3 --page project
run run_graders_0_49 $PY tools/run_graders.py --unit PC3 --seeds 0-49
run mutate_pc3_0_49 $PY tools/mutate_graders.py --unit PC3 --seeds 0-49
run page_smoke_project $PY tools/page_smoke.py --unit PC3 --pages project
run ruff_check_slice .venv/bin/ruff check course/modules/PC/PC3 tests/labs/PC3 ledgers/PC3
run ruff_format_slice .venv/bin/ruff format --check course/modules/PC/PC3 tests/labs/PC3 ledgers/PC3
run verify_refs_offline_pc3 $PY tools/verify_refs.py --offline --unit PC3
echo ALL_DONE
