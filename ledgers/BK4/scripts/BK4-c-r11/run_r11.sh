#!/bin/bash
# Round-11 gate runs for BK4-c (verifier E11). Usage: run_r11.sh <checkout-root>
cd "$1" || exit 2
R="$PWD"
O=ledgers/BK4/scripts/BK4-c-r11/out
mkdir -p "$O"
P=.venv/bin/python
rm -f "$O/_exit_codes.txt"
run() { name="$1"; shift; "$@" > "$O/$name.out" 2>&1; echo "$name exit=$?" >> "$O/_exit_codes.txt"; }
run check_projects_bk4 $P tools/check_projects.py --unit BK4
run check_pages_all $P tools/check_pages.py --all
run check_dag_all $P tools/check_dag.py --all
run run_labs_bk4 $P tools/run_labs.py --unit BK4
run run_graders_bk4 $P tools/run_graders.py --unit BK4 --seeds 0-49
run mutate_graders_bk4 $P tools/mutate_graders.py --unit BK4 --seeds 0-9
run ruff_check .venv/bin/ruff check tests/labs/BK4 course/modules/BK/BK4/grader ledgers/BK4
run ruff_format .venv/bin/ruff format --check tests/labs/BK4 course/modules/BK/BK4/grader ledgers/BK4
run mypy_repo .venv/bin/mypy --no-incremental
run pytest_labs .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py
run verify_refs_offline $P tools/verify_refs.py --unit BK4 --offline
run page_smoke_bk4_project $P tools/page_smoke.py --unit BK4 --pages project
run lab_twin_check $P -W error ledgers/BK4/scripts/BK4-c-r11/lab_twin_check_r11.py "$R"
run instance_sample $P -I ledgers/BK4/scripts/BK4-c-r11/instance_sample_r11.py "$R"
run rederive $P -I ledgers/BK4/scripts/BK4-c-r11/rederive_r11.py "$R"
run alternatives $P -I ledgers/BK4/scripts/BK4-c-r11/run_alts_r11.py "$R"
rm -rf /tmp/bk4r11_coll && mkdir -p /tmp/bk4r11_coll
cp course/modules/BK/BK4/grader/test_project.py course/modules/BK/BK4/grader/instance.py /tmp/bk4r11_coll/
cp course/modules/BK/BK4/grader/reference.py /tmp/bk4r11_coll/clearing_house.py
run collect_only bash -c "cd /tmp/bk4r11_coll && QF_SEED=0 $R/$P -m pytest --collect-only -q -p no:cacheprovider test_project.py"
echo done >> "$O/_exit_codes.txt"
