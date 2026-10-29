import json, collections, sys
base = sys.argv[1]
cards = json.load(open(base + "/course/modules/E/E3/cards.json"))
print("total", len(cards))
print("dup ids", [k for k, v in collections.Counter(c["id"] for c in cards).items() if v > 1])
print("dup fronts", [k for k, v in collections.Counter(c["front"] for c in cards).items() if v > 1])
for l in ("L01", "L02", "L03"):
    print(l, sum(1 for c in cards if c["lesson"] == l))
for c in cards:
    if c["id"] in {"E3-c014", "E3-c026", "E3-c034", "E3-c035", "E3-c037", "E3-c040", "E3-c055"}:
        print(c["id"], c.get("grade"), c.get("basis", c.get("cite", "")), "|", c["back"][:200])
