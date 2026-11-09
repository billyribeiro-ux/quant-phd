"""Duplicate and near-duplicate scan over the whole CS2 deck and the L09-L11 subset (CS2-c r3)."""
import json, difflib, sys, itertools, re
cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
def norm(s): return re.sub(r"\s+", " ", s.lower()).strip()
seen_f, seen_b = {}, {}
for c in cards:
    for key, store in (("front", seen_f), ("back", seen_b)):
        k = norm(c[key])
        if k in store: print("EXACT DUP", key, c["id"], store[k])
        store[k] = c["id"]
mine = [c for c in cards if c["lesson"] in ("L09", "L10", "L11")]
print("L09-L11 cards", len(mine))
pairs = []
for a, b in itertools.combinations(cards, 2):
    if a["lesson"] not in ("L09", "L10", "L11") and b["lesson"] not in ("L09", "L10", "L11"):
        continue
    r = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
    rb = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
    if r > 0.5 or rb > 0.6:
        pairs.append((round(max(r, rb), 2), a["id"], b["id"], round(r, 2), round(rb, 2)))
for p in sorted(pairs, reverse=True)[:25]:
    print("NEAR", p)
