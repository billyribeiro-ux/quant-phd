#!/bin/bash
# Usage: run_mutants.sh <mutants dir>. For each mutant, runs the suite on seeds 0-4 and reports KILLED (with the first failing test) or SURVIVED.
MDIR="$1"
S=/tmp/verify8-AC1-d/ledgers/AC1/scripts/AC1-d-r8/run_suite.sh
for f in "$MDIR"/m*.py; do
  name=$(basename "$f" .py)
  killed=""
  for seed in 0 1 2 3 4; do
    out=$(QF_SEED=$seed $S "$f" /tmp/AC1-v8/AC1-d/mut/$name $seed run 2>&1)
    if ! echo "$out" | grep -q " passed in" || echo "$out" | grep -q "failed"; then
      killed="KILLED seed $seed: $(cd /tmp/AC1-v8/AC1-d/mut/$name && QF_SEED=$seed /tmp/verify8-AC1-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error -rf test_project.py 2>&1 | grep '^FAILED' | head -1 | cut -c1-160)"
      break
    fi
  done
  echo "$name: ${killed:-SURVIVED (seeds 0-4)}"
done
