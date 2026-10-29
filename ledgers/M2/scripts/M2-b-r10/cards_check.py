"""Dump the M2 slice-b cards (lessons L07-L12) and check id, front and grade uniqueness.

Usage: python3 -I cards_check.py <checkout-root>
"""

import collections
import json
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M2/cards.json", encoding="utf-8"))
slice_lessons = {"L07", "L08", "L09", "L10", "L11", "L12"}
sl = [c for c in cards if c.get("lesson") in slice_lessons]
print("total cards", len(cards), "slice", len(sl), dict(collections.Counter(c["lesson"] for c in sl)))
print("dup ids", [k for k, v in collections.Counter(c["id"] for c in cards).items() if v > 1])
print("dup fronts", [k for k, v in collections.Counter(c["front"] for c in cards).items() if v > 1])
print("C cards without basis", [c["id"] for c in sl if c.get("grade") == "C" and "basis" not in c])
for c in sl:
    print(c["id"], c["lesson"], c.get("grade"), "|", c["front"], "|", c["back"])
