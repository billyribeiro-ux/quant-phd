"""SC1-a round 16: dump every L01-L03 card (id, lesson, grade, cite, basis, front, back) and scan for duplicates."""

import collections
import json

cards = json.load(open("course/modules/SC/SC1/cards.json", encoding="utf-8"))
print("total", len(cards))
print("missing grade (all lessons):", sum(1 for c in cards if "grade" not in c))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(c["front"] for c in cards)
print("duplicate ids:", [i for i, n in ids.items() if n > 1])
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
sel = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("L01-L03 cards:", len(sel), "without grade:", sum(1 for c in sel if "grade" not in c))
for c in sel:
    print(f"{c['id']} {c['lesson']} g={c.get('grade')} cite={c['cite']} basis={c.get('basis', '')}")
    print("  F:", c["front"])
    print("  B:", c["back"])
