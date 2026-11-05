#!/bin/sh
# Round-11: run each alternative elicit.py through the CURRENT suite (grader/test_project.py + instance.py) for seeds 0-9.
# usage: run_alts_r11.sh <checkout-root> <python> <alt-dir>...
ROOT="$1"; PY="$2"; shift 2
G="$ROOT/course/modules/E/E3/grader"
for ALT in "$@"; do
  W=/Users/billyribeiro/.fanout/scratch-E3-d-r11/alt_$(basename "$ALT")
  rm -rf "$W"; mkdir -p "$W"
  cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$ALT/elicit.py" "$W/elicit.py"
  pass=0; fails=""
  for seed in 0 1 2 3 4 5 6 7 8 9; do
    out=$(cd "$W" && QF_SEED=$seed "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
    if echo "$out" | grep -q " passed" && ! echo "$out" | grep -q "failed\|error"; then pass=$((pass+1)); else fails="$fails $seed"; fi
  done
  echo "$(basename "$ALT"): seeds passing $pass/10; failing seeds:${fails:- none}"
done
