"""Verifier round 12: every decimal or integer (>= 2 digits, or any decimal) in a card's text must occur in the card's
lesson page (HTML text, expected blocks and problem set included), and every duplicate card front is listed."""
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("course/modules/M/M4")
cards = json.load(open(ROOT / "cards.json", encoding="utf-8"))
texts = {}
for p in sorted(ROOT.glob("L*.html")):
    raw = p.read_text(encoding="utf-8")
    raw = re.sub(r"<[^>]+>", " ", raw)
    texts[p.stem] = html.unescape(re.sub(r"\s+", " ", raw))
bad = []
for c in cards:
    lesson = texts[c["lesson"]]
    body = c["front"] + " " + c["back"]
    nums = set(re.findall(r"(?<![A-Za-z_])\d+\.\d+(?:e[-+]?\d+)?|(?<![A-Za-z_\d])\d{2,}(?![\d/])|\d+e-\d+", body))
    for n in sorted(nums):
        if n not in lesson and n.replace(",", "") not in lesson:
            bad.append((c["id"], c["lesson"], n))
print("cards", len(cards), "number tokens missing from the card's own lesson page:", len(bad))
for b in bad:
    print("  ", b)
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [f for f, k in fronts.items() if k > 1])
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [f for f, k in ids.items() if k > 1])
print("cards per lesson:", dict(Counter(c["lesson"] for c in cards)))
print("grade counts:", dict(Counter(c["grade"] for c in cards)))
print("C cards lacking basis:", [c["id"] for c in cards if c["grade"] == "C" and not c.get("basis")])
print("T cards with basis:", [c["id"] for c in cards if c["grade"] == "T" and c.get("basis")])
