"""Duplicate scan: exact front/back duplicates over all 170 cards; word-set Jaccard >= 0.5 within the slice,
and >= 0.4 between slice cards and cards of other lessons.

Run: python -I ledgers/E3/scripts/E3-g-r3/cross_slice_near_dup.py
"""
import json
import re

cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
SL = ("L05", "L06", "L07", "L08")
fronts, backs = {}, {}
for c in cards:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
    backs.setdefault(c["back"].strip().lower(), []).append(c["id"])
print("cards:", len(cards), "distinct ids:", len({c["id"] for c in cards}))
print("exact duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
print("exact duplicate backs:", [v for v in backs.values() if len(v) > 1])


def words(c):
    return set(re.findall(r"[a-z0-9]+", (c["front"] + " " + c["back"]).lower()))


sl = [c for c in cards if c["lesson"] in SL]
other = [c for c in cards if c["lesson"] not in SL]
print("within slice, Jaccard >= 0.5:")
for i, a in enumerate(sl):
    for b in sl[i + 1:]:
        j = len(words(a) & words(b)) / len(words(a) | words(b))
        if j >= 0.5:
            print("  ", round(j, 2), a["id"], b["id"])
print("slice vs other lessons, Jaccard >= 0.4:")
for a in sl:
    for b in other:
        j = len(words(a) & words(b)) / len(words(a) | words(b))
        if j >= 0.4:
            print("  ", round(j, 2), a["id"], b["id"], "|", a["front"][:60], "|", b["front"][:60])
