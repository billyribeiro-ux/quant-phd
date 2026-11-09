"""Every number token in an M4 card front/back occurs in its lesson text (crude, closing delta, pin 85b109f8)."""
import glob
import html
import json
import re

cards = json.load(open("course/modules/M/M4/cards.json", encoding="utf-8"))
cards = cards if isinstance(cards, list) else cards.get("cards", cards)
lessons = {}
for f in glob.glob("course/modules/M/M4/L0*.html"):
    lessons[f.split("/")[-1][:3]] = html.unescape(re.sub(r"<[^>]+>", " ", open(f, encoding="utf-8").read()))
bad = []
checked = 0
for c in cards:
    if c.get("lesson") not in lessons:
        continue
    checked += 1
    txt = lessons[c["lesson"]]
    for n in re.findall(r"\d+(?:\.\d+)?", c["back"] + " " + c["front"]):
        if n not in txt:
            bad.append((c["id"], n))
print("cards", len(cards), "checked", checked, "numbers missing from lesson text", len(bad), bad[:20])
