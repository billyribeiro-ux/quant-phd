#!/bin/bash
# FC1-b round 5 gate runs. Run from the checkout root. Each command's exit code is recorded in out/_rc.txt.
cd "$(dirname "$0")/../../../.." || exit 1
OUT=ledgers/FC1/scripts/FC1-b-r5/out
mkdir -p "$OUT"
rm -f "$OUT/_rc.txt"
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "$name rc=$?" >> "$OUT/_rc.txt"; }
run check_pages_L04 .venv/bin/python tools/check_pages.py --unit FC1 --page L04
run check_pages_L05 .venv/bin/python tools/check_pages.py --unit FC1 --page L05
run check_pages_unit .venv/bin/python tools/check_pages.py --unit FC1
run check_dag_FC1 .venv/bin/python tools/check_dag.py --unit FC1
run check_projects_FC1 .venv/bin/python tools/check_projects.py --unit FC1
run run_labs_L04 .venv/bin/python tools/run_labs.py --unit FC1 --page L04
run run_labs_L05 .venv/bin/python tools/run_labs.py --unit FC1 --page L05
run run_labs_FC1 .venv/bin/python tools/run_labs.py --unit FC1
run twin_L04_isolated env -i PATH=/usr/bin:/bin .venv/bin/python -I -W error tests/labs/FC1/lab-FC1-L04-1.py
run twin_L05_isolated env -i PATH=/usr/bin:/bin .venv/bin/python -I -W error tests/labs/FC1/lab-FC1-L05-1.py
run ruff_labs .venv/bin/ruff check tests/labs/FC1
run ruff_format_labs .venv/bin/ruff format --check tests/labs/FC1
run mypy_labs .venv/bin/mypy --no-incremental tests/labs/FC1/lab-FC1-L04-1.py tests/labs/FC1/lab-FC1-L05-1.py
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run build_site_check .venv/bin/python tools/build_site.py --check
run page_smoke_L04_L05 .venv/bin/python tools/page_smoke.py --unit FC1 --pages L04 L05
