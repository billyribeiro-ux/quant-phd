import json, collections, sys, re
cards = json.load(open(sys.argv[1]))
print("count", len(cards))
ids = [c["id"] for c in cards]
print("dup ids", [i for i, n in collections.Counter(ids).items() if n > 1])
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("dup fronts", [f for f, n in fronts.items() if n > 1][:10])
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("dup backs", [f[:60] for f, n in backs.items() if n > 1][:10])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets", keys)
print("lessons", collections.Counter(c["lesson"] for c in cards))
for c in cards:
    if c["id"] in ("AC4-c073",):
        print(json.dumps(c, ensure_ascii=False))
