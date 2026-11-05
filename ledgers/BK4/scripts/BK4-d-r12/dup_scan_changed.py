# Duplicate scan: every pair of cards, fronts and backs, similarity ratio; prints exact duplicates and pairs above 0.6,
# and flags the cards changed since the round-11 pin (c043, c044, c047, c086, c090, c091, c094) in the output.
import difflib
import json
cards = json.load(open("course/modules/BK/BK4/cards.json", encoding="utf-8"))
changed = {"BK4-c043", "BK4-c044", "BK4-c047", "BK4-c086", "BK4-c090", "BK4-c091", "BK4-c094"}
ids = [c["id"] for c in cards]
assert len(ids) == len(set(ids)), "duplicate ids"
exact = []
near = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        for fld in ("front", "back"):
            if a[fld] == b[fld]:
                exact.append((a["id"], b["id"], fld))
            r = difflib.SequenceMatcher(None, a[fld], b[fld]).ratio()
            if r > 0.6:
                near.append((round(r, 3), a["id"], b["id"], fld, bool({a["id"], b["id"]} & changed)))
print("cards", len(cards), "unique ids", len(set(ids)))
print("exact duplicates", exact)
print("pairs above 0.6 (field-level):", len(near))
for n in sorted(near, reverse=True)[:40]:
    print(n)
