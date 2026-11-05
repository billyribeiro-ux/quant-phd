"""Schema, id, grade/basis, and duplicate checks for PC3 cards.json (round 8)."""
import difflib
import json
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
nums = [int(i.split("-c")[1]) for i in ids]
print("ascending:", nums == sorted(nums))
print("gaps:", sorted(set(range(1, max(nums) + 1)) - set(nums)))
print("keys:", Counter(tuple(sorted(c.keys())) for c in cards))
print("grade without basis:", [c["id"] for c in cards if ("grade" in c) != ("basis" in c)])
print("cite non-empty:", [c["id"] for c in cards if c.get("cite")])
print("empty front/back:", [c["id"] for c in cards if not c["front"].strip() or not c["back"].strip()])
print("grade counts:", Counter(c.get("grade") for c in cards))
print("per lesson:", sorted(Counter(c["lesson"] for c in cards).items()))
fr = Counter(c["front"] for c in cards)
bk = Counter(c["back"] for c in cards)
print("exact duplicate fronts:", [f[:60] for f, n in fr.items() if n > 1])
print("exact duplicate backs:", [b[:60] for b, n in bk.items() if n > 1])
near = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a = cards[i]["front"] + " " + cards[i]["back"]
        b = cards[j]["front"] + " " + cards[j]["back"]
        r = difflib.SequenceMatcher(None, a, b).ratio()
        if r > 0.6:
            near.append((round(r, 3), cards[i]["id"], cards[j]["id"]))
print("near-duplicate pairs (ratio > 0.6):", sorted(near, reverse=True))
