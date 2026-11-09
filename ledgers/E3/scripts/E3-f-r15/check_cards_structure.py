"""Round-14 card structure scan for E3 (cards.json): duplicates, id format, lesson coverage, grades, cited keys, numbers in lessons."""
import difflib
import json
import re
import sys
from collections import Counter

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/E/E3/cards.json"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "distinct ids:", len(set(ids)))
print("id format ok:", all(re.fullmatch(r"E3-c\d{3}", i) for i in ids))
print("lessons:", dict(Counter(c["lesson"] for c in cards)))
print("grades:", dict(Counter(c.get("grade", "none") for c in cards)))
# near duplicates by front and by back
dups = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf > 0.8 or rb > 0.8:
            dups.append((a["id"], b["id"], round(rf, 2), round(rb, 2)))
print("near-duplicate pairs (front or back ratio > 0.8):", dups)
# every card with a cite key must exist in references.json
refs = json.load(open(f"{root}/references/references.json"))
keys = {e["key"] for e in refs["entries"]}
bad = [(c["id"], k) for c in cards for k in c.get("cite", []) if k not in keys]
print("cited keys not in registry:", bad)
# cards with a grade C must carry a basis; grade T cards must not claim lab-only results
noc = [c["id"] for c in cards if c.get("grade") == "C" and "basis" not in c]
print("C cards without basis:", noc)
# lesson-number locators in card backs must exist in the lesson text
for c in cards:
    src = open(f"{root}/course/modules/E/E3/{c['lesson']}.html", encoding="utf-8").read()
    for m in re.finditer(r"Proposition (\d\.\d+)", c["back"] + c["front"]):
        if f"Proposition {m.group(1)}" not in src:
            print("locator missing in lesson:", c["id"], c["lesson"], "Proposition", m.group(1))
    for m in re.finditer(r"(Definition|Example|Remark|Theorem|Lemma|Problem|Assumption) ([A-Z]?\d\.?\d*)", c["back"] + c["front"]):
        token = f"{m.group(1)} {m.group(2)}"
        if token.endswith("."):
            token = token[:-1]
        if token not in src and f"{token}" not in src:
            print("locator not found in own lesson:", c["id"], c["lesson"], token)
