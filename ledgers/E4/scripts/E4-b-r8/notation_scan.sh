#!/bin/bash
# Round-8 notation and process-word scan of the E4 L04-L06 pages and their cards (run from the checkout root).
F1=course/modules/E/E4/L04.html
F2=course/modules/E/E4/L05.html
F3=course/modules/E/E4/L06.html
echo "== mathbb (must be macros)"; grep -n "mathbb" $F1 $F2 $F3 | cut -c1-120
echo "== registered symbols T, Phi, gamma_3/4, R^ast, R^{e ast}, R_f, mathbb Q in math"; grep -n -o -E '\\Phi|\\gamma_[34]|R\^\\ast|R\^\{e|R_f|\\mathbb\{Q\}' $F1 $F2 $F3 | head
echo "== bare T in math (\\(T\\) or \$T\$)"; grep -n -o -E '\\\(T\\\)|\$T\$' $F1 $F2 $F3 | head
echo "== macro inventory (non-TeX-primitive names)"; grep -o -h -E '\\(E|R|Var|Cov|Corr|Normal|indic|Prob|N|iid|dto|pto|se|tr|diag|argmax|argmin)\b' $F1 $F2 $F3 | sort | uniq -c
echo "== process words in learner text"; for f in $F1 $F2 $F3; do sed 's/<[^>]*>//g' $f | grep -n -i -o -E '.{0,50}(registry|builder|verifier|fragment|ledger|architect|twin|round [0-9]|pin ).{0,30}'; done
echo "== cards: process words"; grep -n -i -o -E '.{0,40}(registry|builder|verifier|ledger|twin).{0,30}' course/modules/E/E4/cards.json | head
