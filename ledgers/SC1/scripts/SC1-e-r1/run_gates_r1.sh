#!/bin/sh
# Slice e round 1 gates, run from the checkout root. Output in out/.
CO=/Users/billyribeiro/.fanout/wt/verifyF31-SC1-e
OUT="$CO/ledgers/SC1/scripts/SC1-e-r1/out"
PY="$CO/.venv/bin/python"
cd "$CO" || exit 1
run() { name="$1"; shift; "$@" > "$OUT/$name.txt" 2>&1; echo "exit $?" >> "$OUT/$name.txt"; }
run check_pages "$PY" tools/check_pages.py --unit SC1
run check_dag "$PY" tools/check_dag.py --unit SC1
run check_projects_SC1 "$PY" tools/check_projects.py --unit SC1
run run_labs "$PY" tools/run_labs.py --unit SC1
run page_smoke_L01_L08 "$PY" tools/page_smoke.py --unit SC1 --pages L01 L02 L03 L04 L05 L06 L07 L08
run build_site_check "$PY" tools/build_site.py --check
run verify_refs_offline "$PY" tools/verify_refs.py --offline
run ruff_labs_sc1 "$PY" -m ruff check tests/labs/SC1
run ruff_format_labs_sc1 "$PY" -m ruff format --check tests/labs/SC1
echo done > "$OUT/GATES_DONE"
