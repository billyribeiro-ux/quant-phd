import json, sys, collections
cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(c["front"] for c in cards)
backs = collections.Counter(c["back"] for c in cards)
print("cards total", len(cards))
print("dup ids", [k for k, v in ids.items() if v > 1])
print("dup fronts", [k for k, v in fronts.items() if v > 1])
print("dup backs", [(c["id"], c["lesson"]) for c in cards if backs[c["back"]] > 1])
sub = [c for c in cards if c["lesson"] in ("L07", "L08", "L09")]
print("L07/L08/L09 count", len(sub), collections.Counter(c["lesson"] for c in sub))
for c in cards:
    if c["id"] in ("M3-c183", "M3-c138", "M3-c160"):
        print(c["id"], "F-marker:", "Assuming F1 to F4" in c["back"] or "Assuming F1 to F4" in c["front"], "grade", c.get("grade"))
