"""Full duplicate scan of course/modules/AC/AC2/cards.json (verifier round 1, slice L07-L08)."""
import json
import re
from itertools import combinations

cards = json.load(open("course/modules/AC/AC2/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
print("id sequence gaps:", sorted(set(f"AC2-c{n:03d}" for n in range(1, len(cards) + 1)) - set(ids))[:20])


def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))


pairs = []
for a, b in combinations(cards, 2):
    ta, tb = toks(a["front"] + " " + a["back"]), toks(b["front"] + " " + b["back"])
    j = len(ta & tb) / max(1, len(ta | tb))
    if j >= 0.45:
        pairs.append((round(j, 2), a["id"], b["id"], a["front"][:60], b["front"][:60]))
print("pairs with token Jaccard >= 0.45:", len(pairs))
for p in sorted(pairs, reverse=True)[:20]:
    print(p)
fronts = [c["front"].strip().lower() for c in cards]
print("exact duplicate fronts:", len(fronts) - len(set(fronts)))
