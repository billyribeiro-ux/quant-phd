"""Dump every card of course/modules/SC/SC1/cards.json as numbered text (read-only)."""
import json
import sys

path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))
for i, c in enumerate(cards, 1):
    print(f"[{i}] {c['id']} L={c['lesson']} grade={c.get('grade','-')} cite={c['cite']} basis={c.get('basis','-')}")
    print(f"   F: {c['front']}")
    print(f"   B: {c['back']}")
