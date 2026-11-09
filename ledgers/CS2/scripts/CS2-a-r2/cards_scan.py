"""Card checks for the CS2 hub-and-L01-L04 slice (verifier round 2).

Checks: unique ids across cards.json; ids well formed; grade T has no basis, grade C has a basis;
every card of the slice lessons carries a lesson field L01..L04; near-duplicate fronts within the
whole file (difflib ratio >= 0.8); each card's back numbers appear in its lesson page text.
Usage: python3 -I cards_scan.py <repo-root>
"""

import difflib
import json
import re
import sys

root = sys.argv[1]
with open(f"{root}/course/modules/CS/CS2/cards.json", encoding="utf-8") as fh:
    cards = json.load(fh)
ids = [c["id"] for c in cards]
print("cards total", len(cards), "unique ids", len(set(ids)))
assert len(set(ids)) == len(ids), "duplicate ids"
bad_form = [i for i in ids if not re.fullmatch(r"CS2-c\d{3}", i)]
print("malformed ids", bad_form)
grade_bad = []
for c in cards:
    if c["grade"] == "T" and c.get("basis"):
        grade_bad.append((c["id"], "T with basis"))
    if c["grade"] == "C" and not c.get("basis"):
        grade_bad.append((c["id"], "C without basis"))
    if c["grade"] not in ("T", "C"):
        grade_bad.append((c["id"], "grade " + c["grade"]))
print("grade mismatches", grade_bad)
slice_cards = [c for c in cards if c["lesson"] in ("L01", "L02", "L03", "L04")]
print("slice cards", len(slice_cards), {k: sum(1 for c in slice_cards if c["lesson"] == k) for k in ("L01", "L02", "L03", "L04")})
pairs = []
fronts = [(c["id"], c["front"]) for c in cards]
for i in range(len(fronts)):
    for j in range(i + 1, len(fronts)):
        r = difflib.SequenceMatcher(None, fronts[i][1], fronts[j][1]).ratio()
        if r >= 0.8:
            pairs.append((fronts[i][0], fronts[j][0], round(r, 3)))
print("near-duplicate fronts (ratio >= 0.8):", pairs)
text = {}
for p in ("index", "L01", "L02", "L03", "L04"):
    with open(f"{root}/course/modules/CS/CS2/{p}.html", encoding="utf-8") as fh:
        raw = fh.read()
    text[p] = re.sub(r"<[^>]+>", " ", raw)
missing = []
for c in slice_cards:
    nums = set(re.findall(r"\d+\.\d+|\d+", c["back"]))
    nums = {n for n in nums if n not in ("1", "0", "2", "3")}
    body = text[c["lesson"]]
    for n in sorted(nums):
        if n not in body:
            missing.append((c["id"], n))
print("back numbers not found in the lesson page (excluding 0-3):", missing)
refs = []
for p in ("index", "L01", "L02", "L03", "L04"):
    for m in re.finditer(r"CS2-c228", text[p]):
        refs.append(p)
print("references to removed CS2-c228 in slice pages:", refs)
