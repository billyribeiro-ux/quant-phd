# For every card, list each numeric token (integers, fractions, decimals) and whether it occurs in the card's own lesson text
# (stripped HTML, from strip.py output) or in the lab twin printout. Reads the stripped texts from a scratch dir passed as argv[1].
import json
import re
import sys

scratch = sys.argv[1]
cards = json.load(open("course/modules/BK/BK4/cards.json", encoding="utf-8"))
texts = {L: open(f"{scratch}/{L}.txt", encoding="utf-8").read() for L in ("L01", "L02", "L03", "L04", "L05")}
tok = re.compile(r"(?<![\w.])(\d+/\d+|\d+\.\d+|\d+)(?![\w.])")
missing = 0
for c in cards:
    lesson = c["lesson"]
    text = texts[lesson]
    for field in ("front", "back"):
        for m in tok.findall(c[field]):
            if m in ("1", "0", "2", "3", "4", "5", "10", "100", "1000", "10000"):
                continue
            if m not in text:
                missing += 1
                print(f"{c['id']} {lesson} {field}: token {m!r} NOT in {lesson} text")
print("missing tokens (excluding common digits):", missing)
