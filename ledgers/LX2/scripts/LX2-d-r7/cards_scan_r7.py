"""LX2-d round 7: scan cards.json against the lesson plain text (run with python -I)."""
import json
import re
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
texts = {f"L0{i}": open(f"/tmp/lx2d-r7/L0{i}.txt", encoding="utf-8").read() for i in range(1, 5)}
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}))
ids = [c["id"] for c in cards]
print("ids sequential:", ids == [f"LX2-c{i:03d}" for i in range(1, len(cards) + 1)])
print("fronts unique:", len({c["front"] for c in cards}) == len(cards), "backs unique:", len({c["back"] for c in cards}) == len(cards))
print("grades", Counter(c.get("grade") for c in cards))
missing = []
for c in cards:
    text = texts[c["lesson"]]
    for tok in re.findall(r"\d[\d,./]*\d|\d", c["front"] + " " + c["back"]):
        if tok not in text:
            missing.append((c["id"], tok))
print("numeric tokens absent from own lesson text:", missing)
for c in cards:
    if c.get("grade") == "T":
        print("T", c["id"], c["lesson"], c["basis"])
