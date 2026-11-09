#!/bin/bash
# Round-1 closing delta gates for E5-d (verifier K1), run at pin f117a7a0.
cd /Users/billyribeiro/.fanout/wt/verifyK1-E5-d || exit 1
O=ledgers/E5/scripts/E5-d-r1/k1out
mkdir -p "$O"
run() { name=$1; shift; "$@" > "$O/$name.out" 2>&1; echo "exit $?" >> "$O/$name.out"; }
run ruff_check .venv/bin/ruff check .
run ruff_format .venv/bin/ruff format --check .
run mypy .venv/bin/mypy --no-incremental
run check_pages .venv/bin/python tools/check_pages.py --all
run check_dag .venv/bin/python tools/check_dag.py --all
run check_projects .venv/bin/python tools/check_projects.py --all
run run_labs_E5 .venv/bin/python tools/run_labs.py --unit E5
run page_smoke_E5 .venv/bin/python tools/page_smoke.py --unit E5
run render_curriculum .venv/bin/python tools/render_curriculum.py
run render_diff git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
run build_site_check .venv/bin/python tools/build_site.py --check
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run fetch_data_check .venv/bin/python tools/fetch_data.py --check
run mutate_graders_E5 .venv/bin/python tools/mutate_graders.py --unit E5
run pytest_labs_E5 .venv/bin/pytest tests/test_labs.py -k E5 -q
run pytest_memo_exemplars .venv/bin/pytest tests/test_memo_exemplars.py -q
run pytest_page_checks .venv/bin/pytest tests/test_page_checks.py -q
run pytest_page_smoke .venv/bin/pytest tests/test_page_smoke.py -q
run pytest_curriculum_cards .venv/bin/pytest tests/test_curriculum.py tests/test_docs_figures.py -q
run standing_mutants .venv/bin/python ledgers/E5/scripts/E5-d-r1/run_standing_mutants.py "$PWD"
echo DONE > "$O/_done"
