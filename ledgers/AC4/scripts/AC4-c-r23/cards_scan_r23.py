"""Round 23 card scan for AC4 slice c. Usage: cards_scan_r23.py <checkout>. Full duplicate scan of cards.json."""
import collections
import json
import re
import sys

root = sys.argv[1]
with open(f"{root}/course/modules/AC/AC4/cards.json", encoding="utf-8") as fh:
    cards = json.load(fh)
ids = collections.Counter(c["id"] for c in cards)
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()  # noqa: E731
fronts = collections.Counter(norm(c["front"]) for c in cards)
backs = collections.Counter(norm(c["back"]) for c in cards)
print("cards", len(cards), "dup ids", [k for k, v in ids.items() if v > 1])
print("dup fronts", [k for k, v in fronts.items() if v > 1])
print("dup backs", [k for k, v in backs.items() if v > 1])
print("per lesson", dict(sorted(collections.Counter(c["lesson"] for c in cards).items())))
mine = [c for c in cards if c["lesson"] in ("L05", "L06")]
print("L05/L06 cards", len(mine), mine[0]["id"], "to", mine[-1]["id"], [c["id"] for c in mine])
for c in cards:
    for field in ("front", "back"):
        if re.search(r"\b(roughly|about|historically|typically|usually)\b|\.\.\.", c[field]):
            print("banned-ish", c["id"], c["lesson"], field)
for c in cards:
    if c["grade"] not in ("T", "C", "A", "B", "D", "E", "F"):
        print("grade?", c["id"], c["grade"])
    if c["grade"] == "C" and "basis" not in c:
        print("C without basis", c["id"])
