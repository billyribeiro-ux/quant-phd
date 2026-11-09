#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyF11-E5-a
echo "== E1 and M2 pages changed f618cf1..HEAD (A = added)"
git diff --name-status f618cf1..HEAD -- course/modules/E/E1 course/modules/M/M2 | awk '{print $1}' | sort | uniq -c
echo "== hub line 35 E1 clause"
sed -n 35p course/modules/E/E5/index.html | grep -o "E1, M1 and P0.1 are referred.*"
echo "== hub line 60"
sed -n 60p course/modules/E/E5/index.html | grep -o "The concepts of P0.1.*"
echo "== concepts.html E1 and M2 entries (HEAD)"
grep -n 'id="comparative-statics"\|id="competitive-equilibrium"\|id="derivative"\|id="implicit-function-theorem"' course/concepts.html | cut -c1-200
echo "== concepts.html P0.1 entries (HEAD)"
grep -n 'id="evidence-grade"\|id="project-ladder"\|id="notation-conventions"' course/concepts.html | cut -c1-200
echo "== E1 index exists at HEAD"
ls course/modules/E/E1/index.html
echo "== h1 lines L01-L08"
grep -n "<h1>" course/modules/E/E5/L0*.html | cut -c1-160
echo "== L05 line 59 and 79; L06 line 73 and 278"
sed -n 59p course/modules/E/E5/L05.html | cut -c1-160; sed -n 79p course/modules/E/E5/L05.html | cut -c1-160
sed -n 73p course/modules/E/E5/L06.html | cut -c1-160; sed -n 278p course/modules/E/E5/L06.html | cut -c1-160
echo "== references.json changed entries"
git diff f618cf1..HEAD -U0 -- references/references.json | grep "^@@" 
