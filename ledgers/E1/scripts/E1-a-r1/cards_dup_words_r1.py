import json, re, sys, itertools
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/E/E1/cards.json", encoding="utf-8"))
def words(s):
    return set(re.findall(r"[a-z]+|\d+", s.lower()))
pairs = []
for a, b in itertools.combinations(cards, 2):
    ta = words(a["front"] + " " + a["back"]); tb = words(b["front"] + " " + b["back"])
    j = len(ta & tb) / len(ta | tb)
    if j >= 0.45:
        pairs.append((round(j, 3), a["id"], b["id"], a["lesson"], b["lesson"]))
pairs.sort(reverse=True)
print("word-token near-dup pairs (Jaccard >= 0.45):", len(pairs))
for p in pairs:
    print(p)
print("--- front-only exact-word duplicates (Jaccard fronts >= 0.6):")
for a, b in itertools.combinations(cards, 2):
    fa, fb = words(a["front"]), words(b["front"])
    j = len(fa & fb) / len(fa | fb)
    if j >= 0.6:
        print(round(j, 3), a["id"], b["id"])
