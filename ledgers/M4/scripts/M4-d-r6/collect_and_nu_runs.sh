#!/bin/sh
# Round-6 verifier (slice d): collect-only count and the seed-0 (nu 4) and seed-1093 (nu 3) runs of the grader suite.
# Usage (from the checkout root): sh ledgers/M4/scripts/M4-d-r6/collect_and_nu_runs.sh
set -u
ROOT=$(pwd)
PY="$ROOT/.venv/bin/python"
WORK=$(mktemp -d /tmp/m4d6-collect-XXXXXX)
cp "$ROOT/course/modules/M/M4/grader/test_project.py" "$ROOT/course/modules/M/M4/grader/instance.py" "$WORK/"
cp "$ROOT/course/modules/M/M4/grader/reference.py" "$WORK/tail_risk.py"
cd "$WORK" || exit 1
"$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py | tail -n 1
for s in 0 1093; do
  echo "seed $s:"
  QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py | tail -n 1
done
rm -rf "$WORK"
