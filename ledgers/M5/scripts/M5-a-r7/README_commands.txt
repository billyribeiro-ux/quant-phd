Round 7, slice M5-a, checkout pin 7aa909e (delta base 44f1eb6 = round-6 pin)
Interpreter: .venv -> /Users/billyribeiro/.local/share/mise/installs/python/3.14.8/bin/python3.14
.venv/bin/python tools/check_pages.py --all             -> check_pages M5: PASS
.venv/bin/python tools/check_dag.py --all               -> check_dag M5: PASS
.venv/bin/python tools/check_projects.py --all          -> check_projects M5: PASS
.venv/bin/python tools/run_labs.py --unit M5            -> run_labs M5: PASS (13/13)   [run_labs_M5.out]
.venv/bin/python tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04 --skip-sweep -> page_smoke M5: PASS [page_smoke_M5a.out]
env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 <venv python> -I -W error tests/labs/M5/lab-M5-L0{1..4}-1.py -> exit 0, stderr 0 bytes [L0n.out]
  (first attempt used /usr/bin/python3 and failed with SyntaxError on PEP 695 generics; harness error, rerun with the venv interpreter)
.venv/bin/ruff check .                                   -> All checks passed!
.venv/bin/ruff format --check .                          -> 362 files already formatted
.venv/bin/mypy --no-incremental                          -> Success: no issues found in 255 source files
.venv/bin/pytest -q tests/test_labs.py -k M5             -> 13 passed
.venv/bin/pytest -q tests/test_page_checks.py tests/test_docs_figures.py -> passed
.venv/bin/python tools/verify_refs.py --offline          -> offline integrity: 560 entries, 0 problems
