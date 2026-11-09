# Round-5 whole-deck duplicate scan for course/modules/FC/FC2/cards.json (all 171 cards).
import json, difflib, re
cards = json.load(open("/Users/billyribeiro/.fanout/wt/verifyS5-FC2-b/course/modules/FC/FC2/cards.json", encoding="utf-8"))
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}))
def norm(s): return re.sub(r"\s+", " ", s.lower()).strip()
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        rb = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
        if rf >= 0.6 or rb >= 0.6 or (rf + rb) >= 1.2:
            pairs.append((round(rf, 2), round(rb, 2), a["id"], a["lesson"], b["id"], b["lesson"]))
pairs.sort(key=lambda t: -(t[0] + t[1]))
for p in pairs[:40]:
    print(p)
print("pairs flagged", len(pairs))
