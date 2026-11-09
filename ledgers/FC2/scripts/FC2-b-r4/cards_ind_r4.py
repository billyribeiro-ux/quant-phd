"""Round-4 independent card checks for FC2 L04-L06: deck counts, exact and near duplicates, slice listing.

Run from the checkout root: python -I ledgers/FC2/scripts/FC2-b-r4/cards_ind_r4.py
"""
import collections
import json
import re

cards = json.load(open("course/modules/FC/FC2/cards.json", encoding="utf-8"))
print("total cards", len(cards), "unique ids", len({c["id"] for c in cards}))
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("exact duplicate fronts", [f for f, n in fronts.items() if n > 1])
print("grades present", sorted({str(c.get("grade")) for c in cards}))


def norm(s):
    return set(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())


pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        A, B = norm(a["front"] + " " + a["back"]), norm(b["front"] + " " + b["back"])
        j = len(A & B) / len(A | B)
        if j >= 0.45 and {a["lesson"], b["lesson"]} & {"L04", "L05", "L06"}:
            pairs.append((round(j, 2), a["id"], a["lesson"], b["id"], b["lesson"]))
print("near-duplicate pairs touching L04-L06 (Jaccard >= 0.45, front+back):", sorted(pairs, reverse=True))

sl = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("slice cards", len(sl), dict(collections.Counter(c["lesson"] for c in sl)))
for c in sl:
    print(f'{c["id"]} {c["lesson"]} grade={c.get("grade")} basis={c.get("basis")}')
    print("  F:", c["front"])
    print("  B:", c["back"])
