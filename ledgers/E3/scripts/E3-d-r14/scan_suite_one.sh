#!/bin/sh
# Full suite on the reference for one seed, in its own scratch workspace. Usage: scan_suite_one.sh <repo-root> <seed>
R="$1"; s="$2"
W=$(mktemp -d /tmp/e3d-r14-scan/s$s.XXXXXX)
cp "$R/course/modules/E/E3/grader/test_project.py" "$R/course/modules/E/E3/grader/instance.py" "$W/"
cp "$R/course/modules/E/E3/grader/reference.py" "$W/elicit.py"
cd "$W" && QF_SEED=$s "$R/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$W/out.txt" 2>&1
rc=$?
echo "seed=$s EXIT=$rc $(grep -E '^(FAILED|[0-9]+ (passed|failed))' "$W/out.txt" | tr '\n' ' ' | cut -c1-300)"
rm -rf "$W"
