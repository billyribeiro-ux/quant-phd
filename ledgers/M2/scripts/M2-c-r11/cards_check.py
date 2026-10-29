import json, collections
cards = json.load(open("course/modules/M/M2/cards.json"))
print("entries", len(cards))
ids = collections.Counter(c["id"] for c in cards)
fr = collections.Counter(c["front"].strip().lower() for c in cards)
bk = collections.Counter(c["back"].strip().lower() for c in cards)
print("dup ids", [k for k, v in ids.items() if v > 1])
print("dup fronts", [k for k, v in fr.items() if v > 1])
print("dup backs", [k for k, v in bk.items() if v > 1])
for c in cards:
    if c["lesson"] in {"L13","L14","L15","L16","L17","L18"} and c["id"] in {"M2-c212","M2-c258"}:
        print(c["id"], c["lesson"], c["grade"])
slice_ids = [c["id"] for c in cards if c["lesson"] in {"L13","L14","L15","L16","L17","L18"}]
print("slice cards", len(slice_ids), slice_ids[0], slice_ids[-1])
for c in cards:
    if c["lesson"] == "L16":
        print(c["id"], "|", c["front"][:110])
