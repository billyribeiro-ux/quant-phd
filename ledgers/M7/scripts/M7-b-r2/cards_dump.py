"""Verifier script (M7-b round 2): card totals, duplicate scan, and the L04-L06 card records (one JSON object per line).

Run from the checkout root with: python3 -I ledgers/M7/scripts/M7-b-r2/cards_dump.py
"""
import collections
import json

cards = json.load(open("course/modules/M/M7/cards.json", encoding="utf-8"))
print("total cards", len(cards))
ids = [c["id"] for c in cards]
print("duplicate ids", [k for k, v in collections.Counter(ids).items() if v > 1])
fr = collections.Counter(c["front"] for c in cards)
print("duplicate fronts", [k for k, v in fr.items() if v > 1])
bk = collections.Counter(c["back"] for c in cards)
print("duplicate backs", [k for k, v in bk.items() if v > 1])
print("lesson counts", dict(collections.Counter(c["lesson"] for c in cards)))
print("grades", dict(collections.Counter(c["grade"] for c in cards)))
sel = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("L04-L06 cards", len(sel), dict(collections.Counter(c["lesson"] for c in sel)))
for c in sel:
    print(json.dumps(c, ensure_ascii=False))
