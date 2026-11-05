#!/bin/sh
# Collect-only count of the SC1 project suite against the reference, plus the page's stated count.
# Usage (from the checkout root): sh ledgers/SC1/scripts/SC1-d-r11/collect_count.sh <checkout-root>
set -e
ROOT="$1"
W=/tmp/sc1d-r11/collect
rm -rf "$W" && mkdir -p "$W"
cp "$ROOT/course/modules/SC/SC1/grader/test_project.py" "$ROOT/course/modules/SC/SC1/grader/instance.py" "$W/"
cp "$ROOT/course/modules/SC/SC1/grader/reference.py" "$W/bm_checks.py"
cd "$W"
QF_SEED=0 "$ROOT/.venv/bin/python" -m pytest --collect-only -q -p no:cacheprovider --assert=plain -W error test_project.py | tail -3
echo "page claims:"
grep -o 'runs [0-9]* tests' "$ROOT/course/modules/SC/SC1/project.html" | sort | uniq -c
grep -o 'has [0-9]* tests' "$ROOT/course/modules/SC/SC1/project.html" | sort | uniq -c
grep -o '[0-9]* tests, and the browser' "$ROOT/course/modules/SC/SC1/project.html" | sort | uniq -c
grep -o 'with [0-9]* tests' "$ROOT/course/modules/SC/SC1/project.html" | sort | uniq -c
