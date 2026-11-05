"""Dump every card of course/modules/SC/SC1/cards.json, grouped by lesson, one card per block.

Usage: python -I dump_cards.py <cards.json> <out_dir>
"""
import json
import sys

src, out_dir = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8") as fh:
    cards = json.load(fh)
if isinstance(cards, dict):
    cards = cards.get("cards", cards)
print("count", len(cards))
ids = [c["id"] for c in cards]
print("distinct ids", len(set(ids)))
keys = sorted({k for c in cards for k in c})
print("keys", keys)
by: dict[str, list[dict]] = {}
for c in cards:
    by.setdefault(c["lesson"], []).append(c)
for lesson in sorted(by):
    with open(f"{out_dir}/cards_{lesson}.txt", "w", encoding="utf-8") as fh:
        for c in by[lesson]:
            fh.write(f"{c['id']} [{c['lesson']}] grade={c.get('grade')} cite={c.get('cite')}\n")
            fh.write(f"  F: {c['front']}\n")
            fh.write(f"  B: {c['back']}\n")
            fh.write(f"  basis: {c.get('basis')}\n")
    print(lesson, len(by[lesson]))
