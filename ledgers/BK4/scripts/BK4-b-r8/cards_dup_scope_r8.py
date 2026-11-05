"""Verifier round 8: duplicate scan of cards.json and scope-word scan of the slice-b pages.

Run as: python -I -W error cards_dup_scope_r8.py <repo root>
"""

import re
import sys
from collections import Counter

root = sys.argv[1]
with open(root + "/course/modules/BK/BK4/cards.json", encoding="utf-8") as fh:
    import json

    cards = json.load(fh)
ids = [c["id"] for c in cards]
fronts = [c["front"] for c in cards]
print("cards", len(cards), "dup ids", sum(n - 1 for n in Counter(ids).values() if n > 1), "dup fronts", sum(n - 1 for n in Counter(fronts).values() if n > 1))
l4 = [c["id"] for c in cards if c["lesson"] == "L04"]
l5 = [c["id"] for c in cards if c["lesson"] == "L05"]
print("L04 cards", len(l4), "L05 cards", len(l5))

words = r"\b(every|all|any|always|never|each|exactly|only|systemic|widely)\b"
for page in ("L04", "L05"):
    with open(f"{root}/course/modules/BK/BK4/{page}.html", encoding="utf-8") as fh:
        text = fh.read()
    hits = [m for m in re.finditer(words, text, re.I)]
    print(page, "scope-word hits (word-level, tags included):", len(hits))
    for m in hits:
        line = text.count("\n", 0, m.start()) + 1
        print(f"  {page}.html:{line} {m.group(0)}")
