"""List E3 L01-L03 cards and check ids, fronts, backs for duplicates (python -I)."""
import json
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
sel = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("total", len(cards), "L01-L03", len(sel))
ids = Counter(c["id"] for c in cards)
fr = Counter(c["front"] for c in cards)
bk = Counter(c["back"] for c in cards)
print("dup ids", [k for k, v in ids.items() if v > 1], "dup fronts", [k for k, v in fr.items() if v > 1], "dup backs", [k for k, v in bk.items() if v > 1])
for c in sel:
    print(c["id"], c["lesson"], c.get("grade"), "|F|", c["front"], "|B|", c["back"])
