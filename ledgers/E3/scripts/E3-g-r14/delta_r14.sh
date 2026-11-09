#!/bin/sh
# Round-14 delta for E3 slice g: previous pin 329c1d7f (round-12 pin) to current pin 1431aa1d.
set -u
cd "$(git rev-parse --show-toplevel)"
echo "pin: $(git rev-parse HEAD)"; echo "prev: $(git rev-parse 329c1d7f)"
echo "--- slice HTML and lab twins (expected: no output)"
git diff --stat 329c1d7f 1431aa1d -- course/modules/E/E3/L05.html course/modules/E/E3/L06.html course/modules/E/E3/L07.html course/modules/E/E3/L08.html tests/labs/E3/lab-E3-L05-1.py tests/labs/E3/lab-E3-L06-1.py tests/labs/E3/lab-E3-L07-1.py tests/labs/E3/lab-E3-L08-1.py
echo "--- slice cards.json diff (hunks read in full)"
git diff --stat 329c1d7f 1431aa1d -- course/modules/E/E3/cards.json
echo "--- shared inputs"
git diff --stat 329c1d7f 1431aa1d -- tools notation references/references.json course/assets/js course/templates
git diff 329c1d7f 1431aa1d -- references/references.json | grep '^[-+] ' | head -8
echo "--- files changed in E3 unit"
git diff --stat 329c1d7f 1431aa1d -- course/modules/E/E3 tests/labs/E3
