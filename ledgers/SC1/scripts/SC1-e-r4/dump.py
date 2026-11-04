import json, sys, html, re
src = sys.argv[1]
cards = json.load(open(src, encoding="utf-8"))
print(type(cards), len(cards))
ids = [c["id"] for c in cards]
print("distinct", len(set(ids)))
keys = {}
for c in cards:
    k = tuple(sorted(c.keys()))
    keys[k] = keys.get(k, 0) + 1
print(keys)
from collections import Counter
print(Counter(c["lesson"] for c in cards))
print(Counter((c.get("grade"), c.get("basis")) for c in cards))
print("cite nonempty", sum(1 for c in cards if c.get("cite")))
for c in cards:
    print(c["id"], c["lesson"], c.get("grade"), c.get("basis"), "|F:", c["front"], "|B:", c["back"])
