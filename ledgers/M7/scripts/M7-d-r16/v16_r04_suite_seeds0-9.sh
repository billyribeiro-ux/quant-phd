#!/bin/sh
# Round-16 verifier: run the M7 grader suite against the equivalent/ mutant r04 on seeds 0-9 (scratch copy only).
# Usage (repository root): sh ledgers/M7/scripts/M7-d-r16/v16_r04_suite_seeds0-9.sh
set -e
ROOT="$(pwd)"
S=/private/tmp/v16-m7d/mut_r04
rm -rf "$S" && mkdir -p "$S"
cp course/modules/M/M7/grader/test_project.py course/modules/M/M7/grader/instance.py "$S/"
cp ledgers/M7/equivalent/r04_budget_left_out_of_primal_residual.py "$S/constrained_allocator.py"
cd "$S"
for s in 0 1 2 3 4 5 6 7 8 9; do QF_SEED=$s "$ROOT/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1; done
