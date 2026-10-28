import json, collections
d = json.load(open("/tmp/verify11-CF1-c/course/modules/CF/CF1/cards.json"))
cards = d if isinstance(d, list) else d.get("cards", d)
ids = collections.Counter(c["id"] for c in cards)
print("cards", len(cards), "dup ids", [k for k, v in ids.items() if v > 1])
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("dup fronts", [k for k, v in fronts.items() if v > 1])
l05 = [c for c in cards if c["lesson"] == "L05"]; l06 = [c for c in cards if c["lesson"] == "L06"]
print("L05 cards", [c["id"] for c in l05], "L06 cards", [c["id"] for c in l06])
