#!/bin/bash
# Round-5 independent verifier gate runs for FC2 slice b (L04-L06, twins, cards). Run from the checkout root.
set -u
OUT=ledgers/FC2/scripts/FC2-b-r5
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$OUT/$name.txt" 2>&1; echo "$name exit=$?" >> "$OUT/gate_exit_codes.txt"; }
rm -f "$OUT/gate_exit_codes.txt"
run check_pages $PY tools/check_pages.py --unit FC2
run check_dag $PY tools/check_dag.py --unit FC2
run check_projects $PY tools/check_projects.py --unit FC2
run run_labs_unit $PY tools/run_labs.py --unit FC2
run run_labs_L04 $PY tools/run_labs.py --unit FC2 --page L04
run run_labs_L05 $PY tools/run_labs.py --unit FC2 --page L05
run run_labs_L06 $PY tools/run_labs.py --unit FC2 --page L06
run page_smoke_L04 $PY tools/page_smoke.py --unit FC2 --pages L04
run page_smoke_L05 $PY tools/page_smoke.py --unit FC2 --pages L05
run page_smoke_L06 $PY tools/page_smoke.py --unit FC2 --pages L06
run twin_L04_isolated $PY -I -W error tests/labs/FC2/lab-FC2-L04-1.py
run twin_L05_isolated $PY -I -W error tests/labs/FC2/lab-FC2-L05-1.py
run twin_L06_isolated $PY -I -W error tests/labs/FC2/lab-FC2-L06-1.py
run ruff_check $PY -m ruff check tests/labs/FC2
run ruff_format $PY -m ruff format --check tests/labs/FC2
run mypy $PY -m mypy --no-incremental
run pytest_fc2 $PY -m pytest tests/test_labs.py -k FC2 -q
run verify_refs_offline $PY tools/verify_refs.py --offline
run pytest_page_checks $PY -m pytest tests/test_page_checks.py tests/test_run_labs.py -q
run run_graders_fc2 $PY tools/run_graders.py --unit FC2 --seeds 0-49
echo DONE >> "$OUT/gate_exit_codes.txt"
