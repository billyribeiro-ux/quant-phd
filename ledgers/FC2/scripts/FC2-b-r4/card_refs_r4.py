"""For each L04-L06 card, check that every cited numbered item (Theorem, Remark, Example, ...) appears in its lesson page text."""
import html
import json
import re
import sys

ROOT = sys.argv[1]
cards = json.load(open(f"{ROOT}/course/modules/FC/FC2/cards.json", encoding="utf-8"))
pat = re.compile(r"\b(Theorem|Remark|Example|Problem|Section|Lemma|Proposition|Definition|Corollary) (\d+(?:\.\d+)?|[A-Z]\d)\b")
bad = 0
for c in cards:
    if c["lesson"] not in ("L04", "L05", "L06"):
        continue
    text = re.sub(r"<[^>]+>", " ", open(f"{ROOT}/course/modules/FC/FC2/{c['lesson']}.html", encoding="utf-8").read())
    text = html.unescape(text)
    for kind, num in pat.findall(c["front"] + " " + c["back"]):
        token = f"{kind} {num}"
        if token not in text:
            bad += 1
            print("MISSING", c["id"], c["lesson"], token)
print("cards checked; missing refs:", bad)
