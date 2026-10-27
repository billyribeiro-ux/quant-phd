"""Card checks for AC2 L07 and L08: ids, counts, lesson membership, and near-duplicate scan over all AC2 cards.
Usage: python3 -I card_scan.py <checkout>"""
import difflib, json, sys
from collections import Counter
root = sys.argv[1]
with open(f"{root}/course/modules/AC/AC2/cards.json", encoding="utf-8") as fh:
    cards = json.load(fh)
ids = [c["id"] for c in cards]
print("total cards", len(cards), "unique ids", len(set(ids)), "lesson counts", Counter(c["lesson"] for c in cards))
mine = [c for c in cards if c["lesson"] in ("L07", "L08")]
print("L07", sum(c["lesson"] == "L07" for c in mine), "L08", sum(c["lesson"] == "L08" for c in mine))
norm = lambda s: " ".join(s.lower().split())
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        fr = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        bk = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
        if fr > 0.8 or bk > 0.8 or (fr > 0.6 and bk > 0.6):
            pairs.append((round(fr, 2), round(bk, 2), a["id"], b["id"]))
print("near-duplicate pairs (front>0.8 or back>0.8 or both>0.6):", pairs if pairs else "none")
# every card's id must be AC2-cNNN in order
print("ids sequential:", ids == [f"AC2-c{n:03d}" for n in range(1, len(ids) + 1)])
