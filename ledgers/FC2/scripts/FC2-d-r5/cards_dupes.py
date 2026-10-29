"""Round 5 FC2-d: near-duplicate card detection (difflib ratio on front, and on back)."""
import difflib, json, pathlib
cards = json.load(open(pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/course/modules/FC/FC2/cards.json"), encoding="utf-8"))
out = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf > 0.6 or rb > 0.6:
            out.append((a["id"], b["id"], round(rf, 2), round(rb, 2), a["front"][:70], b["front"][:70]))
for o in out: print(o)
print("pairs flagged:", len(out))
