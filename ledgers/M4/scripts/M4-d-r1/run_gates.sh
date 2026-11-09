#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyF21-M4-d
G=ledgers/M4/scripts/M4-d-r1/gates
PY=.venv/bin/python
$PY tools/check_pages.py --all > $G/check_pages_all.out 2>&1; echo "exit $?" >> $G/check_pages_all.out
$PY tools/check_dag.py --all > $G/check_dag_all.out 2>&1; echo "exit $?" >> $G/check_dag_all.out
$PY tools/check_projects.py --all > $G/check_projects_all.out 2>&1; echo "exit $?" >> $G/check_projects_all.out
$PY tools/run_labs.py --unit M4 > $G/run_labs_M4.out 2>&1; echo "exit $?" >> $G/run_labs_M4.out
$PY tools/run_graders.py --unit M4 --seeds 0-49 > $G/run_graders_M4_0-49.out 2>&1; echo "exit $?" >> $G/run_graders_M4_0-49.out
$PY tools/page_smoke.py --unit M4 > $G/page_smoke_M4.out 2>&1; echo "exit $?" >> $G/page_smoke_M4.out
$PY tools/verify_refs.py --offline > $G/verify_refs_offline.out 2>&1; echo "exit $?" >> $G/verify_refs_offline.out
$PY tools/render_curriculum.py > $G/render_curriculum.out 2>&1; echo "exit $?" >> $G/render_curriculum.out
git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json > $G/render_curriculum_diff.out 2>&1; echo "exit $?" >> $G/render_curriculum_diff.out
$PY tools/build_site.py --check > $G/build_site_check.out 2>&1; echo "exit $?" >> $G/build_site_check.out
$PY tools/fetch_data.py --check > $G/fetch_data_check.out 2>&1; echo "exit $?" >> $G/fetch_data_check.out
$PY -m ruff check . > $G/ruff_check.out 2>&1; echo "exit $?" >> $G/ruff_check.out
$PY -m ruff format --check . > $G/ruff_format.out 2>&1; echo "exit $?" >> $G/ruff_format.out
$PY -m mypy --no-incremental > $G/mypy.out 2>&1; echo "exit $?" >> $G/mypy.out
$PY -m pytest --collect-only -q course/modules/M/M4/grader/test_project.py > $G/collect_m4_grader.out 2>&1; echo "exit $?" >> $G/collect_m4_grader.out
$PY -m pytest -q tests/test_labs.py tests/test_memo_exemplars.py tests/test_refs.py tests/test_docs_figures.py tests/test_page_checks.py tests/test_run_labs.py tests/test_curriculum.py tests/test_build_site.py tests/test_page_smoke.py > $G/pytest_relevant.out 2>&1; echo "exit $?" >> $G/pytest_relevant.out
$PY tools/mutate_graders.py --unit M4 --seeds 0-9 > $G/mutate_M4_0-9.out 2>&1; echo "exit $?" >> $G/mutate_M4_0-9.out
echo done > $G/ALL_DONE
