#!/bin/sh
# Runs the E3 suite on one elicit.py for each listed seed. Usage: run_suite_seeds.sh <repo-root> <elicit.py> <seed>...
R="$1"; E="$2"; shift 2
W=$(mktemp -d /tmp/e3d-r14-run.XXXXXX)
cp "$R/course/modules/E/E3/grader/test_project.py" "$R/course/modules/E/E3/grader/instance.py" "$W/"
cp "$E" "$W/elicit.py"
cd "$W"
for s in "$@"; do
  QF_SEED=$s PYTHONHASHSEED=0 "$R/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$W/out_$s.txt" 2>&1
  echo "seed=$s EXIT=$? $(tail -1 "$W/out_$s.txt" | cut -c1-200) $(grep -o 'FAILED test_project.py::[a-z_0-9]*' "$W/out_$s.txt" | sed 's/FAILED test_project.py:://' | tr '\n' ' ')"
done
rm -rf "$W"
