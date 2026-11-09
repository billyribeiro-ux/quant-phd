#!/bin/sh
# Gates for the E3 project slice at the verifier pin. Run from the checkout root.
D=ledgers/E3/scripts/E3-d-r18
P=.venv/bin/python
run() { name="$1"; shift; "$@" > "$D/$name.out" 2>&1; rc=$?; echo "EXIT=$rc" >> "$D/$name.out"; echo "== $name rc=$rc: $(tail -2 "$D/$name.out" | tr '\n' ' ' | cut -c1-240)"; }
run check_pages $P tools/check_pages.py --unit E3
run check_dag $P tools/check_dag.py --unit E3
run check_projects $P tools/check_projects.py --unit E3
run run_graders_0_49 $P tools/run_graders.py --unit E3 --seeds 0-49
run run_labs_project $P tools/run_labs.py --unit E3 --page project
run page_smoke_project $P tools/page_smoke.py --unit E3 --pages project
run verify_refs_offline $P tools/verify_refs.py --offline
run ruff_check .venv/bin/ruff check course/modules/E/E3/grader tests/labs/E3
run ruff_format .venv/bin/ruff format --check course/modules/E/E3/grader tests/labs/E3
run mypy_grader .venv/bin/mypy --strict --no-incremental course/modules/E/E3/grader
run mypy_repo .venv/bin/mypy --no-incremental
W=$(mktemp -d /tmp/e3d-r18-collect.XXXXXX)
cp course/modules/E/E3/grader/test_project.py course/modules/E/E3/grader/instance.py $W/
cp course/modules/E/E3/grader/reference.py $W/elicit.py
R=$(pwd)
run collect_only sh -c "cd $W && QF_SEED=0 $R/.venv/bin/python -m pytest --collect-only -q -p no:cacheprovider test_project.py | tail -3"
rm -rf "$W"
echo ALLDONE
