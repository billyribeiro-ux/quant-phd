#!/bin/sh
# Mechanical greps for the E4 slice a (hub and L01-L03). Run from the checkout root.
# Output is recorded in ledgers/E4/scripts/E4-a-r4/logs/grep_checks.txt.
F="course/modules/E/E4/index.html course/modules/E/E4/L01.html course/modules/E/E4/L02.html course/modules/E/E4/L03.html"
echo "== banned phrases"; grep -n -i -E "TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly" $F | wc -l
echo "== ellipsis hits (all must be inside code)"; grep -n -E "\.\.\.|…" $F | cut -c1-120
echo "== process words"; grep -n -i -E "builder|verifier|round|REQUEST|unit report|fixer|ledger" $F | cut -c1-120
echo "== CU"; grep -c -w "CU" $F
echo "== figures"; grep -c -E "data-chart|<svg|<figure" $F
echo "== bibliographic"; grep -n -E "19[0-9][0-9]|20[0-9][0-9]|Muth|Milgrom|Stiglitz|Mas-Colell|Stokey|Econometrica|Journal" $F | cut -c1-120
echo "== notation (registered-collision candidates)"; grep -n -F -e "mathbb" -e "\\Phi" -e "\\gamma" -e "ast}" -e "\\mathbf" $F | wc -l
echo "== \\gg occurrences"; grep -n -F '\gg' $F | cut -c1-60
echo "== scope words"; grep -n -o -i -w -E "only|always|never|every|any|same|exactly|drives|all" $F | wc -l
echo "== define-before-use: out-of-closure names"; grep -n -i -E "Bayes|posterior|state price|martingale|CARA|common knowledge|informationally|Banach|intermediate value|stochastic discount" $F | cut -c1-120
echo "== additive"; grep -c -i "additive" $F
