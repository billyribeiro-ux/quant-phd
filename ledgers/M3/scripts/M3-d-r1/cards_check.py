"""Structural and number checks for M3 cards.json against the M3 lesson pages (text with tags stripped)."""

import html
import json
import re
from collections import Counter
from pathlib import Path

M3 = Path("/Users/billyribeiro/.fanout/wt/verifyD1-M3-d/course/modules/M/M3")
cards = json.loads((M3 / "cards.json").read_text(encoding="utf-8"))
print("count", len(cards))
print("keys", Counter(tuple(sorted(c.keys())) for c in cards))
ids = [c["id"] for c in cards]
print("unique ids", len(set(ids)) == len(ids), "first", ids[0], "last", ids[-1])
print("lesson counts", Counter(c["lesson"] for c in cards))
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts", [f for f, n in fronts.items() if n > 1])
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs", [f[:60] for f, n in backs.items() if n > 1])
print("empty", [c["id"] for c in cards if not c["front"].strip() or not c["back"].strip()])
texts = {}
for lesson in sorted({c["lesson"] for c in cards}):
    raw = (M3 / f"{lesson}.html").read_text(encoding="utf-8")
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    texts[lesson] = re.sub(r"\s+", " ", t)
    nums = set(re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?", texts[lesson]))
    cnums = set()
    for c in cards:
        if c["lesson"] == lesson:
            for n in re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?", c["front"] + " " + c["back"]):
                if n not in nums:
                    cnums.add(n)
    print(lesson, "card numbers absent from lesson text:", sorted(cnums))
