import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
cards = d if isinstance(d, list) else d.get("cards", d)
sel = [c for c in cards if c.get("lesson") in ("L04", "L05", "L06")]
print("total cards", len(cards), "L04-L06", len(sel))
ids = [c["id"] for c in cards]
print("duplicate ids", len(ids) - len(set(ids)))
fronts = [c["front"].strip().lower() for c in cards]
print("duplicate fronts", len(fronts) - len(set(fronts)))
for c in sel:
    print(json.dumps(c, ensure_ascii=False))
