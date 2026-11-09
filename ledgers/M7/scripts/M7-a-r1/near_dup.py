"""M7-a round 1 witness: near-duplicate scan over the L01-L03 cards (Jaccard on word sets of front+back)."""
import json
import re
import sys

root = sys.argv[1]
cards = [c for c in json.load(open(f"{root}/course/modules/M/M7/cards.json", encoding="utf-8")) if c["lesson"] in ("L01", "L02", "L03")]
def words(c):
    return set(re.findall(r"[a-z]+", (c["front"] + " " + c["back"]).lower())) - {"the", "a", "of", "and", "is", "in", "to", "for", "that", "it", "on", "with", "by", "as", "or", "an", "be", "this", "at", "if", "not", "true", "false", "misconception"}
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        wa, wb = words(a), words(b)
        j = len(wa & wb) / max(1, len(wa | wb))
        if j >= 0.35:
            pairs.append((round(j, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
for p in sorted(pairs, reverse=True):
    print(p)
print("pairs >= 0.35:", len(pairs))
