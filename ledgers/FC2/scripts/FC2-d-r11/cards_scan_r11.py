"""Full scan of cards.json for duplicates and near-duplicates (fronts and backs), plus per-card structure checks.
Usage: python3 -I cards_scan_r11.py <cards.json>"""
import difflib
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
assert len(ids) == len(set(ids)), "duplicate ids"
for c in cards:
    assert c["front"].strip() and c["back"].strip() and c["lesson"] in {f"L0{i}" for i in range(1, 9)}, c["id"]
    assert c.get("grade") in (None, "T", "A", "B", "C", "D"), c["id"]
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf >= 0.75 or rb >= 0.75:
            pairs.append((round(rf, 2), round(rb, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
print("cards:", len(cards), "unique ids:", len(set(ids)))
print("near-duplicate pairs (front or back ratio >= 0.75):", len(pairs))
for p in sorted(pairs, reverse=True):
    print(*p)
