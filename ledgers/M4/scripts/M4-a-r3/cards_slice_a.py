import json, sys
path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))
print("total", len(cards))
ids = [c["id"] for c in cards]
dups = {i for i in ids if ids.count(i) > 1}
print("dup ids", sorted(dups))
fronts = {}
for c in cards:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
print("dup fronts", [v for v in fronts.values() if len(v) > 1])
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03", "L04"):
        print(c["id"], c["lesson"], c.get("grade"), "|", c["front"], "||", c["back"], "|| cite", c.get("cite"), "basis", c.get("basis"))
