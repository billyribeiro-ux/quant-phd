import json, re, sys
from collections import Counter
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M4/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(cards), "unique ids", len(set(ids)) == len(ids))
slice_cards = [c for c in cards if c["lesson"] in ("L01", "L02", "L03", "L04")]
print("slice cards", len(slice_cards), Counter(c["lesson"] for c in slice_cards))
norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())
fb = Counter((norm(c["front"]), norm(c["back"])) for c in cards)
print("exact duplicate front+back pairs", sum(1 for v in fb.values() if v > 1))
fr = Counter(norm(c["front"]) for c in cards)
print("duplicate fronts", sum(1 for v in fr.values() if v > 1))
for gone in ("M4-c014", "M4-c028", "M4-c065"):
    print(gone, "present in cards.json:", gone in ids)
text = ""
import glob
for p in glob.glob(f"{root}/course/modules/M/M4/*.html") + glob.glob(f"{root}/tests/labs/M4/*.py"):
    text += open(p, encoding="utf-8").read()
refs = set(re.findall(r"M4-c\d{3}", text))
print("card ids named in M4 pages/labs:", len(refs), "not in cards.json:", sorted(refs - set(ids)))
for c in slice_cards:
    if c["id"] in ("M4-c079",):
        print("c079 lesson", c["lesson"])
print("c079 numbers in L05 check done by hand (see fragment)")
bad = [c["id"] for c in slice_cards if c["grade"] not in ("T", "C")]
print("slice cards with grade not T or C:", bad)
