import json, re, html, sys
base = "course/modules/M/M7/"
cards = json.load(open(base + "cards.json", encoding="utf-8"))
print("cards:", len(cards), "unique ids:", len({c["id"] for c in cards}))
texts = {}
def lesson_text(L):
    if L not in texts:
        raw = open(f"{base}{L}.html", encoding="utf-8").read()
        raw = re.sub(r"<[^>]+>", " ", raw)
        texts[L] = html.unescape(re.sub(r"\s+", " ", raw))
    return texts[L]
bad = []
num_re = re.compile(r"\d+(?:\.\d+)?")
for c in cards:
    t = lesson_text(c["lesson"])
    for n in set(num_re.findall(c["back"] + " " + c["front"])):
        if n not in t:
            bad.append((c["id"], c["lesson"], n))
print("card numbers absent from own lesson:", len(bad))
for b in bad: print(b)
dup = {}
for c in cards:
    dup.setdefault(c["front"].strip().lower(), []).append(c["id"])
print("duplicate fronts:", [v for v in dup.values() if len(v) > 1])
