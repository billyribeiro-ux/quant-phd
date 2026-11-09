"""Round-1 card scan for E1 slice b (L04-L06): full duplicate scan and card-number locator check.

Usage: python -I card_scan.py <checkout-root>
Prints (1) exact duplicate ids/fronts, (2) near-duplicate pairs (Jaccard >= 0.35 on front+back word sets),
(3) for each L04-L06 card, each cited numbered item (Definition/Lemma/Proposition/Theorem/Corollary/Remark/
Example/Problem/Assumption/Lab) and whether that label occurs in its lesson page text.
"""

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))

ids = Counter(c["id"] for c in cards)
fronts = Counter(c["front"].strip().lower() for c in cards)
print("exact duplicate ids:", [k for k, v in ids.items() if v > 1])
print("exact duplicate fronts:", [k for k, v in fronts.items() if v > 1])
print("total cards:", len(cards))


def words(c: dict) -> set[str]:
    text = (c["front"] + " " + c["back"]).lower()
    return {w for w in re.findall(r"[a-z]+", text) if len(w) > 2}


pairs = []
for i in range(len(cards)):
    wi = words(cards[i])
    for j in range(i + 1, len(cards)):
        wj = words(cards[j])
        jac = len(wi & wj) / len(wi | wj)
        if jac >= 0.35:
            pairs.append((round(jac, 3), cards[i]["id"], cards[j]["id"]))
pairs.sort(reverse=True)
print("near-duplicate pairs (Jaccard >= 0.35):", len(pairs))
for p in pairs[:40]:
    print("  ", p)

lesson_text = {}
for L in ("L04", "L05", "L06"):
    raw = (root / f"course/modules/E/E1/{L}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    lesson_text[L] = re.sub(r"\s+", " ", html.unescape(raw))

label = re.compile(r"\b(Definition|Lemma|Proposition|Theorem|Corollary|Remark|Example|Problem|Assumption|Lab) (\d+(?:\.\d+)?|[MPERA]\d|[A-Z])\b")
print("card number locators in L04-L06 cards:")
bad = []
for c in cards:
    if c["lesson"] not in lesson_text:
        continue
    found = label.findall(c["front"] + " " + c["back"])
    for kind, num in found:
        target = f"{kind} {num}"
        where = [L for L, t in lesson_text.items() if target in t]
        status = "OK" if c["lesson"] in where else "MISSING"
        if status == "MISSING":
            bad.append((c["id"], target))
        print(f"  {c['id']} ({c['lesson']}): {target} -> {where or 'NONE'} own-lesson {status}")
print("locators not found anywhere in L04-L06:", bad)
