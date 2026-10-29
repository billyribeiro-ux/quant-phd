import json, re, sys
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M3/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(cards), "unique ids", len(set(ids)) == len(ids))
pages = {l: open(f"{root}/course/modules/M/M3/{l}.html", encoding="utf-8").read() for l in ["L01", "L02", "L03"]}
for c in cards:
    if c["lesson"] not in pages:
        continue
    print(c["id"], c["lesson"], c.get("grade"), c.get("basis", ""), "|", c["front"], "||", c["back"])
    txt = pages[c["lesson"]]
    nums = set(re.findall(r"\b\d+(?:\.\d+)?\b", c["back"]))
    missing = [n for n in nums if n not in txt]
    if missing:
        print("   numbers not in lesson:", missing)
