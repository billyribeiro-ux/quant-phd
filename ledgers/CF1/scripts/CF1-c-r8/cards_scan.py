"""Full duplicate scan and field check of course/modules/CF/CF1/cards.json, plus a literal-basis check against the L05 and L06 pages."""
import collections
import json
import re
import sys

ROOT = sys.argv[1]
cards = json.load(open(f"{ROOT}/course/modules/CF/CF1/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)))
print("duplicate fronts", [k for k, v in collections.Counter(c["front"].strip().lower() for c in cards).items() if v > 1])
print("duplicate backs", [k for k, v in collections.Counter(c["back"].strip().lower() for c in cards).items() if v > 1])
print("grades", dict(collections.Counter(c["grade"] for c in cards)))
print("missing basis", [c["id"] for c in cards if not c.get("basis")])
for lesson in ("L05", "L06"):
    html = open(f"{ROOT}/course/modules/CF/CF1/{lesson}.html", encoding="utf-8").read()
    for c in (c for c in cards if c["lesson"] == lesson):
        key = re.search(r"(Definition [0-9.]+|Proposition [0-9.]+|Remark [0-9.]+|Problem [A-Z][0-9]|Lab 1|Section [0-9]+|misconception)", c["basis"])
        print(c["id"], "basis key", key.group(0) if key else None, "found in page", (key.group(0) in html) if key else "n/a")
print("cards in L05", sum(1 for c in cards if c["lesson"] == "L05"), "in L06", sum(1 for c in cards if c["lesson"] == "L06"))
print("process words", [c["id"] for c in cards if re.search(r"\b(round|builder|verifier|REQUESTS|unit report)\b", json.dumps(c), re.I)])
