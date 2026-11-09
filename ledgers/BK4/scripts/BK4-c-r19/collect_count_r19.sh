#!/bin/bash
# Round 19 (BK4 slice c): collect-only count of the grader, in a fresh scratch workspace holding reference.py as clearing_house.py.
# Usage: collect_count_r19.sh <checkout-root>
ROOT="$1"; W=$(mktemp -d /tmp/bk4r19-collect.XXXX); G="$ROOT/course/modules/BK/BK4/grader"
cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$G/reference.py" "$W/clearing_house.py"
cd "$W" && QF_SEED=0 "$ROOT/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py | tail -1
QF_SEED=0 "$ROOT/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py | tail -1
cp "$G/starter.py" "$W/clearing_house.py"; QF_SEED=0 "$ROOT/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py | tail -1
rm -rf "$W"
