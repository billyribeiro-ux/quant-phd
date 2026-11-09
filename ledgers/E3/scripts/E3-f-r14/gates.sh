#!/bin/bash
# Round-14 mechanical gates for E3 slice f (L01-L04 + cards). Run from the checkout root.
cd "$(dirname "$0")/../../../.." || exit 1
OUT=ledgers/E3/scripts/E3-f-r14/out
mkdir -p "$OUT"
run() { name="$1"; shift; ( "$@" ) > "$OUT/$name.out" 2>&1; echo "$name rc=$?" >> "$OUT/summary.txt"; }
rm -f "$OUT/summary.txt"
run check_pages_unit .venv/bin/python tools/check_pages.py --unit E3
for p in L01 L02 L03 L04; do run check_pages_$p .venv/bin/python tools/check_pages.py --unit E3 --page $p; done
run check_dag_unit .venv/bin/python tools/check_dag.py --unit E3
run check_projects_unit .venv/bin/python tools/check_projects.py --unit E3
for p in L01 L02 L03 L04; do run run_labs_$p .venv/bin/python tools/run_labs.py --unit E3 --page $p; done
run ruff_check .venv/bin/ruff check tests/labs/E3 course/modules/E/E3/grader
run ruff_format .venv/bin/ruff format --check tests/labs/E3
run mypy .venv/bin/mypy --no-incremental
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run build_site_check .venv/bin/python tools/build_site.py --check
run render_curriculum .venv/bin/python tools/render_curriculum.py
run pytest_docs .venv/bin/pytest -q tests/test_docs_figures.py tests/test_refs.py
echo DONE >> "$OUT/summary.txt"
