"""Print the cards of one lesson (verifier round 3, slice e), in file order.

Usage: python -I v3_cards_by_lesson.py L01
"""
import json
import sys

cards = json.load(open("course/modules/M/M7/cards.json", encoding="utf-8"))
lesson = sys.argv[1]
for idx, c in enumerate(cards, 1):
    if c["lesson"] != lesson:
        continue
    print(f"[{idx}] {c['id']} {c['lesson']} grade={c['grade']} cite={c.get('cite')!r} basis={c.get('basis', '-')!r}")
    print(f"  F: {c['front']}")
    print(f"  B: {c['back']}")
