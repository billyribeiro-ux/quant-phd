import json, re, html, sys
cards = json.load(open("cards.json"))
txt = {}
for L in sorted({c["lesson"] for c in cards}):
    raw = open(f"{L}.html", encoding="utf-8").read()
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    txt[L] = re.sub(r"\s+", " ", t)
bad = []
for c in cards:
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["back"] + " " + c["front"]))
    miss = [n for n in nums if n not in txt[c["lesson"]] and n not in txt["L01"] + txt["L06"]]
    if miss:
        bad.append((c["id"], c["lesson"], miss))
print("cards", len(cards), "cards with a number absent from own lesson text:", len(bad))
for b in bad:
    print(b)
