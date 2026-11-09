import json, re, sys, itertools
from collections import Counter
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/E/E1/cards.json", encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
print("cards", len(cards), "unique ids", len(ids), "dup ids", [i for i, k in ids.items() if k > 1])
fr = Counter(c["front"] for c in cards); bk = Counter(c["back"] for c in cards)
print("dup fronts", [f for f, k in fr.items() if k > 1])
print("dup backs", [b for b, k in bk.items() if k > 1])
print("keys", Counter(tuple(sorted(c)) for c in cards))
print("grades", Counter(c.get("grade") for c in cards))
def toks(s):
    return set(re.findall(r"[A-Za-z]+|\d+(?:/\d+)?|[^\sA-Za-z\d]", s.lower()))
pairs = []
for a, b in itertools.combinations(cards, 2):
    ta = toks(a["front"] + " " + a["back"]); tb = toks(b["front"] + " " + b["back"])
    j = len(ta & tb) / len(ta | tb)
    if j >= 0.45:
        pairs.append((round(j, 2), a["id"], b["id"]))
pairs.sort(reverse=True)
print("near-dup pairs (Jaccard >= 0.45):", len(pairs))
for p in pairs:
    print(p)
