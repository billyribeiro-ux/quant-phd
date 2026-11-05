"""Dump every L03 and L04 retrieval card of LX1 for checking against the lesson text; check ids and duplicates.

Usage: python3 -I cards_dump.py <checkout>
"""
import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/LX/LX1/cards.json").read_text(encoding="utf-8"))
cards = cards if isinstance(cards, list) else cards.get("cards", cards)
print("cards", len(cards), dict(Counter(c["lesson"] for c in cards)))
print("duplicate ids", [i for i, n in Counter(c["id"] for c in cards).items() if n > 1])
print("duplicate fronts", [f for f, n in Counter(c["front"] for c in cards).items() if n > 1])
print("keys", sorted({k for c in cards for k in c}))
for c in cards:
    if c["lesson"] in ("L03", "L04"):
        print(c["id"], c["lesson"], "| F:", c["front"], "| B:", c["back"], "| cite", c.get("cite"), "| grade", c.get("grade"), "| basis", c.get("basis"))
