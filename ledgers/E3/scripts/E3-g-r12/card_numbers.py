import json, re, sys
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
texts = {}
for L in ("L05", "L06", "L07", "L08"):
    texts[L] = open(f"{sys.argv[1]}/{L}.txt", encoding="utf-8").read()
allnum = re.compile(r"(?<![A-Za-z_])(\d+(?:\.\d+)?(?:e-?\d+)?)(?![\d])")
bad = 0
for c in cards:
    if c["lesson"] not in texts:
        continue
    body = c["front"] + " " + c["back"]
    nums = sorted(set(allnum.findall(body)))
    lesson = texts[c["lesson"]]
    # also whole-card-level: search for each number as a token in the lesson text
    missing = [n for n in nums if n not in lesson]
    # ids like c078 etc are not in body
    if missing:
        bad += 1
        print(c["id"], c["lesson"], "numbers not literal in lesson:", missing)
print("cards with numbers absent from lesson text:", bad)
