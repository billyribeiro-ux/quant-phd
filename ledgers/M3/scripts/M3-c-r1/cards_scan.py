import json, sys, collections, re, pathlib
root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("cards", len(cards), "dup ids", [k for k, v in ids.items() if v > 1], "dup fronts", [k[:60] for k, v in fronts.items() if v > 1], "dup backs", [k[:60] for k, v in backs.items() if v > 1])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets", keys)
print("lesson counts", collections.Counter(c["lesson"] for c in cards))
print("L07-09 cards", sum(1 for c in cards if c["lesson"] in ("L07", "L08", "L09")))
print("grades", collections.Counter(c.get("grade") for c in cards if c["lesson"] in ("L07", "L08", "L09")))
# ids sequential?
nums = sorted(int(c["id"].split("c")[-1]) for c in cards)
print("id range", nums[0], nums[-1], "missing in range", sorted(set(range(nums[0], nums[-1] + 1)) - set(nums)))
# for T-graded cards in L07-09 with basis None check text has no basis
for c in cards:
    if c["lesson"] in ("L07", "L08", "L09") and c.get("grade") == "T" and c.get("basis"):
        print("T with basis", c["id"])
    if c["lesson"] in ("L07", "L08", "L09") and c.get("grade") in ("C",) and not c.get("basis"):
        print("C without basis", c["id"])
    if c["lesson"] in ("L07", "L08", "L09") and c.get("grade") is None:
        print("ungraded", c["id"])
