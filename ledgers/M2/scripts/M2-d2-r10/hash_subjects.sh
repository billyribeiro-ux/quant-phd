#!/bin/bash
# M2-d2 r10: sha256 of every subject file in the slice at the round-9 pin and at HEAD (delta evidence).
cd "$(dirname "$0")/../../../.." || exit 1
PREV=1e272e5a641f18412703b37778a44db6f7391a69
FILES="course/modules/M/M2/L22.html course/modules/M/M2/L23.html course/modules/M/M2/L24.html course/modules/M/M2/cards.json course/modules/M/M2/index.html tests/labs/M2/lab-M2-L22-1.py tests/labs/M2/lab-M2-L23-1.py tests/labs/M2/lab-M2-L24-1.py references/references.json curriculum/curriculum.json"
for f in $FILES; do
  a=$(git show $PREV:$f | shasum -a 256 | cut -c1-16); b=$(shasum -a 256 "$f" | cut -c1-16)
  echo "$f r9pin=$a head=$b $([ "$a" = "$b" ] && echo SAME || echo CHANGED)"
done
for p in notation tools/run_labs.py tools/check_pages.py tools/check_dag.py tools/page_smoke.py tools/ledger.py; do
  if git diff --quiet $PREV HEAD -- "$p"; then echo "$p unchanged since r9 pin"; else echo "$p CHANGED since r9 pin"; fi
done
