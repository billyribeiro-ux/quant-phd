#!/bin/sh
# Round-11 check: reference.py as elicit.py in a scratch workspace; collect-only count; reference seed 0; starter must fail.
# usage: ref_ws.sh <checkout-root> <python>
ROOT="$1"; PY="$2"; SCR=/Users/billyribeiro/.fanout/scratch-E3-d-r11
G="$ROOT/course/modules/E/E3/grader"
rm -rf "$SCR/ref" "$SCR/starter" && mkdir -p "$SCR/ref" "$SCR/starter"
cp "$G/test_project.py" "$G/instance.py" "$SCR/ref/" && cp "$G/reference.py" "$SCR/ref/elicit.py"
cp "$G/test_project.py" "$G/instance.py" "$SCR/starter/" && cp "$G/starter.py" "$SCR/starter/elicit.py"
cd "$SCR/ref" && echo "== collect-only" && QF_SEED=0 "$PY" -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -3
echo "== reference seed 0" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -3; echo "RC=${PIPESTATUS:-}"
cd "$SCR/starter" && echo "== starter seed 0" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -2
