#!/bin/bash
# Round 11: run each correct alternative solver (ledgers/E4/alternatives/alt_N.py) as solver.py under the public suite,
# for seeds 0-49. Each alternative is copied with the grader files into a fresh scratch directory outside the checkout.
CHECKOUT="$(cd "$(dirname "$0")/../../../.." && pwd)"
PY="$CHECKOUT/.venv/bin/python"
for alt in 1 2 3 4 5; do
  D="$(mktemp -d /tmp/e4r11alt.XXXXXX)"
  cp "$CHECKOUT/course/modules/E/E4/grader/test_project.py" "$CHECKOUT/course/modules/E/E4/grader/instance.py" "$D/"
  cp "$CHECKOUT/ledgers/E4/alternatives/alt_$alt.py" "$D/solver.py"
  pass=0; fail=0
  for seed in $(seq 0 49); do
    if (cd "$D" && QF_SEED=$seed "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); echo "alt_$alt seed $seed FAILED"; fi
  done
  echo "alt_$alt seeds0-49 passed=$pass failed=$fail"
done
