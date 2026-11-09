import json, difflib, re, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
byid = {c["id"]: c for c in cards}
def norm(s):
    return re.sub(r"[^a-z0-9ρφλκσ]+", " ", s.lower()).strip()
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        rb = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
        if rf >= 0.55 or rb >= 0.55 or (rf + rb) / 2 >= 0.45:
            pairs.append((round((rf + rb) / 2, 3), round(rf, 3), round(rb, 3), a["id"], b["id"]))
pairs.sort(reverse=True)
print("pairs flagged:", len(pairs))
for p in pairs[:40]:
    print(p)
print("--- exact duplicate fronts:", len(cards) - len({c['front'] for c in cards}))
print("--- exact duplicate backs:", len(cards) - len({c['back'] for c in cards}))
print("--- pairs with both back ratio >= 0.8:")
for p in pairs:
    if p[2] >= 0.8: print(p)
