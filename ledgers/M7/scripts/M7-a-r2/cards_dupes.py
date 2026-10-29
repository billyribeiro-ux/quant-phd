"""Duplicate scan over the M7 cards file: ids, fronts and backs (normalised), and grade values."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
fronts = Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
backs = Counter(re.sub(r"\W+", " ", c["back"].lower()).strip() for c in cards)
print("cards", len(cards), "dup ids", [k for k, v in ids.items() if v > 1])
print("dup fronts", [k for k, v in fronts.items() if v > 1])
print("dup backs", [k for k, v in backs.items() if v > 1])
print("grades", Counter(c["grade"] for c in cards))
print("L01-L03 ids", sorted(c["id"] for c in cards if c["lesson"] in ("L01", "L02", "L03")))
