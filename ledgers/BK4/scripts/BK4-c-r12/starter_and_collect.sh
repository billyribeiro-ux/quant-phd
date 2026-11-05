#!/bin/sh
# Round 12 (BK4-c): collect-only count of the suite, and the suite run on starter.py (must fail, naming the property).
# Usage: sh starter_and_collect.sh <checkout> <scratch>
CK="$1"; SC="$2"; PY="$CK/.venv/bin/python"; G="$CK/course/modules/BK/BK4/grader"
rm -rf "$SC/starter" "$SC/collect" && mkdir -p "$SC/starter" "$SC/collect"
cp "$G/test_project.py" "$G/instance.py" "$G/starter.py" "$SC/starter/" && cp "$G/starter.py" "$SC/starter/clearing_house.py"
cp "$G/test_project.py" "$G/instance.py" "$SC/collect/" && cp "$G/reference.py" "$SC/collect/clearing_house.py"
(cd "$SC/collect" && QF_SEED=0 "$PY" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py | tail -1)
(cd "$SC/starter" && QF_SEED=0 "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py | tail -1)
