#!/bin/bash
# Round 11: collect-only count of the E4 project grader. The suite imports solver and instance by name, so the
# reference is copied as solver.py, with the grader files, into a fresh scratch directory outside the checkout.
set -u
CHECKOUT="$(cd "$(dirname "$0")/../../../.." && pwd)"
D="$(mktemp -d /tmp/e4r11collect.XXXXXX)"
cp "$CHECKOUT/course/modules/E/E4/grader/test_project.py" "$CHECKOUT/course/modules/E/E4/grader/instance.py" "$D/"
cp "$CHECKOUT/course/modules/E/E4/grader/reference.py" "$D/solver.py"
cd "$D" && QF_SEED=0 "$CHECKOUT/.venv/bin/python" -m pytest --collect-only -q -p no:cacheprovider --assert=plain -W error test_project.py
echo "EXIT $?"
