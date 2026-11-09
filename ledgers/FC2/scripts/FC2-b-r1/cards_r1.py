import json, collections, sys
cards = json.load(open(sys.argv[1]))
print("total", len(cards))
ids = [c["id"] for c in cards]
print("unique ids", len(set(ids)) == len(ids), "sequential", ids == [f"FC2-c{i:03d}" for i in range(1, len(ids)+1)])
fr = collections.Counter(c["front"].strip().lower() for c in cards)
bk = collections.Counter(c["back"].strip().lower() for c in cards)
print("dup fronts", [k for k, v in fr.items() if v > 1])
print("dup backs", [k for k, v in bk.items() if v > 1])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
for k, v in keys.items(): print("keys", v, k)
print("per lesson", sorted(collections.Counter(c["lesson"] for c in cards).items()))
print("grades", collections.Counter(c.get("grade", "<none>") for c in cards))
for c in cards:
    if c["lesson"] in ("L04", "L05", "L06") or c["id"] in ("FC2-c201",):
        print(c["id"], c["lesson"], "grade=" + str(c.get("grade")), "|F|", c["front"], "|B|", c["back"])
