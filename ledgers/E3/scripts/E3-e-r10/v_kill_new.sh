#!/bin/bash
# Verifier r10: run each NEW mutant (r10f_*) against the E3 suite in a scratch dir, seeds 0-9 (killed on first failing seed).
cd /Users/billyribeiro/.fanout/wt/verifyD10-E3-e || exit 1
G=course/modules/E/E3/grader
for m in ledgers/E3/mutants/r10f_*.py; do
  name=$(basename "$m" .py)
  W=/tmp/e3e_r10/kill_$name; rm -rf "$W"; mkdir -p "$W"
  cp "$m" "$W/elicit.py"; cp $G/test_project.py $G/instance.py "$W/"
  killed=""
  for s in 0 1 2 3 4 5 6 7 8 9 49 30; do
    out=$(cd "$W" && QF_SEED=$s /Users/billyribeiro/.fanout/wt/verifyD10-E3-e/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
    if echo "$out" | grep -q "failed"; then
      killed="seed $s: $(echo "$out" | grep -E '^FAILED' | head -1 | cut -c1-220)"; break
    fi
  done
  echo "$name -> ${killed:-SURVIVED seeds 0-9,49,30}"
done
