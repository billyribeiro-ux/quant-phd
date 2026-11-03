"""Token-level check: every number on an L05-L08 card occurs as a whole token in its own lesson dump.

Run: python -I ledgers/E3/scripts/E3-g-r3/token_numbers.py
"""
import json
import re

TXT = "ledgers/E3/scripts/E3-g-r3/text"
lessons = {L: open(f"{TXT}/{L}.txt", encoding="utf-8").read().replace("\\", "") for L in ("L05", "L06", "L07", "L08")}
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
tot = 0
miss = []
for c in cards:
    if c["lesson"] not in lessons:
        continue
    lt = lessons[c["lesson"]]
    for m in re.findall(r"\d+(?:\.\d+)?(?:e-?\d+)?", c["front"] + " " + c["back"]):
        tot += 1
        if not re.search(r"(?<![\d.])" + re.escape(m) + r"(?![\d])", lt):
            miss.append((c["id"], m))
print("numbers checked:", tot, "token-absent:", len(miss))
for x in miss:
    print("  ", x)
