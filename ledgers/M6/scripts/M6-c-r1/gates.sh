#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyF21-M6-c || exit 1
S=ledgers/M6/scripts/M6-c-r1
P=.venv/bin/python
run() { name=$1; shift; "$@" > "$S/$name.out" 2>&1; echo "$name exit=$?" >> "$S/gates_exit.txt"; }
rm -f "$S/gates_exit.txt"
run run_labs_M6 $P tools/run_labs.py --unit M6
run check_pages_M6 $P tools/check_pages.py --unit M6
run check_dag_all $P tools/check_dag.py --all
run check_pages_M6_hub $P tools/check_pages.py --unit M6 --page L09
run build_site_check $P tools/build_site.py --check
run verify_refs_offline $P tools/verify_refs.py --offline
run render_curriculum $P tools/render_curriculum.py
run curriculum_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run ruff_check_M6_labs $P -m ruff check tests/labs/M6
run ruff_format_M6_labs $P -m ruff format --check tests/labs/M6
run mypy_nocache $P -m mypy --no-incremental
run pytest_labs_M6 $P -m pytest -q -k "M6 or lab"
run fetch_data_check $P tools/fetch_data.py --check
run page_smoke_M6_L09_12 $P tools/page_smoke.py --unit M6 --pages L09 L10 L11 L12
echo DONE >> "$S/gates_exit.txt"
