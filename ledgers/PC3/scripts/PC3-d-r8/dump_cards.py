"""Dump every card of PC3 cards.json, one block per card, for reading."""
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
print("COUNT", len(cards))
for c in cards:
    print(f"## {c['id']} | {c['lesson']} | grade={c.get('grade')} | basis={c.get('basis')}")
    print("F:", c["front"])
    print("B:", c["back"])
