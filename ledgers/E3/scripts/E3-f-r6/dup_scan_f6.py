"""Near-duplicate scan over E3 cards.json: pairs with high similarity of front or back text (verifier E3-f round 6)."""
import difflib, json, re, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
def norm(s):
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split()
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        fr = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        bk = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
        if fr >= 0.6 or bk >= 0.6 or (fr + bk) / 2 >= 0.55:
            pairs.append((round((fr + bk) / 2, 3), round(fr, 3), round(bk, 3), a["id"], a["lesson"], b["id"], b["lesson"]))
pairs.sort(reverse=True)
for p in pairs:
    print("score=%s front=%s back=%s  %s(%s) ~ %s(%s)" % p)
print("total flagged pairs", len(pairs))
