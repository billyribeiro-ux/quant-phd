"""Round-4 structural checks of cards.json (PC3-d). usage: python -I cards_struct_r4.py <checkout-root>"""
import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("count", len(cards), "unique ids", len(set(ids)) == len(ids))
nums = sorted(int(i.split("c")[1]) for i in ids)
print("id numbers", nums[0], "..", nums[-1])
missing = sorted(set(range(1, nums[-1] + 1)) - set(nums))
print("missing ids in 1..max:", missing)
print("file order equals sorted id order:", ids == sorted(ids))
print("out-of-order positions:", [(k, ids[k - 1], ids[k]) for k in range(1, len(ids)) if ids[k] < ids[k - 1]])
print("key sets:", Counter(tuple(sorted(c.keys())) for c in cards))
print("cards per lesson:", dict(sorted(Counter(c["lesson"] for c in cards).items())))
print("grades:", dict(Counter(c.get("grade") for c in cards)))
for c in cards:
    g = c.get("grade")
    if g in ("T", "C") and not c.get("basis"):
        print("MISSING BASIS", c["id"])
    if g is None and "basis" in c:
        print("BASIS KEY ON NONE", c["id"], repr(c.get("basis")))
    if c.get("cite") != []:
        print("CITE NON-EMPTY", c["id"], c.get("cite"))
fronts = Counter(c["front"] for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
backs = Counter(c["back"] for c in cards)
print("duplicate backs:", [f for f, n in backs.items() if n > 1])
for c in cards:
    for k in ("front", "back"):
        if c[k] != c[k].strip() or "  " in c[k]:
            print("WHITESPACE", c["id"], k)
