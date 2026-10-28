import json, collections, re, sys
cards = json.load(open("/tmp/verify7-AC4-c/course/modules/AC/AC4/cards.json", encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("cards", len(cards), "dup ids", [k for k, v in ids.items() if v > 1], "dup fronts", [k for k, v in fronts.items() if v > 1])
sl = collections.Counter(c["lesson"] for c in cards)
print("per lesson", dict(sorted(sl.items())))
mine = [c for c in cards if c["lesson"] in ("L05", "L06")]
print("L05/L06 cards", len(mine), "ids", mine[0]["id"], "to", mine[-1]["id"])
for c in mine:
    for field in ("front", "back"):
        if re.search(r"\b(roughly|about|historically|\.\.\.)", c[field]):
            print("banned-ish", c["id"], field)
