# Full pairwise scan (all cards, front and back) for exact duplicates and near-duplicates. Prints counts and pairs above 0.6.
import difflib
import itertools
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
exact = []
near = []
for a, b in itertools.combinations(cards, 2):
    for field in ("front", "back"):
        if a[field].strip().lower() == b[field].strip().lower():
            exact.append((a["id"], b["id"], field))
        r = difflib.SequenceMatcher(None, a[field], b[field]).ratio()
        if r >= 0.6:
            near.append((round(r, 3), a["id"], b["id"], field))
print("exact duplicate field pairs:", exact)
print("near pairs (>=0.6):", len(near))
for r in sorted(near, reverse=True)[:12]:
    print(r)
