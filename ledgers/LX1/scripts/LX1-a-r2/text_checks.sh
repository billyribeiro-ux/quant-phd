#!/bin/bash
# Prose checks on the LX1 slice-a pages: banned phrases, process words, symbol T use, CU, historian/regulator, D1-D15 names, notation macros, why-it-matters word counts.
cd /Users/billyribeiro/.fanout/wt/verifyE2-LX1-a
P="course/modules/LX/LX1/index.html course/modules/LX/LX1/L01.html course/modules/LX/LX1/L02.html"
echo "-- banned (expect none outside script)"; grep -n -i -E 'TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\.\.\.' $P | grep -v '<script' | cut -c1-160
echo "-- process words (expect none)"; grep -n -o -i -E '\b(builder|build|verifier|verify|verified|REQUEST|planner|fixer|unit report|ledger|checkout|pin)\b' $P
echo "-- symbol T in L02 (registered as return observations)"; grep -n -E '\bT\b|_T\b|_\{T\}|\{t = 1, \\dots, T\}' course/modules/LX/LX1/L02.html | grep -v 'data-grade\|grade">T\|>T<' | cut -c1-200
echo "-- CU (expect none)"; grep -n -E '\bCU\b' course/modules/LX/LX1/*.html tests/labs/LX1/lab-LX1-L0[12]-1.py
echo "-- historian/regulator (expect none)"; grep -n -i 'historian\|regulator' $P
echo "-- outside-closure names (expect no concept link)"; grep -n -o -i -E 'bank run|fire[- ]sale|leverage cycle|banking crisis|currency crisis|covered interest|uncovered interest|efficient[- ]markets?|moral hazard|fisher relation|bank reserves|central bank|credit default|contagion|term spread|sovereign|deposit insurance' $P | sort | uniq -c
echo "-- LaTeX commands used"; for f in $P; do python3 -I -c "import re,sys,collections;t=open(sys.argv[1],encoding='utf-8').read();print(sys.argv[1], dict(collections.Counter(re.findall(r'\\\\[A-Za-z]+',t))))" $f; done
echo "-- why-it-matters word counts"; for f in L01 L02; do python3 -I -c "import re,sys,html;t=open(sys.argv[1],encoding='utf-8').read();m=re.search(r'<p class=\"why-it-matters\">(.*?)</p>',t,re.S);print(sys.argv[1],len(html.unescape(re.sub(r'<[^>]+>',' ',m.group(1))).split()),'words')" course/modules/LX/LX1/$f.html; done
echo "-- hub placement item count and categories"; grep -c 'class="item"' course/modules/LX/LX1/index.html
echo "-- hub hours-table rung 1 row"; grep -n 'Rung 1, worked example' course/modules/LX/LX1/index.html | cut -c1-200
echo "-- project rung 1 rows"; grep -n 'Rung 1 · Worked example\|Rung 1, worked example' course/modules/LX/LX1/project.html | cut -c1-240
