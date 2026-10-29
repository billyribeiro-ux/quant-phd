Round 8, slice M5-a, checkout pin ce7b382 (delta base 7aa909e = round-7 pin)
Interpreter: .venv -> /Users/billyribeiro/.fanout/wt/quant-b2/.venv (python 3.14)
.venv/bin/python tools/check_pages.py --all        -> check_pages M5: PASS        [gates.out]
.venv/bin/python tools/check_dag.py --all          -> check_dag M5: PASS          [gates.out]
.venv/bin/python tools/check_projects.py --all     -> check_projects M5: PASS     [gates.out]
.venv/bin/python tools/run_labs.py --unit M5       -> run_labs M5: PASS (13/13)   [gates.out]
.venv/bin/python tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04 --skip-sweep -> page_smoke M5: PASS [gates.out]
env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 .venv/bin/python -I -W error tests/labs/M5/lab-M5-L0{1..4}-1.py
    -> exit 0 each, stderr 0 bytes; stdout L01.out 17 lines, L02.out 7, L03.out 5, L04.out 11
.venv/bin/ruff check .                             -> All checks passed!          [ruff.out]
.venv/bin/ruff format --check .                    -> 362 files already formatted
.venv/bin/mypy --no-incremental                    -> Success: no issues found in 255 source files [mypy.out]
.venv/bin/pytest tests/test_labs.py -k M5 -o addopts=""  -> 13 passed, 227 deselected [pytest_labs_M5.out]
.venv/bin/pytest tests/test_page_checks.py tests/test_docs_figures.py -o addopts="" -> 55 passed [pytest_page_docs.out]
.venv/bin/python tools/verify_refs.py --offline    -> offline integrity: 560 entries, 0 problems (live run not performed)
.venv/bin/python tools/build_site.py --check       -> site data current: 6 outputs [build_site_check.out]
sh xref_bS.sh <checkout>                           -> B(S) cross-reference evidence [xref_bS.out]
