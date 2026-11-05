#!/bin/bash
# Round-9 gates for E3 slice e, run from the verifier checkout root (pin 1e272e5a). Each command's exit code is printed.
cd /Users/billyribeiro/.fanout/wt/verifyD9-E3-e || exit 1
P=.venv/bin/python
run() { echo "== $*"; "$@"; echo "exit=$?"; }
run $P tools/check_pages.py --unit E3
run $P tools/check_dag.py --unit E3
run $P tools/check_projects.py --unit E3
run $P tools/run_labs.py --unit E3
run $P tools/verify_refs.py --offline
run $P tools/page_smoke.py --unit E3 --pages project
run $P -m ruff check course/modules/E/E3 tests/labs/E3
run $P -m ruff format --check course/modules/E/E3/grader tests/labs/E3
run $P -m mypy --no-incremental
run $P -m pytest -q -p no:cacheprovider tests/test_labs.py -k E3
