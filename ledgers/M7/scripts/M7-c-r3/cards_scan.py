"""Scan M7 cards: duplicate ids/fronts/backs, grade/basis rules, and numbers in each L07/L08 card vs its lesson text."""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M7/cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
for key in ("id", "front", "back"):
    c = Counter(card[key] for card in cards)
    print("duplicate", key, [k for k, n in c.items() if n > 1])
norm = Counter(re.sub(r"\W+", " ", card["front"].lower()).strip() for card in cards)
print("near-duplicate fronts (normalised):", [k for k, n in norm.items() if n > 1])
bad = [c["id"] for c in cards if c["grade"] not in ("T", "A", "B", "C", "D", "X")]
print("bad grades:", bad)
nobasis = [c["id"] for c in cards if c["grade"] != "T" and not c.get("basis")]
print("non-T without basis:", nobasis)
print("T cards with basis:", [c["id"] for c in cards if c["grade"] == "T" and c.get("basis")])
ids = [c["id"] for c in cards]
print("ids sorted unique:", len(ids) == len(set(ids)))

def text_of(lid):
    page = (root / f"course/modules/M/M7/{lid}.html").read_text(encoding="utf-8")
    page = re.sub(r"<script.*?</script>", " ", page, flags=re.S)
    page = re.sub(r"<[^>]+>", " ", page)
    return html.unescape(page)

texts = {lid: text_of(lid) for lid in ("L07", "L08")}
NUM = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")
for card in cards:
    lid = card["lesson"]
    if lid not in texts:
        continue
    t = texts[lid]
    nums = set(NUM.findall(card["front"] + " " + card["back"]))
    missing = []
    for n in sorted(nums):
        if not re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", t):
            missing.append(n)
    print(card["id"], lid, "numbers:", sorted(nums), "missing in lesson text:", missing)
