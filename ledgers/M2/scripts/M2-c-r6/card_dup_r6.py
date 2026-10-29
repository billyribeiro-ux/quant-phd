"""Round-4 card scan for M2 slice c: duplicate fronts and backs across cards.json, and ids per lesson."""
import collections
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf8"))
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("cards", len(cards), "ids unique", len({c["id"] for c in cards}) == len(cards))
print("duplicate fronts", [f for f, n in fronts.items() if n > 1])
print("duplicate backs", [b[:60] for b, n in backs.items() if n > 1])
for lesson in ("L13", "L14", "L15", "L16", "L17", "L18"):
    ids = [c["id"] for c in cards if c["lesson"] == lesson]
    print(lesson, len(ids), ids[0], ids[-1])
