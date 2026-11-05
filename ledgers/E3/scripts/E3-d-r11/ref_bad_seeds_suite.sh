#!/bin/sh
# Round-11: the reference as elicit.py through the unchanged suite on the seeds that the scan flagged (157, 165, 269, 108).
ROOT="$1"; PY="$2"; SCR=/Users/billyribeiro/.fanout/scratch-E3-d-r11/ref_bad
rm -rf "$SCR" && mkdir -p "$SCR" && G="$ROOT/course/modules/E/E3/grader"
cp "$G/test_project.py" "$G/instance.py" "$SCR/" && cp "$G/reference.py" "$SCR/elicit.py"
cd "$SCR" || exit 1
for seed in 108 157 165 269; do
  echo "== seed $seed"; QF_SEED=$seed "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | grep -E "^FAILED|passed|failed|Error" | head -4
done
