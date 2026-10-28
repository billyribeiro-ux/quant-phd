import json, sys, difflib, itertools
cards = json.load(open(sys.argv[1], encoding="utf-8"))
fr = {c["id"]: c["front"] for c in cards}
bk = {c["id"]: c["back"] for c in cards}
pairs = []
for a, b in itertools.combinations(sorted(fr), 2):
    r = difflib.SequenceMatcher(None, fr[a].lower(), fr[b].lower()).ratio()
    rb = difflib.SequenceMatcher(None, bk[a].lower(), bk[b].lower()).ratio()
    if r >= 0.6 or rb >= 0.6:
        pairs.append((round(r, 2), round(rb, 2), a, b))
for p in sorted(pairs, reverse=True)[:30]:
    print(p)
print("exact front dups", len(fr) - len(set(fr.values())), "exact back dups", len(bk) - len(set(bk.values())))
