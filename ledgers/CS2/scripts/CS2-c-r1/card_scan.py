"""Duplicate scan of cards.json for CS2 (verifier round 1, slice c)."""
import json, re, sys, difflib
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/CS/CS2/cards.json").read_text())
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower())
fronts = [norm(c["front"]) for c in cards]
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)), "unique fronts", len(set(fronts)))
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = difflib.SequenceMatcher(None, fronts[i], fronts[j]).ratio()
        if r > 0.8:
            pairs.append((round(r, 2), ids[i], ids[j], cards[i]["front"], cards[j]["front"]))
print("near-duplicate fronts (ratio > 0.8):", len(pairs))
for p in pairs[:20]:
    print(p)
for c in cards:
    if c["lesson"] in ("L09", "L10", "L11"):
        print(c["id"], c["lesson"], c.get("grade"), c.get("basis", "-"))
