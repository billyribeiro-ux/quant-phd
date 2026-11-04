"""BK4-b round 4 scans: why-it-matters word counts, cards duplicate scan, card grade/basis rule,
Assumption 4 uses in L04, and first uses of define-before-use terms in L05.

Run from the checkout root: python3 -I ledgers/BK4/scripts/BK4-b-r4/scan_r4.py
"""

import html
import json
import re

root = "."


def read(path):
    with open(f"{root}/{path}", encoding="utf-8") as fh:
        return fh.read()


# 1. why-it-matters word counts
for lesson in ("L04", "L05"):
    text = read(f"course/modules/BK/BK4/{lesson}.html")
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S).group(1)
    plain = html.unescape(re.sub(r"<[^>]+>", "", why))
    plain = re.sub(r"\\\((.*?)\\\)", r"\1", plain)
    print(f"why-words {lesson} {len(plain.split())}")

# 2. cards: duplicates, grade/basis rule, L04/L05 coverage
cards = json.load(open(f"{root}/course/modules/BK/BK4/cards.json", encoding="utf-8"))
print(f"cards total {len(cards)}")
print("duplicate fronts", [f for f in {c["front"] for c in cards} if sum(c["front"] == f for c in cards) > 1])
print("duplicate ids", [i for i in {c["id"] for c in cards} if sum(c["id"] == i for c in cards) > 1])
bad = [c["id"] for c in cards if c.get("grade") not in (None, "T") and not (c.get("cite") or str(c.get("basis", "")).strip())]
print("non-T grade without cite or basis", bad)
tb = [c["id"] for c in cards if c.get("grade") == "T" and not str(c.get("basis", "")).strip() and c["lesson"] in ("L04", "L05")]
print("L04/L05 grade T without basis", tb)
sel = [c["id"] for c in cards if c["lesson"] in ("L04", "L05")]
print("L04/L05 cards", len(sel), sel[0], sel[-1])

# 3. Assumption 4 uses in L04 (the list at :85 must name every use in a derivation or check)
for n, line in enumerate(read("course/modules/BK/BK4/L04.html").splitlines(), 1):
    if re.search(r"Assumption 4|valuation convention|haircut", line):
        print(f"A4 L04:{n} " + re.sub(r"<[^>]+>", "", line).strip()[:110])

# 4. define-before-use: first occurrence lines of terms in L05
l05 = read("course/modules/BK/BK4/L05.html").splitlines()
for term in ("comonotone", "delay", "joint law", "settlement failure", "operational risk", "indicator"):
    hits = [n for n, line in enumerate(l05, 1) if term in line.lower()]
    print(f"first-use {term!r} L05 lines {hits[:4]}")
