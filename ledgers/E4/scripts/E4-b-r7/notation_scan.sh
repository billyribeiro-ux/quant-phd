#!/bin/bash
# Forbidden and registry-conflicting notation in the E4 L04-L06 pages (pin 06994db).
# Usage: bash ledgers/E4/scripts/E4-b-r7/notation_scan.sh   (absolute checkout path below)
cd /Users/billyribeiro/.fanout/wt/verifyE7-E4-b || exit 1
F="course/modules/E/E4/L04.html course/modules/E/E4/L05.html course/modules/E/E4/L06.html"
echo "== raw mathbb (must be \\E, \\R, \\Normal macros)"; grep -n 'mathbb' $F | cut -c1-120
echo "== Phi / gamma_3 / gamma_4 / R^ast / R_f / R^{e ast} / mathbb Q"; grep -n -E '\\Phi|\\gamma_[34]|R\^\\ast|R\^\{e|R_f|\\mathbb\{Q\}' $F | cut -c1-120
echo "== macro inventory"; grep -o -h -E '\\[A-Za-z]+' $F | sort | uniq -c | sort -rn | head -70
echo "== symbol s used in L04 as a bare letter"; grep -n -o -E '\\\(s\b|\bs_[a-z]+' course/modules/E/E4/L04.html | head -5
echo "== symbol x used in L04 as a bare letter"; grep -n -o -E '\\\(x\b|\bx_[a-zA-Z0-9]+' course/modules/E/E4/L04.html | head -5
