#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyE6-SC1-b
O=ledgers/SC1/scripts/SC1-b-r6/out
PY=.venv/bin/python
{ echo "\$ check_pages --unit SC1"; $PY tools/check_pages.py --unit SC1; echo "exit=$?"; } > $O/check_pages.out 2>&1
{ echo "\$ check_dag --unit SC1"; $PY tools/check_dag.py --unit SC1; echo "exit=$?"; } > $O/check_dag.out 2>&1
{ echo "\$ check_projects --unit SC1"; $PY tools/check_projects.py --unit SC1; echo "exit=$?"; } > $O/check_projects.out 2>&1
{ echo "\$ run_labs --unit SC1 --page L04.html"; $PY tools/run_labs.py --unit SC1 --page L04.html; echo "exit=$?"; } > $O/run_labs_L04.out 2>&1
{ echo "\$ run_labs --unit SC1 --page L05.html"; $PY tools/run_labs.py --unit SC1 --page L05.html; echo "exit=$?"; } > $O/run_labs_L05.out 2>&1
{ echo "\$ run_labs --unit SC1 --page L06.html"; $PY tools/run_labs.py --unit SC1 --page L06.html; echo "exit=$?"; } > $O/run_labs_L06.out 2>&1
for t in L04 L05 L06; do
  { echo "\$ python -I -W error tests/labs/SC1/lab-SC1-$t-1.py (cwd scratch)"; d=$(mktemp -d); cp -R course/assets/data "$d/data" 2>/dev/null; (cd "$d" && /usr/bin/env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 "$OLDPWD/$PY" -I -W error "$OLDPWD/tests/labs/SC1/lab-SC1-$t-1.py"; echo "exit=$?"); } > $O/twin_$t.out 2>$O/twin_$t.stderr
done
{ echo "\$ ruff check/format twins"; $PY -m ruff check tests/labs/SC1/lab-SC1-L04-1.py tests/labs/SC1/lab-SC1-L05-1.py tests/labs/SC1/lab-SC1-L06-1.py; echo "exit=$?"; $PY -m ruff format --check tests/labs/SC1/lab-SC1-L04-1.py tests/labs/SC1/lab-SC1-L05-1.py tests/labs/SC1/lab-SC1-L06-1.py; echo "exit=$?"; } > $O/ruff_twins.out 2>&1
{ echo "\$ mypy --no-incremental twins"; $PY -m mypy --no-incremental tests/labs/SC1/lab-SC1-L04-1.py tests/labs/SC1/lab-SC1-L05-1.py tests/labs/SC1/lab-SC1-L06-1.py; echo "exit=$?"; } > $O/mypy_twins.out 2>&1
{ echo "\$ pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q"; $PY -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q -k "SC1 or SC1-" ; echo "exit=$?"; } > $O/pytest_tooling.out 2>&1
{ echo "\$ verify_refs --offline --unit SC1"; $PY tools/verify_refs.py --offline --unit SC1; echo "exit=$?"; } > $O/verify_refs.out 2>&1
echo DONE > $O/cmds.done
