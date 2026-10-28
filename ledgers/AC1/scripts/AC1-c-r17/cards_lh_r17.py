"""Round 17 (AC1-c): card scan for L07/L08 cards and whole-file duplicate scan.

Usage: python -I cards_lh_r17.py <checkout>
Prints every card of lesson L07 or L08 with its grade, checks ids and fronts are unique across cards.json,
and lists cards whose grade field is absent.
"""
import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/AC/AC1/cards.json").read_text(encoding="utf-8"))
print("total cards:", len(cards))
ids = Counter(c["id"] for c in cards)
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
print("lessons:", Counter(c["lesson"] for c in cards))
for c in cards:
    if c["lesson"] in ("L07", "L08"):
        print(c["id"], c["lesson"], c.get("grade", "-"), "|", c["front"])
