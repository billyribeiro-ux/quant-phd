#!/bin/sh
# Round-3 verifier (E3-d): CPython per-test durations of the grader on seed 0, in a scratch copy with the reference as elicit.py.
set -eu
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
W=/tmp/e3d_r3_durations; rm -rf "$W"; mkdir -p "$W"
cp "$ROOT/course/modules/E/E3/grader/test_project.py" "$ROOT/course/modules/E/E3/grader/instance.py" "$W/"
cp "$ROOT/course/modules/E/E3/grader/reference.py" "$W/elicit.py"
cd "$W" && QF_SEED=0 PYTHONDONTWRITEBYTECODE=1 "$ROOT/.venv/bin/python" -B -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py --durations=6 2>&1 | tail -10
