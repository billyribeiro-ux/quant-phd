#!/bin/sh
# Runs the grader suite (copied from grader/) against each alternative implementation over seeds 0-49.
# Usage: sh run_alts.sh <checkout>   (run from the checkout root; scratch copies go to /tmp/M2-v/M2-e-r2)
CK="$1"
G="$CK/course/modules/M/M2/grader"
W=/tmp/M2-v/M2-e-r2/alts
for a in alt1 alt2 alt3 alt4 alt5; do
  mkdir -p "$W/$a" && cp "$G/instance.py" "$G/test_project.py" "$W/$a/" && cp "$CK/ledgers/M2/scripts/M2-e-r2/alts/$a/sensitivity_engine.py" "$W/$a/"
  echo "== $a"
  (cd "$W/$a" && for s in $(seq 0 49); do QF_SEED=$s "$CK/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1; done | sed 's/ in .*//' | sort | uniq -c)
done
