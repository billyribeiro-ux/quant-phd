"""Print the cards of one lesson (argv[2]) from cards.json (argv[1]), one card per block."""
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
for c in cards:
    if c["lesson"] == sys.argv[2]:
        print(f"{c['id']} grade={c.get('grade')} basis={c.get('basis')} cite={c.get('cite')}")
        print(f"  F: {c['front']}")
        print(f"  B: {c['back']}")
