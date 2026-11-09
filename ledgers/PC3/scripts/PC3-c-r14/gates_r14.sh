#!/bin/sh
# The exact commands run for the round-14 PC3 slice-c verification, from the checkout root.
# Each one was run once in this round; the outputs are under ledgers/PC3/scripts/PC3-c-r14/out/.
set -u
P=.venv/bin/python
O=ledgers/PC3/scripts/PC3-c-r14/out
$P tools/check_pages.py --unit PC3 > $O/check_pages.out 2>&1
$P tools/check_dag.py --unit PC3 > $O/check_dag.out 2>&1
$P tools/check_projects.py --unit PC3 > $O/check_projects.out 2>&1
$P tools/run_labs.py --unit PC3 --page project > $O/run_labs_project.out 2>&1
$P tools/run_graders.py --unit PC3 --seeds 0-49 > $O/run_graders.out 2>&1
$P tools/page_smoke.py --unit PC3 --pages project.html > $O/page_smoke_project.out 2>&1
$P tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1
$P tools/mutate_graders.py --unit PC3 --seeds 0-49 > $O/mutate_PC3_0-49_all_r14.out 2>&1
.venv/bin/ruff check course/modules/PC/PC3/grader tests/labs/PC3 tests > $O/ruff_check.out 2>&1
.venv/bin/ruff format --check course/modules/PC/PC3/grader tests/labs/PC3 tests > $O/ruff_format.out 2>&1
.venv/bin/mypy --no-incremental > $O/mypy_repo.out 2>&1
$P -m pytest -p no:cacheprovider -k PC3 > $O/pytest_k_PC3.out 2>&1
# collect-only counts and the reference suite, in scratch copies (see the commands in build notes):
#   for s in 0 7 49 100: copy grader engine.py instance.py test_project.py and reference.py as market_maker.py,
#   then QF_SEED=$s python -B -m pytest --collect-only -q -p no:cacheprovider test_project.py  -> out/collect_counts_r14.out
# starter stubs: copy starter.py as market_maker.py with the suite, QF_SEED=0 pytest -> out/starter_fails_r14.out
# mypy --strict on the four scratch modules (engine, instance, reference as market_maker, test_project) -> out/mypy_strict_scratch.out
$P ledgers/PC3/scripts/PC3-c-r14/run_alts_r14.py "$PWD" $(ls ledgers/PC3/alternatives/*.py) $(ls ledgers/PC3/scripts/PC3-c-r14/alts/*.py) $(ls ledgers/PC3/scripts/PC3-c-r13/alts/*.py) > $O/alts_r14.out 2>&1
