#!/bin/sh
# Strict mypy on grader/test_project.py in the layout the local run uses (solver.py, instance.py beside it).
# Usage: sh ledgers/E4/scripts/E4-d-r2/workspace_mypy.sh <repo-root>
set -e
ROOT="$1"
W=$(mktemp -d /tmp/e4d2-ws-XXXX)
cp "$ROOT/course/modules/E/E4/grader/test_project.py" "$ROOT/course/modules/E/E4/grader/instance.py" "$W/"
cp "$ROOT/course/modules/E/E4/grader/reference.py" "$W/solver.py"
cd "$W"
"$ROOT/.venv/bin/mypy" --strict --no-incremental test_project.py solver.py instance.py || true
rm -rf "$W"
