"""Exact duplicate and near-duplicate scan of course/modules/SC/SC1/cards.json; also checks card ids are unique and well formed."""
import difflib, json, re, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)), "all SC1-cNNN", all(re.fullmatch(r"SC1-c\d{3}", i) for i in ids))
print("lesson counts", {l: sum(1 for c in cards if c["lesson"] == l) for l in sorted({c["lesson"] for c in cards})})
fronts = [c["front"] for c in cards]; backs = [c["back"] for c in cards]
print("identical fronts", [(a, b) for i, a in enumerate(ids) for j, b in enumerate(ids) if i < j and fronts[i] == fronts[j]])
print("identical backs", [(a, b) for i, a in enumerate(ids) for j, b in enumerate(ids) if i < j and backs[i] == backs[j]])
hits = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = difflib.SequenceMatcher(None, fronts[i] + " " + backs[i], fronts[j] + " " + backs[j]).ratio()
        if r >= 0.6:
            hits.append((round(r, 3), ids[i], ids[j]))
print("pairs ratio>=0.6:", sorted(hits, reverse=True))
bad = [c["id"] for c in cards if re.search(r"builder|verifier|round|fixer|ledger|reviewer|sub-agent", c["front"] + c["back"], re.I)]
print("process words", bad)
