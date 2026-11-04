import json, sys, difflib, itertools
cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)))
fronts = [c["front"] for c in cards]
backs = [c["back"] for c in cards]
print("duplicate fronts", len(cards) - len(set(fronts)), "duplicate backs", len(cards) - len(set(backs)))
pairs = []
for i, j in itertools.combinations(range(len(cards)), 2):
    rf = difflib.SequenceMatcher(None, fronts[i], fronts[j]).ratio()
    rb = difflib.SequenceMatcher(None, backs[i], backs[j]).ratio()
    if max(rf, rb) >= 0.6:
        pairs.append((round(rf, 2), round(rb, 2), ids[i], ids[j]))
print("pairs with front or back ratio >= 0.6:", len(pairs))
for p in pairs: print(p)
# schema
bad = []
for c in cards:
    if c["lesson"] not in {f"L0{n}" for n in range(1, 9)}: bad.append((c["id"], "lesson"))
    if c.get("cite"): bad.append((c["id"], "cite nonempty"))
    if ("grade" in c) != ("basis" in c): bad.append((c["id"], "grade/basis pairing"))
    if "grade" in c and c["grade"] not in {"T", "A", "B", "C", "D", "X"}: bad.append((c["id"], "grade value"))
print("schema problems", bad)
