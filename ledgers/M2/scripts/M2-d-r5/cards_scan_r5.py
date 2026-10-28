import json, sys
path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))
ids = [c["id"] for c in cards]
fronts = [c["front"].strip().lower() for c in cards]
backs = [c["back"].strip().lower() for c in cards]
print("cards", len(cards), "dup ids", len(ids) - len(set(ids)), "dup fronts", len(fronts) - len(set(fronts)), "dup backs", len(backs) - len(set(backs)))
print("slice ids c280-c377 present:", sum(1 for i in ids if 280 <= int(i.split("c")[-1]) <= 377))
