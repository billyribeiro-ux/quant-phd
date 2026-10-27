"""Round-4 card scan: ids c001-c140 present once, no duplicate fronts, L07/L08 card list, grade presence."""
import json
import re
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
cards = cards if isinstance(cards, list) else cards.get("cards", cards)
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
want = {f"AC2-c{n:03d}" for n in range(1, 141)}
print("missing ids:", sorted(want - set(ids)), "extra:", sorted(set(ids) - want))
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
fronts = Counter(norm(c["front"]) for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
backs = Counter(norm(c["back"]) for c in cards)
print("duplicate backs:", [f for f, n in backs.items() if n > 1])
l78 = [c for c in cards if c["lesson"] in ("L07", "L08")]
print("L07/L08 cards:", len(l78), [c["id"] for c in l78])
print("L07/L08 cards without grade:", [c["id"] for c in l78 if "grade" not in c])
