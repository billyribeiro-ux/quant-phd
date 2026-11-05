#!/bin/bash
# Round-12 PC3 slice a: text scans of the four slice pages (run from the checkout root). Output: outputs/text_scans_r12.out
cd /Users/billyribeiro/.fanout/wt/verifyE12-PC3-a || exit 1
P=course/modules/PC/PC3
O=ledgers/PC3/scripts/PC3-a-r12/outputs
{
echo "== stripped views (line-numbered, locators are raw-file line numbers)"
for f in index L01 L02 L03; do
  src=$P/$f.html; [ "$f" = index ] && src=$P/index.html
  python3 -I ledgers/PC3/scripts/PC3-a-r12/strip.py $src > $O/view-$f-r12.txt
  echo "$f: $(wc -l < $O/view-$f-r12.txt) lines"
done
echo "== process words (whole word, case-insensitive) and banned strings (expect 0 each)"
for w in build builder round verifier REQUESTS "unit report" fixer TODO TBD lorem "studies show" "experts agree" obviously clearly "well known" "for brevity" "left as an exercise" "beyond the scope" "details omitted" "it is important to note" "you can add more"; do
  echo "$w: $(cat $P/index.html $P/L01.html $P/L02.html $P/L03.html | grep -c -i -w -- "$w")"
done
echo "== D-terms (expect 0 except plain prose)"
for w in martingale "stopping time" adapted sigma-algebra filtration Poisson Kelly CAPM duration DCF "Theorem 3.10"; do
  echo "$w: $(cat $P/index.html $P/L01.html $P/L02.html $P/L03.html | grep -c -- "$w")"
done
echo "== data and external"
echo "data-files: $(cat $P/index.html $P/L01.html $P/L02.html $P/L03.html | grep -c 'data-files')"
echo "external http(s) links: $(cat $P/index.html $P/L01.html $P/L02.html $P/L03.html | grep -c 'https\?://')"
echo "figures or svg: $(cat $P/index.html $P/L01.html $P/L02.html $P/L03.html | grep -c -i '<svg\|<figure\|<canvas\|<img')"
echo "== A_i rename (expect 0)"
echo "A_i/A_1/A_2/A_3 in L02: $(grep -c 'A_i\|A_1\|A_2\|A_3' $P/L02.html)"
echo "C_i/C_1/C_2 occurrences in L02: $(grep -o 'C_i\|C_1\|C_2' $P/L02.html | wc -l | tr -d ' ')"
echo "== why-it-matters word counts and question marks"
for f in L01 L02 L03; do python3 -I -c "
import re,html,sys
s=open('$P/$f.html',encoding='utf-8').read()
m=re.search(r'<p class=\"why-it-matters\">(.*?)</p>', s, re.S)
t=html.unescape(re.sub(r'<[^>]+>','',m.group(1)))
print('$f words', len(t.split()), 'question marks', t.count('?'))
"; done
echo "== twins: open/network imports (expect 0)"
grep -c 'open(\|urllib\|socket\|requests' tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py
echo "== twins md5"
md5sum tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py
echo "== delta of slice files since 00a84795 (expect empty)"
git diff --stat 00a84795 5db69a9 -- $P/index.html $P/L01.html $P/L02.html $P/L03.html tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py
echo "== href values in the four slice pages (sorted, with counts)"
cat $P/index.html $P/L01.html $P/L02.html $P/L03.html | grep -o 'href="[^"]*"' | sort | uniq -c
echo "== data-concept values in the four slice pages"
cat $P/index.html $P/L01.html $P/L02.html $P/L03.html | grep -o 'data-concept="[^"]*"' | sort | uniq -c
echo "== dfn and data-concept in slice pages"
grep -o '<dfn[^>]*>' $P/L01.html $P/L02.html $P/L03.html
} > $O/text_scans_r12.out 2>&1
echo "text scans written: exit=$?"
