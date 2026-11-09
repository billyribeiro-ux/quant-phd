#!/bin/bash
# Round-6 delta evidence for M5 slice c: hunks in the slice files between the previous pin and this pin.
cd "$(dirname "$0")/../../../.." || exit 1
A=dde0486beeb0312e4ac1cc03aaa02e56644adb24
B=e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a
echo "pin HEAD: $(git rev-parse HEAD)  previous pin: $A"
echo "== stat of slice files (dde0486b..e896b7a4)"
git diff --stat $A $B -- course/modules/M/M5/L08.html course/modules/M/M5/L09.html course/modules/M/M5/L10.html course/modules/M/M5/cards.json tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L10-1.py course/modules/M/M5/index.html references/references.json course/assets/data/notation.json
echo "== hunks (-U0)"
git diff -U0 $A $B -- course/modules/M/M5/L08.html course/modules/M/M5/L09.html course/modules/M/M5/L10.html tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L10-1.py | grep -E '^(\+\+\+|@@|[-+][^-+])' | cut -c1-220
echo "== cards.json hunk headers"
git diff -U0 $A $B -- course/modules/M/M5/cards.json | grep -E '^@@'
echo "== previous-pin byte identity (exit 0 = identical)"
for f in course/modules/M/M5/L09.html tests/labs/M5/lab-M5-L09-1.py tests/labs/M5/lab-M5-L08-1.py tests/labs/M5/lab-M5-L10-1.py course/modules/M/M5/index.html references/references.json course/assets/data/notation.json; do git diff --quiet $A $B -- $f; echo "$f identical=$?"; done
