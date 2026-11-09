#!/bin/sh
# Full E3 grader suite on one elicit.py for one seed. Usage: suite_one.sh <repo-root> <elicit.py> <seed>
R="$1"; E="$2"; s="$3"
W=$(mktemp -d /tmp/e3d-r15-suite.XXXXXX)
cp "$R/course/modules/E/E3/grader/test_project.py" "$R/course/modules/E/E3/grader/instance.py" "$W/"
cp "$E" "$W/elicit.py"
cd "$W" && QF_SEED=$s PYTHONHASHSEED=0 "$R/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$W/out.txt" 2>&1
rc=$?
echo "seed=$s EXIT=$rc $(tail -1 "$W/out.txt" | cut -c1-200) $(grep -o 'FAILED test_project.py::[a-z_0-9]*' "$W/out.txt" | sed 's/FAILED test_project.py:://' | tr '\n' ' ')"
rm -rf "$W"
