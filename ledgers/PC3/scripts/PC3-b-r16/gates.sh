#!/bin/bash
# PC3-b round 16 gate runs; outputs under ledgers/PC3/scripts/PC3-b-r16/out
cd /Users/billyribeiro/.fanout/wt/verifyE16-PC3-b || exit 1
O=ledgers/PC3/scripts/PC3-b-r16/out
PY=.venv/bin/python
$PY tools/run_labs.py --unit PC3 > $O/run_labs_unit.out 2>&1; echo "exit=$?" >> $O/run_labs_unit.out
$PY tools/check_pages.py --unit PC3 > $O/check_pages_unit.out 2>&1; echo "exit=$?" >> $O/check_pages_unit.out
$PY tools/check_dag.py --unit PC3 > $O/check_dag_unit.out 2>&1; echo "exit=$?" >> $O/check_dag_unit.out
$PY tools/check_dag.py --all > $O/check_dag_all.out 2>&1; echo "exit=$?" >> $O/check_dag_all.out
$PY tools/page_smoke.py --unit PC3 --pages L04 L05 L06 > $O/page_smoke_slice.out 2>&1; echo "exit=$?" >> $O/page_smoke_slice.out
$PY -m ruff check tests/labs/PC3 > $O/ruff_check_twins.out 2>&1; echo "exit=$?" >> $O/ruff_check_twins.out
$PY -m ruff format --check tests/labs/PC3 > $O/ruff_format_twins.out 2>&1; echo "exit=$?" >> $O/ruff_format_twins.out
$PY -m ruff check . > $O/ruff_check_repo.out 2>&1; echo "exit=$?" >> $O/ruff_check_repo.out
$PY -m ruff format --check . > $O/ruff_format_repo.out 2>&1; echo "exit=$?" >> $O/ruff_format_repo.out
$PY -m mypy --no-incremental > $O/mypy.out 2>&1; echo "exit=$?" >> $O/mypy.out
$PY -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py > $O/pytest_labs_tooling.out 2>&1; echo "exit=$?" >> $O/pytest_labs_tooling.out
$PY tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1; echo "exit=$?" >> $O/verify_refs_offline.out
$PY tools/fetch_data.py --check > $O/fetch_data_check.out 2>&1; echo "exit=$?" >> $O/fetch_data_check.out
$PY tools/build_site.py --check > $O/build_site_check.out 2>&1; echo "exit=$?" >> $O/build_site_check.out
$PY tools/render_curriculum.py > $O/render_curriculum.out 2>&1; echo "exit=$?" >> $O/render_curriculum.out
git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json > $O/render_curriculum_diff.out 2>&1; echo "exit=$?" >> $O/render_curriculum_diff.out
echo done > $O/ALL_DONE
