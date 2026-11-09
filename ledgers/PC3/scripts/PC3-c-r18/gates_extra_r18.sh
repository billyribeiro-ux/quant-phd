#!/bin/bash
# Round 18, PC3 slice c. Whole-unit and targeted commands run by this verifier (outputs under out/).
cd /Users/billyribeiro/.fanout/wt/verifyE18-PC3-c || exit 1
O=ledgers/PC3/scripts/PC3-c-r18/out
PY=.venv/bin/python
S=ledgers/PC3/scripts/PC3-c-r18
run() { name="$1"; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > "$O/$name.out" 2>&1; echo "$name $(tail -1 "$O/$name.out")"; }
run check_pages_unit $PY tools/check_pages.py --unit PC3
run verify_refs_offline_all $PY tools/verify_refs.py --offline
run verify_refs_live_pc3 $PY tools/verify_refs.py --unit PC3
run mutate_pc3_0_49_final $PY tools/mutate_graders.py --unit PC3 --seeds 0-49
run ruff_repo $PY -m ruff check .
run ruff_format_repo .venv/bin/ruff format --check .
run mypy_repo .venv/bin/mypy --no-incremental
run pytest_labs_pc3 .venv/bin/pytest tests/test_labs.py tests/test_page_checks.py -k PC3 -q -p no:cacheprovider
run pytest_run_labs_page_smoke .venv/bin/pytest tests/test_run_labs.py tests/test_page_smoke.py -q -p no:cacheprovider
run collect_counts $S/collect_counts_r18.sh
run mypy_grader $S/mypy_grader_r18.sh
run candidates_seed0 $S/run_candidates_r18.sh 0 $S/alt_r18_*.py ledgers/PC3/alternatives/*.py ledgers/PC3/mutants/r18_0*.py course/modules/PC/PC3/grader/reference.py course/modules/PC/PC3/grader/starter.py
run candidates_seed77314143 $S/run_candidates_r18.sh 77314143 $S/alt_r18_*.py ledgers/PC3/alternatives/*.py course/modules/PC/PC3/grader/reference.py course/modules/PC/PC3/grader/starter.py
run sample_instances $PY -I $S/sample_instances_r18.py
echo ALL_DONE
