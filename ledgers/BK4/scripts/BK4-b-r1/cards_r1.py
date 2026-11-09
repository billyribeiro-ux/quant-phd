"""Cards for BK4 lessons L04 and L05: numbers on each card must appear in its lesson; duplicate scan over all 100 cards.

Run: .venv/bin/python -I -W error ledgers/BK4/scripts/BK4-b-r11/cards_r11.py  (from the checkout root)
"""

import html
import json
import re

cards = json.load(open("course/modules/BK/BK4/cards.json", encoding="utf-8"))
page = {
    "L04": html.unescape(re.sub(r"<[^>]+>", " ", open("course/modules/BK/BK4/L04.html", encoding="utf-8").read())),
    "L05": html.unescape(re.sub(r"<[^>]+>", " ", open("course/modules/BK/BK4/L05.html", encoding="utf-8").read())),
}
missing = []
checked = 0
for c in cards:
    if c["lesson"] not in page:
        continue
    checked += 1
    text = c["front"] + " " + c["back"]
    nums = set(re.findall(r"\d+(?:/\d+)?", text))
    for n in sorted(nums):
        if len(n) < 2 and "/" not in n:
            continue
        if n not in page[c["lesson"]]:
            missing.append((c["id"], n))
print("cards in L04/L05:", checked)
print("numbers not found in own lesson text:", missing if missing else "none")
fronts = {}
for c in cards:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
dups = {k: v for k, v in fronts.items() if len(v) > 1}
print("duplicate fronts across all cards:", dups if dups else "none")
backs = {}
for c in cards:
    backs.setdefault(c["back"].strip().lower(), []).append(c["id"])
print("duplicate backs across all cards:", [v for v in backs.values() if len(v) > 1] or "none")
print("total cards:", len(cards), "ids unique:", len({c["id"] for c in cards}) == len(cards))
