import json, collections, pathlib, re
D = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS6-FC1-b/course/modules/FC/FC1")
cards = json.loads((D / "cards.json").read_text(encoding="utf-8"))
print("total cards", len(cards))
ids = [c["id"] for c in cards]
dup = [k for k, v in collections.Counter(ids).items() if v > 1]
print("duplicate ids", dup)
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs", [k for k, v in backs.items() if v > 1])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets", keys)
print("grades", collections.Counter(c.get("grade") for c in cards))
for c in cards:
    if c["lesson"] in ("L04", "L05") or c["id"] in ("FC1-c050",):
        print(json.dumps(c, ensure_ascii=False))
