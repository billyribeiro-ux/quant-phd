import json, sys
cards = json.load(open(sys.argv[1]))
ids = [c["id"] for c in cards]
print("total", len(cards), "unique ids", len(set(ids)), "unique fronts", len({c["front"] for c in cards}))
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03", "L04"):
        print(c["id"], c["lesson"], c["grade"], "|F:", c["front"], "|B:", c["back"])
