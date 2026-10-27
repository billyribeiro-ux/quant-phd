"""Full duplicate and sequence scan of course/modules/AC/AC2/cards.json. Run: python -I cards_scan.py <checkout>."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

cards = json.loads((Path(sys.argv[1]) / "course/modules/AC/AC2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("n", len(cards), "dup ids", [i for i, n in Counter(ids).items() if n > 1])
print("id seq ok", sorted(ids) == [f"AC2-c{n:03d}" for n in range(1, 131)])
print("dup fronts", [f for f, n in Counter(c["front"].strip().lower() for c in cards).items() if n > 1])
print("dup backs", [f for f, n in Counter(c["back"].strip().lower() for c in cards).items() if n > 1])
hits = [c["id"] for c in cards for k in ("front", "back") if re.search(r"\.\.\.|…", c[k])]
print("ellipsis in cards", hits)
