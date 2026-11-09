#!/bin/sh
# LX1 slice a closing delta round 1: text, notation, DAG and claim greps on the slice pages at pin 95f3f8cb. Run from the checkout root.
L=course/modules/LX/LX1
H=67a2d13e
O=ledgers/LX1/scripts/LX1-a-r1/out-delta
echo "== banned strings (index, L01, L02)"; grep -n -i -E "TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|it can be shown|roughly|historically|well known|of course|\.\.\.|…" $L/index.html $L/L01.html $L/L02.html; echo "hits=$?"
echo "== process words (index, L01, L02)"; grep -n -i -o -E ".{30}\b(ruling|verifier|fixer|ledger|fragment|mutant|blind|architect|checkout|slice|round [0-9])\b.{20}" $L/index.html $L/L01.html $L/L02.html; echo "hits=$?"
echo "== concept anchors and dfn ids, old vs new"
for f in L01 L02; do
  git show $H:$L/$f.html | grep -o 'data-concept="[^"]*"\|<dfn id="[^"]*"' > $O/_old_$f.txt
  grep -o 'data-concept="[^"]*"\|<dfn id="[^"]*"' $L/$f.html > $O/_new_$f.txt
  diff -q $O/_old_$f.txt $O/_new_$f.txt && echo "$f identical"
  rm -f $O/_old_$f.txt $O/_new_$f.txt
done
echo "== outside-closure names (index, L01, L02)"; grep -n -i -E "bank run|fire sale|leverage cycle|banking crisis|currency crisis|covered interest|uncovered interest|efficient market|moral hazard|fisher relation|bank reserves|central bank|credit default|contagion|term spread|sovereign|deposit insurance" $L/index.html $L/L01.html $L/L02.html; echo "hits=$?"
echo "== figure tokens (index, L01, L02)"; grep -c -E "<svg|class=\"chart\"|data-figures|data-files" $L/index.html $L/L01.html $L/L02.html
echo "== L03/L04 closure words"; grep -c -i -E "national account|business cycle" $L/L03.html $L/L04.html
echo "== L01 notation: price symbols (P_ must be absent, ruling 16)"; grep -c "P_[{0-9t]" $L/L01.html; echo "A_t/A_0/B_t uses:"; grep -o "A_[{0-9t]\|B_t" $L/L01.html | sort | uniq -c
echo "== historian/regulator"; grep -c -i -E "historian|regulator" $L/index.html $L/L01.html $L/L02.html
echo "== P0.1 in concepts.html"; grep -c "P0.1" course/concepts.html
echo "== project hours values (project.html)"; grep -o '<td class="num">[0-9.]*</td>' $L/project.html | sed -n '1,6p' | tr -d '\n'; echo
echo "== hub hours values (index.html)"; grep -o '<td>[0-9.]*</td>' $L/index.html | sed -n '1,6p' | tr -d '\n'; echo
echo "== registry records for slice keys: identical except used_by"
git show $H:references/references.json > $O/_refs_old.json
git show HEAD:references/references.json > $O/_refs_new.json
.venv/bin/python -I -c "
import json, sys
O = sys.argv[1]
o = {e['key']: e for e in json.load(open(O + '/_refs_old.json'))['entries']}
n = {e['key']: e for e in json.load(open(O + '/_refs_new.json'))['entries']}
for k in ['friedman1963monetary', 'eichengreen1992golden', 'garber2000famous']:
    a = {x: y for x, y in o[k].items() if x != 'used_by'}
    b = {x: y for x, y in n[k].items() if x != 'used_by'}
    print(k, 'same except used_by:', a == b, '| used_by old', o[k]['used_by'], 'new', n[k]['used_by'])
" $O
rm -f $O/_refs_old.json $O/_refs_new.json
