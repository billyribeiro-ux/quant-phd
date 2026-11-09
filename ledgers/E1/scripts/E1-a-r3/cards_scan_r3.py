"""Full scan of E1 cards: ids, exact duplicate fronts and backs, near-duplicate pairs (Jaccard on word sets) (verifier r3)."""
import json
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

cards = json.loads(Path(sys.argv[1], "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)), "dup ids", [i for i, n in Counter(ids).items() if n > 1])
print("dup fronts", [k for k, n in Counter(c["front"].strip().lower() for c in cards).items() if n > 1])
print("dup backs", [k for k, n in Counter(c["back"].strip().lower() for c in cards).items() if n > 1])
words = [set(re.findall(r"[a-z]+", (c["front"] + " " + c["back"]).lower())) for c in cards]
pairs = []
for (i, a), (j, b) in combinations(enumerate(words), 2):
    jac = len(a & b) / len(a | b)
    if jac >= 0.45:
        pairs.append((round(jac, 2), cards[i]["id"], cards[j]["id"]))
for p in sorted(pairs, reverse=True):
    print("near-dup", p)
print("near-dup pairs >=0.45:", len(pairs))
print("cards without grade:", sorted(c["id"] for c in cards if "grade" not in c))
