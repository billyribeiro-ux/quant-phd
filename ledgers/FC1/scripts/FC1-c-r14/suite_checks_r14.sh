#!/bin/sh
# Round 14, FC1-c: collect-only count, starter failure shape, and the grader strict-mypy check in scratch copies.
# Usage (from the checkout root): sh ledgers/FC1/scripts/FC1-c-r14/suite_checks_r14.sh
set -u
ROOT="$(pwd)"
G="$ROOT/course/modules/FC/FC1/grader"
OUT="$ROOT/ledgers/FC1/scripts/FC1-c-r14/out"
PY="$ROOT/.venv/bin/python"
W=$(mktemp -d /tmp/fc1c14-suite.XXXX)
cp "$G/test_project.py" "$G/instance.py" "$W/"
cp "$G/reference.py" "$W/instruments.py"
(cd "$W" && "$PY" -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1) > "$OUT/collect_count_r14.out"
(cd "$W" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1) > "$OUT/reference_seed0_r14.out"
cp "$G/starter.py" "$W/instruments.py"
(cd "$W" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1; QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | grep -c Traceback) > "$OUT/starter_seed0_r14.out"
cp "$G/reference.py" "$W/instruments.py"
(cd "$W" && "$PY" -m mypy --strict --no-incremental test_project.py instance.py instruments.py 2>&1 | tail -1) > "$OUT/mypy_strict_grader_scratch_r14.out"
rm -rf "$W"
echo done
