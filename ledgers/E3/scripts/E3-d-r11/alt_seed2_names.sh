#!/bin/sh
# Round-11: names of the failing tests for the alternatives that fail at seed 2 (alt1c, alt6) under the current suite.
ROOT="$1"; PY="$2"
for A in alt1c_zoom_then_reference_newton alt6_fd_step_1e-4; do
  SRC="$ROOT/ledgers/E3/scripts/E3-d-r10/alts/$A"
  W=/Users/billyribeiro/.fanout/scratch-E3-d-r11/names_$A
  rm -rf "$W" && mkdir -p "$W" && cp "$ROOT/course/modules/E/E3/grader/test_project.py" "$ROOT/course/modules/E/E3/grader/instance.py" "$W/" && cp "$SRC/elicit.py" "$W/elicit.py"
  echo "== $A seed 2"; (cd "$W" && QF_SEED=2 "$PY" -m pytest -q -p no:cacheprovider -rf --assert=plain -W error test_project.py 2>&1 | grep -E "^FAILED|passed|failed")
done
