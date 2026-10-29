Round 6 (M7-d) commands, run from /Users/billyribeiro/.fanout/wt/verifyB6-M7-d (pin 44f1eb6) with .venv/bin/python:
tools/check_projects.py --unit M7 ; tools/check_pages.py --unit M7 ; tools/check_dag.py --unit M7 ; tools/run_graders.py --unit M7 --seeds 0-49
tools/run_labs.py --unit M7 ; ruff check tests/labs/M7 course/modules/M/M7/grader ; ruff format --check tests/labs/M7 course/modules/M/M7/grader
MYPYPATH=course/modules/M/M7/grader mypy --no-incremental --strict grader/reference.py grader/instance.py grader/starter.py tests/labs/M7/*.py
tools/mutate_graders.py --unit M7 --seeds 0-9 (logs/mutate_0_9.txt) ; tools/verify_refs.py --offline ; tools/page_smoke.py --unit M7
Scratch workspace /tmp/m7d_r6/ws (copies of grader/*.py outside the repo): pytest --collect-only per seed 0-49 gives 363 each.
Twin run: python -I -W error on each tests/labs/M7/lab-M7-L0N-1.py (logs/lab-M7-L0N-1.out); labcheck.py compares page code and expected output.
make_verifier_mutants_r6.py writes ledgers/M7/mutants/q01-q04. make_alt_float_r6.py writes alt_float/constrained_allocator.py.
cards_numbers_r6.py scans cards.json numbers against each lesson text.
