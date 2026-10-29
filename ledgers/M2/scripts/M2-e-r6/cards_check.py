"""Mechanical card checks for M2 cards.json: unique ids, lesson exists, duplicate fronts, numbers present in the lesson text."""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

MOD = Path(sys.argv[1]) / "course/modules/M/M2"
cards = json.load(open(MOD / "cards.json", encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
print("cards:", len(cards), "unique ids:", len(ids), "dup ids:", [k for k, v in ids.items() if v > 1])
keys = Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets:", dict(keys))
text = {}
for n in range(1, 25):
    p = MOD / f"L{n:02d}.html"
    raw = p.read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    text[f"L{n:02d}"] = html.unescape(raw)
fronts = Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
bad_lesson = [c["id"] for c in cards if c["lesson"] not in text]
print("cards with missing lesson:", bad_lesson)
num_re = re.compile(r"(?<![A-Za-z_\\])\d+(?:\.\d+)?")
missing = []
for c in cards:
    body = c["front"] + " " + c["back"]
    for num in set(num_re.findall(body)):
        if num not in text.get(c["lesson"], ""):
            missing.append((c["id"], c["lesson"], num))
print("card numbers not found in own lesson:", len(missing))
for m in missing:
    print("  ", m)
print("cards per lesson:", dict(sorted(Counter(c["lesson"] for c in cards).items())))
lens = [len(c["front"]) + len(c["back"]) for c in cards]
print("max front len", max(len(c["front"]) for c in cards), "max back len", max(len(c["back"]) for c in cards))
