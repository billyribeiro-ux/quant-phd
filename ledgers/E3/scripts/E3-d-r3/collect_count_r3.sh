#!/bin/sh
# Round-3 verifier (E3-d): pytest --collect-only count of grader/test_project.py, run in a scratch directory.
set -eu
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
W=/tmp/e3d_r3_collect; rm -rf "$W"; mkdir -p "$W"
cp "$ROOT/course/modules/E/E3/grader/test_project.py" "$ROOT/course/modules/E/E3/grader/instance.py" "$W/"
cp "$ROOT/course/modules/E/E3/grader/reference.py" "$W/elicit.py"
cd "$W" && QF_SEED=0 PYTHONDONTWRITEBYTECODE=1 "$ROOT/.venv/bin/python" -B -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1
