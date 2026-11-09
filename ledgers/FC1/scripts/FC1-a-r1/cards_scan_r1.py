# Closing-delta card scan for FC1 cards.json at pin 2a805c83: counts, unique ids, duplicate fronts, c016 text.
import collections
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
dups = [k for k, v in collections.Counter(ids).items() if v > 1]
by_lesson = collections.Counter(c["lesson"] for c in cards)
print("total cards", len(cards), "unique ids", len(set(ids)), "duplicate ids", dups)
print("per lesson", dict(sorted(by_lesson.items())))
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts", [f for f, v in fronts.items() if v > 1])
c16 = next(c for c in cards if c["id"] == "FC1-c016")
print("c016 grade", c16["grade"], "lesson", c16["lesson"])
print("c016 back:", c16["back"])
print("c016 back numbers:", re.findall(r"\d+(?:\.\d+)?", c16["back"]))
l01 = (root / "course/modules/FC/FC1/L01.html").read_text(encoding="utf-8")
print("L01 has 'misconception 2' cite target (misconception li count):", l01.count('class="misconception"'))
print("L01 Proposition 3.1 present:", "Proposition 3.1" in l01)
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03") and not c.get("back", "").strip():
        print("EMPTY BACK", c["id"])
