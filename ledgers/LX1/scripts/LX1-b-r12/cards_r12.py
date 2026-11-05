"""LX1-b round 12: dump every L03 and L04 card, check ids, duplicates, grade/basis pairing and that each card's
lesson exists. Run: .venv/bin/python -I <this file> <checkout>
"""
import collections
import json
import re
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/LX/LX1/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
fronts = [c["front"].strip().lower() for c in cards]
print("cards", len(cards), "by lesson", collections.Counter(c["lesson"] for c in cards))
print("duplicate ids", [k for k, v in collections.Counter(ids).items() if v > 1])
print("duplicate fronts", [k[:50] for k, v in collections.Counter(fronts).items() if v > 1])
print("bad ids", [i for i in ids if not re.fullmatch(r"LX1-c\d{3}", i)])
print("T cards without basis", [c["id"] for c in cards if c.get("grade") == "T" and not c.get("basis")])
print("C cards without basis", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("cards with a cite list", [(c["id"], c["cite"]) for c in cards if c.get("cite")])
for c in cards:
    if c["lesson"] in ("L03", "L04"):
        print(c["id"], c["lesson"], c.get("grade"), "|", c["front"])
        print("   back:", c["back"])
        print("   cite:", c.get("cite"), "| basis:", c.get("basis"))
