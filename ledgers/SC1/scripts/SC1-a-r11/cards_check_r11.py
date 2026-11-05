"""Scan of SC1 cards.json (round 11): duplicates, and card numbers that do not appear in their lesson (L01-L03).

Also prints every L01-L03 card whose hypotheses mention Assumption A1 or A2.1, so the hypotheses can be read.
"""

import collections
import json
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE11-SC1-a/course/modules/SC/SC1/"
cards = json.load(open(ROOT + "cards.json", encoding="utf-8"))
print("cards:", len(cards))
print("duplicate ids:", [i for i, n in collections.Counter(c["id"] for c in cards).items() if n > 1])
print("duplicate fronts:", [f for f, n in collections.Counter(c["front"].strip().lower() for c in cards).items() if n > 1])
print("duplicate backs:", [b for b, n in collections.Counter(c["back"].strip().lower() for c in cards).items() if n > 1])
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03"):
        text = open(ROOT + c["lesson"] + ".html", encoding="utf-8").read()
        nums = set(re.findall(r"\b\d+\.\d+\b|\b\d{2,}\b", c["back"]))
        missing = sorted(n for n in nums if n not in text)
        if missing:
            print("numbers not in lesson:", c["id"], missing)
print("L01-L03 cards whose text mentions A1 or 2.1 or 3.2 (hypotheses to read):")
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03") and re.search(r"A1|Assumption 2\.1|Assumption 3\.2", c["front"] + c["back"]):
        print(" ", c["id"], "|", c["front"][:150])
