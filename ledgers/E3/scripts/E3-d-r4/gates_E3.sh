#!/bin/sh
# Round-4 verifier (E3-d): gate commands run at pin 4eb6788, each output saved beside this script.
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
D="$ROOT/ledgers/E3/scripts/E3-d-r4"
cd "$ROOT" || exit 1
run() { name="$1"; shift; "$@" > "$D/$name.out" 2>&1; echo "EXIT $?" >> "$D/$name.out"; tail -2 "$D/$name.out" | sed "s/^/$name: /"; }
run check_dag_E3 .venv/bin/python tools/check_dag.py --unit E3
run check_projects_E3 .venv/bin/python tools/check_projects.py --unit E3
run check_pages_E3 .venv/bin/python tools/check_pages.py --unit E3
run run_labs_project .venv/bin/python tools/run_labs.py --unit E3 --page project
run run_labs_E3_all .venv/bin/python tools/run_labs.py --unit E3
run run_graders_E3_0_49 .venv/bin/python tools/run_graders.py --unit E3 --seeds 0-49
run page_smoke_project .venv/bin/python tools/page_smoke.py --unit E3 --pages project
run ruff_check .venv/bin/ruff check .
run ruff_format .venv/bin/ruff format --check .
run mypy_strict .venv/bin/mypy --no-incremental
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
