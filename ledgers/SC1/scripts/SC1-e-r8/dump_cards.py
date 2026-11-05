"""Dump cards.json grouped by lesson, one card per block, for line-by-line reading.

Usage: python -I dump_cards.py <cards.json> [LESSON ...]
"""
import json
import sys

path = sys.argv[1]
only = set(sys.argv[2:])
with open(path, encoding="utf-8") as fh:
    cards = json.load(fh)
for c in cards:
    if only and c["lesson"] not in only:
        continue
    print(f"{c['id']} [{c['lesson']}] grade={c.get('grade', '-')} cite={c['cite']} basis={c.get('basis', '-')}")
    print(f"  F: {c['front']}")
    print(f"  B: {c['back']}")
