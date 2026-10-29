#!/bin/sh
# Stage grader files in a scratch dir (reference.py as elicit.py) and count real tests.
set -e
REPO="$(cd "$(dirname "$0")/../../../.." && pwd)"
W="$(mktemp -d /tmp/E3d-collect.XXXX)"
G="$REPO/course/modules/E/E3/grader"
cp "$G/test_project.py" "$G/instance.py" "$W/"
cp "$G/reference.py" "$W/elicit.py"
cd "$W"
"$REPO/.venv/bin/python" -m pytest --collect-only -q -p no:cacheprovider test_project.py | tail -2
