import json, difflib, itertools
root = "/Users/billyribeiro/.fanout/wt/verifyS7-FC2-b"
cards = json.load(open(f"{root}/course/modules/FC/FC2/cards.json"))
pairs = []
for a, b in itertools.combinations(cards, 2):
    fr = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
    bk = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
    if fr >= 0.6 or bk >= 0.6:
        pairs.append((round(fr, 2), round(bk, 2), a["id"], a["lesson"], b["id"], b["lesson"]))
print("near-duplicate pairs (front>=0.6 or back>=0.6):", len(pairs))
for p in sorted(pairs, reverse=True)[:40]:
    print(p)
