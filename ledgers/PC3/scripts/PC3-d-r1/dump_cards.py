"""Dump every card of course/modules/PC/PC3/cards.json, one block per card, with index and full fields."""
import json
import sys

path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))
for i, c in enumerate(cards, 1):
    print(f"[{i}] {c['id']} lesson={c['lesson']} cite={c['cite']} grade={c.get('grade')!r} basis={c.get('basis')!r}")
    print(f"  FRONT: {c['front']}")
    print(f"  BACK: {c['back']}")
