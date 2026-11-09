#!/bin/sh
# Round-1 delta verifier (M3 slice d), pin 95f3f8cb. Gate commands; run from the checkout root.
ROOT="$(pwd)"
OUT="$ROOT/ledgers/M3/scripts/M3-d-r1/out"
PY="$ROOT/.venv/bin/python"
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "EXIT $?" >> "$OUT/$name.out"; echo "$name: $(tail -2 "$OUT/$name.out" | tr '\n' ' ')"; }
run check_pages_M3 "$PY" tools/check_pages.py --unit M3
run check_dag_M3 "$PY" tools/check_dag.py --unit M3
run check_projects_M3 "$PY" tools/check_projects.py --unit M3
run run_labs_M3 "$PY" tools/run_labs.py --unit M3
run run_graders_M3 "$PY" tools/run_graders.py --unit M3 --seeds 0-49
run page_smoke_project "$PY" tools/page_smoke.py --unit M3 --pages project
run ruff_check "$PY" -m ruff check tests/labs/M3 course/modules/M/M3/grader
run ruff_format "$PY" -m ruff format --check tests/labs/M3 course/modules/M/M3/grader
run mypy "$PY" -m mypy --no-incremental
run verify_refs_offline "$PY" tools/verify_refs.py --offline
run collect_only_M3 "$PY" -m pytest --collect-only -q course/modules/M/M3/grader/test_project.py
