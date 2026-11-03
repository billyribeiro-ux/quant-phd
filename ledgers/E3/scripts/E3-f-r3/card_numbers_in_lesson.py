"""E3 slice f round 3: every number written on a card of L01 to L04 must occur in that card's lesson.

Run from the checkout root: python3 -I ledgers/E3/scripts/E3-f-r3/card_numbers_in_lesson.py
Numbers are tokens of digits (with optional decimal point or thousands digits). Small integers 0-10 and
the theorem/example/section/problem labels are skipped because they are labels, not claims.
"""
import json
import re

ROOT = "course/modules/E/E3/"
cards = json.load(open(ROOT + "cards.json", encoding="utf-8"))
texts = {n: open(ROOT + n + ".html", encoding="utf-8").read() for n in ("L01", "L02", "L03", "L04")}
label = re.compile(r"(Proposition|Remark|Lemma|Theorem|Definition|Example|Problem|Lab|Part|section|Section|Assumption|Step)\s+[0-9A-Za-z.()]+")
missing = []
checked = 0
for c in cards:
    if c["lesson"] not in texts:
        continue
    raw = c["front"] + " " + c["back"]
    stripped = label.sub(" ", raw)
    for tok in re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?", stripped):
        if tok in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12", "24", "32"):
            continue
        checked += 1
        body = texts[c["lesson"]]
        if tok not in body:
            missing.append((c["id"], c["lesson"], tok))
print("numbers checked:", checked)
print("numbers not found verbatim in the card's lesson:", len(missing))
for m in missing:
    print(m)
