import json, re, sys, collections
root = sys.argv[1]
cards = json.load(open(root + "/course/modules/FC/FC2/cards.json", encoding="utf-8"))
print("count", len(cards))
ids = [c["id"] for c in cards]
print("dup ids", [k for k, v in collections.Counter(ids).items() if v > 1])
nums = sorted(int(i.split("c")[-1]) for i in ids)
print("missing numbers in c001..c145:", [n for n in range(1, max(nums) + 1) if n not in nums])
for c in cards:
    if c["lesson"] in ("L04", "L05", "L06"):
        print(c["id"], c["lesson"], c.get("grade"), "|", c["front"], "|", c["back"][:400], "|", c.get("basis", ""))
# content-level duplicates of fronts
fr = collections.Counter(c["front"].strip().lower() for c in cards)
print("dup fronts", [k for k, v in fr.items() if v > 1])
