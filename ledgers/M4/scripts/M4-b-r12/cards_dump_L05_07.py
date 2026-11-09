"""Round 12 slice b: dump the L05-L07 cards (id, front, back, grade, basis) and per-lesson counts; check unique ids."""
import json

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD12-M4-b/"
cards = json.load(open(ROOT + "course/modules/M/M4/cards.json", encoding="utf-8"))
from collections import Counter

print("cards", len(cards), "per lesson", sorted(Counter(c["lesson"] for c in cards).items()))
print("duplicate ids", len(cards) - len({c["id"] for c in cards}))
for c in cards:
    if c["lesson"] in ("L05", "L06", "L07"):
        print(json.dumps(c, ensure_ascii=False))
