"""Dump every SC1 card as one block: id, lesson, front, back, grade, basis, cite. Usage: python -I dump_cards.py <cards.json>."""
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print(f"cards={len(cards)} distinct_ids={len(set(ids))}")
per = {}
for c in cards:
    per[c["lesson"]] = per.get(c["lesson"], 0) + 1
print("per_lesson", dict(sorted(per.items())))
for c in cards:
    print(f"{c['id']} {c['lesson']} | F: {c['front']} | B: {c['back']} | grade={c.get('grade')} basis={c.get('basis')} cite={c.get('cite')}")
