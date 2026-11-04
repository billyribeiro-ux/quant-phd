"""Full scan of course/modules/FC/FC2/cards.json: ids, duplicates, near-duplicate fronts, and card numbers in lessons.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r5/cards_scan_r5.py <repo_root>
Prints every near-duplicate pair (fronts or backs with difflib ratio >= 0.6) and checks that each numbered item the card
cites (Proposition, Theorem, Definition, Remark, Lemma, Example, Assumption, Problem with a number) occurs in the
card's own lesson text.
"""

import difflib
import html
import json
import os
import re
import sys

root = sys.argv[1]
base = os.path.join(root, "course", "modules", "FC", "FC2")
cards = json.load(open(os.path.join(base, "cards.json"), encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)) == len(ids))
print("unique fronts", len({c["front"] for c in cards}) == len(cards), "unique backs", len({c["back"] for c in cards}) == len(cards))
print("grades", sorted({c.get("grade", "-") for c in cards}))
print("lessons", sorted({c["lesson"] for c in cards}))
texts = {}
for lesson in sorted({c["lesson"] for c in cards}):
    raw = open(os.path.join(base, lesson + ".html"), encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    texts[lesson] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        r = max(
            difflib.SequenceMatcher(None, a["front"], b["front"]).ratio(),
            difflib.SequenceMatcher(None, a["back"], b["back"]).ratio(),
        )
        if r >= 0.6:
            pairs.append((round(r, 3), a["id"], b["id"]))
print("near-duplicate pairs (ratio >= 0.6):", len(pairs))
for p in sorted(pairs, reverse=True)[:20]:
    print("  ", p)
pat = re.compile(r"\b(Proposition|Theorem|Definition|Remark|Lemma|Example|Assumption|Problem|Section)\s+(\d+(?:\.\d+)?)")
missing = []
for c in cards:
    for kind, num in pat.findall(c["front"] + " " + c["back"]):
        token = f"{kind} {num}"
        if token not in texts[c["lesson"]] and not re.search(re.escape(token) + r"(?!\d)", texts[c["lesson"]]):
            missing.append((c["id"], c["lesson"], token))
print("card numbers not found in own lesson:", missing)
