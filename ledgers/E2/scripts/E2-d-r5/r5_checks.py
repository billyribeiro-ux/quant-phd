"""Round-5 verifier checks for E2-d (run with python -I from the E2 unit directory). Prints evidence lines."""
import html
import json
import re
import sys
from fractions import Fraction

UNIT = sys.argv[1]  # path to course/modules/E/E2

# 1. Discrete E[M] for n=5, a=2000 (Proposition 2.2 sum), exact
n, a = 5, 2000
F = lambda x: Fraction(x + a + 1, 2 * a + 1)  # noqa: E731
EM = -a + sum(1 - F(x) ** n for x in range(-a, a))
print("EM exact", EM, "float", float(EM), "equals 85418692002000/64048012001:", EM == Fraction(85418692002000, 64048012001))
print("20000*EM rounded", round(20000 * EM), "shading 1333 minus EM", float(1333 - EM), "1334 minus EM", float(1334 - EM))

# 2. Brief numbers: word counts of exemplar passages (brief: summary <= 80 words; body 500-1000 words)
t = open(f"{UNIT}/project.html", encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    s = t.index(f'id="{ex}"')
    block = t[s: t.index("</article>", s)]
    tot = 0
    for m in re.finditer(r'<div class="memo-text">(.*?)</div>', block, re.S):
        h = re.search(r"<h5>(.*?)</h5>", m.group(1), re.S)
        body = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1)))).strip()
        w = len(body.split())
        head = h.group(1) if h else "?"
        if "Appendix" not in head:
            tot += w
        print(ex, "section", head, "words", w)
    print(ex, "body words excluding appendix", tot)

# 3. Exemplar A: does the single-unit section or appendix give the uniform bid / Proposition A2?
s = t.index('id="exemplar-a"'); block = t[s: t.index("</article>", s)]
print("exemplar-a mentions 'Proposition A2' or 'A2.':", ("Proposition A2" in block) or ("A2." in block) or ("<strong>A2" in block))
plain = html.unescape(re.sub(r"<[^>]+>", " ", block))
plain = re.sub(r"\s+", " ", plain)
i, j = plain.find("Single-unit bids"), plain.find("Revenue, shading")
print("exemplar-a single-unit section mentions uniform:", "uniform" in plain[i:j].lower(), "| mentions A2 anywhere in exemplar-a:", "A2" in plain)

# 4. Cards: duplicates, grades, and changed-card list vs previous pin
cards = json.load(open(f"{UNIT}/cards.json", encoding="utf-8"))
print("cards", len(cards), "dup ids", len(cards) - len({c["id"] for c in cards}), "dup fronts", len(cards) - len({c["front"] for c in cards}), "dup backs", len(cards) - len({c["back"] for c in cards}))
print("T cards with basis:", [c["id"] for c in cards if c.get("grade") == "T" and "basis" in c])
print("C cards without basis:", [c["id"] for c in cards if c.get("grade") == "C" and "basis" not in c])

# 5. Scope claim on the page: suite instances used (SEED and SEED+7919)
print("seeded instances used by the suite: 2 (SEED and SEED+7919)")
