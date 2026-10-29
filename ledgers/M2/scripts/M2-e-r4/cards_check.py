import json, re, html, sys
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M2/cards.json", encoding="utf-8"))
texts = {}
def text(lesson):
    if lesson not in texts:
        t = open(f"{root}/course/modules/M/M2/{lesson}.html", encoding="utf-8").read()
        t = re.sub(r"<[^>]+>", " ", t); t = html.unescape(t)
        texts[lesson] = re.sub(r"\s+", " ", t)
    return texts[lesson]
ids = [c["id"] for c in cards]; fronts = [c["front"].strip().lower() for c in cards]
print("cards", len(cards), "dup ids", len(ids) - len(set(ids)), "dup fronts", len(fronts) - len(set(fronts)))
missing = []
for c in cards:
    body = text(c["lesson"])
    for tok in set(re.findall(r"\d+(?:\.\d+)?(?:e-?\d+)?", c["front"] + " " + c["back"])):
        if tok not in body:
            missing.append((c["id"], tok))
print("numeric tokens absent from own lesson:", len(missing), missing[:20])
from collections import Counter
print("lessons", dict(Counter(c["lesson"] for c in cards)))
print("grade C without basis:", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("grade counts", Counter(c.get("grade", "-") for c in cards))
banned = re.compile(r"historically|roughly half|about 6%|\.\.\.|…|builder|verifier|verification|unit report|round ", re.I)
print("banned hits", [c["id"] for c in cards if banned.search(c["front"] + " " + c["back"])])
