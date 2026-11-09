#!/bin/sh
# Strict mypy on the grader with reference.py copied as elicit.py (the suite imports elicit and instance).
# Usage: mypy_grader_with_reference.sh <repo-root>
set -e
W=$(mktemp -d /tmp/e3d-r14-mypy.XXXXXX)
cp "$1/course/modules/E/E3/grader/test_project.py" "$1/course/modules/E/E3/grader/instance.py" "$W/"
cp "$1/course/modules/E/E3/grader/reference.py" "$W/elicit.py"
cd "$W" && "$1/.venv/bin/mypy" --no-incremental --strict elicit.py instance.py test_project.py
