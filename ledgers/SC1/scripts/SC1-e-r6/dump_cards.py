"""Dump every card of course/modules/SC/SC1/cards.json, one per block, with schema counts. Usage: dump_cards.py <cards.json>."""
import json
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)))
print("keys", Counter(tuple(sorted(c)) for c in cards))
print("lessons", sorted(Counter(c["lesson"] for c in cards).items()))
print("cite nonempty", sum(1 for c in cards if c.get("cite")))
print("grade/basis", Counter((c.get("grade"), c.get("basis") is not None) for c in cards))
for c in cards:
    print(f"{c['id']} {c['lesson']} grade={c.get('grade')} basis={c.get('basis')!r} cite={c.get('cite')}")
    print(f"  F: {c['front']}")
    print(f"  B: {c['back']}")
