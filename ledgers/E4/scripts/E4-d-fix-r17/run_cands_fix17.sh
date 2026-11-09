#!/bin/bash
# Fixer round 17: the E4 project suite (grader/test_project.py, as edited in this round) against the reference,
# alternatives alt_1..alt_8 and the equivalents, seeds 0-49, via the verifier's run_candidate_r17.py (same flags).
cd "$(dirname "$0")/../../../.." || exit 1
export E4_ROOT="$(pwd)"
PY="$(pwd)/.venv/bin/python"
RUNNER="$(pwd)/ledgers/E4/scripts/E4-d-r17/run_candidate_r17.py"
O="$(pwd)/ledgers/E4/scripts/E4-d-fix-r17/out/cand"
mkdir -p "$O"
run_one() {
  "$PY" "$RUNNER" "$1" 0-49 > "$O/$2.txt" 2>&1
}
run_one course/modules/E/E4/grader/reference.py reference &
for f in ledgers/E4/alternatives/alt_*.py; do run_one "$f" "$(basename "$f" .py)" & done
for f in ledgers/E4/equivalent/*.py; do run_one "$f" "eq_$(basename "$f" .py)" & done
wait
for f in "$O"/*.txt; do echo "$(basename "$f" .txt): $(head -1 "$f")"; done
echo ALLDONE
