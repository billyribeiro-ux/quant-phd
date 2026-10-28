"""List the cards of lessons L01-L04 from cards.json, with grade, cite and basis, and check duplicates and lesson links.

Usage: python cards_l01_l04.py <checkout>. Reads only.
"""
import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
print("total cards", len(cards))
ids = Counter(c["id"] for c in cards)
print("duplicate ids", [k for k, v in ids.items() if v > 1])
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs", [k for k, v in backs.items() if v > 1])
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03", "L04"):
        print(json.dumps(c, ensure_ascii=False))
