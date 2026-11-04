#!/bin/bash
# Round-6 remaining gate runs for SC1 slice d (run from the verifier checkout root). Outputs go to out/.
set -u
cd /Users/billyribeiro/.fanout/wt/verifyE6-SC1-d || exit 1
O=ledgers/SC1/scripts/SC1-d-r6/out
PY=.venv/bin/python
W=/tmp/sc1d_r6_suite
rm -rf "$W" && mkdir -p "$W"
cp course/modules/SC/SC1/grader/test_project.py course/modules/SC/SC1/grader/instance.py "$W"/
cp course/modules/SC/SC1/grader/reference.py "$W"/bm_checks.py
( cd "$W" && "$OLDPWD/$PY" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1 ) > "$OLDPWD/$O/collect_test_project_r6.txt"
( cd "$W" && QF_SEED=0 "$OLDPWD/$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 ) > "$OLDPWD/$O/suite_reference_seed0_r6.txt"
cp course/modules/SC/SC1/grader/starter.py "$W"/bm_checks.py
( cd "$W" && QF_SEED=0 "$OLDPWD/$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 ) > "$OLDPWD/$O/suite_starter_seed0_r6.txt"
rm -rf "$W"
$PY tools/page_smoke.py --unit SC1 --pages project > $O/page_smoke_SC1_project_r6.txt 2>&1; echo "exit $?" >> $O/page_smoke_SC1_project_r6.txt
$PY -m ruff --version >/dev/null 2>&1; .venv/bin/ruff check . > $O/ruff_check.txt 2>&1; echo "exit $?" >> $O/ruff_check.txt
.venv/bin/ruff format --check . > $O/ruff_format.txt 2>&1; echo "exit $?" >> $O/ruff_format.txt
.venv/bin/mypy --no-incremental > $O/mypy_full.txt 2>&1; echo "exit $?" >> $O/mypy_full.txt
.venv/bin/pytest -q -p no:cacheprovider tests/test_labs.py -k SC1 tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py > $O/pytest_related_r6.txt 2>&1; echo "exit $?" >> $O/pytest_related_r6.txt
$PY tools/verify_refs.py --offline > $O/verify_refs_offline_all.txt 2>&1; echo "exit $?" >> $O/verify_refs_offline_all.txt
$PY tools/verify_refs.py --unit SC1 > $O/verify_refs_live_SC1_r6.txt 2>&1; echo "exit $?" >> $O/verify_refs_live_SC1_r6.txt
