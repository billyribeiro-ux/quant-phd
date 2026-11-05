#!/bin/sh
# LX1-b round 8: banned-phrase, process-word, DAG-name, concept-link and quiz/solution counts for L03 and L04.
# Usage: sh prose_scan.sh <checkout>
cd "$1" || exit 1
for f in L03 L04; do
  p=course/modules/LX/LX1/$f.html
  echo "== $f banned phrases and process words (learner text, tags stripped)"
  sed -e 's/<[^>]*>//g' "$p" | grep -n -i -E "TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|builder|verifier|round [0-9]|this section will|we will|REQUEST|unit report|\.\.\." 
  echo "== $f outside-closure concept names (plain prose expected)"
  sed -e 's/<[^>]*>//g' "$p" | grep -n -i -o -E "bank run|fire.sale|leverage cycle|banking crisis|currency crisis|covered interest|uncovered interest|efficient markets|moral hazard|fisher|bank reserves|central-bank balance|credit.default swap|network contagion|term spread|expectation|fx market|sovereign default|crisis-mechanism|contagion"
  echo "== $f concept links and concepts.html anchors"
  grep -o 'data-concept="[^"]*"' "$p" | sort | uniq -c
  grep -o 'href="[^"]*concepts.html[^"]*"' "$p" | sort | uniq -c
  echo "== $f quiz items / explanations / correct options / solutions / misconceptions"
  echo "items=$(grep -c 'class="item"' "$p") explain=$(grep -c 'class="explain"' "$p") correct=$(grep -c 'data-correct' "$p") solutions=$(grep -c 'class="solution"' "$p") misconceptions=$(grep -c 'class="misconception"' "$p")"
  echo "== $f registered notation symbols in math (T, Phi, gamma, R_f, R^*, Q)"
  python3 -I -c "
import re,sys
t=open(sys.argv[1],encoding='utf-8').read()
segs=re.findall(r'\\\\\((.*?)\\\\\)|\\\\\[(.*?)\\\\\]', t, re.S)
m=[a or b for a,b in segs]
pats=[r'\bT\b', r'\\\\Phi', r'\\\\gamma', r'R_f', r'R\^', r'\\\\mathbb']
print({p: sum(1 for s in m if re.search(p,s)) for p in pats}, 'segments', len(m))
" "$p"
done
