#!/bin/bash
# Round 18: alternatives alt_1..alt_8, the five equivalents and the reference on seeds 0-49, with the edited suite.
cd "$(dirname "$0")/../../../.." || exit 1
export E4_ROOT="$(pwd)"
PY="$(pwd)/.venv/bin/python"
O=ledgers/E4/scripts/E4-d-r18/out/cand
for f in ledgers/E4/alternatives/alt_*.py; do
  n=$(basename "$f" .py)
  "$PY" -I ledgers/E4/scripts/E4-d-r17/run_candidate_r17.py "$f" 0-49 > "$O/$n.txt" 2>&1
  echo "$n: $(head -1 "$O/$n.txt")"
done
for f in ledgers/E4/equivalent/*.py; do
  n=$(basename "$f" .py)
  "$PY" -I ledgers/E4/scripts/E4-d-r17/run_candidate_r17.py "$f" 0-49 > "$O/eq_$n.txt" 2>&1
  echo "eq_$n: $(head -1 "$O/eq_$n.txt")"
done
"$PY" -I ledgers/E4/scripts/E4-d-r17/run_candidate_r17.py course/modules/E/E4/grader/reference.py 0-49 > "$O/reference.txt" 2>&1
echo "reference: $(head -1 "$O/reference.txt")"
echo ALLDONE
