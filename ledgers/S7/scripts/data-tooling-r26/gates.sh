#!/bin/bash
# Gate runner for the S7 data-tooling round 26 (checkout pinned at 47bac8d). Each step logs its exit code.
cd /tmp/verify-s7-r1-dt || exit 1
P=.venv/bin/python
L=/tmp/ap1-r5/data-tooling/logs
run() { name=$1; shift; "$@" > "$L/$name.log" 2>&1; echo "$name exit=$?" >> "$L/summary.txt"; }
: > "$L/summary.txt"
run ruff_check .venv/bin/ruff check .
run ruff_format .venv/bin/ruff format --check .
run mypy .venv/bin/mypy --no-incremental
run render_curriculum $P tools/render_curriculum.py
run curriculum_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run build_site_check $P tools/build_site.py --check
run verify_refs_offline $P tools/verify_refs.py --offline
run fetch_data_check $P tools/fetch_data.py --check
run check_pages_all $P tools/check_pages.py --all
run check_dag_all $P tools/check_dag.py --all
run check_projects_all $P tools/check_projects.py --all
run fetch_vendor_check $P tools/fetch_vendor.py --check
run vendor_py_check $P tools/vendor.py check
run run_labs_all $P tools/run_labs.py --all
run run_graders_S7 $P tools/run_graders.py --unit S7 --seeds 0-49
run mutate_graders_S7 $P tools/mutate_graders.py --unit S7 --seeds 0-9
run pytest_full .venv/bin/pytest
echo DONE >> "$L/summary.txt"
