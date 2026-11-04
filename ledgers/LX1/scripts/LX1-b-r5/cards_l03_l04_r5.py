"""Verifier round 5: every number of two or more characters in each L03/L04 card (front and back) must appear
in that card's lesson page text (tags stripped); reports unmatched numbers; checks ids, duplicates, and that
each card's lesson exists. Usage: python3 -I cards_l03_l04_r5.py <checkout>"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/LX/LX1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
fronts = [c["front"].strip().lower() for c in cards]
print("cards:", len(cards), "duplicate ids:", len(ids) - len(set(ids)), "duplicate fronts:", len(fronts) - len(set(fronts)))
pages = {}
for lesson in ("L01", "L02", "L03", "L04"):
    t = (root / f"course/modules/LX/LX1/{lesson}.html").read_text(encoding="utf-8")
    t = re.sub(r"<[^>]+>", " ", t).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    pages[lesson] = re.sub(r"\s+", " ", t)
num = re.compile(r"\d[\d,.]*\d|\d")
unmatched = []
count = 0
for c in cards:
    if c["lesson"] not in pages:
        unmatched.append((c["id"], "no lesson"))
        continue
    if c["lesson"] not in ("L03", "L04"):
        continue
    count += 1
    for field in ("front", "back"):
        for n in set(num.findall(c[field])):
            core = n.rstrip(".,")
            if len(core) < 2:
                continue
            if core not in pages[c["lesson"]] and core.replace(",", "") not in pages[c["lesson"]]:
                unmatched.append((c["id"], field, core))
print("L03/L04 cards scanned:", count)
print("unmatched numbers (>= 2 characters):", unmatched)
