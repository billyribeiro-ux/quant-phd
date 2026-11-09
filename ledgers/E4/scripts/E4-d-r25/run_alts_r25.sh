#!/bin/bash
# Round 25 (ruling 25): reference, alternatives alt_1..alt_8 and the moved equivalent mutant_r19_02 on seeds 0-49.
cd "$(dirname "$0")/../../../.." || exit 1
export E4_ROOT="$(pwd)"
PY="$(pwd)/.venv/bin/python"
O=ledgers/E4/scripts/E4-d-r25/out
mkdir -p "$O"
"$PY" -I ledgers/E4/scripts/E4-d-r17/run_candidate_r17.py course/modules/E/E4/grader/reference.py 0-49 > "$O/reference.txt" 2>&1
echo "reference: $(head -1 "$O/reference.txt")"
for f in ledgers/E4/alternatives/alt_*.py; do
  n=$(basename "$f" .py)
  "$PY" -I ledgers/E4/scripts/E4-d-r17/run_candidate_r17.py "$f" 0-49 > "$O/$n.txt" 2>&1
  echo "$n: $(head -1 "$O/$n.txt")"
done
f=ledgers/E4/equivalent/mutant_r19_02_price_denominator_drops_uninformed_posterior_precision.py
"$PY" -I ledgers/E4/scripts/E4-d-r17/run_candidate_r17.py "$f" 0-49 > "$O/equiv_r19_02_0_49.txt" 2>&1
echo "equiv_r19_02: $(head -1 "$O/equiv_r19_02_0_49.txt")"
echo ALLDONE
