#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyF11-CS2-a
for f in course/modules/CS/CS2/index.html course/modules/CS/CS2/L01.html course/modules/CS/CS2/L02.html course/modules/CS/CS2/L03.html course/modules/CS/CS2/L04.html tests/labs/CS2/lab-CS2-L01-1.py tests/labs/CS2/lab-CS2-L02-1.py tests/labs/CS2/lab-CS2-L03-1.py tests/labs/CS2/lab-CS2-L04-1.py notation/notation.json curriculum tools tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py; do
  if git diff --quiet aa659725 95f3f8cb -- "$f"; then echo "IDENTICAL $f"; else echo "CHANGED $f"; fi
done
echo "cards.json (whole file): $(git diff --quiet aa659725 95f3f8cb -- course/modules/CS/CS2/cards.json && echo IDENTICAL || echo CHANGED)"
echo "HEAD == 95f3f8cb: $(git rev-parse HEAD)"
