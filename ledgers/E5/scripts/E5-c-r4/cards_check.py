import json, re, html, sys, collections
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/E/E5/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
dups = [k for k, v in collections.Counter(ids).items() if v > 1]
print("total cards", len(cards), "unique ids", len(set(ids)), "dup ids", dups)
fronts = collections.Counter(c["front"] for c in cards)
print("dup fronts", [f for f, v in fronts.items() if v > 1])
lessons = {}
for L in ("L07", "L08"):
    txt = open(f"{root}/course/modules/E/E5/{L}.html", encoding="utf-8").read()
    txt = re.sub(r"<[^>]+>", " ", txt)
    lessons[L] = html.unescape(txt)
for c in cards:
    if c["lesson"] not in lessons:
        continue
    nums = re.findall(r"\d[\d,]*\.?\d*", c["back"] + " " + c["front"])
    missing = []
    for n in nums:
        n2 = n.rstrip(".")
        if n2 not in lessons[c["lesson"]] and n2.replace(",", "") not in lessons[c["lesson"]].replace(",", ""):
            missing.append(n2)
    print(c["id"], c["lesson"], c.get("grade"), "| FRONT:", c["front"])
    print("    BACK:", c["back"])
    print("    numbers not in lesson text:", missing)
