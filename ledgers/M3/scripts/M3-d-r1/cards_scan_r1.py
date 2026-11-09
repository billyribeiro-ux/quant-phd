# Round-1 delta (M3 slice d): structure, id sequence, duplicates, grade/basis fields and lesson-anchored numbers in cards.json.
import json, re, sys, collections
root = sys.argv[1]
cards = json.load(open(root + "/course/modules/M/M3/cards.json"))
print("records", len(cards))
ids = [c["id"] for c in cards]
print("unique ids", len(set(ids)), "dup ids", [k for k, v in collections.Counter(ids).items() if v > 1])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets", dict((str(k), v) for k, v in keys.items()))
nums = sorted(int(i.split("-c")[1]) for i in ids)
missing = sorted(set(range(1, max(nums) + 1)) - set(nums))
print("id range", nums[0], nums[-1], "missing numbers", missing)
print("out-of-order append check", [i for i, c in enumerate(cards) if i and int(c["id"].split("-c")[1]) < int(cards[i - 1]["id"].split("-c")[1])][:10])
fronts = collections.Counter(re.sub(r"\s+", " ", c["front"].strip().lower()) for c in cards)
print("duplicate fronts", [k[:80] for k, v in fronts.items() if v > 1])
backs = collections.Counter(re.sub(r"\s+", " ", c["back"].strip().lower()) for c in cards)
print("duplicate backs", [k[:80] for k, v in backs.items() if v > 1])
for c in cards:
    if c["id"] in ("M3-c042", "M3-c094", "M3-c097", "M3-c100", "M3-c145", "M3-c179", "M3-c167", "M3-c175", "M3-c189", "M3-c190", "M3-c209"):
        print(c["id"], c["lesson"], "grade=", c.get("grade"), "basis=", c.get("basis"), "cite=", c.get("cite"))
