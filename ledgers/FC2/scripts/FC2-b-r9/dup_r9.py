import json, difflib, sys, itertools
cards = json.load(open(sys.argv[1]))
slice_ = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
pairs = []
for a, b in itertools.combinations(cards, 2):
    fr = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
    bk = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
    if (fr > 0.6 or bk > 0.6) and (a in slice_ or b in slice_):
        pairs.append((round(fr, 2), round(bk, 2), a["id"], b["id"]))
for p in sorted(pairs, reverse=True): print(p)
print("pairs", len(pairs))
# grade C cards need basis; T cards need no basis check here
for c in cards:
    if c.get("grade") == "C" and "basis" not in c: print("C without basis", c["id"])
    if c.get("basis") and c["lesson"] in ("L04", "L05", "L06"): print("basis", c["id"], c["basis"])
