#!/bin/bash
# Round 9 slice a: targeted greps, run from checkout root. Output is the evidence for the grep-based rows.
cd "$(dirname "$0")/../../../.." || exit 1
M=course/modules/M/M4
echo "[PROCESS] process words in hub and L01-L04 prose"; for f in index L01 L02 L03 L04; do sed -e 's/<[^>]*>/ /g' $M/$f.html | grep -o -i -E "\b(builder|verifier|round [0-9]+|reviewer|draft|placeholder|lorem|todo|tbd|we will|this section will|ledger|fragment)\b" | sort | uniq -c | sed "s/^/$f: /"; done
echo "[SCOPE] scope words with context (always/never/most/heavy/fat)"; for f in index L01 L02 L03 L04; do sed -e 's/<[^>]*>//g' $M/$f.html | grep -n -i -E "\b(always|never|most|heavy|fat)\b" | cut -c1-160 | sed "s/^/$f:/"; done
echo "[DATA] data-file attributes and data reads in labs"; grep -c 'data-files' $M/index.html $M/L0[1-4].html; grep -n -E "open\(|urllib|requests|socket|subprocess|data/" tests/labs/M4/lab-M4-L0[1-4]-1.py | head -3; echo "(no lines above = no reads)"
echo "[NOTATION] forbidden registry symbols in slice"; grep -n -o -E "\\\\(Phi|phi|varphi|ast|mathbb|Prob)[^a-zA-Z]|R_f|R\^" $M/index.html $M/L0[1-4].html | head -3; echo "(no lines above = none)"
echo "[NOTATION] \\Var macro and Assumption words in slice"; grep -c "\\\\Var[^a-z]" $M/index.html $M/L0[1-4].html; grep -c "Assumption" $M/L0[1-4].html
echo "[DAG-SD] standard deviation definitions"; grep -n "standard deviation)" $M/L0[1-5].html | cut -c1-140
echo "[DAG-A] normal/Gaussian words in L03; Prop 2.8 / Assumption 2.7 anywhere in M4 pages or cards"; grep -c -i "normal\|gaussian" $M/L03.html; grep -n "Proposition 2.8\|Assumption 2.7" $M/*.html $M/cards.json | head -3; echo "(no lines above = none)"
echo "[CARDS] card id M4-c219 and removed c066/c220"; grep -c '"M4-c219"' $M/cards.json; grep -c '"M4-c066"' $M/cards.json; grep -c '"M4-c220"' $M/cards.json
echo "[REG] blitzstein record fields"; .venv/bin/python -I -c "
import json
d=json.load(open('references/references.json'))
items=d if isinstance(d,list) else d.get('entries', d.get('references', []))
e=[x for x in items if x.get('key')=='blitzstein2019introduction'][0]
print({k:e.get(k) for k in ('doi','year','isbn','publisher','source_strings','verified_by','status')}, 'edition' in e)"
echo "[HOURS] data-hours attributes"; grep -o 'data-hours[a-z-]*="[0-9]*"' index.html 2>/dev/null; grep -o 'data-hours[a-z-]*="[0-9]*"' $M/index.html $M/L0[1-4].html
echo "[FWD] lesson links in L01 (only the next-lesson nav link is expected)"; grep -n 'L0[2-9]\.html\|L10\.html' $M/L01.html | cut -c1-120
