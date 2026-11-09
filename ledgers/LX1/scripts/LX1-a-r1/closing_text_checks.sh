#!/bin/sh
# LX1 slice a closing delta: banned strings, process words, concept/dfn identity vs 95f3f8cb, changed-line scope words, notation registry macros. Run from checkout root.
L=course/modules/LX/LX1
H=95f3f8cb
O=ledgers/LX1/scripts/LX1-a-r1/out-closing
echo "== banned strings (index, L01, L02)"; grep -n -i -E "TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|it can be shown|roughly|historically|well known|of course|\.\.\.|…" $L/index.html $L/L01.html $L/L02.html; echo "hits=$?"
echo "== process words (index, L01, L02)"; grep -n -i -o -E ".{30}\b(ruling|verifier|fixer|ledger|fragment|mutant|blind|architect|checkout|slice|round [0-9])\b.{20}" $L/index.html $L/L01.html $L/L02.html; echo "hits=$?"
echo "== concept anchors and dfn ids, base vs now"
for f in L01 L02; do
  git show $H:$L/$f.html | grep -o 'data-concept="[^"]*"\|<dfn id="[^"]*"' > $O/_old_$f.txt
  grep -o 'data-concept="[^"]*"\|<dfn id="[^"]*"' $L/$f.html > $O/_new_$f.txt
  diff -q $O/_old_$f.txt $O/_new_$f.txt && echo "$f identical"
done
echo "== added lines of the delta in L01/L02/index (new text)"
git diff -U0 $H..HEAD -- $L/L01.html $L/L02.html $L/index.html | grep '^+' | grep -v '^+++' > $O/added_lines.txt; wc -l < $O/added_lines.txt
echo "== scope words in added lines"; grep -n -o -i -E ".{0,40}\b(only|all|always|every|any|same|drives|exactly|none|no|never)\b.{0,40}" $O/added_lines.txt
echo "== symbols in added lines: macros"; grep -o '\\[A-Za-z]\+' $O/added_lines.txt | sort | uniq -c | tr '\n' ' '; echo
echo "== registered symbols in added lines (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q)"; grep -n -E 'Phi|gamma_[34]|R\^|R_f|mathbb\{Q\}|\\\\T|\(T\)|T =' $O/added_lines.txt; echo "hits=$?"
echo "== registry-symbol and assumption tokens in changed lines"; grep -o -E '\(A[0-9]\)' $O/added_lines.txt | sort | uniq -c | tr '\n' ' '; echo
