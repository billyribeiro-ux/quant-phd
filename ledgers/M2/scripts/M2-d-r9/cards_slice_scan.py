"""Count M2 cards in lessons L19-L24, check ids are unique, and check fronts are not duplicated."""
import json
import sys
from collections import Counter

cards = json.load(open(f"{sys.argv[1]}/course/modules/M/M2/cards.json", encoding="utf-8"))
slice_cards = [c for c in cards if c["lesson"] in {"L19", "L20", "L21", "L22", "L23", "L24"}]
print("all M2 cards:", len(cards), "unique ids:", len({c["id"] for c in cards}))
print("slice cards:", len(slice_cards))
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts across M2:", [f for f, n in fronts.items() if n > 1])
for c in slice_cards:
    if c["id"] == "M2-c299":
        print("c299:", c["lesson"], "grade" in c, c["back"][:90])
