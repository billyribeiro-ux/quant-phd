import json, difflib, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        fr = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        ba = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if fr > 0.6 or ba > 0.6:
            pairs.append((round(fr, 2), round(ba, 2), a["id"], a["lesson"], b["id"], b["lesson"]))
slice_pairs = [p for p in pairs if {p[3], p[5]} & {"L04", "L05", "L06"}]
for p in sorted(slice_pairs, reverse=True):
    print(p)
print("total pairs over 0.6 in deck:", len(pairs), "involving slice:", len(slice_pairs))
