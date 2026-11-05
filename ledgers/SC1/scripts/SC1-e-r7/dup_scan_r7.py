"""Full pairwise near-duplicate scan of SC1 cards (front, back and joined text). Usage: python -I dup_scan_r7.py <cards.json>.
Prints the pairs whose joined-text similarity is at least 0.6, and any identical front or back text."""
import difflib
import json
import sys
from itertools import combinations

cards = json.load(open(sys.argv[1], encoding="utf-8"))
def norm(s):
    return " ".join(s.split())
for a, b in combinations(cards, 2):
    if norm(a["front"]) == norm(b["front"]) or norm(a["back"]) == norm(b["back"]):
        print("IDENTICAL FIELD", a["id"], b["id"])
pairs = []
for a, b in combinations(cards, 2):
    r = difflib.SequenceMatcher(None, norm(a["front"] + " " + a["back"]), norm(b["front"] + " " + b["back"])).ratio()
    if r >= 0.6:
        pairs.append((r, a["id"], b["id"]))
pairs.sort(reverse=True)
print("pairs checked:", len(cards) * (len(cards) - 1) // 2, " pairs with ratio >= 0.6:", len(pairs))
for r, x, y in pairs[:25]:
    print(f"{r:.3f} {x} {y}")
