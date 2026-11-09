#!/bin/bash
# Round-1 (closing delta) mechanical gates for E3 slice g (L05-L08 + cards + twins). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyG1-E3-g || exit 1
OUT=ledgers/E3/scripts/E3-g-r1/out
mkdir -p "$OUT"
run() { name="$1"; shift; ( "$@" ) > "$OUT/$name.out" 2>&1; echo "$name rc=$?" >> "$OUT/summary.txt"; }
rm -f "$OUT/summary.txt"
for p in L05 L06 L07 L08; do run check_pages_$p .venv/bin/python tools/check_pages.py --unit E3 --page $p; done
run check_dag_unit .venv/bin/python tools/check_dag.py --unit E3
run check_projects_unit .venv/bin/python tools/check_projects.py --unit E3
for p in L05 L06 L07 L08; do run run_labs_$p .venv/bin/python tools/run_labs.py --unit E3 --page $p; done
run page_smoke_L05_L08 .venv/bin/python tools/page_smoke.py --unit E3 --pages L05 L06 L07 L08
run ruff_check .venv/bin/ruff check tests/labs/E3 course/modules/E/E3/grader
run ruff_format .venv/bin/ruff format --check tests/labs/E3
run mypy .venv/bin/mypy --no-incremental
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run build_site_check .venv/bin/python tools/build_site.py --check
run render_curriculum .venv/bin/python tools/render_curriculum.py
run render_curriculum_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run pytest_docs .venv/bin/pytest -q tests/test_docs_figures.py tests/test_refs.py
run pytest_labs_E3 .venv/bin/pytest -q tests -k "E3 or e3"
echo DONE >> "$OUT/summary.txt"
