#!/bin/bash
# Round-6 text scans for PC3 slice a (index.html, L01-L03). Run from the checkout root: bash ledgers/PC3/scripts/PC3-a-r6/scans_a_r6.sh
S="course/modules/PC/PC3/index.html course/modules/PC/PC3/L01.html course/modules/PC/PC3/L02.html course/modules/PC/PC3/L03.html"
echo "== banned phrases in prose (pre blocks and tags stripped)"
for f in $S; do
  .venv/bin/python -I -c '
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
t = re.sub(r"<pre.*?</pre>", "", t, flags=re.S)
t = re.sub(r"<[^>]+>", " ", t)
pats = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
        "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
        "obviously", "clearly", "...", "…"]
hits = [(p, t.lower().count(p.lower())) for p in pats if t.lower().count(p.lower())]
print(sys.argv[1], "banned hits:", hits if hits else "none")
' "$f"
done
echo "== process words (whole words, full text)"; grep -n -i -w -E "build|builder|builders|round|rounds|verifier|requests|unit report|fixer" $S; echo "(end)"
echo "== D-terms outside the closure"; grep -n -i -E "martingale|stopping.time|optional.stopping|markov|poisson|kelly|capm|security market|duration|dcf|bayesian inference|adverse selection|inventory model|probability of informed|spread decomposition|roll spread|binomial distribution|permutation|combination|sigma-algebra|probability space" $S | cut -c1-160; echo "(end)"
echo "== citation words"; grep -n -i -E "zhou|crack|heard on|practical guide|edition|chapter|p\. [0-9]" $S | cut -c1-160; echo "(end)"
echo "== data and external references"; grep -n -E "data-cite|data-files|https?://" $S | cut -c1-160; echo "(end)"
echo "== P0.1 mentions"; grep -n -E "P0\.1" $S | cut -c1-120; echo "(end)"
echo "== registered and local macros used in slice math"; grep -o -E "\\\\[A-Za-z]+" $S | sort | uniq -c | sort -rn | head -70
echo "== structure counts"
for f in course/modules/PC/PC3/L01.html course/modules/PC/PC3/L02.html course/modules/PC/PC3/L03.html; do
  echo "$f quiz=$(grep -c 'class="item"' $f) problems=$(grep -c 'class="problem"' $f) solutions=$(grep -c '<details class="solution"' $f) misconceptions=$(grep -c 'class="misconception"' $f) grades=$(grep -o 'data-grade="[TABCDX]"' $f | wc -l | tr -d ' ')"
done
echo "index placement items=$(grep -c 'class="item"' course/modules/PC/PC3/index.html)"
echo "== theorem 3.10, adapted, martingale (should be 0)"; grep -c -E "Theorem 3.10|adapted|martingale|optional stopping" $S
echo "== why-it-matters question marks"; for f in course/modules/PC/PC3/L01.html course/modules/PC/PC3/L02.html course/modules/PC/PC3/L03.html; do echo "$f $(grep 'class="why-it-matters"' $f | grep -c '?')"; done
echo "== bag, ball label (should be 0)"; grep -c "bag, ball" course/modules/PC/PC3/L02.html tests/labs/PC3/lab-PC3-L02-1.py
echo "== lab twins: file and network access (should be 0)"; grep -c -E "open\(|read_text|csv|json\.|urllib|requests|http" tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py
echo "== figures and images (should be 0)"; grep -c -E "<svg|<img|<canvas" $S
echo "== project file names referenced by the hub and the project"; grep -n -o -E "policy\.py|pnl\.py|market_maker\.py" course/modules/PC/PC3/index.html course/modules/PC/PC3/project.html | sort | uniq -c
echo "== completion rung wording: hub vs project"; grep -n -o -E "cash-flow line and the mark line (removed|left blank)" course/modules/PC/PC3/index.html; grep -n -o -E "(two lines|line)[^.]{0,60}(left blank|blanked with)" course/modules/PC/PC3/project.html | head -3
