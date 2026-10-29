"""For each cards.json card, list numeric tokens (front+back) and whether the token occurs in its lesson HTML text."""
import json, re, html, sys
base = "course/modules/CF/CF8/"
cards = json.load(open(base + "cards.json"))
lessons = {}
for L in ["L01", "L02", "L03", "L04", "L05"]:
    raw = open(base + L + ".html", encoding="utf-8").read()
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lessons[L] = re.sub(r"\s+", " ", txt)
tok = re.compile(r"(?<![A-Za-z_])\d[\d,]*(?:\.\d+)?")
miss = 0
for c in cards:
    text = c["front"] + " " + c["back"]
    nums = sorted(set(m.group(0).rstrip(",") for m in tok.finditer(text)))
    absent = [n for n in nums if n not in lessons[c["lesson"]]]
    if absent:
        miss += 1
        print(c["id"], c["lesson"], "ABSENT:", absent)
print("cards", len(cards), "cards with absent numbers", miss)
