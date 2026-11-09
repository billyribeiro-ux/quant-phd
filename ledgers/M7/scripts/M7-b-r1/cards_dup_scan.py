# Verifier script (M7-b round 1): near-duplicate scan over all cards.json entries (front and back text).
import difflib
import json

cards = json.load(open("course/modules/M/M7/cards.json", encoding="utf-8"))
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf >= 0.8 or rb >= 0.9:
            pairs.append((round(rf, 3), round(rb, 3), a["id"], b["id"]))
print("cards", len(cards), "ids", len({c["id"] for c in cards}))
for p in pairs:
    print("near-duplicate", p)
print("pairs flagged", len(pairs))
