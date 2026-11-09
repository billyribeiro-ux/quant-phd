"""Flatten E4 cards.json to one card per block (verifier scratch view; reads cards.json only)."""
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
print("count", len(cards), "unique ids", len({c["id"] for c in cards}))
for c in cards:
    print(f"## {c['id']} | {c['lesson']} | grade={c.get('grade')} | basis={c.get('basis')}")
    print(f"F: {c['front']}")
    print(f"B: {c['back']}")
