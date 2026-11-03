# Full scan of course/modules/M/M2/cards.json for duplicate ids and near-duplicate fronts or backs (word Jaccard).
# Usage: python -I cards_dup_scan_r3.py <checkout-root>
import json, os, re, sys
root = os.path.abspath(sys.argv[1])
cards = json.load(open(os.path.join(root, "course/modules/M/M2/cards.json"), encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)))
print("keys", sorted({k for c in cards for k in c}))
def words(s): return set(re.findall(r"[a-z0-9]+", s.lower()))
pairs = []
for i in range(len(cards)):
    wf = words(cards[i]["front"]); wb = words(cards[i]["back"])
    for j in range(i + 1, len(cards)):
        f2 = words(cards[j]["front"]); b2 = words(cards[j]["back"])
        jf = len(wf & f2) / max(1, len(wf | f2)); jb = len(wb & b2) / max(1, len(wb | b2))
        if jf >= 0.5 or jb >= 0.5:
            pairs.append((round(max(jf, jb), 2), cards[i]["id"], cards[j]["id"], round(jf, 2), round(jb, 2)))
pairs.sort(reverse=True)
print("pairs with front or back Jaccard >= 0.5:", len(pairs))
for p in pairs[:60]:
    a = next(c for c in cards if c["id"] == p[1]); b = next(c for c in cards if c["id"] == p[2])
    print(p, "|", a["lesson"], a["front"][:90], "||", b["lesson"], b["front"][:90])
