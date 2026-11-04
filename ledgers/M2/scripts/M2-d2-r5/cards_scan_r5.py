import json, collections
cards = json.load(open("/Users/billyribeiro/.fanout/wt/verifyD5-M2-d2/course/modules/M/M2/cards.json", encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
print("cards", len(cards), "dup ids", [i for i, n in ids.items() if n > 1])
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("dup fronts", [f for f, n in fronts.items() if n > 1])
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("dup backs", [f[:60] for f, n in backs.items() if n > 1])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets", keys)
for c in cards:
    if c["lesson"] in ("L22", "L23", "L24"):
        assert c["id"].startswith("M2-c")
bylesson = collections.Counter(c["lesson"] for c in cards)
print("per lesson", sorted(bylesson.items()))
# ids that look like they belong to L22-L24 by number range
