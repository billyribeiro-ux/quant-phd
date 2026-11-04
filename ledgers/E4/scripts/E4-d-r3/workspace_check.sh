#!/bin/sh
# Layout check for grader/test_project.py: copies it with instance.py and reference.py (as solver.py) into a scratch
# directory, runs strict mypy there (the local-run layout), collects the tests, and runs the suite on seeds 0-49.
# Usage: sh ledgers/E4/scripts/E4-d-r3/workspace_check.sh <repo-root>
set -u
ROOT="$1"
PY="$ROOT/.venv/bin/python"
W=$(mktemp -d /tmp/e4d3-ws-XXXX)
cp "$ROOT/course/modules/E/E4/grader/test_project.py" "$ROOT/course/modules/E/E4/grader/instance.py" "$W/"
cp "$ROOT/course/modules/E/E4/grader/reference.py" "$W/solver.py"
cd "$W" || exit 1
echo "== strict mypy (local layout)"
"$ROOT/.venv/bin/mypy" --strict --no-incremental test_project.py solver.py instance.py; echo "mypy exit=$?"
echo "== collect-only"
"$PY" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -2
echo "== suite seeds 0-49 with reference"
fails=0
for s in $(seq 0 49); do
  QF_SEED=$s "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > /tmp/e4d3-seed-$s.txt 2>&1 || { fails=$((fails+1)); echo "seed $s failed"; }
done
echo "reference seeds failing: $fails"
rm -rf "$W"
