#!/bin/bash
# Round-4 verifier: grep and link checks for PC3 slice a. Run from the checkout root:
#   bash ledgers/PC3/scripts/PC3-a-r4/link_and_grep_checks_a_r4.sh > ledgers/PC3/scripts/PC3-a-r4/outputs/link_and_grep_checks_a_r4.out
S=course/modules/PC/PC3
PAGES="$S/index.html $S/L01.html $S/L02.html $S/L03.html"

echo "== data-cite hits (registry keys cited on the pages)"
grep -c "data-cite" $PAGES

echo "== 'Theorem 3.10' and 'adapted' hits"
grep -c "Theorem 3.10\|adapted" $PAGES

echo "== registered symbols that must not appear (T, Phi, gamma, R^ast, R_f, mathbb Q)"
grep -n -o "\\\\(\s*T[^a-zA-Z]\|\bT\s*=\|Phi\|gamma\|mathbb{Q}\|R_f\|R\^\\\\ast" $PAGES || echo "no hits"

echo "== data-file reads in PC3 twins and grader"
grep -ln "read_text\|open(\|csv\|json.load\|Path(" tests/labs/PC3/*.py $S/grader/*.py 2>/dev/null || echo "no hits"

echo "== data-files attributes on the slice pages"
grep -c "data-files" $S/L01.html $S/L02.html $S/L03.html

echo "== cross-reference counts"
for pat in "Research problem R1" "Research problem R3" "Problem P2" "Problem P3" "Section 4" "Section 3" "Example 2.9" "Example 3.11" "Lab 1, Part 3b" "Lab 1, Part 4" "Lab 1, Part 2"; do
  printf "%s: " "$pat"; grep -c "$pat" $S/L01.html $S/L02.html $S/L03.html | tr "\n" " "; echo
done

echo "== concept links on the slice pages: target id and the concepts.html section that holds it"
.venv/bin/python -I - <<'PY'
import re
conc = open("course/concepts.html", encoding="utf-8").read()
sec_of = {}
for m in re.finditer(r'<section aria-labelledby="c-([^"]+)">(.*?)</section>', conc, re.S):
    for i in re.findall(r'id="([^"]+)"', m.group(2)):
        sec_of.setdefault(i, m.group(1))
for p in ["index", "L01", "L02", "L03"]:
    t = open(f"course/modules/PC/PC3/{p}.html", encoding="utf-8").read()
    ids = sorted(set(re.findall(r"concepts\.html#([A-Za-z0-9._\-]+)", t)))
    print(p, [(i, sec_of.get(i, "MISSING")) for i in ids])
    print(p, "P0.1 targets:", [i for i in ids if sec_of.get(i) == "P0.1"])
PY

echo "== P0.1 section entries read 'not yet released'"
grep -c "not yet released" course/concepts.html
sed -n 34,41p course/concepts.html | grep -c "not yet released"

echo "== project labs and the grader read no data file"
grep -ln "read_text\|open(" tests/labs/PC3/lab-PC3-project-*.py course/modules/PC/PC3/grader/*.py 2>/dev/null || echo "no hits"

echo "== M4 definitions that PC3 restates (dfn tags in the prerequisite)"
grep -n "data-concept=\"expectation\"\|data-concept=\"conditional-expectation-elementary\"" course/modules/M/M4/L02.html course/modules/M/M4/L04.html | cut -c1-160
grep -n "event" course/modules/M/M4/L01.html | head -2 | cut -c1-160

echo "== PC3 dfn tags on the slice pages"
grep -n "<dfn" $PAGES | cut -c1-160
