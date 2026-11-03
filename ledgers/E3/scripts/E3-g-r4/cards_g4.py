"""List the L05-L08 cards of E3 with ids, grades, basis and text (stdlib only).

Usage: python -I cards_g4.py <cards.json>
"""
import json
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    cards = json.load(fh)
ids = [c["id"] for c in cards]
dups = sorted({i for i in ids if ids.count(i) > 1})
print(f"total cards {len(cards)}; duplicate ids {dups}")
for c in cards:
    if c.get("lesson") not in ("L05", "L06", "L07", "L08"):
        continue
    print(f"[{c['id']}] {c['lesson']} grade={c.get('grade')} basis={c.get('basis')!r}")
    print(f"  F: {c['front']}")
    print(f"  B: {c['back']}")
