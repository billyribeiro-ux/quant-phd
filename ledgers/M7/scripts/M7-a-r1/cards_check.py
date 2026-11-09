"""M7-a round 1 witness: card id uniqueness, lesson-slice membership, duplicate fronts/backs, numbers on cards vs lesson text."""
import json
import re
import sys
from collections import Counter

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M7/cards.json", encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
print("total cards", len(cards), "duplicate ids", [i for i, n in ids.items() if n > 1])
sl = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("slice cards", len(sl), Counter(c["lesson"] for c in sl))
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
fronts = Counter(norm(c["front"]) for c in cards)
print("exact duplicate fronts (whole file)", [f for f, n in fronts.items() if n > 1])
backs = Counter(norm(c["back"]) for c in cards)
print("exact duplicate backs (whole file)", [f for f, n in backs.items() if n > 1])
# numbers on the card back that do not appear in the cited lesson page (L01-L03 text + lab output)
pages = {}
for L in ("L01", "L02", "L03"):
    pages[L] = open(f"{root}/course/modules/M/M7/{L}.html", encoding="utf-8").read()
for c in sl:
    text = pages[c["lesson"]]
    nums = set(re.findall(r"(?<![A-Za-z_])\d+(?:/\d+)?", c["back"]))
    missing = [n for n in sorted(nums) if n not in text]
    if missing:
        print("card", c["id"], "numbers not in its lesson page:", missing)
for c in sl:
    if c["grade"] != "T" and not c.get("basis"):
        print("non-T without basis", c["id"])
    if set(c) - {"id", "lesson", "front", "back", "grade", "basis"}:
        print("extra keys", c["id"], set(c))
