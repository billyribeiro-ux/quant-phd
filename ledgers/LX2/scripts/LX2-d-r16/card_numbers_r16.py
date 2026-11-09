# usage: card_numbers_r16.py <cards.json> <L01.txt> <L02.txt> <L03.txt> <L04.txt>
# Every number token in a card (integers, fractions, decimals) must occur in the card's own lesson text (whitespace-normalised).
# Tokens that occur in a lesson other than the card's lesson are flagged separately.
import json, re, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
lessons = {}
for i, name in enumerate(["L01", "L02", "L03", "L04"]):
    lessons[name] = re.sub(r"\s+", " ", open(sys.argv[2 + i], encoding="utf-8").read())
pat = re.compile(r"(?<![A-Za-z0-9_.])(\d+/\d+|\d+\.\d+|\d+)(?![A-Za-z0-9_])")
miss = 0
for c in cards:
    text = c["front"] + " " + c["back"] + " " + str(c.get("basis", ""))
    toks = sorted(set(pat.findall(text)))
    own = lessons[c["lesson"]]
    absent = [t for t in toks if t not in own]
    if absent:
        miss += 1
        print(f"{c['id']} ({c['lesson']}): tokens not in own lesson: {absent}")
print(f"cards checked: {len(cards)}; cards with a number absent from own lesson: {miss}")
