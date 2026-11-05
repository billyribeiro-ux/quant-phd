#!/bin/sh
# Round-9 check: collect-only count and per-seed run of the M4 grader on reference.py, in a scratch copy.
# usage: collect_and_run_r9.sh <checkout-root> <solution.py> <seed> [...]
ROOT="$1"; SOL="$2"; shift 2
W=$(mktemp -d /tmp/m4r9.XXXXXX)
cp "$ROOT/course/modules/M/M4/grader/test_project.py" "$ROOT/course/modules/M/M4/grader/instance.py" "$W/"
cp "$SOL" "$W/tail_risk.py"
cd "$W" || exit 1
PY="$ROOT/.venv/bin/python"
"$PY" -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1
for s in "$@"; do
  echo "seed $s:"; QF_SEED=$s PYTHONHASHSEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1
done
rm -rf "$W"
