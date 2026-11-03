"""Full scan of FC1 cards.json: duplicates, ids, lesson field, numbered references present in the cited lesson, sample list."""
import collections
import json
import re
import sys

base = sys.argv[1]
cards = json.load(open(f"{base}/cards.json"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
print("ids sequential c001..c124:", ids == [f"FC1-c{i:03d}" for i in range(1, len(cards) + 1)])
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
print("lessons:", collections.Counter(c["lesson"] for c in cards))
print("grades:", collections.Counter(c.get("grade", "-") for c in cards))
lessons = {}
for L in ["L01", "L02", "L03", "L04", "L05"]:
    lessons[L] = open(f"/tmp/fc1c_v4_{L}.txt").read()
bad = []
for c in cards:
    text = lessons[c["lesson"]]
    refs = re.findall(r"(Assumption [A-Z]?\d[\d.]*|Proposition \d+\.\d+|Definition \d+\.\d+|Remark \d+\.\d+|Section \d+|Lemma \d+\.\d+|Theorem \d+\.\d+)", c["back"] + " " + c["front"])
    for r in refs:
        if r not in text:
            bad.append((c["id"], c["lesson"], r))
print("numbered references not found in the card's own lesson:", bad)
other = []
for c in cards:
    for L, text in lessons.items():
        if L == c["lesson"]:
            continue
