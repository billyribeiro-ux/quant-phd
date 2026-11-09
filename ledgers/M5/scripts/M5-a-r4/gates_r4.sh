#!/bin/sh
# M5 slice a, round 4 (pin edbb7aa8). Run from the checkout root. Each output file sits beside this script.
set -u
O=ledgers/M5/scripts/M5-a-r4
PY=.venv/bin/python
$PY tools/check_pages.py --unit M5 > $O/r4_check_pages_M5.out 2>&1; echo "exit $?" >> $O/r4_check_pages_M5.out
$PY tools/check_dag.py --unit M5 > $O/r4_check_dag_M5.out 2>&1; echo "exit $?" >> $O/r4_check_dag_M5.out
$PY tools/check_projects.py --unit M5 > $O/r4_check_projects_M5.out 2>&1; echo "exit $?" >> $O/r4_check_projects_M5.out
$PY tools/run_labs.py --unit M5 --page index > $O/r4_run_labs_index.out 2>&1; echo "exit $?" >> $O/r4_run_labs_index.out
for p in L01 L02 L03 L04; do $PY tools/run_labs.py --unit M5 --page $p > $O/r4_run_labs_$p.out 2>&1; echo "exit $?" >> $O/r4_run_labs_$p.out; done
for i in 1 2 3 4; do
  d=$(mktemp -d /tmp/m5a_r4_scratch/L0$i.XXXX); cp tests/labs/M5/lab-M5-L0$i-1.py "$d/"
  (cd "$d" && "$OLDPWD/$PY" -I -W error lab-M5-L0$i-1.py > "$OLDPWD/$O/r4_twin_L0$i.out" 2> "$OLDPWD/$O/r4_twin_L0$i.err"; echo "exit $?" > "$OLDPWD/$O/r4_twin_L0$i.exit")
done
.venv/bin/ruff check . > $O/r4_ruff_check.out 2>&1; echo "exit $?" >> $O/r4_ruff_check.out
.venv/bin/ruff format --check . > $O/r4_ruff_format.out 2>&1; echo "exit $?" >> $O/r4_ruff_format.out
$PY -m mypy --no-incremental > $O/r4_mypy.out 2>&1; echo "exit $?" >> $O/r4_mypy.out
$PY tools/verify_refs.py --offline > $O/r4_verify_refs_offline_all.out 2>&1; echo "exit $?" >> $O/r4_verify_refs_offline_all.out
$PY tools/verify_refs.py --unit M5 > $O/r4_verify_refs_M5_live.out 2>&1; echo "exit $?" >> $O/r4_verify_refs_M5_live.out
$PY -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q > $O/r4_pytest_M5_relevant.out 2>&1; echo "exit $?" >> $O/r4_pytest_M5_relevant.out
$PY tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04 > $O/r4_page_smoke_M5_a.out 2>&1; echo "exit $?" >> $O/r4_page_smoke_M5_a.out
$PY tools/build_site.py --check > $O/r4_build_site_check.out 2>&1; echo "exit $?" >> $O/r4_build_site_check.out
$PY tools/render_curriculum.py > $O/r4_render_curriculum.out 2>&1; echo "exit $?" >> $O/r4_render_curriculum.out
git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json > $O/r4_render_curriculum_diff.out 2>&1; echo "exit $?" >> $O/r4_render_curriculum_diff.out
echo GATES_DONE > $O/r4_GATES_DONE
