#!/bin/bash
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
D=$(mktemp -d /tmp/e4d21-collect.XXXXXX)
cp "$ROOT/course/modules/E/E4/grader/instance.py" "$ROOT/course/modules/E/E4/grader/test_project.py" "$D/"
cp "$ROOT/course/modules/E/E4/grader/reference.py" "$D/solver.py"
cd "$D" && QF_SEED=0 "$ROOT/.venv/bin/python" -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -2
grep -c "^def test_" "$D/test_project.py"
