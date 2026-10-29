#!/bin/sh
# Round-12 check: each of the five alternative correct implementations, and the reference, must pass the
# FC1 suite on seeds 0-19 under the browser flags; prints the collect-only count. Run from the checkout root.
set -u
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
PY="$ROOT/.venv/bin/python"
G="$ROOT/course/modules/FC/FC1/grader"
W=$(mktemp -d /tmp/fc1c12_alts.XXXXXX)
cp "$G/test_project.py" "$G/instance.py" "$W/"
echo "collect:"; (cd "$W" && cp "$G/reference.py" instruments.py && "$PY" -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1)
for f in "$ROOT"/ledgers/FC1/alternatives/*.py "$G/reference.py"; do
  cp "$f" "$W/instruments.py"
  fails=0
  for s in $(seq 0 19); do
    if ! (cd "$W" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then fails=$((fails+1)); fi
  done
  echo "$(basename "$f"): failing seeds $fails of 20"
done
rm -rf "$W"
