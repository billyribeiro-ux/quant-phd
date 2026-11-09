#!/bin/bash
# Round-1 independent verifier (M2-e closing delta, pin 2a805c83, base 95f3f8cb): slice gates, one output file per command.
R=/Users/billyribeiro/.fanout/wt/verifyG1-M2-e
O=$R/ledgers/M2/scripts/M2-e-r1
P=$R/.venv/bin/python
cd "$R" || exit 1
run() { name=$1; shift; { "$@"; echo "exit $?"; } > "$O/g1_$name.out" 2>&1; echo "$name: $(tail -1 "$O/g1_$name.out")"; }
run check_pages $P tools/check_pages.py --unit M2
run check_dag $P tools/check_dag.py --unit M2
run check_projects $P tools/check_projects.py --unit M2
run run_graders $P tools/run_graders.py --unit M2 --seeds 0-49
run run_labs_M2 $P tools/run_labs.py --unit M2
run build_site_check $P tools/build_site.py --check
run render_curriculum_check bash -c "$P tools/render_curriculum.py && git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json"
run fetch_data_check $P tools/fetch_data.py --check
run verify_refs_offline $P tools/verify_refs.py --offline
run ruff_labs $P -m ruff check tests/labs/M2 course/modules/M/M2/grader
run ruff_format $P -m ruff format --check tests/labs/M2 course/modules/M/M2/grader
run mypy_labs $P -m mypy tests/labs/M2 --no-incremental
run mypy_grader_strict bash -c "d=\$(mktemp -d) && cp $R/course/modules/M/M2/grader/test_project.py $R/course/modules/M/M2/grader/instance.py \"\$d\"/ && cp $R/course/modules/M/M2/grader/reference.py \"\$d\"/sensitivity_engine.py && $P -m mypy --strict --no-incremental \"\$d\"/test_project.py \"\$d\"/instance.py \"\$d\"/sensitivity_engine.py"
run pytest_labs $P -m pytest -q tests/test_labs.py tests/test_run_labs.py -k M2
run grader_collect bash -c "cd $R/course/modules/M/M2/grader && $P -m pytest --collect-only -q -p no:cacheprovider test_project.py | tail -3"
run grader_pytest_seed0 bash -c "cd $R/course/modules/M/M2/grader && QF_SEED=0 $P -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py | tail -3"
run page_smoke_M2 $P tools/page_smoke.py --unit M2
echo DONE_FAST
