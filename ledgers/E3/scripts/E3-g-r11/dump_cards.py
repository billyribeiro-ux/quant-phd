"""Dump the cards of lessons L05..L08 of E3 as id | lesson | grade | basis | front | back, one card per block."""
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
lessons = set(sys.argv[2].split(","))
for c in cards:
    if c["lesson"] not in lessons:
        continue
    print(f'### {c["id"]} | {c["lesson"]} | grade={c.get("grade")} | basis={c.get("basis")}')
    print(f'F: {c["front"]}')
    print(f'B: {c["back"]}')
    extra = {k: v for k, v in c.items() if k not in ("id", "lesson", "grade", "basis", "front", "back")}
    if extra:
        print(f"X: {extra}")
